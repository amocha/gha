# DEPv2 Onboarding


## Introduction

1. Prepare a PR against this repo with relevant details
2. The onboard script will be called from github acitons periodically. 
   - The onboarded teams will be marked as onboarded
   - The new to onboard teams will go through the following 
      - Namespace Creation in k8s
      - MI creation and provisioning in the end user namespace 
   - Update of status and hash of the file in a different repo


## Where will this workflow run
The github workflow orchestrating this will run on github runner (dep-shared) which has access to the clusters.
