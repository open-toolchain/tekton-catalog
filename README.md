# Open-Toolchain Tekton Catalog

Catalog of Tasks usable in [Continuous Delivery Tekton Pipelines](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines)

**Note**: 
- These tasks are usable with Tekton Beta Worker Agent (Tekon definition with apiVersion: v1beta1). These tasks have been updated from `tkn_pipeline_beta_support` branch (that consists mainly of v0.10.1 tekton posture) following migration path described in https://github.com/tektoncd/pipeline/blob/v0.11.2/docs/migrating-v1alpha1-to-v1beta1.md

**Breaking Changes**:
- These tasks are using **kebab-case style for EVERY parameters names**. So parameter `pathToContext` (in previous versions of the tasks) has been renamed as `path-to-context`, parameter `clusterName` has been renamed to `cluster-name` and so on...

## Git related tasks

- **clone-repo-task**: This Task fetches the credentials needed to perform a git clone of a repo specified by a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses them to clone the repo. [Documentation is here](./git/README.md)
- **set-commit-status**: This task is setting a git commit status for a given git commit (revision) in a git repository repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using). [Documentation is here](./git/README.md)


## IBM Cloud Container Registry related tasks

- **containerize-task**: This task is building and pushing an image to [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task is relying on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image. [Documentation is here](./container-registry/README.md)
- **cr-build-task**: this task builds and pushes an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started) `build` command to perform the build of the image. [Documentation is here](./container-registry/README.md)
- **execute-in-dind-task**: This task runs `docker` commands (build, inspect...) that communicate with a sidecar dind, and push the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). [Documentation is here](./container-registry/README.md)
- **execute-in-dind-cluster-task**: This task runs `docker` commands (build, inspect...) that communicate with a docker dind instance hosted in a kubernetes cluster (eventually deploying the Docker DinD if needed), and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). [Documentation is here](./container-registry/README.md)
- **vulnerability-advisor-task**: This task is verifying that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and process the outcome of the scan. [Documentation is here](./container-registry/README.md)

## IBM Cloud Kubernetes Service related tasks

- **fetch-iks-cluster-config**: This task is fetching the configuration of a [IBM Cloud Kubernetes Service cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) that is required to perform `kubectl` commands. [Documentation is here](./kubernetes-service/README.md)
- **kubernetes-contextual-execution**: This task is executing bash snippet/script in the context of a Kubernetes cluster configuration. [Documentation is here](./kubernetes-service/README.md)

## Communication related tasks

- **post-slack**: This Task posts a message to the Slack channel(s) integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack). [Documentation is here](./communication/README.md)
