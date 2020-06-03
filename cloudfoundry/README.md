# Cloud Foundry related tasks

- **cf-deploy-cf-app**: this task allows to perform a deployment of a Cloud Foundry application using `ibmcloud cf` commands

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `cloudfoundry`

## Mappings between Toolchains & Deployables helper task: toolchain-publish-deployable-mapping

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **cf-apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Cloud Foundry target (secret name and secret key can be configured using Task's params).

### Parameters

*  **region**: (Optional) Name of the region for IBM Public Cloud Cloud Foundry operation. Will default to the toolchain region if none or empty value. Accessible as `${CF_REGION}` in the cf commands snippet.
*  **cf-org**: Name of organization to be targeted. Accessible as `${CF_ORG}` in the cf commands snippet.
*  **cf-space**: Name of space to be targeted. Accessible as `${CF_SPACE}` in the cf commands snippet.
*  **cf-app**: Name of the CF application to be managed. Accessible as `${CF_APP}` in the cf commands snippet.
*  **cf-commands**: (Optional) The snippet with ibmcloud cf command(s) to run. Default to `ibmcloud cf push "${CF_APP}"`
*  **ibmcloud-api**: (Optional) the ibmcloud api. Default to https://cloud.ibm.com
*  **continuous-delivery-context-secret**: (Optional) Name of the configmap containing the continuous delivery pipeline context secrets. Default to `secure-properties`
*  **cloud-foundry-apikey-secret-key**: field in the secret that contains the api key used to connect to cloud foundry. Default to `cf-apikey`
* **pipeline-debug**: (optional) Pipeline debug mode. Value can be 0 or 1. Default to 0

### Results

* **region**: Name of the region where Cloud Foundry commands were executed
* **cf-target-url**: Cloud Foundry API endpoint
* **cf-org-id**: Id of the Cloud Foundry organization
* **cf-space-id**: Id of the Cloud Foundry space
* **cf-app-guid**: GUID of the Cloud Foundry application managed using this tasks

### Workspaces

* **source**: A workspace containing the source of the Cloud Foundry application
