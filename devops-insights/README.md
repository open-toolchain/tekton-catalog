# IBM Cloud Devops Insights related tasks

## Available tasks
- **[doi-evaluate-gate](#doi-evaluate-gate) [deprecated]**: This task evaluates [DevOps Insights gate policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-evaluate-gates-cli)
- **[doi-publish-buildrecord](#doi-publish-buildrecord) [deprecated]**: This task publishes build record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-publish-deployrecord](#doi-publish-deployrecord) [deprecated]**: This task publishes deploy record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-publish-testrecord](#doi-publish-testrecord) [deprecated]**: This task publishes test record(s) to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-publishing-test-data)

## Pre-requisites
These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `devops-insights`

## Usage
The `sample` sub-directory contains an EventListener and Pipeline definition that you can include in your Tekton pipeline configuration to run an example of the differents DOI related tasks.

## Details
### doi-evaluate-gate [deprecated]

This task evaluates [DevOps Insights gate policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-evaluate-gates-cli)

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets

  Secret containing:
  * **toolchain-apikey**: field in the secret that contains the api key used to access toolchain and DOI instance

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: Toolchain service instance id. Default to the toolchain containing the CD Tekton PipelineRun currently executed
* **build-number**: Devops Insights build number reference. Default to the CD Tekton Pipeline build number
* **policy**: The name of the policy that the gate uses to make its decision
* **force**: indicate if the evaluation gate should be forced or not ("true" | "false") (default to `true`)
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets (default to `secure-properties`)
* **toolchain-apikey-secret-key**: field in the secret that contains the api key used to access toolchain and DOI instance (default to `toolchain-apikey`)
* **evaluate-gate-step-image**: image to use for the evaluate-gate step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. Default to 0 (default to `0`)

### doi-publish-buildrecord [deprecated]

This task publishes build record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets

  Secret containing:
  * **toolchain-apikey**: field in the secret that contains the api key used to access toolchain and DOI instance

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: Toolchain service instance id. Default to the toolchain containing the CD Tekton PipelineRun currently executed
* **build-number**: Devops Insights build number reference. Default to the CD Tekton Pipeline build number
* **build-status**: the build status (can be either pass | fail) (default to `pass`)
* **git-repository**: The url of the git repository
* **git-branch**: The repository branch on which the build has been performed
* **git-commit**: The git commit id
* **job-url**: The url to the job's build logs. Default to the CD Tekton PipelineRun currently executed
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets (default to `secure-properties`)
* **toolchain-apikey-secret-key**: field in the secret that contains the api key used to access toolchain and DOI instance (default to `toolchain-apikey`)
* **publish-build-record-step-image**: image to use for the publish-build-record step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. Default to 0 (default to `0`)

#### Results
* **build-number**: Devops Insights build number reference used

### doi-publish-deployrecord [deprecated]

This task publishes deploy record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets

  Secret containing:
  * **toolchain-apikey**: field in the secret that contains the api key used to access toolchain and DOI instance

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: Toolchain service instance id. Default to the toolchain containing the CD Tekton PipelineRun currently executed
* **build-number**: Devops Insights build number reference. Default to the CD Tekton Pipeline build number
* **environment**: The environment where the pipeline job deployed the app.
* **deploy-status**: The deployment status (can be either pass | fail) (default to `pass`)
* **job-url**: The url to the job's deployment logs. Default to the CD Tekton PipelineRun currently executed
* **app-url**: The URL where the deployed app is running
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets (default to `secure-properties`)
* **toolchain-apikey-secret-key**: field in the secret that contains the api key used to access toolchain and DOI instance (default to `toolchain-apikey`)
* **publish-deployrecord-step-image**: image to use for the publish-deployrecord step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)

### doi-publish-testrecord [deprecated]

This task publishes test record(s) to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-publishing-test-data)

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets

  Secret containing:
  * **toolchain-apikey**: field in the secret that contains the api key used to access toolchain and DOI instance

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **app-name**: Logical application name for DevOps Insights
* **toolchain-id**: Toolchain service instance id. Default to the toolchain containing the CD Tekton PipelineRun currently executed
* **build-number**: Devops Insights build number reference. Default to the CD Tekton Pipeline build number
* **file-locations**: Semi-colon separated list of test result file locations
* **test-types**: Semi-colon separated list of test result types
* **environment**: Optional, The environment name to associate with the test results. This option is ignored for unit tests, code coverage tests, and static security scans.
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets (default to `secure-properties`)
* **toolchain-apikey-secret-key**: field in the secret that contains the api key used to access toolchain and DOI instance (default to `toolchain-apikey`)
* **publish-testrecord-step-image**: image to use for the publish-testrecord step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. Default to 0 (default to `0`)

#### Workspaces

* **artifacts**: A workspace containing the test results file to pubslih to DOI
