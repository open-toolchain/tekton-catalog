# Open-Toolchain Tekton Catalog

Catalog of Tasks usable in [Continuous Delivery Tekton Pipelines](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines)

## Git related tasks

- clone-repo-task: This Task fetches the credentials needed to perform a git clone of a repo specified by a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses them to clone the repo. [Documentation is here](./git/README.md)

## IBM Cloud Container Registry related tasks

- containerize-task: This task is building and pushing an image to IBM Cloud Container Registry. This taks is relying on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image. [Documentation is here](./container-registry/README.md)