# Open-Toolchain Tekton Catalog

Catalog of Tasks usable in [Continuous Delivery Tekton Pipelines](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines)

**If you want `v1alpha1` resources, you need to reference the [`tekton_pipeline0.10.1`](https://github.com/open-toolchain/tekton-catalog/releases/tag/tekton_pipeline0.10.1) tag (or
[`tekton_pipeline0.10.1_workspace`](https://github.com/open-toolchain/tekton-catalog/releases/tag/tekton_pipeline0.10.1_workspace) tag to have `v1alpha1` resources using workspaces). The master branch will be synced with tkn_v1beta1 on 2020, 17th June.**

**Note**: 
- These tasks are usable with Tekton Beta Worker Agent (Tekon definition with apiVersion: v1beta1). These tasks have been updated  following migration path described in https://github.com/tektoncd/pipeline/blob/v0.11.2/docs/migrating-v1alpha1-to-v1beta1.md

## Breaking Changes

- These tasks are using **kebab-case style for EVERY parameters names**. So parameter `pathToContext` (in previous versions of the tasks) has been renamed as `path-to-context`, parameter `clusterName` has been renamed to `cluster-name` and so on...
- `communication` folder has been renamed to `slack` folder
- Some tasks has been renamed to match the following name format `<category alias>-<task>` where category alias is depending on the folder containing the tasks:

  | Folder/Category | Category alias |
  |--------|----------------|
  | cloudfoundry | cf |
  | container-registry | icr |
  | devops-insights | doi |
  | git | git |
  | kubernetes-service | iks |
  | slack | slack |
  | toolchain | toolchain |

  The task new names are listed in the following table:

  | Folder | Old task name | New task name |
  |--------|---------------|---------------|
  | container-registry | containerize-task | icr-containerize |
  | container-registry | cr-build-task | icr-cr-build |
  | container-registry | execute-in-dind-task | icr-execute-in-dind |
  | container-registry | execute-in-dind-cluster-task | icr-execute-in-dind-cluster |
  | container-registry | vulnerability-advisor-task | icr-check-va-scan |
  | git | clone-repo-task | git-clone-repo |
  | git | set-commit-status | git-set-commit-status |
  | kubernetes-service | fetch-iks-cluster-config | iks-fetch-config |
  | kubernetes-service | kubernetes-contextual-execution | iks-contextual-execution |
  | slack | post-slack | slack-post-message |

- Tasks that use workspace(s) may have changed the expected workspace name. Here is the list of the breaking changes for the expected workspace name

  | Folder | Task | Old workspace name | New workspace name | Description |
  | -- | -- | -- | -- | -- | 
  | container-registry | icr-containerize | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-cr-build | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-execute-in-dind | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-execute-in-dind-cluster | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-check-va-scan | workspace | artifacts | Workspace that may contain image information and will have the va report from the VA scan after this task exection |
  | git | git-clone-repo | workspace | output | Workspace where the git repository will be cloned into |
  | git | git-set-commit-status | workspace | artifacts | Workspace that may contain git repository information (ie build.properties). Should be marked as optional when Tekton will permit it |
  | kubernetes-service | iks-fetch-config | workspace | cluster-configuration | A workspace where the kubernetes cluster config is exported |
  | kubernetes-service | iks-contextual-execution | workspace | cluster-configuration | A workspace that contain the kubectl cluster config to be used |
  
# Tasks 

## Cloud Foundry related tasks

- **cf-deploy-app**: This task allows to perform a deployment of a Cloud Foundry application using `ibmcloud cf` commands. [Documentation is here](./cloudfoundry/README.md)

## Git related tasks

- **git-clone-repo**: This Task fetches the credentials needed to perform a git clone of a repo specified by a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses them to clone the repo. [Documentation is here](./git/README.md)
- **git-set-commit-status**: This task is setting a git commit status for a given git commit (revision) in a git repository repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using). [Documentation is here](./git/README.md)


## IBM Cloud Container Registry related tasks

- **icr-containerize**: This task is building and pushing an image to [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task is relying on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image. [Documentation is here](./container-registry/README.md)
- **icr-cr-build**: This task builds and pushes an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started) `build` command to perform the build of the image. [Documentation is here](./container-registry/README.md)
- **icr-execute-in-dind**: This task runs `docker` commands (build, inspect...) that communicate with a sidecar dind, and push the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). [Documentation is here](./container-registry/README.md)
- **icr-execute-in-dind-cluster**: This task runs `docker` commands (build, inspect...) that communicate with a docker dind instance hosted in a kubernetes cluster (eventually deploying the Docker DinD if needed), and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). [Documentation is here](./container-registry/README.md)
- **icr-check-va-scan**: This task is verifying that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and process the outcome of the scan. [Documentation is here](./container-registry/README.md)

## IBM Cloud Devops Insights related tasks

- **doi-publish-buildrecord**: This task publishes build record to DevOps Insights
- **doi-publish-testrecord**: This task publishes test record to DevOps Insights
- **doi-publish-deployrecord**: This task publishes deploy record to DevOps Insights
- **doi-evaluate-gate**: This task evaluates DevOps Insights gate policy

## IBM Cloud Kubernetes Service related tasks

- **iks-fetch-config**: This task is fetching the configuration of a [IBM Cloud Kubernetes Service cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) that is required to perform `kubectl` commands. [Documentation is here](./kubernetes-service/README.md)
- **iks-contextual-execution**: This task is executing bash snippet/script in the context of a Kubernetes cluster configuration. [Documentation is here](./kubernetes-service/README.md)

## Open-Toolchain related tasks

- **toolchain-publish-deployable-mapping**: This task creates or updates a toolchain deployable mapping for the toolchain [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). [Documentation is here](./toolchain/README.md)

## Slack related tasks

- **slack-post-message**: This Task posts a message to the Slack channel(s) integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack). [Documentation is here](./slack/README.md)
