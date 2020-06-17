# Open-Toolchain related tasks

# Tasks

- **[toolchain-publish-deployable-mapping](#toolchain-publish-deployable-mapping)**: This task creates or updates a toolchain deployable mapping for the toolchain [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies toolchain endpoints described in [IBM Toolchain API](https://otc-swagger.us-south.devops.dev.cloud.ibm.com/swagger-ui?url=https://otc-api.us-south.devops.dev.cloud.ibm.com/spec/swagger.json#/toolchain_deployable_mappings).
- **[toolchain-extract-value](#toolchain-extract-value)**: This task extracts values from the desired config map with a given jq expression.

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `toolchain`

## toolchain-publish-deployable-mapping

This task helps to create or update mappings between Toolchains & Deployables. 

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

## toolchain-extract-value
This task is for extracting values from the desired config map with a given jq expression.
You have to provide a jq expression and the targeted config map's details.

### Parameters

- **config-map-name**: (Default: `toolchain`) The name of the ConfigMap
- **config-map-key**: (Default: `toolchain.json`) The key of the ConfigMap
- **expression**: A valid jq expression which is used to search
- **pipeline-debug**: (Default: `"0"`) enable pipeline debug mode

### Usage

The `toolchain-extract-value` task will save the desired value into a tekton task result.
Check out the example below, where we pass the result of the `extract-value` task to the `use-result-task` task.
In addition, you have to add the `extracted-value` param to the `use-result-task` task itself.

``` yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: example-pipeline
spec:
  params:
    - name: expression
      description: A valid jq expression which is used to search
  tasks:
    - name: extract-value
      taskRef:
        name: toolchain-extract-value
      params:
        - name: expression
          value: $(params.expression)
    - name: use-result-task
      runAfter: [extract-value]
      taskRef:
        name: use-result-task
      params:
        - name: extracted-value
          value: "$(tasks.extract-value.results.extracted-value)"
```
``` yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: use-result-task
spec:
  params:
    - name: extracted-value
      description: The extracted value from the extract-value task
  steps:
- name: use-result-task
  command: ["/bin/bash", "-c"]
  args:
    - |
      echo "$(params.extracted-value)"
```
