# Git related tasks

## Available tasks
- **[git-clone-repo](#git-clone-repo)**: This Task fetches the credentials needed to perform git operations on a repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses it to clone (and/or perform the appropriate checkout if pull request parameters are given) of the repository. The output of this task is the repository cloned into the directory on the workspace `workspace`.
- **[git-set-commit-status](#git-set-commit-status)**: This task is setting a git commit status for a given git commit (revision) in a git repository repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using).

## Install the Tasks
- Add a github integration in your toolchain to the repository containing the task (https://github.com/open-toolchain/tekton-catalog)
- Add that github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `git`

## Usages

- The `sample` sub-directory contains an EventListener definition that you can include in your CD tekton pipeline configuration to run an example showing a simple usage of the `git-clone-repo`.

  See the documentation [here](./sample/README.md)

- The `sample-git-trigger` sub-directory contains several EventListener definitions that you can include in your CD tekton pipeline configuration to run an example showing usage of the git-clone-repo in the context of CD tekton pipeline triggered by git event(s) (Commit pushed or PullRequest opened/updated)

  See the documentation [here](./sample-git-trigger/README.md)

- The `sample-set-commit-status` sub-directory contains several EventListener definitions that you can include in your CD tekton pipeline configuration to run an example demonstrating the usage of the `git-set-commit-status` task in the context of a CD Tekton pipeline triggered by a Git event (Commit push).

  See the documentation [here](./sample-set-commit-status/README.md)

- The `sample-git-pr-status` sub-directory contains several EventListener definitions that you can include in your CD tekton pipeline configuration to run an example demonstrating the usage of the `git-set-commit-status` in the context of a CD Tekton pipeline triggered by a Git Pull Request event (PullRequest push/update).

  See the documentation [here](./sample-git-pr-status/README.md)

## Details
### git-clone-repo

git clone

This Task fetches the credentials needed to perform git operations on a repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses it to clone (and/or perform the appropriate checkout if pull request parameters are given) of the repository.
The output of this task is the repository cloned into the directory on the workspace `workspace`.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains an [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and git intergation toolcard like `Git Repos and Issue Tracking` service if used).

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **ibmcloud-apikey-secret-key**: field in the secret that contains an [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and git intergation toolcard like `Git Repos and Issue Tracking` service if used). (default to `apikey`)
* **git-access-token**: (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **repository**: the git repository url that the toolchain is integrating
* **branch**: the git branch (default to `master`)
* **revision**: the git revision/commit to update the git HEAD to. Default is to mean only use the branch
* **fetch-gitoken-step-image**: image to use for the fetch-gitoken step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.49`)
* **git-client-image**: The image to use to run git clone commands (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.49`)
* **git-max-retry**: max retry for the git clone operation (default to `1`)
* **pr-repository**: the originating repository where the PullRequest comes from (in case of a fork) '' means same repository (not a fork) or it can be the same as the repository to clone
* **pr-branch**: the branch that is the source of this PullRequest
* **pr-revision**: the commit/revision in the source branch of the PullRequest that is to be built
* **directory-name**: name of the new directory to clone into. `.` means to clone at the root of the workspace It will be set to the "humanish" part of the repository if this param is set to blank (default to `.`)
* **properties-file**: name of the properties file that will be created as an additional outcome of this task in the workspace `workspace`. This file will contains the git related information (`GIT_URL`, `GIT_BRANCH` and `GIT_COMMIT`). This file can be used by downstream tasks to get the git information. (default to `build.properties`)
* **git-credentials-json-file**: JSON file containing the git credentials as found out of the clone task (can be a file path relative to the workspace). Default to '' meaning no output of this information
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)

#### Workspaces

* **output**: The git repo will be cloned onto the volume backing this workspace

#### Results
* **git-repository**: The cloned repository
* **git-branch**: The active branch for the repository
* **git-commit**: The current commit id that was cloned
* **git-user**: The auth user that cloned the repository
* **clone-directory**: the directory where the cloned repository content is located

### git-set-commit-status

set git commit status

This task is setting a git commit status for a given git commit (revision) in a git repository repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using).

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **ibmcloud-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **git-access-token**: (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **repository**: The git repository url
* **revision**: (optional) Commit SHA to set the status for. If left empty, will attempt to read GIT_COMMIT from build-properties
* **description**: A short description of the status.
* **context**: A string label to differentiate this status from the status of other systems. ie: "continuous-integration/tekton" (default to `continuous-integration/tekton`)
* **state**: The state of the status. Can be one of the following: `pending`, `running`, `success`, `failed`, `canceled` or the execution status of pipelineTask (or aggregation status of pipeline Tasks) : `Succeeded`, `Failed`, `Completed` and `None` (see https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md#using-aggregate-execution-status-of-all-tasks) or a value meaningful for the target git repository - gitlab/hostedgit: `pending`, `running`, `success`, `failed`, `canceled` - github/integrated github: `pending`, `success`, `failure`, `error` - bitbucket: `SUCCESSFUL`, `FAILED`, `INPROGRESS`, `STOPPED`
* **state-var**: Customized variable stored in build-properties to use as state if state params is empty.
* **build-properties**: file containing properties out of clone task (can be a filepath name relative to the workspace/volume) (default to `build.properties`)
* **target-url**: (optional) a url to set as the status detail link for the PR. If left empty, the status detail link will point to the pipeline run.
* **fetch-git-information-step-image**: image to use for the fetch-git-information step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **set-status-step-image**: image to use for the fetch-git-information step (default to `registry.access.redhat.com/ubi8/ubi:8.1`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)

#### Workspaces

* **artifacts**: Workspace that may contain git repository information (ie build.properties). Should be marked as optional when Tekton will permit it
