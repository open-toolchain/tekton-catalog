# Git integration clone task helper

This Task fetch credentials to be able to perform a git clone of a given repository referenced in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and perform the clone

## Install the Task
- Add a github integration in your toolchain to the existing github repository: https://github.com/open-toolchain/tekton-catalog
- Add the above github integration as inputs of you Continous Delivery tekton pipeline and path `git`

## Inputs

### Context - ConfigMap/Secret

  The task expected the following kubernetes resource to be defined:

* **ConfigMap cd-config**

  ConfigMap corresponding to the CD tekton pipeline context:
  * **API**: IBM Cloud api
  * **TOOLCHAIN_ID**: Id of the toolchain
  * **REGION**: Region where the toolchain is defined

* **Secret cd-secret**

  Secret containing:
  * **API_KEY**: An IBM Cloud Api Key allowing access to the toolchain

### Parameters

* **task-pvc**: the output pvc - this is where the cloned repository will be stored
* **repository**: the git repository url that the toolchain is integrating
* **branch**: the git branch (default value to `master`)
* **revision**: (optional) the git revision/commit to update the git HEAD to (default to empty meaning only use the branch information)
* **directoryName**: (optional) name of the new directory to clone into (default to `.` in order to clone at the root of the volume mounted for the pipeline run). Note: It will be to the "humanish" part of the repository if this param is set to blank
* **propertiesFile**: (optional) name of the properties file that will be created as additional outcome of this task in the pvc. This file will contains the git related information (`GIT_URL`, `GIT_BRANCH` and `GIT_COMMIT`)

## Output
The output of this task is the clone operation performed in the specified directory (if any)

## Usage
The `sample` sub-directory contains an EventListener definition that you can include in your tekton pipeline configuration to run a sample usage the `clone-repo-task`

1) Create a toolchain (or update a toolchain) to include:

   - the (private) git repository that you want to clone
   - the repository containing this tekton task
   - a tekton pipeline definition

   ![Toolchain overview](./sample/sample-toolchain-overview.png)

2) Add the definitions of this task and the sample (`git` and `git/sample` paths)

   ![Tekton pipeline definitions](./sample/sample-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `toolchainId`, `apikey` (and optionally `toolchainRegion` if the toolchain is not in `us-south`) to inject Continuous Delivery toolchain context
   - `repository` to indicate the git repository url to clone (correspoding to the one integrated in the toolchain)

   ![Tekton pipeline environment properties](./sample/sample-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./sample/sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline
