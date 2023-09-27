#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: ./onboard_team.py

from utils.helper import *

exit_errors = []


def onboard_team(team_name, details):
    team_info = details['info']
    if team_info.get('ignore'):
        print('Ignoring team %s ' % team_name)
        return
    if not team_info.get('environments') or len(team_info.get('environments')) == 0:
        print('No Environments provided for team %s ' % team_name)
        return
    return


def create_ns(team_name, envionments, metadata ):
    print('Creating Team namespace in Private cluster')
    for region, envs in environments 
    namespace = 
    if env != "prod":
        run_command(['kubectl', 'create','namespace', ])

def add_error(err):
    print(err)
    exit_errors.append(err)


def main():
    teams = team_dir_list()
    cached_onboard_teams = get_onboarded_teams()
    onboard_teams = onboard_team_list(teams, cached_onboard_teams)




def cleanup():
   pass 

if __name__ == "__main__":
    main()