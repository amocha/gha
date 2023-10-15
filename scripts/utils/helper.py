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
import requests
import multiprocessing
from pathlib import Path


ROOT_PATH = os.getcwd()
TEAMS_DIR = os.path.join(ROOT_PATH, 'teams',ENV_CLASS)


def get_onboarded_teams():
    try:
        with open(ONBOARD_FILE_PATH, 'r') as f:
            yaml_data = yaml.safe_load(f)
            team_list = []
            for key, value in yaml_data.items():
                if value['onboard_status'] == 'onboarded':
                    team_list.append(key)
            return yaml.dump(team_list)
    except yaml.YAMLError:
        print("error in the onboarding status file")



def print_error(err):
    print(err, file=sys.stderr)
    exit(-1)




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



def az_set_subscription(s):
    run_command(['az', 'account', 'set', '--subscription', s])



def run_command(command: list, **kwargs) -> subprocess.CompletedProcess:
    """
    run a system command

    :raises:
        ExitError: invalid command
    :param command: command string as a list
    :return: completed process class
    """
    if 'stdout' not in kwargs.keys():
        kwargs['stdout'] = subprocess.PIPE
    if 'stderr' not in kwargs.keys():
        kwargs['stderr'] = subprocess.PIPE

    # print('[DEBUG] Running command: %s' % ' '.join(command))
    try:
        output = subprocess.run(command, **kwargs)
    except Exception as e:
        raise ExitError("invalid command `%s`" % ' '.join(command), e)

    stdout, stderr = '', ''
    if output.stderr and type(output.stderr) != str:
        stderr = output.stderr.decode()
    if output.stdout and type(output.stdout) != str:
        stdout = output.stdout.decode()

    if output.returncode != 0:
        # if stderr:
        # print("\n--------\ncommand `%s` has some stderr output"
        # "\n-------\nError: %s\n" % (' '.join(command), stderr))
        raise ExitError("Error running command `%s`"
                        "\n-------\nError: %s"
                        "\n----\nOutput: %s\n" % (' '.join(command),
                                                  stderr,
                                                  stdout))
    return output


#def assign_contributor(access_token, subscription_id, object_id, env):
#    if env != "prod":
#        operating_environment = "N"
#    else:
#        operating_environment = "P"
#    API_ENDPOINT = "https://azasroleassignments.trafficmanager.net/api/Create"
#    parameters = {
#        "OperatingEnvironment": operating_environment,
#        "CloudEnvironment": "EXT",
#        "TargetObjectId": object_id,
#        "TargetRole": "ShellContributorExternal",
#        "TargetScope": "/subscriptions/" + subscription_id
#
#    }
#    headers = {
#        "Authorization": "Bearer " + access_token,
#        "Content-Type": "application/json"
#    }
#    response = requests.post(API_ENDPOINT, json=parameters, headers=headers)
#    # Check the response status code.
#    if response.status_code == 200:
#        # The request was successful.
#        print(response.content)
#    else:
#        # The request failed.
#        print("Failed to call the API: {}".format(response.status_code))
