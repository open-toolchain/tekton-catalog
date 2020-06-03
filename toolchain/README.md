# Open-Toolchain related tasks

- **toolchain-publish-deployable-mapping**: this task creates or updates a toolchain deployable mapping for the toolchain [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies toolchain endpoints described in [IBM Toolchain API](https://otc-swagger.us-south.devops.dev.cloud.ibm.com/swagger-ui?url=https://otc-api.us-south.devops.dev.cloud.ibm.com/spec/swagger.json#/toolchain_deployable_mappings).

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `toolchain`

## Mappings between Toolchains & Deployables helper task: toolchain-publish-deployable-mapping

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **toolchain-apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Toolchain (secret name and secret key can be configured using Task's params).

### Parameters

* **deployable-type**: Type of the deployable. Can be either `app` (for a CF application) or `kubernetes_cluster` (for K8S deployment)
* **deployable-region-id**: IBM Cloud Region where the deployable is located. A fully qualified id is expected (such as ibm:yp:us-south). If not fully qualified, the ibmcloud production prefix is appended (ie 'ibm:yp:')
* **deployable-guid**: GUID of the deployable (either cluster guid or cf app guid)
* **deployable-cf-org-id**: CF organization id (only required when deployable-type is `app`)
* **deployable-cf-space-id**: CF space id (only required when deployable-type is `app`)
* **deployable-rg-id**: Resource Group id (only required when deployable-type is `kubernetes_cluster`)
* **ibmcloud-api**: (optional) the ibmcloud api. Default to https://cloud.ibm.com
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
* **toolchain-apikey-secret-key**: (optional) field in the secret that contains the api key used to access toolchain and DOI instance. Default to `toolchain-apikey`
* **pipeline-debug**: (optional) Pipeline debug mode. Value can be 0 or 1. Default to 0