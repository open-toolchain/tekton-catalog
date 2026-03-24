# Sonarqube related tasks

## Available tasks
- **[sonarqube-run-scan](#sonarqube-run-scan)**: This task starts a SonarQube scan for the code in a workspace using the SonarQube server integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/devsecops?topic=ContinuousDelivery-sonarqube) and upload the test results to DevOps Insights (optional)

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `sonarqube`

## Usages

- The `sample` sub-directory contains an EventListener definition that you can include in your CD tekton pipeline configuration to run an example showing a simple usage of the `sonarqube-run-scan` task.

  See the documentation [here](./sample/README.md)

## Details
### sonarqube-run-scan

This task starts a SonarQube scan for the code in a workspace using the SonarQube server integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/devsecops?topic=ContinuousDelivery-sonarqube) and upload the test results to DevOps Insights (optional)

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Name of the secret containing the continuous delivery pipeline context secrets

  Secret containing:
  * **toolchain-apikey**: field in the secret that contains the api key used to access toolchain and DOI instance
  * **doi-sonarqube-token**: field in the secret that contains the SonarQube token to publish the SonarQube report to DOI. It has some specific permissions which are required that a Global Analysis Token may not have. See https://cloud.ibm.com/docs/devsecops?topic=devsecops-sonarqube#permissions-for-sonarqube-token

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **sonarqube-name**: name of the sonarqube toolcard integration in the toolchain ("" meaning the first sonarqube integration found will be used)
* **sonarqube-project-key**: project key of the sonarqube project ("" meaning a project key will be computed out of the toolchain name)
* **path-to-sources**: the path to the sources (`.` meaning current directory) (default to `.`)
* **prepare-step-image**: image used for the prepare step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **scan-step-image**: image used for the scan step (default to `icr.io/continuous-delivery/toolchains/devsecops/sonar-scanner-cli:29-11-2024-10-26`)
* **post-to-doi-step-image**: image used for the post to doi step (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **sonar-scan-command**: Sonar scan command to use. The following environment variables are available: - SONAR_DIR : Sonar Scanner Working directory - SONAR_HOST_URL: URL of the sonarqube server - SONAR_USER : Sonar Userid - SONAR_PASS : Sonar Password/Token - SONAR_PROJECT_KEY: Sonar Project key of the sonarqube project - WORKSPACE_PATH: Path to the workspace - PATH_TO_SOURCES : workspace relative path to the sources to scan The command can be another kind of command for maven java project like mvn -Dmaven.repo.local="${WORKSPACE_PATH}/.m2" -Dsonar.login="${SONAR_USER}" -Dsonar.token="${SONAR_PASS}" -Dsonar.host.url="$SONAR_HOST_URL" -Dsonar.projectKey="$SONAR_PROJECT_KEY" -Dsonar.projectName="$SONAR_PROJECT_KEY" -Dsonar.working.directory="$SONAR_DIR" sonar:sonar (default to `sonar-scanner -Dsonar.working.directory=$SONAR_DIR`)
* **doi-app-name**: Logical application name for DevOps Insights post
* **doi-toolchain-id**: Toolchain service instance id used for DevOps Insights post. Default to the toolchain containing the CD Tekton PipelineRun currently executed
* **doi-build-number**: Devops Insights build number reference. Default to the CD Tekton Pipeline build number
* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **continuous-delivery-context-secret**: Name of the secret containing the continuous delivery pipeline context secrets (default to `secure-properties`)
* **toolchain-apikey-secret-key**: field in the secret that contains the api key used to access toolchain and DOI instance (default to `toolchain-apikey`)
* **doi-sonarqube-token-secret-key**: field in the secret that contains the SonarQube token to publish the SonarQube report to DOI. It has some specific permissions which are required that a Global Analysis Token may not have. See https://cloud.ibm.com/docs/devsecops?topic=devsecops-sonarqube#permissions-for-sonarqube-token (default to `doi-sonarqube-token`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)

#### Workspaces

* **workspace**: A workspace where the source is expected to be
