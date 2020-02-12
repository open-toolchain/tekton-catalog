# Open-Toolchain Tekton Catalog

Catalog of Tasks usable in [Continuous Delivery Tekton Pipelines](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines)

## Git related tasks

- **clone-repo-task**: This Task fetches the credentials needed to perform a git clone of a repo specified by a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses them to clone the repo. [Documentation is here](./git/README.md)

## IBM Cloud Container Registry related tasks

- **containerize-task**: This task is building and pushing an image to [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This taks is relying on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image. [Documentation is here](./container-registry/README.md)
- **vulnerability-advisor-task**: This task is verifying that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and process the outcome of the scan. [Documentation is here](./container-registry/README.md)

## IBM Cloud Kubernetes Service related tasks

- **fetch-iks-cluster-config**: This task is fetching the configuration of a [IBM Cloud Kubernetes Service cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) that is required to perform `kubectl` commands. [Documentation is here](./kubernetes-service/README.md)
- **kubernetes-contextual-execution**: This task is executing bash snippet/script in the context of a Kubernetes cluster configuration. [Documentation is here](./kubernetes-service/README.md)

## Communication related tasks

- **post-slack**: This Task posts a message to the Slack channel(s) integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack). [Documentation is here](./communication/README.md)
