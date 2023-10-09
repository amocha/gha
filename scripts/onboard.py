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
    #az_admin_login()
    #jenkins_load_credentials()
#    service_account = k8s_kubespray_service_account_name(team_name)
#    kubeconfig_files = []
#    aad_group_ids = team_info.get('aad_group_id')
#    for region, envs in team_info['environments'].items():
#        for env, sp_info in envs.items():
#            print('\n-------------\nOnboarding team %s on %s %s\n-------------\n' % (team_name, region, env))
#            credentials = vault_get_spn_credentials(sp_info['aad_spn_name'])
#            ocenv = True if env in ['oc', 'devoc', 'devinfra'] else False
#            subscription_id = SUBSCRIPTIONS[region][env]
#            if not ocenv:
#                if env == 'admin':
#                    add_admin_spn(credentials, sp_info['aad_sp_client_id'], team_name, subscription_id)
#                    continue
#                if not credentials_update:
#                    azure_set_acr_shellai_role(team_name, region, env, "AcrPush", sp_info['aad_sp_object_id'])
#                    azure_set_vnet_network_contributor_role(team_name, region, env, sp_info['aad_sp_object_id'])
#                    for group_id in aad_group_ids:
#                        azure_set_acr_shellai_role(team_name, region, env, "AcrPull", group_id)
#            az_set_subscription(subscription_id)
#            if not ocenv and not credentials_update:
#                keyvault_create(team_name, region, env, sp_info, aad_group_ids, True)
#            print('Creating kubeconfigs for team "%s" in %s %s.' % (team_name, region, env))
#            add_kubeconfig(kubeconfig_files, service_account, team_name, region, env, program_team, AKS, sp_info,
#                           aad_group_ids)
#            if not ocenv and not credentials_update:
#                keyvault_create(team_name, region, env, sp_info, aad_group_ids, False)
#            add_spn(credentials, sp_info['aad_sp_client_id'], team_name, region, env, 'ci', subscription_id,
#                    aad_group_ids, sp_info['aad_sp_object_id'])
#            add_spn(credentials, sp_info['aad_sp_client_id'], team_name, region, env, 'cd', subscription_id, None, None)
#
#    save_kubeconfig(kubeconfig_files, team_name)

    return

#def azure_set_acr_shellai_role(team_name, region, env, role, object_id):
#    az_set_subscription(SUBSCRIPTIONS[region]['oc'])
#    acr_name = 'shellai'
#    p = run_command(["az", "acr", "show", "--name", acr_name, "--query", "id", "--output", "tsv"])
#    acr_registry_id = p.stdout.decode('utf-8').strip()
#    p = run_command(["az", "role", "assignment", "list", "--role", role, "--scope", acr_registry_id])
#    if object_id in p.stdout.decode():
#        return
#    print('Assigning %s permissions for Service Principal "%s" for team "%s" on "%s".' % (
#        role, object_id, team_name, acr_registry_id))
#    run_command(["az", "role", "assignment", "create", "--assignee-object-id", object_id, "--scope",
#                 acr_registry_id, "--role", role])
#
#
#def azure_set_vnet_network_contributor_role(team_name, region, env, object_id):
#    scope = "/subscriptions/%s/resourceGroups/%s-%s-platform-spoke-network-private-rg/providers/Microsoft.Network" \
#            "/virtualNetworks/%s-%s-platform-vnet" % (
#                SUBSCRIPTIONS[region][env], region, env, region, env)
#    p = run_command(["az", "role", "assignment", "list", "--role", "Network Contributor", "--scope", scope])
#    if object_id in p.stdout.decode():
#        return
#    print('Adding network contributor role on VNET for team "%s" on "%s" to object ID "%s".' % (
#        team_name, scope, object_id))
#    run_command(
#        ["az", "role", "assignment", "create", "--role", "Network Contributor", "--assignee-object-id",
#         object_id, "--scope", scope])
#
#
#def save_kubeconfig(kubeconfig_files, team_name):
#    if len(kubeconfig_files) == 0:
#        add_error("[WARNING] No kubeconfigs are generated for '%s'" % team_name)
#        return
#    final_kubeconfig = k8s_merge_kubeconfigs(kubeconfig_files)
#    vault_set_team_kubeconfig(team_name, final_kubeconfig)
#    try:
#        jenkins_set_team_kubeconfig(team_name, final_kubeconfig)
#    except Exception as e:
#        add_error("[WARNING] Failed to set kubeconfig for team '%s' in Jenkins: %s" % (team_name, str(e)))
#
#
#def add_spn(credentials, client_id, team_name, region, env, pipeline, subscription_id, aad_group_id, aad_sp_object_id):
#    vault_path = 'kv/cicd/%s' % team_name
#    # if vault_path_exists(vault_path):
#    #     return
#    vault_path = '%s/%s/common/azure/%s/credentials' % (vault_path, pipeline, env)
#    add_spn_vault(credentials, client_id, team_name, vault_path, subscription_id)
#    if pipeline == 'ci':
#        try:
#            jenkins_add_spn(credentials, client_id, team_name, region, env, subscription_id, aad_group_id,
#                            aad_sp_object_id)
#        except Exception as e:
#            add_error("[WARNING] Failed to add SPN for team '%s' in Jenkins: %s" % (team_name, str(e)))
#        try:
#            keyvault_set_team_spn(credentials, client_id, team_name, region, env, subscription_id, aad_group_id)
#        except Exception as e:
#            add_error("[WARNING] Failed to set SPN for team '%s' in Keyvault: %s" % (team_name, str(e)))
#    return vault_path
#
#
#def add_admin_spn(credentials, client_id, team_name, subscription_id):
#    add_spn_vault(credentials, client_id, team_name, 'kv/cicd/%s/cd/common/azure/onboarding/credentials' % team_name,
#                  subscription_id)
#    add_spn_vault(credentials, client_id, team_name, 'kv/cicd/%s/cd/common/azure/oc/credentials' % team_name,
#                  subscription_id)
#
#
#def add_spn_vault(credentials, client_id, team_name, vault_path, subscription_id=None):
#    print('Storing SPN credentials for team "%s" in Vault %s.' % (team_name, vault_path))
#    run_command(
#        ['vault', 'kv', 'put', vault_path,
#         'client_certificate_pfx=%s' % credentials['certificate_pfx'],
#         'client_certificate_password=%s' % credentials['certificate_password'],
#         'client_certificate_pem=%s' % credentials['certificate_pem'],
#         'tenant_id=%s' % TENANT_ID,
#         'client_id=%s' % client_id,
#         'subscription_id=%s' % subscription_id,
#         ])
#    return vault_path
#

def add_error(err):
    print(err)
    exit_errors.append(err)


#def add_kubeconfig(kubeconfig_files, service_account, team_name, region, env, program_team, k8s_type, sp_info,
#                   aad_group_ids):
#    kc = False
#    try:
#        kc = k8s_generate_kubeconfig(service_account, team_name, region, env, k8s_type)
#    except ExitError:
#        pass
#    if not kc:
#        add_error("[WARNING] Could not generate kubeconfig for '%s' in %s %s %s" % (team_name, region, env, k8s_type))
#        return
#    try:
#        keyvault_set_team_kubeconfig(team_name, region, env, program_team, k8s_type, kc, sp_info, aad_group_ids)
#    except ExitError:
#        add_error(
#            "[WARNING] Could not add kubeconfig in keyvault for '%s' in %s %s %s" % (team_name, region, env, k8s_type))
#    kubeconfig_files.append(kc)


def main():
    teams = team_dir_list()
    cached_onboard_teams = get_onboarded_teams()
    onboard_teams = onboard_team_list(teams, cached_onboard_teams)
    #offboard_teams = offboard_team_list(teams, cached_onboard_teams)
    print('%d teams to onboard (%s)' % (len(onboard_teams), ','.join(onboard_teams)))
    #print('%d teams to offboard (%s)' % (len(offboard_teams), ','.join(offboard_teams)))
    #for team_name, details in onboard_teams.items():
    #    onboard_team(team_name, details)
    #    cache_onboard_team(team_name, details, cached_onboard_teams)

    #if len(onboard_teams) or len(offboard_teams):
    #    cache_onboard_teams(teams)
    #cleanup()
    #if len(exit_errors) > 0:
    #    print('Onboarding successful but has the following warning:')
    #    print("\n".join(exit_errors))
    #    # exit(-1)


def cleanup():
   pass 

if __name__ == "__main__":
    main()
