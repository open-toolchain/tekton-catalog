# Container-Registry related tasks

- **icr-containerize**: this task builds and pushes an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image.
- **icr-cr-build**: this task builds and pushes an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started) `build` command to perform the build of the image.
- **icr-execute-in-dind**: this task runs `docker` commands (build, inspect...) against a Docker engine running as a sidecar container, and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **iks-contextual-execution**: this task runs `docker` commands (build, inspect...) against a Docker engine running in a Kubernetes cluster (a Docker DinD instance will be deployed if none is available on the build cluster), and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **icr-check-va-scan**: this task verifies that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and processes the outcome of the scan.

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `container-registry`

## Build Image helper task: icr-containerize

### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample/listener-containerize.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

### Parameters

* **image-url** : (optional) the url of the image to build - required if no image pipeline resource provided to this task
* **path-to-context**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **path-to-dockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.` meaning current directory)
* **buildkit-image**: (optional) The name of the BuildKit image used (default to `moby/buildkit:v0.6.3-rootless`)
* **additional-tags**: (optional) comma-separated list of tags for the built image
* **additional-tags-script**: (optional) Shell script commands that will be invoked to provide additional tags for the build image
* **properties-file**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the pvc. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `REGISTRY_REGION`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation

### Results

* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

### Resources

#### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## Build Image helper task: icr-cr-build

### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample/listener-containerize.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

### Parameters

* **image-url** : (optional) the url of the image to build - required if no image pipeline resource provided to this task
* **path-to-context**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **path-to-dockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.` meaning current directory)
* **additional-tags**: (optional) comma-separated list of tags for the built image
* **additional-tags-script**: (optional) Shell script commands that will be invoked to provide additional tags for the build image
* **properties-file**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `REGISTRY_REGION`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation

### Results

* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

### Resources

#### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## Docker In Docker (DIND) helper task: icr-execute-in-dind
This task runs `docker` commands (build, inspect...) that communicate with a sidecar dind,
and pushes the resulting image to the IBM Cloud Container Registry.

**Note:** the **Docker engine** used to execute the commands is **transient**, created by the task as a sidecar container,
and is available only during the task's lifespan.

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample-docker-dind-sidecar/listener-docker-in-docker.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

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

### Results

* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

### Resources

#### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## Docker In Docker (DIND) Kubernetes Cluster Hosted helper task: icr-execute-in-dind-cluster
This task runs `docker` commands (build, inspect...) that communicate with a docker dind instance hosted in a kubernetes cluster (eventually deploying the Docker DinD if needed), and pushes the resulting image to the IBM Cloud Container Registry.

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample-docker-dind-cluster/listener-docker-dind-cluster.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

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

### Results

* **image-tags**: the tags for the built image
* **image-digest**: the image digest (sha-256 hash) for the built image

### Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

#### Resources

##### Inputs

* **cluster**: (optional) The Cluster PipelineResource that will be used to host the Docker DinD to build Docker images. Only the name property is used to identify the cluster name.

##### Outputs

* **built-image**: (optional) The Image PipelineResource that will be created as output of this task.

## Vulnerability Advisor helper task: icr-check-va-scan

### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample/listener-containerize.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

### Parameters

* **image-url**: (optional) url of the image to VA scan - required if no image pipeline resource provided to this task
* **image-digest**: (optional) SHA id of the image to VA scan - required if no image pipeline resource provided and no `image-properties-file` value provided
* **image-properties-file**: file containing properties of the image to be scanned (default to 'build.properties')
* **max-iteration**: maximum number of iterations allowed while loop to check for va report (default to 30 iterations maximum)
* **sleep-time**: sleep time (in seconds) between invocation of ibmcloud cr va in the loop (default to 10 seconds between scan result inquiry)
* **scan-report-file**: (optional) filename for the scan report (json format) of the given image. It will be copied in the workspace
* **fail-on-scanned-issues**: flag (`true` | `false`) to indicate if the task should fail or continue if issues are found in the image scan result (default to 'true')
* **resource-group**: (optional) target resource group (name or id) for the ibmcloud login operation

### Results

* **scan-report-file**: the filename if the scan report for the image stored in the workspace
* **scan-status**: the status from Vulnerability Advisor - possible values: OK, WARN, FAIL, UNSUPPORTED, INCOMPLETE, UNSCANNED

### Workspaces

* **workspace**: The workspace backing by a volume that will be used to store output file

#### Resources

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

