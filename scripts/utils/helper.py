# -*- coding: utf-8 -*-


import yaml
import os
import io
import sys
import subprocess
import base64
import json
import shutil
import hashlib
import multiprocessing
from pathlib import Path



#ROOT_PATH=os.path.dirname("/home/amol/repo/amocha/")
SCRIPT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
ROOT_PATH = os.path.abspath(os.path.join(SCRIPT_PATH, '../'))
ONBOARD_FILE_PATH = os.path.join(ROOT_PATH,'../onboard/onboard.yaml')
TEAMS_DIR = os.path.join(ROOT_PATH, 'teams')
#TEAMS_PATH = os.path.join(ROOT_PATH, 'teams')

def get_onboarded_teams():
    try:
       with open(ONBOARD_FILE_PATH,'r') as f:
         yaml_data = yaml.safe_load(f)
         team_list = []
         for key, value in yaml_data.items():
             if value['onboard_status'] == 'onboarded':
                 team_list.append(key)
         return yaml.dump(team_list)
    except yaml.YAMLError:
        print("error in the onboarding status file")


def team_dir_list():
    hashes = {}
    team_files = file_list(TEAMS_DIR)
    for f in team_files:
        team_info = read_yaml(read_file(f))
        if len(team_info) != 1:
            print_error("Invalid yaml file format '%s'" % f)
        if not team_info[0].get('team_name'):
            print_error("Team name (team_name) in file '%s' is not provided" % f)
        hashes[team_info[0]['team_name']] = {
            'md5': md5(read_file(f)),
            'path': f,
            'info': team_info[0],
        }
    return hashes

def file_list(path_to_files, file_ext='yaml'):
    file_list = []
    for f in os.listdir(path_to_files):
        if f.endswith(file_ext):
            file_list.append(os.path.join(path_to_files, f))
    return sorted(file_list)

def read_file(path: str) -> str:
    """
    Read text from file

    :raises:
        ExitError: invalid file
    :param path: file path
    :return: str
    """
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception as e:
        raise ExitError("Could not read file: %s" % path, e)


def print_error(err):
    print(err, file=sys.stderr)
    exit(-1)

def read_yaml(stream) -> iter:
    """
    Read the yaml manifests into a list of dictionaries containing yaml data

    :raises:
        ExitError: invalid yaml manifests
    :param stream: manifests stream
    :return: list of Dict yaml data
    """
    try:
        return list(yaml.safe_load_all(stream))
    except Exception as e:
        contents = stream
        name = ''
        if isinstance(stream, io.IOBase):
            try:
                stream.seek(0)
            except:
                pass
            contents = stream.read()
            name = stream.name
        raise ExitError("invalid yaml: %s\n%s" % (
            name, contents), e)

class ExitError(Exception):
    """
    Exit error exception to format the exception text and show more meaningful errors.

    """

    def __init__(self, message: str, exception: BaseException = None) -> None:
        """
        Format and print output error message based on error message, command line parameters and previous exception.

        :raises:
            BaseException: previous system exception
        :param message: error message
        :param exception: previous exception
        :return: None
        """
        print(
            """
======================================================================
Error: %s
----------------------------------------------------------------------
Failed Command: %s
----------------------------------------------------------------------
            """ % (message, ' '.join(sys.argv)), file=sys.stderr)
        if exception:
            raise exception


def md5(t):
    return hashlib.md5(str(t).encode('utf-8')).hexdigest()


def onboard_team_list(teams, onboard_teams):
    hashes = {}
    for team_name, details in teams.items():
        if team_name in onboard_teams: 
            continue
        if team_name in hashes:
            print_error('Duplicate team name %s' % team_name)
        hashes[team_name] = details
    return hashes




def offboard_team_list(teams, onboard_teams):
    ls = []
    for team_name in onboard_teams:
        if team_name in teams:
            continue
        ls.append(team_name)
    return ls


def create_ns():
  pass
