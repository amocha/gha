#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: ./onboard_team.py
import subprocess

from utils.helper import *

exit_errors = []


def onboard_team(team_name, details):
    print("In Onboard Team")
    team_info = details['info']
    if len(team_info) == 0:
        print ('No Team Details')
        return
    if team_info.get('ignore'):
        print('Ignoring team %s ' % team_name)
        return
    # Refactor this function down
    create_resources(details)
    return


def create_resources(team_info):
    metadata = team_info['metadata']
    env_class = team_info['env_class']
    env = team_info['env']
    namespace = (metadata['project_stream'] + "-" + metadata['work_stream'] + "-" + env).lower()
    #for key, value in team_info['info'].items():
    #    namespace = (metadata['project_stream'] + "-" + metadata['work_stream'] + "-" + env).lower()
    if env_class != "prd":
        # Code for more env variations like sbx1, pre1
        resource_group = ("DEP-MGMT-EUW-" + env + "-AKS-PRIV-CC-RG").upper()
        cluster_name = ("dep-aks-priv-cc-euw-" + env).lower()
        aks_subscription_id="b91c973e-2dbe-421e-ab54-b6eaef942acf"
    else:
        if env != "prd":
            resource_group = ("DEP-MGMT-EUN-NPD-AKS-PRIV-CC-RG").upper()
            cluster_name = ("dep-aks-priv-cc-eun-npd").lower()
        else:
            cluster_name = ("dep-aks-priv-cc-eun-prd").lower()
            resource_group = ("DEP-MGMT-EUN-PRD-AKS-PRIV-CC-RG").upper()
        aks_subscription_id="4a6e6b74-cb13-46ee-af3f-c12789e34d51"

    # Set Kubeconfig
    kubeconfig = ("/tmp/" + env).lower()

    # Prepare AKS Kubeconfig + Get OIDC issuer
    run_command(
        ['az', 'aks', 'get-credentials', '--resource-group', resource_group, '--name', cluster_name, '--public-fqdn', '--admin', '-f',
         kubeconfig,'--subscription',aks_subscription_id])
    tmp_aks_oidc_issuer=run_command(['az','aks','show','--resource-group',resource_group,'--name',cluster_name,'--query','oidcIssuerProfile.issuerUrl'])
    aks_oidc_issuer=json.loads(tmp_aks_oidc_issuer.stdout)

    # Set user Subscription
    subscription_id = team_info['info']['subscription_id']
    az_set_subscription(subscription_id)

    # Create RG to house managed identity
    run_command(['az', 'group', 'create', '-l', 'westeurope', 'DEP-MI'])

    # Create MI
    run_command(['az', 'identity', 'create', '--name', 'depidentity', '--location', 'westeurope', '--subscription',
                 subscription_id, '--resource-group', 'DEP-MI'])

    # Create Federated Identity
    subject = ("system:serviceaccount:" + namespace + ":" + namespace).lower()
    run_command(
        ['az', 'identity', 'federated-credential', 'create', '--name', 'depfederatedidentity', '--identity-name',
         'depidentity', '--resource-group', 'DEP-MI', '--issuer', aks_oidc_issuer,
         '--subject', subject])

    # Get Client ID & Object ID of MI
    tmp_client_id = run_command(
        ['az', 'identity', 'show', '--resource-group', 'DEP-MI', '--name', 'depidentity', '--query', 'clientId'])
    client_id = json.loads(tmp_client_id.stdout)
    tmp_object_id = run_command(
        ['az', 'identity', 'show', '--resource-group', 'DEP-MI', '--name', 'depidentity', '--query', 'principalId'])
    object_id = json.loads(tmp_object_id.stdout)

    # Grant MI Contributor on the Subscription

    if env != "prd":
        tmp_access_token = run_command(
            ['az', 'account', 'get-access-token', '--scope', 'api://61e863bc-13a5-4a35-92c6-5c95b28d3d16/.default',
             '--query', 'accessToken'])
    else:
        tmp_access_token = run_command(
            ['az', 'account', 'get-access-token', '--scope', 'api://35f0fbec-9eb2-49bf-8b8e-0c7bd01305ee/.default',
             '--query', 'accessToken'])
    access_token = json.loads(tmp_access_token.stdout)
    # Call function
    assign_contributor(access_token, subscription_id, object_id, env)

    # Create Namespace and SA with Azure MI config

    run_command(['kubectl', 'create', 'namespace', namespace, '-f', kubeconfig])
    run_command(['kubectl', 'create', 'sa', '-n', namespace, namespace, '-f', kubeconfig])
    run_command(['kubectl', 'annotate', 'sa', 'azure.workload.identity/client-id=', client_id, '-f', kubeconfig])
    run_command(['kubectl', 'label', 'sa', 'azure.workload.identity/use=', '"true"', '-f', kubeconfig])


def main():
    teams = team_dir_list()
    print(teams)
    onboard_t_list = onboard_team_list(teams)
    print(onboard_t_list)
    for team_env, details in onboard_t_list.items():
       onboard_team(team_env, details)


    # To-do Offboarding

    

def cleanup():
    pass


if __name__ == "__main__":
    main()
