## Simple kubernetes related tasks sample ##

This `sample` sub-directory contains an EventListener definition `kubernetes-service-no-resources` that you can include in your tekton pipeline configuration to run an example usage of the `iks-fetch-config` and `iks-contextual-execution` tasks.

1) Create a toolchain (or update a toolchain) to include:

   - the git repository that you want to clone, which can be private
   - the repository containing this tekton task
   - a tekton pipeline definition

   ![Toolchain overview](./kubernetes-service-sample-toolchain-overview.png)

2) Add the definitions:

   - for the tasks and the sample (`kubernetes-service` and `kubernetes-service/sample` paths)

   ![Tekton pipeline definitions](./kubernetes-service-sample-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `apikey` to provide an API key used for the ibmcloud login/access
   - `cluster-name` to indicate the name of the IKS cluster that you want to target

   ![Tekton pipeline environment properties](./kubernetes-service-sample-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./kubernetes-service-sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline
