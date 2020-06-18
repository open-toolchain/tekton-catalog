# IBM Cloud Devops Insights related tasks

- **[doi-publish-buildrecord](#doi-publish-buildrecord)**: This task publishes build record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-publish-testrecord](#doi-publish-testrecord)**: This task publishes test record(s) to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-publishing-test-data)
- **[doi-publish-deployrecord](#doi-publish-deployrecord)**: This task publishes deploy record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-evaluate-gate](#doi-evaluate-gate)**: This task evaluates [DevOps Insights gate policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-evaluate-gates-cli)

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `container-registry`

## doi-publish-buildrecord
This task publishes build record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)

## doi-publish-testrecord
This task publishes test record(s) to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-publishing-test-data)

## doi-publish-deployrecord
This task publishes deploy record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)

## doi-evaluate-gate
This task evaluates [DevOps Insights gate policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-evaluate-gates-cli)

## Usage
The `sample` sub-directory contains an EventListener and Pipeline definition that you can include in your Tekton pipeline configuration to run an example of the differents DOI related tasks.
