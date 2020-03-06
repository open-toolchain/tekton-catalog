# Docker In Docker (DIND) Task example usage
The `sample-docker-dind-sidecar` sub-directory contains an `event-listener-dind` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `execute-in-dind-task` and `vulnerability-advisor-task`.

**Note:** this sample also relies on the clone-repo task to clone the application to containerize.

1) Create or update a toolchain to include:

   - the git repository that you want to clone, which can be private
   - the repository containing this Tekton task
   - a [Tekton pipeline definition](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines#create_tekton_pipeline)

   ![Toolchain overview](./images/dind-sample-toolchain-overview.png)

2) Add the definitions:

   - for the `clone-repo-task` (`git` path)
   - for this task and the sample (`container-registry` and `container-registry/sample-docker-dind-sidecar` paths)

   ![Tekton pipeline definitions](./images/dind-sample-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `apikey` to provide an API key used for the ibmcloud login/access
   - `repository` to indicate the git repository url to clone (correspoding to the one integrated in the toolchain)
   - `imageUrl` to indicate the URL of the image to push to the IBM Cloud Container Registry

   ![Tekton pipeline environment properties](./images/dind-sample-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./images/dind-sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline

6) Verify that the image was build and pushed by looking at the pipeline run execution log:
   
   ![Tekton pipeline sample log](./images/dind-sample-tekton-pipeline-run-log.png)
