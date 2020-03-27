# Git integration clone task helper

This Task fetches the credentials needed to perform git operations on a repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses it to clone (and/or perform the appropriate checkout if pull request parameters are given) of the repository.

Note: Specific access token can be provided specifically by providing a value for the optional parameter `gitAccessToken`.

## Install the Task
- Add a github integration in your toolchain to the repository containing the task (https://github.com/open-toolchain/tekton-catalog)
- Add that github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `git`

## Inputs

### Context - ConfigMap/Secret

  The task expects the following kubernetes resource to be defined:

* **Secret cd-secret (optional)**

  Secret containing:
  * **API_KEY**: An IBM Cloud Api Key allowing access to the toolchain (and `Git Repos and Issue Tracking` service if used)

  If this secret is provided, it will be used to obtain the the git token for the git integration in the toolchain

  See [sample TriggerTemplate](./sample/listener-simple-clone.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

### Parameters

* **gitAccessToken**: (optional) token to access the git repository. Either `cd-secret` or gitAccessToken has to be provided.
* **repository**: the git repository url that the toolchain is integrating
* **branch**: the git branch (default value to `master`)
* **revision**: (optional) the git revision/commit to update the git HEAD to (default to empty meaning only use the branch information)
* **pr_repository**: the originated repository where the PullRequest come from (in case of a fork). Default to '' means same repository (not a fork) or it can be the same as repository to clone.
* **pr_branch**: the branch that is the source of this PullRequest. Default to ''.
* **pr_revision**: the commit/revision in the source branch of the PullRequest that is to be built. Defaults to ''.
* **directoryName**: (optional) name of the new directory to clone into (default to `.` in order to clone at the root of the volume mounted for the pipeline run). Note: It will be to the "humanish" part of the repository if this param is set to blank
* **propertiesFile**: (optional) name of the properties file that will be created as an additional outcome of this task in the workspace `workspace`. This file will contains the git related information (`GIT_URL`, `GIT_BRANCH` and `GIT_COMMIT`)
* **resourceGroup**: (optional) target resource group (name or id) for the ibmcloud login operation
* **continuous-delivery-context-secret**: (optional) name of the configmap containing the continuous delivery pipeline context secret (default to `cd-secret`)
* **gitCredentialsJsonFile**: (optional) name of JSON file to store git credentials found out of the clone task (it can be a file path relative to the workspace `workspace` backed by a volume). Default to '' meaning no output of this information.

## Workspaces

* **workspace**: The git repo will be cloned onto the volume backing this workspace

## Outputs
The output of this task is the repository cloned into the directory on the workspace `workspace`.

## Usages

- The `sample` sub-directory contains an EventListener definition that you can include in your CD tekton pipeline configuration to run an example showing a simple usage of the `clone-repo-task`.

  See the documentation [here](./sample/README.md)

- The `sample-git-trigger` sub-directory contains several EventListener definitions that you can include in your CD tekton pipeline configuration to run an example showing usage of the clone-repo-task in the context of CD tekton pipeline triggered by git event(s) (Commit pushed or PullRequest opened/updated)

  See the documentation [here](./sample-git-trigger/README.md)
