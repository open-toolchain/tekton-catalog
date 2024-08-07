# Git related tasks

- **[git-clone-repo](#git-clone-repo)**: This Task fetches the credentials needed to perform git operations on a repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses it to clone (and/or perform the appropriate checkout if pull request parameters are given) of the repository.
- **[git-set-commit-status](#git-set-commit-status)**: This task is setting a git commit status for a given git commit (revision) in a git repository repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using)

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

## git-clone-repo

Git integration clone task

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and `Git Repos and Issue Tracking` service if used). Note: secret name and secret key can be configured using Task's params.

  If this secret is provided, it will be used to obtain the the git token for the git integration in the toolchain

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

### Parameters

* **git-access-token**: (optional) token to access the git repository. Either `secure-properties` or git-access-token has to be provided.
* **git-max-retry**: max retry for the git clone operation (default to "1")
* **repository**: the git repository url that the toolchain is integrating
* **branch**: the git branch (default value to `master`). This param can also be given as a full _git ref_ like `refs/heads/master` (as described by [Git References](https://git-scm.com/book/en/v2/Git-Internals-Git-References))
* **revision**: (optional) the git revision/commit to update the git HEAD to (default to empty meaning only use the branch information)
* **pr-repository**: the originated repository where the PullRequest come from (in case of a fork). Default to '' means same repository (not a fork) or it can be the same as repository to clone.
* **pr-branch**: the branch that is the source of this PullRequest. Default to ''.
* **pr-revision**: the commit/revision in the source branch of the PullRequest that is to be built. Defaults to ''.
* **directory-name**: (optional) name of the new directory to clone into (default to `.` in order to clone at the root of the volume mounted for the pipeline run). Note: It will be to the "humanish" part of the repository if this param is set to blank
* **properties-file**: (optional) name of the properties file that will be created as an additional outcome of this task in the workspace `workspace`. This file will contains the git related information (`GIT_URL`, `GIT_BRANCH` and `GIT_COMMIT`)
* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secret (default to `secure-properties`)
* **ibmcloud-apikey-secret-key**: (optional) field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **git-credentials-json-file**: (optional) name of JSON file to store git credentials found out of the clone task (it can be a file path relative to the workspace `workspace` backed by a volume). Default to '' meaning no output of this information.
* **fetch-gitoken-step-image**: (optional) image to use for the fetch-gitoken step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.46`

### Workspaces

* **output**: The git repo will be cloned onto the volume backing this workspace

### Results
* **git-repository**: The cloned repository
* **git-branch**: The active branch for the repository
* **git-commit**: The current commit id that was cloned
* **git-user**: The auth user that cloned the repository
* **clone-directory**: The directory where the cloned repository content is located

### Outcome
The output of this task is the repository cloned into the directory on the workspace `workspace`.

## git-set-commit-status

Git commit status setter task

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and `Git Repos and Issue Tracking` service if used). Note: secret name and secret key can be configured using Task's params.

  If this secret is provided, it will be used to obtain the the git token for the git integration in the toolchain

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

### Parameters

* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secret (default to `secure-properties`)
* **ibmcloud-apikey-secret-key**: (optional) field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **git-access-token**: (optional) token to access the git repository. Either `secure-properties` secret or `git-access-token` has to be provided.
* **repository**: the git repository url that the toolchain is integrating
* **revision**: the git revision/commit to update the status
* **description**: A short description of the status.
* **context**: (optional) A string label to differentiate this status from the status of other systems. (default to `continuous-integration/tekton`)
* **state**: The state of the status. Can be one of the following: `pending`, `running`, `success`, `failed`, `canceled` or a value meaningful for the target git repository (gitlab/hostedgit: `pending`, `running`, `success`, `failed`, `canceled` - github/integrated github: `pending`, `success`, `failure`, `error` - bitbucket: `SUCCESSFUL`, `FAILED`, `INPROGRESS`, `STOPPED`)
* **state-var**: Customized variable stored in `properties-file` (like `build-properties` for instance) to use as state if `state` input param is empty.
* **properties-file**: (optional) name of a properties file that may contain the state as value for the entry/key defined by `state-var` (default to `build.properties`)
* **target-url**: (optional) a url to set as the status detail link for the PR.  If left empty, the status detail link will point to the pipeline run.
* **fetch-git-information-step-image**: (optional) image to use for the fetch-git-information step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.46`)
* **set-status-step-image**: (optional) image to use for the fetch-git-information step (default to `registry.access.redhat.com/ubi8/ubi:8.1`)

### Workspaces

* **artifacts**: Workspace that may contain git repository information (ie build.properties). Should be marked as optional when Tekton will permit it

## Git commit status setter task - set-commit-status

### Inputs

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resource to be defined:

* **Secret secure-properties (optional)**

  Secret containing:
  * **apikey**: An IBM Cloud Api Key allowing access to the toolchain (and `Git Repos and Issue Tracking` service if used)

  If this secret is provided, it will be used to obtain the the git token for the git integration in the toolchain

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

#### Parameters

* **task-pvc**: the input pvc - this is where the properties file (like `build.properties` defined in `propertiesFile` parameter) would be stored
* **resourceGroup**: (optional) target resource group (name or id) for the ibmcloud login operation
* **continuous-delivery-context-secret**: (optional) name of the configmap containing the continuous delivery pipeline context secret (default to `secure-properties`)
* **ibmcloud-apikey-secret-key**: (optional) field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **gitAccessToken**: (optional) token to access the git repository. Either `secure-properties` or gitAccessToken has to be provided.
* **repository**: the git repository url that the toolchain is integrating
* **revision**: the git revision/commit to update the status
* **description**: A short description of the status.
* **context**: (optional) A string label to differentiate this status from the status of other systems. (default to `continuous-integration/tekton`)
* **state**: The state of the status. Can be one of the following: `pending`, `running`, `success`, `failed`, `canceled` or a value meaningful for the target git repository (gitlab/hostedgit: `pending`, `running`, `success`, `failed`, `canceled` - github/integrated github: `pending`, `success`, `failure`, `error` - bitbucket: `SUCCESSFUL`, `FAILED`, `INPROGRESS`, `STOPPED`)
* **state-var**: Customized variable stored in `propertiesFile` (like `build-properties` for instance) to use as state if `state` input param is empty.
* **propertiesFile**: (optional) name of a properties file that may contain the state as value for the entry/key defined by `state-var` (default to `build.properties`)
