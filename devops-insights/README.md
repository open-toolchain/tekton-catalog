# IBM Cloud Devops Insights related tasks

- **[doi-publish-buildrecord](#doi-publish-buildrecord)**: This task publishes build record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-publish-testrecord](#doi-publish-testrecord)**: This task publishes test record(s) to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-publishing-test-data)
- **[doi-publish-deployrecord](#doi-publish-deployrecord)**: This task publishes deploy record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-evaluate-gate](#doi-evaluate-gate)**: This task evaluates [DevOps Insights gate policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-evaluate-gates-cli)

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `devops-insights`

## Usage
The `sample` sub-directory contains an EventListener and Pipeline definition that you can include in your Tekton pipeline configuration to run an example of the differents DOI related tasks.

## doi-publish-buildrecord
This task publishes build record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **toolchain-apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Toolchain (secret name and secret key can be configured using Task's params).

### Parameters

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: (optional) Toolchain service instance id. Default to the toolchain containing the CD Tekton pipelineRun currently executed.
* **build-number**: (optional) Devops Insights build number reference. Default to the CD Tekton Pipeline build number.
* **build-status**: (optional) the build status (can be either pass | fail). Default to pass.
* **git-repository**: The url of the git repository
* **git-branch**: The repository branch on which the build has been performed
* **git-commit**: The git commit id
* **job-url**: (optional) The url to the job's build logs. Default to the CD Tekton PipelineRun currently executed.
* **ibmcloud-api**: (optional) the ibmcloud api. Default to https://cloud.ibm.com
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
* **toolchain-apikey-secret-key**: (optional) field in the secret that contains the api key used to access toolchain and DOI instance. Default to `toolchain-apikey`
* **pipeline-debug**: (optional) Pipeline debug mode. Value can be 0 or 1. Default to 0
* **publish-build-record-step-image**: (optional) image to use for the publish-build-record step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.46`

## doi-publish-testrecord
This task publishes test record(s) to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-publishing-test-data)

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: (optional) Toolchain service instance id. Default to the toolchain containing the CD Tekton pipelineRun currently executed.
* **build-number**: (optional) Devops Insights build number reference. Default to the CD Tekton Pipeline build number.
* **file-locations**: Semi-colon separated list of test result file locations
* **test-types**: Semi-colon separated list of test result types
* **environment**: (optional) The environment name to associate with the test results. This option is ignored for unit tests, code coverage tests, and static security scans.
* **ibmcloud-api**: (optional) the ibmcloud api. Default to https://cloud.ibm.com
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
* **toolchain-apikey-secret-key**: (optional) field in the secret that contains the api key used to access toolchain and DOI instance. Default to `toolchain-apikey`
* **publish-testrecord-step-image**: (optional) Image to use for the publish-testrecord step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.46`
* **pipeline-debug**: (optional) Pipeline debug mode. Value can be 0 or 1. Default to 0

## doi-publish-deployrecord
This task publishes deploy record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: (optional) Toolchain service instance id. Default to the toolchain containing the CD Tekton pipelineRun currently executed.
* **build-number**: (optional) Devops Insights build number reference. Default to the CD Tekton Pipeline build number.
* **environment**: The environment name to associate with the test results. This option is ignored for unit tests, code coverage tests, and static security scans.
* **deploy-status**: (optional) The deployment status (can be either pass | fail). Default to pass
* **job-url**: (optional) The url to the job's deployment logs. Default to the CD Tekton PipelineRun currently executed.
* **app-url**: (optional) The URL where the deployed app is running
* **ibmcloud-api**: (optional) the ibmcloud api. Default to https://cloud.ibm.com
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
* **toolchain-apikey-secret-key**: (optional) field in the secret that contains the api key used to access toolchain and DOI instance. Default to `toolchain-apikey`
* **publish-deployrecord-step-image**: (optional) Image to use for the publish-deployrecord step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.46`
* **pipeline-debug**: (optional) Pipeline debug mode. Value can be 0 or 1. Default to 0

## doi-evaluate-gate
This task evaluates [DevOps Insights gate policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-evaluate-gates-cli)

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: (optional) Toolchain service instance id. Default to the toolchain containing the CD Tekton pipelineRun currently executed.
* **build-number**: (optional) Devops Insights build number reference. Default to the CD Tekton Pipeline build number.
* **policy**: The name of the policy that the gate uses to make its decision
* **force**: (optional) indicate if the evaluation gate should be forced or not ("true" | "false"). Default to true
* **ibmcloud-api**: (optional) the ibmcloud api. Default to https://cloud.ibm.com
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
* **toolchain-apikey-secret-key**: (optional) field in the secret that contains the api key used to access toolchain and DOI instance. Default to `toolchain-apikey`
* **evaluate-gate-step-image**: (optional) image to use for the evaluate-gate step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.46`
* **pipeline-debug**: (optional) Pipeline debug mode. Value can be 0 or 1. Default to 0
