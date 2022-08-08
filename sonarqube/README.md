# Sonarqube related tasks

# Tasks

- **[sonarqube-run-scan](#sonarqube-run-scan)**: This task starts a SonarQube scan for the code in a workspace using the SonarQube server integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/devsecops?topic=ContinuousDelivery-sonarqube) and upload the test results to DevOps Insights (optional)

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `sonarqube`

## Usages

- The `sample` sub-directory contains an EventListener definition that you can include in your CD tekton pipeline configuration to run an example showing a simple usage of the `sonarqube-run-scan` task.

  See the documentation [here](./sample/README.md)

## sonarqube-run-scan

This task starts a SonarQube scan for the code in a workspace using the SonarQube server integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/devsecops?topic=ContinuousDelivery-sonarqube) and upload the test results to DevOps Insights (optional)

### Parameters

* **sonarqube-name**: Name of the sonarqube toolcard integration in the toolchain. Default to "" meaning the first sonarqube integration found will be used.
* **sonarqube-project-key**: Project key of the sonarqube project. Default to "" meaning a project key will be computed out of the toolchain name
* **path-to-sources**: The path to the sources. Default to `.` meaning current directory of the mounted workspace.
* **prepare-step-image**: Image used for the prepare step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.8`
* **scan-step-image**: Image used for the scan step. Default to `icr.io/continuous-delivery/toolchains/devsecops/sonar-scanner-cli@sha256:af782cf68bbfe32982aac08e3215d95f57c9ce49444ab8bfa017819ba4905548`
* **post-to-doi-step-image**: Image used for the post to doi step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.8`
* **sonar-scan-command**: Sonar scan command to use. Default to `sonar-scanner -Dsonar.working.directory=$SONAR_DIR`.
  The following environment variables are available:
    - SONAR_DIR : Sonar Scanner Working directory
    - SONAR_HOST_URL: URL of the sonarqube server
    - SONAR_USER : Sonar Userid
    - SONAR_PASS : Sonar Password
    - SONAR_PROJECT_KEY: Sonar Project key of the sonarqube project
    - WORKSPACE_PATH: Path to the workspace
    - PATH_TO_SOURCES : workspace relative path to the sources to scan

  The command can be another kind of command for maven java project like the following: `mvn -Dmaven.repo.local="${WORKSPACE_PATH}/.m2" -Dsonar.login="${SONAR_USER}" -Dsonar.password="${SONAR_PASS}" -Dsonar.host.url="$SONAR_HOST_URL" -Dsonar.projectKey="$SONAR_PROJECT_KEY" -Dsonar.projectName="$SONAR_PROJECT_KEY" -Dsonar.working.directory="$SONAR_DIR" sonar:sonar`
* **doi-app-name**: Logical application name for DevOps Insights
* **doi-toolchain-id**: (optional) Toolchain service instance id. Default to the toolchain containing the CD Tekton pipelineRun currently executed.
* **doi-build-number**: (optional) Devops Insights build number reference. Default to the CD Tekton Pipeline build number.
* **ibmcloud-api**: (optional) the ibmcloud api. Default to https://cloud.ibm.com
* **continuous-delivery-context-secret**: (optional) Name of the secret containing the continuous delivery pipeline context secrets. Default to `secure-properties`
* **toolchain-apikey-secret-key**: (optional) field in the secret that contains the api key used to access toolchain and DOI instance. Default to `toolchain-apikey`
* **pipeline-debug**: (optional) turn on task script context debugging

### Workspaces

* **workspace**: A workspace containing the source code to perform the sonarqube scan against
