# Docker In Docker (DIND) Kubernetes Cluster Hosted task example usage
The `sample-docker-dind-cluster` sub-directory contains an `event-listener-dind-cluster` EventListener definition that you can include in your Tekton pipeline configuration to run an example usage of the `execute-in-dind-cluster-task` and `vulnerability-advisor-task`.

It also contains a `dind-cluster-no-resources` EventListener definition which is the providing the same example but without the needs to define PipelineResources for image as it uses the task's parameter `image-url` to provide the information

**Note:** this sample also relies on the clone-repo task to clone the application to containerize.

1) Create or update a toolchain to include:

   - the git repository that you want to clone, which can be private
   - the repository containing this Tekton task
   - a [Tekton pipeline definition](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines#create_tekton_pipeline)

   ![Toolchain overview](./images/dind-cluster-sample-toolchain-overview.png)

2) Add the definitions:

   - for the `clone-repo-task` (`git` path)
   - for this task and the sample (`container-registry` and `container-registry/sample-docker-dind-cluster` paths)

   ![Tekton pipeline definitions](./images/dind-cluster-sample-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `apikey` to provide an API key used for the ibmcloud login/access
   - `buildCluster` to provide the kubernetes cluster name that will be used as a build cluster (ie hosting the Docker DinD)
   - `imageUrl` to indicate the URL of the image to push to the IBM Cloud Container Registry
   - `repository` to indicate the git repository url to clone (correspoding to the one integrated in the toolchain)

   ![Tekton pipeline environment properties](./images/dind-cluster-sample-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./images/dind-cluster-sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline

6) Verify that the image was build and pushed by looking at the pipeline run execution log:
   
   ![Tekton pipeline sample log](./images/dind-cluster-sample-tekton-pipeline-run-log.png)
