# Code Risk Analyzer

Tasks to scan your codebase using the Code Risk Analyzer scanners

## Available Tasks
- **[cra-bom](#cra-bom) [deprecated]**: This task creates a Bill-of-Material (BoM) for a given repository that captures pedigree of all the dependencies and it is collected at different granularities.
- **[cra-cis-check](#cra-cis-check) [deprecated]**: This tasks runs configuration checks on kubernetes deployment manifests.
- **[cra-comm-editor](#cra-comm-editor) [deprecated]**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.
- **[cra-discovery](#cra-discovery) [deprecated]**: This task accesses various source artifacts from the repository and performs deep discovery to identify all dependencies (including transitive dependencies).
- **[cra-terraform-scan-v2](#cra-terraform-scan-v2) [deprecated]**: This task uses `ibmcloud cli` and the `cra` plugin to scan ibm-terraform-provider files for compliance issues.
- **[cra-terraform-scan](#cra-terraform-scan) [deprecated]**: This task scans ibm-terraform-provider files for compliance issues. To configure CRA Terraform scan, Read more about using [terraform scan profile](./terraform-profile.md)
- **[cra-v2-cra](#cra-v2-cra) [deprecated]**: This task accesses various source artifacts from a repository and performs deep discovery to identify all dependencies (including transitive dependencies). A Bill-of-Material (BoM) is generated that captures pedigree of all dependencies, collected at different granularities. The BoM is scanned to discover and report any known vulnerabilities in OS and Application pacakges. Finally, configuration checks on kubernetes deployment manifests are performed to uncover any issues.
- **[cra-vulnerability-remediation](#cra-vulnerability-remediation) [deprecated]**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.

## Install the Tasks

- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `cra`

## Usages

- The `sample` sub-directory contains an EventListener definition to configure on Pull Request (or Merge Request for Gitlab/GRIT) that you can include in your tekton pipeline configuration to run the CRA tasks.

  See the documentation [here](./sample/README.md)

- The `sample-v2` sub-directory contains an EventListener definition to configure on Pull Request (or Merge Request for Gitlab/GRIT), on commit push, or manually that you can include in your tekton pipeline configuration to run the CRA tasks.

  See the documentation [here](./sample-v2/README.md)

- The `sample-cra-ci` sub-directory contains an EventListener definition to configure on commit push that you can include in your tekton pipeline configuration to run the CRA tasks.

  See the documentation [here](./sample-cra-ci/README.md)

## Details
### cra-bom [deprecated]

This task creates a Bill-of-Material (BoM) for a given repository that captures pedigree of all the dependencies and it is collected at different granularities.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Reference name for the secret resource

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **repository**: the git repo url
* **revision**: the revision (default to `master`)
* **source-repository**: the source git repo which could be different in case of forked repo
* **commit-id**: git commit id
* **pr-url**: pull request html url
* **ibmcloud-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **continuous-delivery-context-secret**: Reference name for the secret resource (default to `secure-properties`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **git-access-token**: (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
* **target-branch**: target branch
* **target-commit-id**: target branch commit id
* **project-id**: for gitlab repository, specify project-id
* **scm-type**: source code type used (github, github-ent, gitlab) (default to `github-ent`)
* **pipeline-debug**: toggles debug mode for the pipeline (default to `0`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located
* **secrets**: The workspace where the secrets are located

#### Results
* **status**: status of bom task, possible value are-success|failure
* **evidence-store**: filepath to store bom task evidence

### cra-cis-check [deprecated]

This tasks runs configuration checks on kubernetes deployment manifests.

#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Reference name for the secret resource

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **repository**: the git repo
* **revision**: the revision (default to `master`)
* **source-repository**: the source git repo which could be different in case of forked repo
* **commit-id**: git commit id
* **pr-url**: pull request html url
* **ibmcloud-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **continuous-delivery-context-secret**: Reference name for the secret resource (default to `secure-properties`)
* **git-access-token**: (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **project-id**: for gitlab repository specify project-id
* **directory-name**: directory name where the repository is cloned
* **scm-type**: source code type used (github, github-ent, gitlab) (default to `github-ent`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located
* **secrets**: The workspace where the secrets are located

#### Results
* **status**: status of cis task, possible value are-success|failure
* **evidence-store**: filepath to store cis task evidence

### cra-comm-editor [deprecated]

This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.

#### Parameters

* **repository**: the git repo url
* **pr-url**: merge request url
* **project-id**: project id
* **comment-fp**: comments filepath
* **scm-type**: source code type used (github, github-ent, gitlab)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located

### cra-discovery [deprecated]

This task accesses various source artifacts from the repository
and performs deep discovery to identify all dependencies (including transitive dependencies).


#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Reference name for the secret resource

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **repository**: the git repo
* **revision**: the revision (default to `master`)
* **commit-id**: git commit id
* **commit-timestamp**: git commit timestamp
* **directory-name**: directory name where the repository is cloned
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)
* **continuous-delivery-context-secret**: Reference name for the secret resource (default to `secure-properties`)
* **ibmcloud-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **continuous-delivery-context-environment**: Name of the configmap containing the continuous delivery pipeline context environment properties (default to `environment-properties`)
* **maven-exclude-scopes**: Tag dependencies in scope as dev for the vulnerability scan
* **gradle-exclude-configs**: Tag dependencies in gradle configurations as dev for the vulnerability scan
* **nodejs-create-package-lock**: Enable CRA discovery to build the package-lock.json file for node.js repos (default to `false`)
* **python-create-requirements-txt**: Enable CRA discovery to build the requirements.txt file for python repos (default to `false`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located

#### Results
* **status**: status of discovery task, possible value are-success|failure

### cra-terraform-scan-v2 [deprecated]

This task uses `ibmcloud cli` and the `cra` plugin to scan ibm-terraform-provider files for compliance issues.


#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Reference name for the secret resource

  Secret containing:
  * **apikey**: Field in the secret that contains the api key used to login to ibmcloud

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **continuous-delivery-context-environment**: Name of the configmap containing the continuous delivery pipeline context environment properties (default to `environment-properties`)
* **continuous-delivery-context-secret**: Reference name for the secret resource (default to `secure-properties`)
* **ibmcloud-api**: The ibmcloud api (default to `https://cloud.ibm.com`)
* **ibmcloud-apikey-secret-key**: Field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **ibmcloud-region**: (Optional) ibmcloud region to use
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1 (default to `0`)
* **resource-group**: (Optional) Target resource group (name or id) for the ibmcloud login operation
* **custom-script**: (Optional) Filepath to a custom script that is ran prior to CRA scanning
* **ibmcloud-trace**: (Optional) Enables IBMCLOUD_TRACE for ibmcloud cli logging (default to `false`)
* **output**: (Optional) Prints command result to console (default to `false`)
* **path**: Directory where the repository is cloned (default to `/artifacts`)
* **strict**: (Optional) Enables strict mode for scanning (default to `false`)
* **toolchainid**: (Optional) The target toolchain id to be used. Defaults to the current toolchain id
* **verbose**: (Optional) Enable verbose log messages (default to `false`)
* **terraform-report**: Filepath to store generated Terraform report (default to `terraform.json`)
* **tf-dir**: The directory where the terraform main entry file is found
* **tf-plan**: (Optional) Filepath to Terraform Plan file.
* **tf-var-file**: (Optional) Filepath to the Terraform var-file
* **tf-version**: (Optional) The terraform version to use to create Terraform plan (default to `0.15.5`)
* **tf-policy-file**: (Optional) Filepath to policy profile. This flag can accept an SCC V2 profile or a custom json file with a set of SCC rules.
* **tf-attachment-file**: (Optional) Path of SCC V2 attachment file.
* **cra-scan-image**: Image to use for `scan` task (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located

### cra-terraform-scan [deprecated]

This task scans ibm-terraform-provider files for compliance issues.
To configure CRA Terraform scan, Read more about using [terraform scan profile](./terraform-profile.md)


#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Reference name for the secret resource

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **repository**: the git repo
* **branch**: the branch (default to `master`)
* **commit-id**: git commit id
* **tf-dir**: the directory where the terraform main entry file is found
* **ibmcloud-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **continuous-delivery-context-secret**: Reference name for the secret resource (default to `secure-properties`)
* **directory-name**: directory name where the repository is cloned
* **pipeline-debug**: toggles debug mode for the pipeline (default to `0`)
* **policy-config-json**: Configure policies to control thresholds
* **pr-url**: pull request html url
* **project-id**: for gitlab repository, specify project-id
* **scm-type**: source code type used (github, github-ent, gitlab) (default to `github-ent`)
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **git-access-token**: (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
* **tf-var-file**: (optional) terraform var-file

#### Workspaces

* **artifacts**: The workspace where the artifacts are located
* **secrets**: The workspace where the secrets are located

#### Results
* **status**: status of deployment analyzer task, possible value are- success|failed
* **evidence-store**: filepath to store deployment analyzer task evidence

### cra-v2-cra [deprecated]

This task accesses various source artifacts from a repository and performs deep discovery to identify all dependencies (including transitive dependencies).
A Bill-of-Material (BoM) is generated that captures pedigree of all dependencies, collected at different granularities. The BoM is scanned to discover and
report any known vulnerabilities in OS and Application pacakges. Finally, configuration checks on kubernetes deployment manifests are performed to uncover any issues.


#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Reference name for the secret resource

  Secret containing:
  * **apikey**: Field in the secret that contains the api key used to login to ibmcloud
  * **docker-registry-secret**: Field in the secret that contains the secret used to login to docker-registry-url

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **continuous-delivery-context-environment**: Name of the configmap containing the continuous delivery pipeline context environment properties (default to `environment-properties`)
* **continuous-delivery-context-secret**: Reference name for the secret resource (default to `secure-properties`)
* **docker-registry-secret**: Field in the secret that contains the secret used to login to docker-registry-url (default to `docker-registry-secret`)
* **ibmcloud-api**: The ibmcloud api (default to `https://cloud.ibm.com`)
* **ibmcloud-apikey-secret-key**: Field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **ibmcloud-region**: (Optional) ibmcloud region to use
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1 (default to `0`)
* **registry-region**: (Optional) The ibmcloud container registry region
* **resource-group**: (Optional) Target resource group (name or id) for the ibmcloud login operation
* **custom-script**: (Optional) Filepath to a custom script that is ran prior to CRA scanning
* **env-props**: (Optional) A custom configuration of environment properties to source before execution, ex. 'export ABC=123 export DEF=456'
* **fileignore**: (Optional) Filepath to .fileignore
* **ibmcloud-trace**: (Optional) Enables IBMCLOUD_TRACE for ibmcloud cli logging (default to `false`)
* **output**: (Optional) Prints command result to console (default to `false`)
* **path**: Directory where the repository is cloned (default to `/artifacts`)
* **strict**: (Optional) Enables strict mode for scanning (default to `false`)
* **toolchainid**: (Optional) The target toolchain id to be used. Defaults to the current toolchain id
* **verbose**: (Optional) Enable verbose log messages (default to `false`)
* **asset-type**: Security checks to run (apps, image, os, all) (default to `all`)
* **bom-report**: Filepath to store generated Bill of Materials (default to `bom.json`)
* **docker-build-flags**: (Optional) Customize docker build command for build stage scanning
* **docker-build-context**: (Optional) If specified, CRA will use the directory in the path parameter as docker build context (default to `false`)
* **dockerfile-pattern**: (Optional) Pattern to identify Dockerfile in the repository (default to `Dockerfile`)
* **docker-registry-url**: Registry url to use for docker login
* **docker-registry-username**: Username to authenticate for docker-registry-url
* **gradle-exclude-configs**: (Optional) Exclude gradle configurations, ex. 'runtimeClasspath,testCompileClasspath'
* **gradle-props**: (Optional) Customize gradle command with props for gradle dependency scanning.
* **maven-exclude-scopes**: (Optional) Exclude maven scopes, ex. 'test,compile'
* **nodejs-create-package-lock**: (Optional) Enable the task to build the package-lock.json for node.js projects (default to `false`)
* **prev-report**: (Optional) Filepath to previous BoM report to skip Dockerfile or application manifest scans
* **deploy-report**: Filepath to store generated Deploy Analytic report (default to `deploy.json`)
* **cveignore**: (Optional) File path to cveignore
* **exclude-dev**: (Optional) Exclude dev dependencies during vulnerability scan (default to `false`)
* **vulnerability-report**: Filepath to store generated Vulnerability report, not stored if empty (default to `vulnerability.json`)
* **cra-scan-image**: Image to use for `scan` task (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **dind-image**: image to use for the Docker-in-Docker sidecar (default to `icr.io/continuous-delivery/pipeline/docker:20.10.22-dind`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located

### cra-vulnerability-remediation [deprecated]

This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.


#### Context - ConfigMap/Secret

  The task may rely on the following kubernetes resources to be defined:

* **Secret secure-properties**
  Reference name for the secret resource

  Secret containing:
  * **apikey**: field in the secret that contains the api key used to login to ibmcloud

Note: secret name and secret key(s) can be configured using Task's params.
#### Parameters

* **ibmcloud-api**: the ibmcloud api (default to `https://cloud.ibm.com`)
* **repository**: the git repo
* **source-repository**: the source git repo which could be different in case of forked repo
* **revision**: the revision (default to `master`)
* **pr-url**: pull request url
* **commit-id**: git commit id
* **ibmcloud-apikey-secret-key**: field in the secret that contains the api key used to login to ibmcloud (default to `apikey`)
* **continuous-delivery-context-secret**: Reference name for the secret resource (default to `secure-properties`)
* **git-access-token**: (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
* **resource-group**: target resource group (name or id) for the ibmcloud login operation
* **project-id**: for gitlab repository, specify project-id
* **scm-type**: source code type used (github, github-ent, gitlab) (default to `github-ent`)
* **pipeline-debug**: Pipeline debug mode. Value can be 0 or 1. (default to `0`)
* **exclude-dev**: (optional) Exclude dev dependencies during scan (default to `false`)
* **repo-dir**: Specifies the path for the repository or .cracveomit file (default to `/artifacts`)

#### Workspaces

* **artifacts**: The workspace where the artifacts are located
* **secrets**: The workspace where the secrets are located

#### Results
* **status**: status of vulnerability task, possible value are-success|failure
* **evidence-store**: filepath to store vulnerability task evidence
