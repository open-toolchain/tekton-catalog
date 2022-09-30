# Sonarqube Scan Task example usage
The `sample` sub-directory contains an `event-listener-container-registry` EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `sonarqube-run-scan`.

**Note:** this sample also relies on the `git-clone-repo`, `doi-publish-buildrecord`, `toolchain-build` and `doi-evaluate-gate`  tasks to clone the application, perform a build script, push the appropriate information to DevOps Insights and use the DevOps insights gate for evaluation.

1) Create or update a toolchain to include:

   - the git repository containing the source to scan - that will be git clone, which can be private - for instance `https://github.com/open-toolchain/hello-containers.git`
   - the git repository containing this tekton task
   - a DevOps Insights integration
   - a SonarQube integration
   - a [Tekton pipeline definition](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines#create_tekton_pipeline)

   ![Toolchain overview](./images/sonarqube-toolchain-overview.png)

2) Define a policy in DevOps Insights that will be evaluated - It only need to have one rule related to sonarqube test result in it.
    - Click on the DevOps Insights card
    - Create a [policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-defining-policies-rules#create_policies) with a name
      ![Create Policy](./images/doi-new-policy.png)
    - Add a new [rule](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-defining-policies-rules#create_policies) to include SonarQube Data set
      ![Add Rule](./images/doi-create-rule.png)

3) Add the tekton definitions in the tekton pipeline:

   - for the `git-clone-repo` task (`git` path)
   - for the DevOps Insights tasks `doi-publish-buildrecord` and `doi-evaluate-gate` (`devops-insights` path)
   - for the `toolchain-build` task (`toolchain` path)
   - for this task and the sample (`sonarqube` and `sonarqube/sample` paths)

   ![Tekton pipeline definitions](./images/sonarqube-pipeline-definitions.png)

4) Choose a Worker for the pipeline - Select one of the IBM Managed workers

5) Add the environment properties:

   - `app-name` the name of the application
   - `doi-policy` to indicate the name of DevOps Insoghts Policy you have created in previous step
   - `toolchain-apikey` to provide an API key used for the ibmcloud login/access
   - `repository` to indicate the git repository url to clone (correspoding to the one integrated in the toolchain)

   ![Tekton pipeline environment properties](./images/sonarqube-pipeline-environment-properties.png)

5) Create a manual trigger to start the `default` EventListener

   ![Tekton pipeline sample trigger](./images/sonarqube-pipeline-sample-trigger.png)

   If your sample code is a maven project then you can select the alternate `maven` EventListener that will define the appropriate command and target `mvn sonar:sonar` to perform the sonarqube scan

6) Run the pipeline using the manual trigger created

   When pipeline-run is started (or terminated) you can click on it to open the pipelinerun dashboard

   ![Pipeline runs](./images/sonarqube-pipeline-runs.png)

   You can then see the detail of the pipeline execution and especially the sonarqube scan task

   ![SonarQube sample pipeline run](./images/sonarqube-sample-pipeline-run.png)

7) If you navigate to the sonarqube server, the sonarqube project will have been created and scanned

   ![SonarQube project overview](./images/sonarqube-project-overview.png)

8) The DevOps insights dashboard shows also the SonarQube scan result

   ![DevOps Insights Quality Dashboard](./images/sonarqube-doi-quality-dashboard.png)
