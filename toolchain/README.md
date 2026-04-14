# Open-Toolchain related tasks

## Available tasks
- **[toolchain-build](#toolchain-build)**: This task perform build operation on the given workspace. Default build operations managed are maven build for instance.
- **[toolchain-extract-value](#toolchain-extract-value)**: This task extracts values from the desired config map with a given jq expression.
- **[toolchain-publish-deployable-mapping](#toolchain-publish-deployable-mapping)**: This task creates or updates a toolchain deployable mapping for a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using). This task relies toolchain endpoints described in [IBM Toolchain API] (https://otc-swagger.us-south.devops.dev.cloud.ibm.com/swagger-ui?url=https://otc-api.us-south.devops.dev.cloud.ibm.com/spec/swagger.json#/toolchain_deployable_mappings).

## Prerequisites
These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `toolchain`

## Usages

- The `sample-build` sub-directory contains an EventListener definition that you can include in your CD tekton pipeline configuration to run an example showing a simple usage of the `toolchain-build`.

- The `sample-dm` sub-directory contains an EventListener definition that you can include in your CD tekton pipeline configuration to run an example showing a simple usage of the `toolchain-publish-deployable-mapping`.

- The `sample-environment` sub-directory contains an EventListener definition that you can include in your CD tekton pipeline configuration to run an example showing the available environment context provide by the IBM Cloud Continuous Delivery Tekton Support - See https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop.

- The `toolchain-extract-value` task will save the desired value into a tekton task result.
  Check out the example below, where we pass the result of the `extract-value` task to the `use-result-task` task.
  In addition, you have to add the `extracted-value` param to the `use-result-task` task itself.

  ``` yaml
  apiVersion: tekton.dev/v1
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
  apiVersion: tekton.dev/v1
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

## Details
### toolchain-build

This task perform build operation on the given workspace. Default build operations managed are maven build for instance.

#### Parameters

* **custom-script**: The command(s) to run the build in run-build step. It will override the default commands (default to empty string)
* **run-build-image**: The name of the image used for the run-build step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)

#### Workspaces

* **output**: A workspace backing by a volume

### toolchain-extract-value

This task extracts values from the desired config map with a given jq expression.

#### Parameters

* **config-map-name**: name of the config map (default to `toolchain`)
* **config-map-key**: key of the config map (default to `toolchain.json`)
* **expression** **[required]**: A valid jq expression which is used to search
* **extract-value-jq-step-image**: image to use for the extract-value-jq step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)
* **raw**: determines if extracted value should be a raw string (default to `1`)

#### Results
* **extracted-value**: The extracted value

### toolchain-publish-deployable-mapping

This task creates or updates a toolchain deployable mapping for a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using). This task relies toolchain endpoints described in [IBM Toolchain API] (https://otc-swagger.us-south.devops.dev.cloud.ibm.com/swagger-ui?url=https://otc-api.us-south.devops.dev.cloud.ibm.com/spec/swagger.json#/toolchain_deployable_mappings).

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets

  Secret containing:
  * **toolchain-apikey**: field in the secret that contains the api key used to access toolchain and DOI instance

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **deployable-type** **[required]**: type of the deployable. Can be either: - `app` for a CF application or - `kubernetes_cluster` for K8S deployment
* **deployable-region-id** **[required]**: IBM Cloud Region where the deployable is located. A fully qualified id is expected (such as ibm:yp:us-south) If not fully qualified, the ibmcloud production prefix is appended (ie 'ibm:yp:')
* **deployable-guid** **[required]**: GUID of the deployable (either cluster guid or cf app guid)
* **deployable-cf-org-id**: CF organization id (only required when deployable-type is `app`) (default to empty string)
* **deployable-cf-org-name**: CF organization name (only required when deployable-type is `app`). It will only be used for traceability event purpose. Default to `deployable-cf-org-id` (default to empty string)
* **deployable-cf-space-id**: CF space id (only required when deployable-type is `app`) (default to empty string)
* **deployable-cf-space-name**: CF space name (only required when deployable-type is `app`). It will only be used for traceability event purpose. Default to `deployable-cf-space-id` (default to empty string)
* **deployable-rg-id**: Resource Group id (only required when deployable-type is `kubernetes_cluster`) (default to empty string)
* **deployable-url**: an URL that represent the deployable, e.g. the application's URL. (default to empty string)
* **git-inputs**: list of git repository,commit and branch triple (repository,commit id and branch spearated by a comma). each triple-element of the list is contained in one line (default to empty string)
* **environment-label**: the label of the environment where the deployment has occured (default to `label of the deployed environment`)
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets (default to `secure-properties`)
* **toolchain-apikey-secret-key**: field in the secret that contains the api key used to access toolchain and DOI instance (default to `toolchain-apikey`)
* **publish-deployable-mapping-step-image**: image to use for the publish-deployable-mapping step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)
