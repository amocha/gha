#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: ./onboard_team.py
import subprocess

from utils.helper import *

exit_errors = []


#def onboard_team(team_name, details):
#    team_info = details['info']
#    if team_info.get('ignore'):
#        print('Ignoring team %s ' % team_name)
#        return
#    if not team_info.get('environments') or len(team_info.get('environments')) == 0:
#        print('No Environments provided for team %s ' % team_name)
#        return
#    # Refactor this function down
#    create_resources(team_info)
#    return
#
#
#def create_resources(team_info):
#    metadata = team_info['metadata']
#    env_class = team_info['env_class']
#    for env, details in team_info['environments'].items():
#        namespace = (metadata['project_stream'] + "-" + metadata['work_stream'] + "-" + env).lower()
#
#        if env_class != "prd":
#            az_login("npd")
#            # Code for more env variations like sbx1, pre1
#            resource_group = ("DEP-MGMT-EUW-" + env + "-AKS-PRIV-CC-RG").upper()
#            cluster_name = ("dep-aks-priv-euw-" + env).lower()
#            aks_subscription_id="4a6e6b74-cb13-46ee-af3f-c12789e34d51"
#        else:
#            az_login("prd")
#            resource_group = ("DEP-MGMT-EUN-" + env + "-AKS-PRIV-CC-RG").upper()
#            if env != "prd":
#                cluster_name = ("dep-aks-priv-eun-npd").lower()
#            else:
#                cluster_name = ("dep-aks-priv-eun-prd").lower()
#            aks_subscription_id="b91c973e-2dbe-421e-ab54-b6eaef942acf"
#
#        # Set Kubeconfig
#        kubeconfig = ("/tmp/" + env).lower()
#
#        # Prepare AKS Kubeconfig + Get OIDC issuer
#        run_command(
#            ['az', 'aks', 'get-credentials', '--resource_group', resource_group, '--name', cluster_name, '--public-fqdn', '--admin', '-f',
#             kubeconfig,'--subscription',aks_subscription_id])
#        tmp_aks_oidc_issuer=run_command(['az','aks','show','--resource_group',resource_group,'--name',cluster_name,'--query','oidcIssuerProfile.issuerUrl'])
#        aks_oidc_issuer=json.loads(tmp_aks_oidc_issuer.stdout)
#
#        # Set user Subscription
#        subscription_id = details['subscription_id']
#        az_set_subscription(subscription_id)
#
#        # Create RG to house managed identity
#        run_command(['az', 'group', 'create', '-l', 'westeurope', 'DEP-MI'])
#
#        # Create MI
#        run_command(['az', 'identity', 'create', '--name', 'depidentity', '--location', 'westeurope', '--subscription',
#                     subscription_id, '--resource-group', 'DEP-MI'])
#
#        # Create Federated Identity
#        subject = ("system:serviceaccount:" + namespace + ":" + namespace).lower()
#        run_command(
#            ['az', 'identity', 'federated-credential', 'create', '--name', 'depfederatedidentity', '--identity-name',
#             'depidentity', '--resource-group', 'DEP-MI', '--issuer', aks_oidc_issuer,
#             '--subject', subject])
#
#        # Get Client ID & Object ID of MI
#        tmp_client_id = run_command(
#            ['az', 'identity', 'show', '--resource-group', 'DEP-MI', '--name', 'depidentity', '--query', 'clientId'])
#        client_id = json.loads(tmp_client_id.stdout)
#        tmp_object_id = run_command(
#            ['az', 'identity', 'show', '--resource-group', 'DEP-MI', '--name', 'depidentity', '--query', 'principalId'])
#        object_id = json.loads(tmp_object_id.stdout)
#
#        # Grant MI Contributor on the Subscription
#
#        if env != "prod":
#            tmp_access_token = run_command(
#                ['az', 'account', 'get-access-token', '--scope', 'api://61e863bc-13a5-4a35-92c6-5c95b28d3d16/.default',
#                 '--query', 'accessToken'])
#        else:
#            tmp_access_token = run_command(
#                ['az', 'account', 'get-access-token', '--scope', 'api://35f0fbec-9eb2-49bf-8b8e-0c7bd01305ee/.default',
#                 '--query', 'accessToken'])
#        access_token = json.loads(tmp_access_token.stdout)
#        # Call function
#        assign_contributor(access_token, subscription_id, object_id, env)
#
#        # Create Namespace and SA with Azure MI config
#
#        run_command(['kubectl', 'create', 'namespace', namespace, '-f', kubeconfig])
#        run_command(['kubectl', 'create', 'sa', '-n', namespace, namespace, '-f', kubeconfig])
#        run_command(['kubectl', 'annotate', 'sa', 'azure.workload.identity/client-id=', client_id, '-f', kubeconfig])
#        run_command(['kubectl', 'label', 'sa', 'azure.workload.identity/use=', '"true"', '-f', kubeconfig])
#
#
def main():
    teams = team_dir_list()
    print(teams)
#    cached_onboard_teams = get_onboarded_teams()
#    onboard_teams = onboard_team_list(teams, cached_onboard_teams)
#    for team_name, details in onboard_teams.items():
#        onboard_team(team_name, details)

    # To-do Offboarding

    

def cleanup():
    pass


if __name__ == "__main__":
    main()
