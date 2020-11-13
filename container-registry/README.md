# Container-Registry related tasks

- **[icr-containerize](#icr-containerize)**: This task builds and pushes an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image.
- **[icr-execute-in-dind](#icr-execute-in-dind)**: This task runs `docker` commands (build, inspect...) against a Docker engine running as a sidecar container, and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **[icr-execute-in-dind-cluster](#icr-execute-in-dind-cluster)**: This task runs `docker` commands (build, inspect...) against a Docker engine running in a Kubernetes cluster (a Docker DinD instance will be deployed if none is available on the build cluster), and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **[icr-check-va-scan](#icr-check-va-scan)**: This task verifies that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and processes the outcome of the scan.
- **[icr-cr-build](#icr-cr-build) - deprecated**: This task relies on [IBM Cloud Container Registry](https://cloud.ibm.com/docs/container-registry-cli-plugin?topic=container-registry-cli-plugin-containerregcli#bx_cr_build) `build` command that is deprecated.

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `container-registry`

## icr-containerize

Build Image helper task using buildkit

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service (secret name and secret key can be configured using Task's params).

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

### Parameters

* **image-url** : (optional) the url of the image to build required if no image pipeline resource provided or no registry region, namespace and image name parameters are provided to this task.
* **registry-region**: (optional) container registry region id. required if no image-url or no image pipeline resources provided.
* **registry-namespace**: (optional) container registry namespace. required if no image-url or no image pipeline resources provided.
* **image-name**: (optional) image name. required if no image-url or no image pipeline resources provided.
* **path-to-context**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **path-to-dockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.` meaning current directory)
* **buildkit-image**: (optional) The name of the BuildKit image used (default to `moby/buildkit:v0.6.3-rootless`)
* **additional-tags**: (optional) comma-separated list of tags for the built image
* **additional-tags-script**: (optional) Shell script commands that will be invoked to provide additional tags for the build image
* **properties-file**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the pvc. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `REGISTRY_REGION`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation
*  **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
*  **container-registry-apikey-secret-key**: field in the secret that contains the api key used to connect to ibmcloud container registry. Default to `apikey`

### Results

* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

### Resources

#### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## icr-cr-build - deprecated

Build Image helper task using `ibmcloud cr build` command

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service (secret name and secret key can be configured using Task's params).

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

### Parameters

* **image-url** : (optional) the url of the image to build required if no image pipeline resource provided or no registry region, namespace and image name parameters are provided to this task.
* **registry-region**: (optional) container registry region id. required if no image-url or no image pipeline resources provided.
* **registry-namespace**: (optional) container registry namespace. required if no image-url or no image pipeline resources provided.
* **image-name**: (optional) image name. required if no image-url or no image pipeline resources provided.
* **path-to-context**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **path-to-dockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.` meaning current directory)
* **additional-tags**: (optional) comma-separated list of tags for the built image
* **additional-tags-script**: (optional) Shell script commands that will be invoked to provide additional tags for the build image
* **properties-file**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `REGISTRY_REGION`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation
*  **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
*  **container-registry-apikey-secret-key**: (optional) field in the secret that contains the api key used to connect to ibmcloud container registry. Default to `apikey`

### Results

* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

### Resources

#### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## icr-execute-in-dind

This task runs `docker` commands (build, inspect...) that communicate with a sidecar _Docker-In-Docker_ (DIND), and pushes the resulting image to the IBM Cloud Container Registry.

**Note:** the **Docker engine** used to execute the commands is **transient**, created by the task as a sidecar container,
and is available only during the task's lifespan.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service (secret name and secret key can be configured using Task's params).

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

### Parameters

* **image-url** : (optional) the url of the image to build - required if no image pipeline resource provided to this task
* **image-tag**: (optional) the tag for the built image (default to `latest`) 
* **path-to-context**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **path-to-dockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.`) 
* **dockerfile**: (optional) the name of the Dockerfile that is used for the build (default to `Dockerfile`) 
* **docker-client-image**: (optional) The Docker image to use to run the Docker client (default to `docker`) 
* **properties-file**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **docker-commands**: (optional) The docker command(s) to run. Default commands:
  ```
  docker build --tag "$IMAGE_URL:$IMAGE_TAG" --file $PATH_TO_DOCKERFILE/$DOCKERFILE $PATH_TO_CONTEXT
  docker inspect ${IMAGE_URL}:${IMAGE_TAG}
  docker push ${IMAGE_URL}:${IMAGE_TAG}
  ```
*  **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
*  **container-registry-apikey-secret-key**: (optional) field in the secret that contains the api key used to connect to ibmcloud container registry. Default to `apikey`

### Results

* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

### Resources

#### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## icr-execute-in-dind-cluster

This task runs `docker` commands (build, inspect...) that communicate with a  _Docker-In-Docker_ (DIND) instance hosted in a kubernetes cluster (eventually deploying the Docker DinD if needed), and pushes the resulting image to the IBM Cloud Container Registry.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service (secret name and secret key can be configured using Task's params).

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

### Parameters

* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation
* **cluster-region**: (optional) the ibmcloud region hosting the cluster (if value is `` it will default to the toolchain region)
* **cluster-namespace**: (optional) the kubernetes cluster namespace where the docker engine is hosted/deployed (default to `build`)
* **cluster-name**: (optional) name of the docker build cluster - required if no cluster pipeline resource provided to this task
* **image-url** : (optional) the url of the image to build - required if no image pipeline resource provided to this task
* **image-tag**: (optional) the tag for the built image (default to `latest`) 
* **path-to-context**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **path-to-dockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.`) 
* **dockerfile**: (optional) the name of the Dockerfile that is used for the build (default to `Dockerfile`) 
* **docker-client-image**: (optional) The Docker image to use to run the Docker client (default to `docker`) 
* **properties-file**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **docker-commands**: (optional) The docker command(s) to run. Default commands:
  ```
  docker build --tag "$IMAGE_URL:$IMAGE_TAG" --file $PATH_TO_DOCKERFILE/$DOCKERFILE $PATH_TO_CONTEXT
  docker inspect ${IMAGE_URL}:${IMAGE_TAG}
  docker push ${IMAGE_URL}:${IMAGE_TAG}
  ```
*  **continuous-delivery-context-secret**: (Optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
*  **container-registry-apikey-secret-key**: (optional) field in the secret that contains the api key used to connect to ibmcloud container registry. Default to `apikey`

### Results

* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

### Resources

#### Inputs

* **cluster**: (optional) The Cluster PipelineResource that will be used to host the Docker DinD to build Docker images. Only the name property is used to identify the cluster name.

#### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## icr-check-va-scan

Vulnerability Advisor helper task

### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**

  Secret containing:
  * **apikey**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service (secret name and secret key can be configured using Task's params).

  Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

### Parameters

* **image-url**: (optional) url of the image to VA scan - required if no image pipeline resource provided to this task
* **image-digest**: (optional) SHA id of the image to VA scan - required if no image pipeline resource provided and no `image-properties-file` value provided
* **image-properties-file**: file containing properties of the image to be scanned (default to 'build.properties')
* **max-iteration**: maximum number of iterations allowed while loop to check for va report (default to 30 iterations maximum)
* **sleep-time**: sleep time (in seconds) between invocation of ibmcloud cr va in the loop (default to 10 seconds between scan result inquiry)
* **scan-report-file**: (optional) filename for the scan report (json format) of the given image. It will be copied in the workspace
* **fail-on-scanned-issues**: flag (`true` | `false`) to indicate if the task should fail or continue if issues are found in the image scan result (default to 'true')
* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation
*  **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
*  **container-registry-apikey-secret-key**: (optional) field in the secret that contains the api key used to connect to ibmcloud container registry. Default to `apikey`

### Results

* **scan-report-file**: the filename if the scan report for the image stored in the workspace
* **scan-status**: the status from Vulnerability Advisor - possible values: OK, WARN, FAIL, UNSUPPORTED, INCOMPLETE, UNSCANNED

### Workspaces

* **artifacts**: Workspace that may contain image information and will have the va report from the VA scan after this task execution

### Resources

#### Inputs

* **image**: (optional) The Image PipelineResource that this task will process the Vulnerability Advisor scan result.

## Usages

- The `sample` sub-directory contains an `event-listener-container-registry` EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `icr-containerize` and `icr-check-va-scan`.
  It also contains a `buildkit-no-resources` EventListener definition which is the providing the same example but without the needs to define PipelineResources for image as it uses the task's parameter `image-url` to provide the information

  See the documentation [here](./sample/README.md)

- The `sample-cr-build` sub-directory contains an `cr-build` EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `icr-cr-build` and `icr-check-va-scan`.
  It also contains a `cr-build-no-resources` EventListener definition which is the providing the same example but without the needs to define PipelineResources for image as it uses the task's parameter `image-url` to provide the information.

  See the documentation [here](./sample-cr-build/README.md)

- The `sample-docker-dind-sidecar` sub-directory contains an `event-listener-dind` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `icr-execute-in-dind` and `icr-check-va-scan`.
  It also contains a `dind-no-resources` EventListener definition which is the providing the same example but without the needs to define PipelineResources for image as it uses the task's parameter `image-url` to provide the information

  See the documentation [here](./sample-docker-dind-sidecar/README.md)

- The `sample-docker-dind-cluster` sub-directory contains an `event-listener-dind-cluster` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `icr-execute-in-dind-cluster` and `icr-check-va-scan`.
  It also contains a `dind-cluster-no-resources` EventListener definition which is the providing the same example but without the needs to define PipelineResources for image as it uses the task's parameter `image-url` to provide the information

  See the documentation [here](./sample-docker-dind-cluster/README.md)

