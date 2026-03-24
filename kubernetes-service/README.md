# Kubernetes-Service related tasks

## Available Tasks
- **[iks-contextual-execution](#iks-contextual-execution)**: This task is executing bash snippet/script in the context of a Kubernetes cluster configuration.
- **[iks-deploy-to-kubernetes](#iks-deploy-to-kubernetes)**: This task allows to perform scripts typically doing deployment of a Kubernetes application with `ibmcloud ks` cli and `kubectl` cli configured for a given cluster.
- **[iks-fetch-config](#iks-fetch-config)**: This task is fetching the configuration of a [IBM Cloud Kubernetes Service cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) that is required to perform `kubectl` commands.

## Pre-requisites
These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.

## Install the Tasks
- Add a github integration in your toolchain to the repository containing the task (https://github.com/open-toolchain/tekton-catalog)
- Add that github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `kubernetes-service`

## Usage
The `sample` sub-directory contains an EventListener definition `kubernetes-service-no-resources` that you can include in your tekton pipeline configuration to run an example usage of the `iks-fetch-config` and `iks-contextual-execution` tasks.

  See the documentation [here](./sample/README.md)

## Details
### iks-contextual-execution

This task is executing bash snippet/script in the context of a Kubernetes cluster configuration.

#### Parameters

* **cluster-pipeline-resources-directory**: directory in which the kubeconfig file(s) for cluster are available (default to `/clusters`)
* **cluster-name**: name of the cluster - required if no cluster pipeline resource provided to this task
* **script**: the bash snippet to execute within the context of the kubernetes configuration (default to `kubectl version`)
* **execute-step-image**: image to use for the setup step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)

#### Workspaces

* **cluster-configuration**: A workspace that contain the kubectl cluster config to be used

### iks-deploy-to-kubernetes

This task allows to perform scripts typically doing deployment of a Kubernetes application with `ibmcloud ks` cli and `kubectl` cli configured for a given cluster.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud kubernetes service

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **kubernetes-service-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud kubernetes service (default to `apikey`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **cluster-region**: the ibmcloud region hosting the cluster (if none is found it will default to the toolchain region)
* **cluster-name**: name of the cluster - required if no cluster pipeline resource provided to this task
* **image-url**: URL of an image that is relevant to the deployment action
* **shuttle-properties-file**: name of the properties file that contain properties to include in the environment for the `script` snippet/script execution
* **setup-script**: script that typically set up environment before the _deployment_ script execution.
* **script**: _deployment_ script to be executed
* **post-execution-script**: script that get executed after the _deployment_ script has been executed.
* **execute-step-image**: image to use for the execute step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)

#### Workspaces

* **artifacts**: A workspace

#### Results
* **app-url**: The running application's URL (obtained from APP_URL variable set by the executed script)
* **cluster-name**: The cluster name
* **cluster-id**: The cluster identifier
* **resource-group-name**: The resource-group name that this cluster is part of
* **resource-group-id**: The resource-group identifier that this cluster is part of
* **region**: The region (ie us-south) where the cluster is located

### iks-fetch-config

This task is fetching the configuration of a [IBM Cloud Kubernetes Service cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) that is required to perform `kubectl` commands.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop)

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud kubernetes service

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **kubernetes-service-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud kubernetes service (default to `apikey`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **cluster-region**: (optional) the ibmcloud region hosting the cluster (if none is found it will default to the toolchain region)
* **cluster-name**: name of the cluster - required if no cluster pipeline resource provided to this task
* **kube-api-server-accessible**: indicates if the kubeAPIServer is exposed which is not the case for IBM Cloud Public Shared Workers (Calico network policy). If 'true', the task is trying to update the Cluster Pipeline Resources definition with the appropriate informations; When 'false', the fallback mechanism (copy file(s)) is used. (default to `false`)
* **cluster-pipeline-resources-directory-fallback**: directory in the workspace that will be used as a fallback mechanism to store the kubeconfig file (default to `.tekton-cluster-pipeline-resources`)
* **cluster-and-worker-nodes-json-export**: directory in the workspace that will be used to store the cluster and worker nodes export json files
* **setup-step-image**: image to use for the setup step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)

#### Workspaces

* **cluster-configuration**: A workspace where the kubernetes cluster config is exported

#### Results
* **cluster-name**: The cluster name
* **cluster-id**: The cluster identifier
* **resource-group-name**: The resource-group name that this cluster is part of
* **resource-group-id**: The resource-group identifier that this cluster is part of
* **region**: The region (ie us-south) where the cluster is located
