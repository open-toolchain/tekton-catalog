# Container-Registry related tasks

## Available tasks
- **[icr-check-va-scan](#icr-check-va-scan)**: This task verifies that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and processes the outcome of the scan.
- **[icr-containerize](#icr-containerize)**: This task builds and pushes (optionaly) an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image.
- **[icr-cr-build](#icr-cr-build) [deprecated]**: The [`ibmcloud cr build`](https://cloud.ibm.com/docs/container-registry-cli-plugin?topic=container-registry-cli-plugin-containerregcli#bx_cr_build) command is deprecated. If you use the [icr-cr-build](./container-registry/README.md#icr-cr-build) Tekton task, you can migrate to one of the three above Tekton tasks to build container images. For more information about this replacement, see the [IBM Cloud™ Container Registry is Deprecating Container Builds](https://www.ibm.com/cloud/blog/announcements/ibm-cloud-container-registry-deprecating-container-builds) blog post.
- **[icr-execute-in-dind-cluster](#icr-execute-in-dind-cluster)**: This task runs `docker` commands (build, inspect...) against a Docker engine running in a Kubernetes cluster (a Docker DinD instance will be deployed if none is available on the build cluster), and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **[icr-execute-in-dind](#icr-execute-in-dind)**: This task runs `docker` commands (build, inspect...) against a Docker engine running as a sidecar container, and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).

## Prerequisites
These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `container-registry`

## Usages

- The `sample` sub-directory contains an `buildkit-no-resources` EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `icr-containerize` and `icr-check-va-scan`.

  See the documentation [here](./sample/README.md)

- The `sample-cr-build` sub-directory contains an `cr-build-no-resources` EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `icr-cr-build` and `icr-check-va-scan`.

  See the documentation [here](./sample-cr-build/README.md)

- The `sample-docker-dind-sidecar` sub-directory contains an `dind-no-resources` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `icr-execute-in-dind` and `icr-check-va-scan`.

  See the documentation [here](./sample-docker-dind-sidecar/README.md)

- The `sample-docker-dind-cluster` sub-directory contains an `dind-cluster-no-resources` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `icr-execute-in-dind-cluster` and `icr-check-va-scan`.

  See the documentation [here](./sample-docker-dind-cluster/README.md)

## Details
### icr-check-va-scan

This task verifies that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and processes the outcome of the scan.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud container registry

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **container-registry-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud container registry (default to `apikey`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **image-url**: url of the image to VA scan - required if no image pipeline resource provided to this task
* **image-digest**: SHA id of the image to VA scan - required if no image pipeline resource provided to this task
* **image-properties-file**: file containing properties of the image to be scanned (default to `build.properties`)
* **max-iteration**: maximum number of iterations allowed while loop to check for va report (default to `30`)
* **sleep-time**: sleep time (in seconds) between invocation of ibmcloud cr va in the loop (default to `10`)
* **scan-report-file**: filename for the scan report (json format) of the given image. It will be copied in the workspace
* **fail-on-scanned-issues**: flag (`true` | `false`) to indicate if the task should fail or continue if issues are found in the image scan result (default to `true`)
* **scan-step-image**: image to use for the scan step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. Default to 0 (default to `0`)

#### Workspaces

* **artifacts**: Workspace that may contain image information and will have the va report from the VA scan after this task execution.

#### Results
* **scan-report-file**: the filename if the scan report for the image stored in the workspace
* **scan-status**: the status from Vulnerability Advisor - possible values: OK, WARN, FAIL, UNSUPPORTED, INCOMPLETE, UNSCANNED

### icr-containerize

This task builds and pushes (optionaly) an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud container registry

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **container-registry-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud container registry (default to `apikey`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **image-url**: url of the image to build required if no image pipeline resource provided or no registry region, namespace and image name parameters are provided to this task
* **registry-region**: container registry region id. required if no image-url or no image pipeline resources provided
* **registry-namespace**: container registry namespace. required if no image-url or no image pipeline resources provided
* **registry-create-namespace**: create container registry namespace if it doesn't already exists (default to `true`)
* **image-name**: image name. required if no image-url or no image pipeline resources provided
* **path-to-context**: the path to the context that is used for the build (default to `.` meaning current directory) (default to `.`)
* **path-to-dockerfile**: the path to the Dockerfile that is used for the build (default to `.` meaning current directory) (default to `.`)
* **dockerfile**: The name of the Dockerfile (default to `Dockerfile`)
* **build-args**: build argument list in the format 'KEY=VALUE' with a key-value pair per line.
* **buildkit-image**: The name of the BuildKit image (default to `moby/buildkit:v0.10.6`)
* **push-to-registry**: option to push the built image to registry or not. Default is `true` (default to `true`)
* **check-step-image**: image to use for the check (pre-build) step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **process-log-step-image**: image to use for the process log (post-build) steps (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **additional-tags**: comma-separated list of additional-tags
* **additional-tags-script**: Shell script that allows to add tags for the image to be build.
* **properties-file**: name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `REGISTRY_REGION`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`). This file can be used by downstream tasks to access the image registry-related information. (default to `build.properties`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. Default to 0 (default to `0`)
* **disable-caching**: Disable caching layers when building images. Value can be 0 or 1. Default to 0 (default to `0`)

#### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

#### Results
* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### icr-cr-build [deprecated]

The [`ibmcloud cr build`](https://cloud.ibm.com/docs/container-registry-cli-plugin?topic=container-registry-cli-plugin-containerregcli#bx_cr_build) command is deprecated.
If you use the [icr-cr-build](./container-registry/README.md#icr-cr-build) Tekton task, you can migrate to one of the three above Tekton tasks to build container images.
For more information about this replacement, see the [IBM Cloud™ Container Registry is Deprecating Container Builds](https://www.ibm.com/cloud/blog/announcements/ibm-cloud-container-registry-deprecating-container-builds) blog post.


#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud container registry

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **container-registry-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud container registry (default to `apikey`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **image-url**: url of the image to build required if no image pipeline resource provided or no registry region, namespace and image name parameters are provided to this task
* **registry-region**: container registry region id. required if no image-url or no image pipeline resources provided
* **registry-namespace**: container registry namespace. required if no image-url or no image pipeline resources provided
* **registry-create-namespace**: create container registry namespace if it doesn't already exists (default to `true`)
* **image-name**: image name. required if no image-url or no image pipeline resources provided
* **path-to-context**: the path to the context that is used for the build (default to `.` meaning current directory) (default to `.`)
* **path-to-dockerfile**: the path to the Dockerfile that is used for the build (default to `.` meaning current directory) (default to `.`)
* **dockerfile**: The name of the Dockerfile (default to `Dockerfile`)
* **build-args**: build argument list in the format 'KEY=VALUE' with a key-value pair per line.
* **additional-tags**: comma-separated list of additional-tags
* **additional-tags-script**: Shell script that allows to add tags for the image to be build.
* **properties-file**: file containing properties out of containerize task (default to `build.properties`)
* **check-and-build-step-image**: image to use for the scan step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. Default to 0 (default to `0`)

#### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

#### Results
* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### icr-execute-in-dind-cluster

This task runs `docker` commands (build, inspect...) against a Docker engine running in a Kubernetes cluster (a Docker DinD instance will be deployed if none is available on the build cluster),
 and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud container registry

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **container-registry-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud container registry (default to `apikey`)
* **ibmcloud-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **cluster-region**: (optional) the ibmcloud region hosting the cluster (if value is `` it will default to the toolchain region)
* **cluster-name**: name of the docker build cluster - required if no cluster pipeline resource provided to this task
* **cluster-namespace**: (optional) the kubernetes cluster namespace where the docker engine is hosted/deployed (default to `build`)
* **registry-create-namespace**: create container registry namespace if it doesn't already exists (default to `true`)
* **image-url**: url of the image to build - required if no image pipeline resource provided to this task
* **image-tag**: the default image tag if none is provided using the built-image url (default to `latest`)
* **path-to-context**: the path to the context that is used for the build (default to `.` meaning current directory) (default to `.`)
* **path-to-dockerfile**: the path to the Dockerfile that is used for the build (default to `.` meaning current directory) (default to `.`)
* **dockerfile**: The name of the Dockerfile (default to `Dockerfile`)
* **docker-client-image**: The Docker image to use to run the Docker client (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **docker-commands**: The docker command(s) to run. (default to `# Default docker build / inspect / push command
docker build --tag "$IMAGE_URL:$IMAGE_TAG" --file $PATH_TO_DOCKERFILE/$DOCKERFILE $PATH_TO_CONTEXT
docker inspect ${IMAGE_URL}:${IMAGE_TAG}
docker push ${IMAGE_URL}:${IMAGE_TAG}
`)
* **check-step-image**: image to use for the check (pre-build) step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **cluster-setup-step-image**: image to use for the cluster setup step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **dind-image**: image to use for the Docker-in-Docker sidecar (default to icr.io/continuous-delivery/pipeline/docker:20.10.22-dind) (default to `icr.io/continuous-delivery/pipeline/docker:20.10.22-dind`)
* **properties-file**: file containing properties out of the docker in docker task (default to `build.properties`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)

#### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

#### Results
* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### icr-execute-in-dind

This task runs `docker` commands (build, inspect...) against a Docker engine running as a sidecar container,
 and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud container registry

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **container-registry-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud container registry (default to `apikey`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **registry-create-namespace**: create container registry namespace if it doesn't already exists (default to `true`)
* **image-url**: url of the image to build - required if no image pipeline resource provided to this task
* **image-tag**: the default image tag if none is provided using the built-image url (default to `latest`)
* **path-to-context**: the path to the context that is used for the build (default to `.` meaning current directory) (default to `.`)
* **path-to-dockerfile**: the path to the Dockerfile that is used for the build (default to `.` meaning current directory) (default to `.`)
* **dockerfile**: The name of the Dockerfile (default to `Dockerfile`)
* **docker-client-image**: The Docker image to use to run the Docker client (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **docker-commands**: The docker command(s) to run. (default to `# Default docker build / inspect / push command
docker build --tag "$IMAGE_URL:$IMAGE_TAG" --file $PATH_TO_DOCKERFILE/$DOCKERFILE $PATH_TO_CONTEXT
docker inspect ${IMAGE_URL}:${IMAGE_TAG}
docker push ${IMAGE_URL}:${IMAGE_TAG}
`)
* **check-step-image**: image to use for the check (pre-build) step (default to icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72) (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72`)
* **dind-image**: image to use for the Docker-in-Docker sidecar (default to icr.io/continuous-delivery/pipeline/docker:20.10.22-dind) (default to `icr.io/continuous-delivery/pipeline/docker:20.10.22-dind`)
* **properties-file**: file containing properties out of the docker in docker task (default to `build.properties`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. Default to 0 (default to `0`)
* **registry-region**: container registry region id. required if no image-url or no image pipeline resources provided
* **registry-namespace**: container registry namespace. required if no image-url or no image pipeline resources provided
* **image-name**: image name. required if no image-url or no image pipeline resources provided

#### Workspaces

* **source**: A workspace containing the source (Dockerfile, Docker context) to create the image

#### Results
* **image-repository**: the repository for the built image
* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image
