# Kubernetes-Service related tasks

- **fetch-iks-cluster-config**: This task is fetching the configuration of a [IBM Cloud Kubernetes Service cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) that is required to perform `kubectl` commands.
- **kubernetes-contextual-execution**: This task is executing bash snippet/script in the context of a Kubernetes cluster configuration.

**WARNING: These tasks needs to run on Kubernetes cluster with minimal version 1.16. If you are using your own Delivery Pipeline Private Worker to run your tekton pipeline(s), ensure your cluster is updated to this version at least.**

## Install the Tasks
- Add a github integration in your toolchain to the repository containing the task (https://github.com/open-toolchain/tekton-catalog)
- Add that github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `kubernetes-service`

## Fetch IKS Cluster Configuration helper task

### Inputs

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An IBM Cloud Api Key use to access to the IBM Cloud Container registry service (https://cloud.ibm.com/iam/apikeys)

  See [sample TriggerTemplate](./sample/listener-kubernetes-service.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

#### Resources

* **cluster**: The Cluster PipelineResource that will be updated as output of this task. Only the name property is used to identify the cluster name.

#### Parameters

* **resourceGroup**: (optional) target resource group (name or id) for the ibmcloud login operation.
* **clusterRegion**: (optional) the ibmcloud region hosting the target cluster. If not specified, it will use the toolchain region as a default.
* **clusterPipelineResourcesDirectoryFallback**: (optional) that will be used as a fallback mechanism to store the kubeconfig file for the target cluster (expressed by the inputs)

## Workspaces

* **workspace**: The workspace backing by a volume

### Outputs

#### Resources

* **cluster**: The Cluster PipelineResource that will be updated as output of this task.

## Kubernetes Contextual Execution helper task

### Inputs

#### Context - ConfigMap/Secret

  The task expects the following kubernetes resources to be defined:

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An IBM Cloud Api Key use to access to the IBM Cloud Container registry service (https://cloud.ibm.com/iam/apikeys)

  See [sample TriggerTemplate](./sample/listener-kubernetes-service.yaml) on how to create the secret using `resourcetemplates` in a `TriggerTemplate`

#### Resources

* **cluster**: The Cluster PipelineResource that corresponds to the kubernetes cluster target for the kubectl command execution.

#### Parameters

* **clusterPipelineResourcesDirectory**: directory of the workspace in which the kubeconfig file(s) for clusterPipelineResources are available (using the fallback mechanism of kubeconfig copy to the workspace)
* **script**: the bash snippet to execute within the context of the kubernetes configuration (default to `kubectl version`)

## Workspaces

* **workspace**: The workspace backing by a volume that contains the Dockerfile and Docker context

# Usage
The `sample` sub-directory contains an EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `fetch-iks-cluster-config` and `kubernetes-contextual-execution` tasks.

1) Create a toolchain (or update a toolchain) to include:

   - the git repository that you want to clone, which can be private
   - the repository containing this tekton task
   - a tekton pipeline definition

   ![Toolchain overview](./sample/kubernetes-service-sample-toolchain-overview.png)

2) Add the definitions:

   - for the tasks and the sample (`kubernetes-service` and `kubernetes-service/sample` paths)

   ![Tekton pipeline definitions](./sample/kubernetes-service-sample-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `apikey` to provide an API key used for the ibmcloud login/access
   - `clusterName` to indicate the name of the IKS cluster that you want to target

   ![Tekton pipeline environment properties](./sample/kubernetes-service-sample-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./sample/kubernetes-service-sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline
