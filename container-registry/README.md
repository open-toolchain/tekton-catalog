# Container-Registry related tasks

- **containerize-task**: this task builds and pushes an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image.
- **execute-in-dind-task**: this task runs `docker` commands (build, inspect...) against a Docker engine running as a sidecar container, and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **execute-in-dind-cluster-task**: this task runs `docker` commands (build, inspect...) against a Docker engine running in a Kubernetes cluster (a Docker DinD instance will be deployed if none is available on the build cluster), and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **vulnerability-advisor-task**: this task verifies that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and processes the outcome of the scan.

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `container-registry`

## Build Image helper task: containerize-task

### Inputs

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample/listener-containerize.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

#### Parameters

* **pathToContext**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **pathToDockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.` meaning current directory)
* **buildkit_image**: (optional) The name of the BuildKit image used (default to `moby/buildkit:v0.6.3-rootless`)
* **directoryName**: (optional) name of the new directory to clone into (default to `.` in order to clone at the root of the volume mounted for the pipeline run). Note: It will be to the "humanish" part of the repository if this param is set to blank
* **additionalTags**: (optional) comma-separated list of tags for the built image
* **additionalTagsScript**: (optional) Shell script commands that will be invoked to provide additional tags for the build image
* **propertiesFile**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `REGISTRY_REGION`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **resourceGroup**: (optional) target resource group (name or id) for the ibmcloud login operation

## Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

### Outputs

#### Resources

* **builtImage**: The Image PipelineResource that will be created as output of this task.

## Docker In Docker (DIND) helper task: execute-in-dind-task
This task runs `docker` commands (build, inspect...) that communicate with a sidecar dind,
and pushes the resulting image to the IBM Cloud Container Registry.

**Note:** the **Docker engine** used to execute the commands is **transient**, created by the task as a sidecar container,
and is available only during the task's lifespan.

### Inputs

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample-docker-dind-sidecar/listener-docker-in-docker.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

#### Parameters

* **imageTag**: (optional) the tag for the built image (default to `latest`) 
* **pathToContext**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **pathToDockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.`) 
* **dockerfile**: (optional) the name of the Dockerfile that is used for the build (default to `Dockerfile`) 
* **dockerClientImage**: (optional) The Docker image to use to run the Docker client (default to `docker`) 
* **propertiesFile**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **dockerCommands**: (optional) The docker command(s) to run. Default commands:
```
docker build --tag "$IMAGE_URL:$IMAGE_TAG" --file $PATH_TO_DOCKERFILE/$DOCKERFILE $PATH_TO_CONTEXT
docker inspect ${IMAGE_URL}:${IMAGE_TAG}
docker push ${IMAGE_URL}:${IMAGE_TAG}
```

## Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

### Outputs

#### Resources

* **builtImage**: The Image PipelineResource that will be created as output of this task.

## Docker In Docker (DIND) Kubernetes Cluster Hosted helper task: execute-in-dind-cluster-task
This task runs `docker` commands (build, inspect...) that communicate with a docker dind instance hosted in a kubernetes cluster (eventually deploying the Docker DinD if needed), and pushes the resulting image to the IBM Cloud Container Registry.

### Inputs

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample-docker-dind-cluster/listener-docker-dind-cluster.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

#### Parameters

* **resourceGroup**: (optional) target resource group (name or id) for the ibmcloud login operation
* **clusterRegion**: (optional) the ibmcloud region hosting the cluster (if value is `` it will default to the toolchain region)
* **clusterNamespace**: (optional) the kubernetes cluster namespace where the docker engine is hosted/deployed (default to `build`)
* **imageTag**: (optional) the tag for the built image (default to `latest`) 
* **pathToContext**: (optional) the path to the context that is used for the build (default to `.` meaning current directory)
* **pathToDockerfile**: (optional) the path to the Dockerfile that is used for the build (default to `.`) 
* **dockerfile**: (optional) the name of the Dockerfile that is used for the build (default to `Dockerfile`) 
* **dockerClientImage**: (optional) The Docker image to use to run the Docker client (default to `docker`) 
* **propertiesFile**: (optional) name of the properties file that will be created (if needed) or updated (if existing) as an additional outcome of this task in the workspace. This file will contains the image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`)
* **dockerCommands**: (optional) The docker command(s) to run. Default commands:
```
docker build --tag "$IMAGE_URL:$IMAGE_TAG" --file $PATH_TO_DOCKERFILE/$DOCKERFILE $PATH_TO_CONTEXT
docker inspect ${IMAGE_URL}:${IMAGE_TAG}
docker push ${IMAGE_URL}:${IMAGE_TAG}
```
#### Resources

* **cluster**: The Cluster PipelineResource that will be used to host the Docker DinD to build Docker images. Only the name property is used to identify the cluster name.

## Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

### Outputs

#### Resources

* **builtImage**: The Image PipelineResource that will be created as output of this task.

## Vulnerability Advisor helper task: vulnerability-advisor-task

### Inputs

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the IBM Cloud Container registry service.

  See this [sample TriggerTemplate](./sample/listener-containerize.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

#### Parameters

* **imagePropertiesFile**: file containing properties of the image to be scanned (default to 'build.properties')
* **maxIteration**: maximum number of iterations allowed while loop to check for va report (default to 30 iterations maximum)
* **sleepTime**: sleep time (in seconds) between invocation of ibmcloud cr va in the loop (default to 10 seconds between scan result inquiry)
* **scanReportFile**: (optional) filename for the scan report (json format) of the given image. It will be copied in the workspace
* **failOnScannedIssues**: flag (`true` | `false`) to indicate if the task should fail or continue if issues are found in the image scan result (default to 'true')
* **resourceGroup**: (optional) target resource group (name or id) for the ibmcloud login operation

## Workspaces

* **workspace**: The workspace backing by a volume that will be used to store output file

#### Resources

* **image**: The Image PipelineResource that this task will process the Vulnerability Advisor scan result.

## Usages

- The `sample` sub-directory contains an `event-listener-container-registry` EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `containerize-task` and `vulnerability-advisor-task`.

  See the documentation [here](./sample/README.md)

- The `sample-docker-dind-sidecar` sub-directory contains an `event-listener-dind` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `execute-in-dind-task` and `vulnerability-advisor-task`.

  See the documentation [here](./sample-docker-dind-sidecar/README.md)

- The `sample-docker-dind-cluster` sub-directory contains an `event-listener-dind-cluster` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `execute-in-dind-cluster-task` and `vulnerability-advisor-task`.

  See the documentation [here](./sample-docker-dind-cluster/README.md)

