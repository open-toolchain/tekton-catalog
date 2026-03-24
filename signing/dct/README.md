# These tasks have been deprecated and are no longer supported.
# Signing - Docker Content Trust related tasks

## Available Tasks
- **[signing-dct-enforcement-policy](#signing-dct-enforcement-policy) [deprecated]**: This task installs [Container Image Security Enforcement](https://cloud.ibm.com/docs/Registry?topic=Registry-security_enforce) on a given cluster.
- **[signing-dct-init](#signing-dct-init) [deprecated]**: This task initialize Docker Content Trust GUN/repository
- **[signing-dct-sign](#signing-dct-sign) [deprecated]**: This task performs a Docker Content Trust signature on a given image

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `signing/dct`

## Details
### signing-dct-enforcement-policy [deprecated]

This task installs [Container Image Security Enforcement](https://cloud.ibm.com/docs/Registry?topic=Registry-security_enforce) on a given cluster.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud service

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **shuttle-properties-file** **[required]**: properties file in the workspace that contains DCT initialization information
* **region** **[required]**: target region
* **resource-group** **[required]**: the resource group
* **cluster-name** **[required]**: the name of the targeted cluster
* **cluster-namespace** **[required]**: The cluster namespace to deploy rules
* **helm-version**: specific helm version (default to `2.16.6`)
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud service (default to `apikey`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)
* **commons-hosted-region**:  (default to `https://raw.githubusercontent.com/open-toolchain/commons/master`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located

### signing-dct-init [deprecated]

This task initialize Docker Content Trust GUN/repository

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud service

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **image-name** **[required]**: The image name that Docker Content Trust will be configured for
* **vault-region**: the region of the keyprotect instance (default to empty string)
* **vault-resource-group**: the resource group of the keyprotect instance (default to empty string)
* **vault-name** **[required]**: the key protect instance name
* **registry-namespace** **[required]**: The registry namespace
* **registry-region** **[required]**: the registry region
* **validation-signer** **[required]**: validation signer
* **build-signer** **[required]**: build signer
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud service (default to `apikey`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)
* **commons-hosted-region**:  (default to `https://raw.githubusercontent.com/open-toolchain/commons/master`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located

#### Results
* **shuttle-properties-file**: The properties file that will contains Docker Content Trust initialization information

### signing-dct-sign [deprecated]

This task performs a Docker Content Trust signature on a given image

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud service

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **image-repository** **[required]**: the repository of the image to sign
* **image-digest** **[required]**: the image digest (sha-256 hash) for the image to sign
* **image-tags** **[required]**: the tags for the image to sign
* **signer** **[required]**: current signer
* **vault-region** **[required]**: the region of the keyprotect instance
* **vault-resource-group** **[required]**: the resource group of the keyprotect instance
* **vault-name** **[required]**: the key protect instance name
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud service (default to `apikey`)
* **docker-client-image**: The Docker image to use to run the Docker client (default to `docker`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)
* **commons-hosted-region**:  (default to `https://raw.githubusercontent.com/open-toolchain/commons/master`)
