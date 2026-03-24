# Configuring Code Risk Analyzer v2 for Your Code Repositories - triggered on Pull Requests or commit push
To configure Code Risk Analyzer for your repositories, you will need to take the following steps:
- Create an empty Toolchain
- Add DevOps Insights card to your Toolchain
- Add a card for each code repository that you want to scan.  You can start with a single card and add more later.
- Create a Tekton pipeline and configure it.

Before you start, ensure that you have admin access to your code repositories.

## Create an Empty Toolchain
1. Login to your IBM Cloud account and go to the Toolchains page https://cloud.ibm.com/devops/toolchains?env_id=ibm:yp:us-south.

2. Click on  `Create Toolchain`

3.  Select `Build your own toolchain` template, change the default toolchain name if desired and click the Create button.

## API Key for the toolchain
You will need an API Key that has access to this toolchain.  For creating an API Key via the User Interface, click on Manage->Access->API Keys.  Click on Create an IBM Cloud API key to create an API Key.  Copy the API Key - you will need it later.

## Add DevOps Insights card to your Toolchain
Click on Add Tool button, select DevOps Insights card and click on Create Integration button.  Now, DevOps Insights card should be added to your toolchain.

## Add a card for your code repository to your Toolchain
Now, you need to add a card for your code repository to the toolchain.  Click on Add tool button then select the GitHub card or the Git Repos and Issue Tracking card to add the card to the toolchain.

## Add a card for the code repository where Tekton tasks have been defined
Click on Add tool button and then click on GitHub Enterprise Whitewater card.  Add the existing repository https://github.ibm.com/open-toolchain/tekton-catalog.

## Add and Configure a Tekton pipeline to your toolchain
- In this step, you will add a Tekton pipeline to the toolchain. Click on Add tool button and then click on Delivery Pipeline card.  Specify a Pipeline Name. For Pipeline Type, select Tekton.  Click Create Integration.
- Click on the pipeline card so that you can configure the pipeline.
- In this step, you will import Tekton task defintions into your toolchain. On the Definitions tab, click on Add button.  Select tekton-catalog repository.  Select branch `master`. Select path `toolchain` and click on Add button.  Similarly, add the following paths:  `git`,`utils`, `cra` and `cra-v2/sample`.  Now click Validate button and then Save button.

| Repository        | Branch | Path           |
| ----------------- | ------ | -------------- |
| tekton-catalog	| master | toolchain      |
| tekton-catalog	| master | git            |
| tekton-catalog	| master | utils          |
| tekton-catalog	| master | cra            |
| tekton-catalog	| master | cra/sample-v2  |


- In this step, you will specify the Tekton worker pool for this pipeline. There is a managed worker pool that IBM provides for Dallas location - you can select that.  You can also choose to host a private worker pool.

- In this step, you will set up a Trigger for you code repository.  Click on Triggers menu. Click Add trigger button and select Git Repository.  For Repository, select your code repository.  Select the branch for which you want to enable the trigger.  Select the checkboxes for the events the trigger should listen for.  Select the appropriate EventListener. Click Save button.  You can add a trigger for each repo for which you want to run Code Risk Analyzer pipeline. Configure your trigger by adding any trigger properties defined [here](../README.md).

- In this step, you will specify Environment Properties for your pipeline. Click on Environment properties tab. Click on Add button and then click on Secure. Specify Property Name apikey. Now specify the API Key that you generated earlier in the Value field.  Click on Save button.

# Scanning your Pull Requests
After the above set up is complete, follow these steps:
- Open a Pull Request or push a commit to your repository
- The Code Risk Analyzer pipeline that you configured above will start running automatically.
- The pipeline first discovers the dependencies that your repository has.  These dependencies could be application packages, container images or OS pacakges.
- The pipeline then identifies vulnerabilities associated with these dependencies.
- The pipeline then scans Dockerfiles and Kubernetes yaml files for best practices.

# Manual scanning
You can set up a trigger to be ran manually. The following additional parameters are supported for manual triggers.

## Detailed Description

This pipeline and relevant trigger(s) can be configured using the properties described below.

See https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines&interface=ui#configure_tekton_pipeline for more information.


**EventListeners:**

- [github-listener](#github-listener) - github enterprise pull-request listener
- [gl-ci-listener](#gl-ci-listener) - github enterprise commit push listener
- [gl-pr-listener](#gl-pr-listener) - grit/gitlab pull-request listener

### github-listener

**EventListener**: github-listener - github enterprise pull-request listener


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` | The ibmcloud api key | - | Yes | string |
| `apikey` (**secured property**) | [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and git intergation toolcard like `Git Repos and Issue Tracking` service if used). | - | Yes | secret |
| `asset-type` | Security checks to run (apps, image, os, all) | `all` | No | string |
| `bom-report` | Filepath to store generated Bill of Materials. Default to `./bom.json` | `bom.json` | No | string |
| `branch` | The git branch | `` | No | string |
| `commit-id` | commit id | `` | No | string |
| `cra-scan-image` | Image to use for `scan` task. | `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72` | No | string |
| `custom-script` | Filepath to a custom script that is ran prior to CRA scanning | `` | No | string |
| `cveignore` | Filepath to cveignore | `` | No | string |
| `deploy-report` | Filepath to store generated Deploy Analytic report. Default to `./deploy.json` | `deploy.json` | No | string |
| `docker-build-context` | If specified, CRA will use the directory in the path parameter as docker build context | - | Yes | string |
| `docker-build-flags` | Customize docker build command for build stage scanning | `` | No | string |
| `docker-registry-secret` | Secret to authenticate for docker-registry-url | - | Yes | string |
| `docker-registry-secret` (**secured property**) | the secret used to login to docker-registry-url | - | Yes | secret |
| `docker-registry-url` | Registry url to use for docker login | `` | No | string |
| `docker-registry-username` | Username to authenticate for docker-registry-url | `` | No | string |
| `dockerfile-pattern` | Pattern to identify Dockerfile in the repository | - | Yes | string |
| `env-props` | A custom configuration of environment properties to source before execution, ex. 'export ABC=123 export DEF=456' | `` | No | string |
| `exclude-dev` | Exclude dev dependencies during vulnerability scan | `false` | No | string |
| `fileignore` | Filepath to .fileignore | `` | No | string |
| `git-credentials-json-file` | JSON file containing the git credentials as found out of the clone task | `output/secrets/thecredentials.json` | No | string |
| `gradle-exclude-configs` | Exclude gradle configurations, ex. 'runtimeClasspath,testCompileClasspath' | `` | No | string |
| `gradle-props` | Customize gradle command with props for gradle dependency scanning. | `` | No | string |
| `ibmcloud-api` | The ibmcloud api | `https://cloud.ibm.com` | No | string |
| `ibmcloud-region` | ibmcloud region to use | `` | No | string |
| `ibmcloud-trace` | Enables IBMCLOUD_TRACE for ibmcloud cli logging | `false` | No | string |
| `maven-exclude-scopes` | Exclude maven scopes, ex. 'test,compile' | `` | No | string |
| `nodejs-create-package-lock` | Enable the task to build the package-lock.json for node.js projects | `false` | No | string |
| `output` | Prints command result to console | `false` | No | string |
| `path` | Repository path to scan | `/artifacts` | No | string |
| `pipeline-debug` | Toggles debug mode for the pipeline | `0` | No | string |
| `pr-branch` | The branch in the forked git repo from where the PR is made | `` | No | string |
| `pr-repository` | The forked git repo from where the PR is made | `` | No | string |
| `prev-report` | Filepath to previous BoM report to skip Dockerfile or application manifest scans | `` | No | string |
| `registry-region` | The ibmcloud container registry region | `` | No | string |
| `repository` | The git repo | - | Yes | string |
| `resource-group` | Target resource group (name or id) for the ibmcloud login operation | `` | No | string |
| `strict` | Enables strict mode for scanning | `false` | No | string |
| `terraform-report` | Filepath to store generated Terraform report. Default to `./terraform.json` | `terraform.json` | No | string |
| `tf-attachment-file` | Path of SCC V2 attachment file. | `` | No | string |
| `tf-dir` | The directory where the terraform main entry file is found if not in parent directory | `` | No | string |
| `tf-plan` | Filepath to Terraform Plan file. | `` | No | string |
| `tf-policy-file` | Filepath to policy profile. This flag can accept an SCC V2 profile or a custom json file with a set of SCC rules. | `` | No | string |
| `tf-var-file` | terraform var-file | `` | No | string |
| `tf-version` | The terraform version to use to create Terraform plan | `0.15.5` | No | string |
| `toolchainid` | The target toolchain id to be used. Defaults to the current toolchain id | `` | No | string |
| `verbose` | Enable verbose log messages | `false` | No | string |
| `vulnerability-report` | Filepath to store Vulnerability report, not stored if empty. Default to `./vulnerability.json` | `vulnerability.json` | No | string |


### gl-ci-listener

**EventListener**: gl-ci-listener - github enterprise commit push listener


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` | The ibmcloud api key | - | Yes | string |
| `apikey` (**secured property**) | [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and git intergation toolcard like `Git Repos and Issue Tracking` service if used). | - | Yes | secret |
| `asset-type` | Security checks to run (apps, image, os, all) | `all` | No | string |
| `bom-report` | Filepath to store generated Bill of Materials. Default to `./bom.json` | `bom.json` | No | string |
| `branch` | The git branch | `` | No | string |
| `commit-id` | commit id | `` | No | string |
| `cra-scan-image` | Image to use for `scan` task. | `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72` | No | string |
| `custom-script` | Filepath to a custom script that is ran prior to CRA scanning | `` | No | string |
| `cveignore` | Filepath to cveignore | `` | No | string |
| `deploy-report` | Filepath to store generated Deploy Analytic report. Default to `./deploy.json` | `deploy.json` | No | string |
| `docker-build-context` | If specified, CRA will use the directory in the path parameter as docker build context | - | Yes | string |
| `docker-build-flags` | Customize docker build command for build stage scanning | `` | No | string |
| `docker-registry-secret` | Secret to authenticate for docker-registry-url | - | Yes | string |
| `docker-registry-secret` (**secured property**) | the secret used to login to docker-registry-url | - | Yes | secret |
| `docker-registry-url` | Registry url to use for docker login | `` | No | string |
| `docker-registry-username` | Username to authenticate for docker-registry-url | `` | No | string |
| `dockerfile-pattern` | Pattern to identify Dockerfile in the repository | - | Yes | string |
| `env-props` | A custom configuration of environment properties to source before execution, ex. 'export ABC=123 export DEF=456' | `` | No | string |
| `exclude-dev` | Exclude dev dependencies during vulnerability scan | `false` | No | string |
| `fileignore` | Filepath to .fileignore | `` | No | string |
| `git-credentials-json-file` | JSON file containing the git credentials as found out of the clone task | `output/secrets/thecredentials.json` | No | string |
| `gradle-exclude-configs` | Exclude gradle configurations, ex. 'runtimeClasspath,testCompileClasspath' | `` | No | string |
| `gradle-props` | Customize gradle command with props for gradle dependency scanning. | `` | No | string |
| `ibmcloud-api` | The ibmcloud api | `https://cloud.ibm.com` | No | string |
| `ibmcloud-region` | ibmcloud region to use | `` | No | string |
| `ibmcloud-trace` | Enables IBMCLOUD_TRACE for ibmcloud cli logging | `false` | No | string |
| `maven-exclude-scopes` | Exclude maven scopes, ex. 'test,compile' | `` | No | string |
| `nodejs-create-package-lock` | Enable the task to build the package-lock.json for node.js projects | `false` | No | string |
| `output` | Prints command result to console | `false` | No | string |
| `path` | Repository path to scan | `/artifacts` | No | string |
| `pipeline-debug` | Toggles debug mode for the pipeline | `0` | No | string |
| `pr-branch` | The branch in the forked git repo from where the PR is made | `` | No | string |
| `pr-repository` | The forked git repo from where the PR is made | `` | No | string |
| `prev-report` | Filepath to previous BoM report to skip Dockerfile or application manifest scans | `` | No | string |
| `registry-region` | The ibmcloud container registry region | `` | No | string |
| `repository` | The git repo | - | Yes | string |
| `resource-group` | Target resource group (name or id) for the ibmcloud login operation | `` | No | string |
| `strict` | Enables strict mode for scanning | `false` | No | string |
| `terraform-report` | Filepath to store generated Terraform report. Default to `./terraform.json` | `terraform.json` | No | string |
| `tf-attachment-file` | Path of SCC V2 attachment file. | `` | No | string |
| `tf-dir` | The directory where the terraform main entry file is found if not in parent directory | `` | No | string |
| `tf-plan` | Filepath to Terraform Plan file. | `` | No | string |
| `tf-policy-file` | Filepath to policy profile. This flag can accept an SCC V2 profile or a custom json file with a set of SCC rules. | `` | No | string |
| `tf-var-file` | terraform var-file | `` | No | string |
| `tf-version` | The terraform version to use to create Terraform plan | `0.15.5` | No | string |
| `toolchainid` | The target toolchain id to be used. Defaults to the current toolchain id | `` | No | string |
| `verbose` | Enable verbose log messages | `false` | No | string |
| `vulnerability-report` | Filepath to store Vulnerability report, not stored if empty. Default to `./vulnerability.json` | `vulnerability.json` | No | string |


### gl-pr-listener

**EventListener**: gl-pr-listener - grit/gitlab pull-request listener


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` | The ibmcloud api key | - | Yes | string |
| `apikey` (**secured property**) | [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and git intergation toolcard like `Git Repos and Issue Tracking` service if used). | - | Yes | secret |
| `asset-type` | Security checks to run (apps, image, os, all) | `all` | No | string |
| `bom-report` | Filepath to store generated Bill of Materials. Default to `./bom.json` | `bom.json` | No | string |
| `branch` | The git branch | `` | No | string |
| `commit-id` | commit id | `` | No | string |
| `cra-scan-image` | Image to use for `scan` task. | `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.72` | No | string |
| `custom-script` | Filepath to a custom script that is ran prior to CRA scanning | `` | No | string |
| `cveignore` | Filepath to cveignore | `` | No | string |
| `deploy-report` | Filepath to store generated Deploy Analytic report. Default to `./deploy.json` | `deploy.json` | No | string |
| `docker-build-context` | If specified, CRA will use the directory in the path parameter as docker build context | - | Yes | string |
| `docker-build-flags` | Customize docker build command for build stage scanning | `` | No | string |
| `docker-registry-secret` | Secret to authenticate for docker-registry-url | - | Yes | string |
| `docker-registry-secret` (**secured property**) | the secret used to login to docker-registry-url | - | Yes | secret |
| `docker-registry-url` | Registry url to use for docker login | `` | No | string |
| `docker-registry-username` | Username to authenticate for docker-registry-url | `` | No | string |
| `dockerfile-pattern` | Pattern to identify Dockerfile in the repository | - | Yes | string |
| `env-props` | A custom configuration of environment properties to source before execution, ex. 'export ABC=123 export DEF=456' | `` | No | string |
| `exclude-dev` | Exclude dev dependencies during vulnerability scan | `false` | No | string |
| `fileignore` | Filepath to .fileignore | `` | No | string |
| `git-credentials-json-file` | JSON file containing the git credentials as found out of the clone task | `output/secrets/thecredentials.json` | No | string |
| `gradle-exclude-configs` | Exclude gradle configurations, ex. 'runtimeClasspath,testCompileClasspath' | `` | No | string |
| `gradle-props` | Customize gradle command with props for gradle dependency scanning. | `` | No | string |
| `ibmcloud-api` | The ibmcloud api | `https://cloud.ibm.com` | No | string |
| `ibmcloud-region` | ibmcloud region to use | `` | No | string |
| `ibmcloud-trace` | Enables IBMCLOUD_TRACE for ibmcloud cli logging | `false` | No | string |
| `maven-exclude-scopes` | Exclude maven scopes, ex. 'test,compile' | `` | No | string |
| `nodejs-create-package-lock` | Enable the task to build the package-lock.json for node.js projects | `false` | No | string |
| `output` | Prints command result to console | `false` | No | string |
| `path` | Repository path to scan | `/artifacts` | No | string |
| `pipeline-debug` | Toggles debug mode for the pipeline | `0` | No | string |
| `pr-branch` | The branch in the forked git repo from where the PR is made | `` | No | string |
| `pr-repository` | The forked git repo from where the PR is made | `` | No | string |
| `prev-report` | Filepath to previous BoM report to skip Dockerfile or application manifest scans | `` | No | string |
| `registry-region` | The ibmcloud container registry region | `` | No | string |
| `repository` | The git repo | - | Yes | string |
| `resource-group` | Target resource group (name or id) for the ibmcloud login operation | `` | No | string |
| `strict` | Enables strict mode for scanning | `false` | No | string |
| `terraform-report` | Filepath to store generated Terraform report. Default to `./terraform.json` | `terraform.json` | No | string |
| `tf-attachment-file` | Path of SCC V2 attachment file. | `` | No | string |
| `tf-dir` | The directory where the terraform main entry file is found if not in parent directory | `` | No | string |
| `tf-plan` | Filepath to Terraform Plan file. | `` | No | string |
| `tf-policy-file` | Filepath to policy profile. This flag can accept an SCC V2 profile or a custom json file with a set of SCC rules. | `` | No | string |
| `tf-var-file` | terraform var-file | `` | No | string |
| `tf-version` | The terraform version to use to create Terraform plan | `0.15.5` | No | string |
| `toolchainid` | The target toolchain id to be used. Defaults to the current toolchain id | `` | No | string |
| `verbose` | Enable verbose log messages | `false` | No | string |
| `vulnerability-report` | Filepath to store Vulnerability report, not stored if empty. Default to `./vulnerability.json` | `vulnerability.json` | No | string |
