# This task has been deprecated and is no longer supported.

# Cloud Foundry related tasks

## Available tasks
- **[cf-deploy-app](#cf-deploy-app) [deprecated]**: This task allows to perform a deployment of a Cloud Foundry application using ibmcloud cf commands.

## Pre-requisites
These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `cloudfoundry`

## Details
### cf-deploy-app [deprecated]

This task allows to perform a deployment of a Cloud Foundry application using ibmcloud cf commands.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **cf-apikey**: field in the secret that contains the api key used to connect to cloud foundry

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **region**: Name of the region for IBM Public Cloud Cloud Foundry operation. Will default to the toolchain region if none or empty value. (default to empty string)
* **cf-org** **[required]**: Name of organization to be targeted
* **cf-space** **[required]**: Name of space to be targeted
* **cf-app** **[required]**: Name of the CF application to be managed
* **setup-script**: script that typically set up environment before the _cf-commands_ script execution. (default to empty string)
* **cf-commands**: The ibmcloud cf command(s) to run. (default to `# Push app
ibmcloud cf push "${CF_APP}"
`)
* **post-execution-script**: script that get executed after the _cf-commands_ script has been executed. (default to empty string)
* **shuttle-properties-file**: name of the properties file that contain properties to include in the environment for the _cf-commands_ script execution. (default to empty string)
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **cloud-foundry-apikey-secret-key**: field in the secret that contains the api key used to connect to cloud foundry (default to `cf-apikey`)
* **deploy-step-image**: image to use for the deploy step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)

#### Workspaces

* **source**: A workspace containing the source of the CF application to deploy

#### Results
* **region**: Name of the region where Cloud Foundry commands were executed
* **cf-target-url**: Cloud Foundry API endpoint
* **cf-org-id**: Id of the Cloud Foundry organization
* **cf-space-id**: Id of the Cloud Foundry space
* **cf-app-guid**: GUID of the Cloud Foundry application managed using this tasks
