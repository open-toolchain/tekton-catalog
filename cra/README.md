# Code Risk Analyzer

Tasks to scan your codebase using the Code Risk Analyzer scanners

## Tasks

- **[cra](#cra)**: This task accesses various source artifacts from a repository and performs deep discovery to identify all dependencies (including transitive dependencies). A Bill-of-Material (BoM) is generated that captures pedigree of all dependencies, collected at different granularities. The BoM is scanned to discover and report any known vulnerabilities in OS and Application pacakges. Finally, configuration checks on kubernetes deployment manifests are performed to uncover any issues.
- **[cra-discovery](#cra-discovery)**: This task accesses various source artifacts from the repository and performs deep discovery to identify all dependencies (including transitive dependencies).
- **[cra-bom](#cra-bom)**: This task creates a Bill-of-Material (BoM) for a given repository that captures pedigree of all the dependencies and it is collected at different granularities.
- **[cra-cis-check](#cra-cis-check)**: This tasks runs configuration checks on kubernetes deployment manifests.
- **[cra-vulnerability-remediation](#cra-vulnerability-remediation)**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.
- **[cra-comm-editor](#cra-comm-editor)**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.
- **[cra-terraform-scan](#cra-terraform-scan)**: This task scans ibm-terraform-provider files for compliance issues.

## Install the Tasks
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `cra`

## Usages

- The `sample` sub-directory contains an EventListener definition to configure on Pull Request (or Merge Request for Gitlab/GRIT) that you can include in your tekton pipeline configuration to run the CRA tasks.

  See the documentation [here](./sample/README.md)

- The `sample-v2` sub-directory contains an EventListener definition to configure on Pull Request (or Merge Request for Gitlab/GRIT), on commit push, or manually that you can include in your tekton pipeline configuration to run the CRA tasks.

  See the documentation [here](./sample-v2/README.md)

- The `sample-cra-ci` sub-directory contains an EventListener definition to configure on commit push that you can include in your tekton pipeline configuration to run the CRA tasks.

  See the documentation [here](./sample-cra-ci/README.md)


## cra

This task uses `ibmcloud cli` and the `cra` plugin to accesses various source artifacts from the repository and performs deep discovery
to identify all dependencies (including transitive dependencies). Specifically, it parses the following assets:

1. Dockerfile: All Build stages, Base Images in every stage, list of packages from base images,
any add-on packages installed on top of base image(s).

2. Package Manifests: requirements.txt (python), package-lock.json (Node.js), pom.xml (java)

A Bill-of-Material (BoM) for a given repository is then generated to capture pedigree of all dependencies, collected at different granularities. For instance, it captures a list of base images used in the build, lists of packages from the base images, and lists of application packages installed over base images. The BoM essentially acts as a ground truth for our analytic results and can potentially be used to enforce policy gates.

Finally, configuration checks are run on kubernetes deployment manifests.

Docker CIS provides prescriptive guidance for establishing a secure configuration posture for Docker container.
Code Risk Analyzer takes these security configurations as point of reference and identifies security controls that can be
checked in the deployment artifacts (*.yaml) for kubernetes applications.
In addition, this task also provides security `risk` for every control failure.

The following controls have been identified from CIS Docker 1.13.0 that we can implement in DevSecOps. Some additional controls are added based on open source references of [KCCSS](https://github.com/octarinesec/kccss)



|ID | Rule | Risk |
|---------|---------|:----------:|
|5.3|Ensure containers do not have CAP_SYS_ADMIN capability|High|
|5.3|Ensure containers do not have CAP_NET_RAW capability|High|
|5.4|Ensure privileged containers are not used|High|
|5.5|Ensure sensitive host system directories are not mounted on containers|Medium|
|5.7|Ensure privileged ports are not mapped within containers|Low|
|5.9|Ensure the host's network namespace is not shared|Medium|
|5.10|Ensure memory usage for container is limited|Medium|
|5.11|Ensure CPU priority is set appropriately on the container|Medium|
|5.12|Ensure the container's root filesystem is mounted as read only|Medium|
|5.15|Ensure the host's process namespace is not shared|Medium|
|5.16|Ensure the host's IPC namespace is not shared|Medium|
|5.31|Ensure the Docker socket is not mounted inside any containers|High|
|-|Ensure containers do not allow unsafe allocation of CPU resources|Medium|
|-|Ensure containers do not allow privilege escalation|Medium|
|-|Ensure containers do not expose unsafe parts of /proc|Medium|
|-|Ensure containers are not exposed through a shared host port|Medium|

### Inputs

#### Parameters

  - **continuous-delivery-context-environment**: (Default: `environment-properties`) Name of the configmap containing the continuous delivery pipeline context environment properties
  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource
  - **docker-registry-secret**: (Default: `docker-registry-secret`) Field in the secret that contains the secret used to login to docker-registry-url
  - **ibmcloud-api**: (Default: `https://cloud.ibm.com`) The ibmcloud api url
  - **ibmcloud-apikey-secret-key**: (Default: `apikey`) field in the secret that contains the api key used to login to ibmcloud
  - **ibmcloud-region**: (Optional) The ibmcloud target region
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug
  - **registry-region**: (Optional) The ibmcloud container registry region
  - **resource-group**: (Optional) Target resource group (name or id) for the ibmcloud login operation
  - **custom-script**: (Optional) A custom script to be ran prior to CRA scanning
  - **env-props**: (Optional) A custom configuration of environment properties to source before execution, ex. 'export ABC=123 export DEF=456'
  - **fileignore**: (Optional) Filepath to .fileignore
  - **ibmcloud-trace**: (Default: `false`) Enables IBMCLOUD_TRACE for ibmcloud cli logging
  - **output**: (Default: `false`) Prints command result to console
  - **path**: (Default: `/artifacts`) Directory where the repository is cloned
  - **strict**: (Optional) Enables strict mode for scanning
  - **toolchainid**: The ibmcloud target toolchain to be used
  - **verbose**: (Optional) Enable verbose log messages
  - **asset-type**: (Default: `all`) Security checks to run (apps, image, os, all)
  - **bom-report**: (Default: `./bom.json`) Filepath to store generated Bill of Materials
  - **docker-build-flags**: (Optional) Customize docker build command for build stage scanning
  - **docker-build-context**: (Optional) If specified, CRA will use the directory in the path parameter as docker build context
  - **dockerfile-pattern**: (Optional) Pattern to identify Dockerfile in the repository
  - **docker-registry-url**: (Optional) Registry url to use for docker login. Valid only if combined with `docker-registry-username` and `docker-registry-secret`
  - **docker-registry-username**: (Optional) Username to authenticate for docker-registry-url. Valid only if combined with `docker-registry-url` and `docker-registry-secret`
  - **gradle-exclude-configs**: (Optional) Exclude gradle configurations, ex. 'runtimeClasspath,testCompileClasspath'
  - **maven-exclude-scopes**: (Optional) Exclude maven scopes, ex. 'test,compile'
  - **nodejs-create-package-lock**: (Default: `false`) Enable the task to build the package-lock.json for node.js projects
  - **prev-report**: (Optional) Filepath to previous BoM report to skip Dockerfile or application manifest scans
  - **deploy-report**: (Default: `./deploy.json`) Filepath to store generated Deploy Analytic report
  - **cveignore**: (Optional) File path to cveignore
  - **exclude-dev**: (Default: `false`) Exclude dev dependencies during vulnerability scan
  - **vulnerability-report**: (Default: `./vulnerability.json`) Filepath to store generated Vulnerability report
  - **cra-scan-image**: (Default: `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.9`) Image to use for `scan` task
  - **dind-image**: (Default to `icr.io/continuous-delivery/pipeline/docker:19.03.15-dind`) Image to use for the Docker-in-Docker sidecar 

#### Implicit
The following inputs are coming from tekton annotation:
 - **PIPELINE_RUN_ID**: ID of the current pipeline run

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

### Results

- **status**: Status of cra discovery task, possible value are - success|failure

### Usage

Example usage in a pipeline.
``` yaml
    - name: code-risk-analyzer
      runAfter:
        - checkout
      taskRef:
        name: cra
      params:
        - name: ibmcloud-api
          value: $(params.ibmcloud-api)
        - name: ibmcloud-region
          value: $(params.ibmcloud-region)
        - name: pipeline-debug
          value: $(params.pipeline-debug)
        - name: registry-region
          value: $(params.registry-region)
        - name: resource-group
          value: $(params.resource-group)
        - name: custom-script
          value: $(params.custom-script)
        - name: env-props
          value: $(params.env-props)
        - name: fileignore
          value: $(params.fileignore)
        - name: ibmcloud-trace
          value: $(params.ibmcloud-trace)
        - name: output
          value: $(params.output)
        - name: path
          value: $(params.path)
        - name: strict
          value: $(params.strict)
        - name: toolchainid
          value: $(params.toolchainid)
        - name: verbose
          value: $(params.verbose)
        - name: asset-type
          value: $(params.asset-type)
        - name: bom-report
          value: $(params.bom-report)
        - name: docker-build-flags
          value: $(params.docker-build-flags)
        - name: docker-build-context
          value: $(params.docker-build-context)
        - name: dockerfile-pattern
          value: $(params.dockerfile-pattern)
        - name: docker-registry-url
          value: $(params.docker-registry-url)
        - name: docker-registry-username
          value: $(params.docker-registry-username)
        - name: gradle-exclude-configs
          value: $(params.gradle-exclude-configs)
        - name: maven-exclude-scopes
          value: $(params.maven-exclude-scopes)
        - name: nodejs-create-package-lock
          value: $(params.nodejs-create-package-lock)
        - name: prev-report
          value: $(params.prev-report)
        - name: deploy-report
          value: $(params.deploy-report)
        - name: cveignore
          value: $(params.cveignore)
        - name: exclude-dev
          value: $(params.exclude-dev)
        - name: vulnerability-report
          value: $(params.vulnerability-report)
        - name: cra-scan-image
          value: $(params.cra-scan-image)
      workspaces:
        - name: artifacts
          workspace: artifacts
```

## terraform-v2

This task uses `ibmcloud cli` and the `cra` plugin to scan ibm-terraform-provider files for compliance issues.
### Inputs

#### Parameters

  - **continuous-delivery-context-environment**: (Default: `environment-properties`) Name of the configmap containing the continuous delivery pipeline context environment properties
  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource
  - **docker-registry-secret**: (Default: `docker-registry-secret`) Field in the secret that contains the secret used to login to docker-registry-url
  - **ibmcloud-api**: (Default: `https://cloud.ibm.com`) The ibmcloud api url
  - **ibmcloud-apikey-secret-key**: (Default: `apikey`) field in the secret that contains the api key used to login to ibmcloud
  - **ibmcloud-region**: (Optional) The ibmcloud target region
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug
  - **registry-region**: (Optional) The ibmcloud container registry region
  - **resource-group**: (Optional) Target resource group (name or id) for the ibmcloud login operation
  - **custom-script**: (Optional) A custom script to be ran prior to CRA scanning
  - **ibmcloud-trace**: (Default: `false`) Enables IBMCLOUD_TRACE for ibmcloud cli logging
  - **output**: (Default: `false`) Prints command result to console
  - **path**: (Default: `/artifacts`) Directory where the repository is cloned
  - **strict**: (Optional) Enables strict mode for scanning
  - **toolchainid**: The ibmcloud target toolchain to be used
  - **verbose**: (Optional) Enable verbose log messages
  - **terraform-report**: (Default: `./terraform.json`) Filepath to store generated Terraform report
  - **tf-dir**: (Default `""`) The directory where the terraform main entry files are found.
  - **tf-plan**: (Optional) Filepath to Terraform Plan file.
  - **tf-var-file**: (Optional) Filepath to the Terraform var-file
  - **tf-version**: (Default: `0.15.5`)  The terraform version to use to create Terraform plan
  - **tf-policy-file**: (Optional) Filepath to policy profile. This file should contain "scc_goals" and "scc_goal_parameters" that will overwrite default checks
  - **tf-format**: (Optional) Report format. Requires --policy-file. Supported values: OSCAL
  - **tf-state-file**: (Optional) Path of terraform state file. Requires --format to be set to OSCAL.
  - **cra-scan-image**: (Default: `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.9`) Image to use for `scan` task

#### Implicit
The following inputs are coming from tekton annotation:
 - **PIPELINE_RUN_ID**: ID of the current pipeline run

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

### Results

- **status**: Status of cra terraform task, possible value are - success|failure

### Usage

Example usage in a pipeline.
``` yaml
    - name: cra-terraform-scan
      when:
        - input: "$(params.tf-dir)"
          operator: notin
          values: [""]
      runAfter:
        - code-risk-analyzer
      taskRef:
        name: cra-terraform-scan-v2
      workspaces:
        - name: artifacts
          workspace: artifacts
      params:
        - name: ibmcloud-api
          value: $(params.ibmcloud-api)
        - name: ibmcloud-region
          value: $(params.ibmcloud-region)
        - name: pipeline-debug
          value: $(params.pipeline-debug)
        - name: resource-group
          value: $(params.resource-group)
        - name: custom-script
          value: $(params.custom-script)
        - name: ibmcloud-trace
          value: $(params.ibmcloud-trace)
        - name: output
          value: $(params.output)
        - name: path
          value: $(params.path)
        - name: strict
          value: $(params.strict)
        - name: toolchainid
          value: $(params.toolchainid)
        - name: verbose
          value: $(params.verbose)
        - name: terraform-report
          value: $(params.terraform-report)
        - name: tf-dir
          value: $(params.tf-dir)
        - name: tf-plan
          value: $(params.tf-plan)
        - name: tf-var-file
          value: $(params.tf-var-file)
        - name: tf-policy-file
          value: $(params.tf-policy-file)
        - name: tf-version
          value: $(params.tf-version)
        - name: tf-format
          value: $(params.tf-format)
        - name: tf-state-file
          value: $(params.tf-state-file)
        - name: cra-scan-image
          value: $(params.cra-scan-image)

```


## cra-discovery

This task is being deprecated. It is recommended to use the `cra` task in it's place.

This task accesses various source artifacts from the repository and performs deep discovery
to identify all dependencies (including transitive dependencies). Specifically, it parses the following assets:

1. Dockerfile: All Build stages, Base Images in every stage, list of packages from base images,
any add-on packages installed on top of base image(s).

2. Package Manifests: requirements.txt (python), package-lock.json (Node.js), pom.xml (java)


### Inputs

#### Parameters

  - **repository**: The full URL path to the repo with the deployment files to be scanned
  - **revision**: (Default: `master`) The branch to scan
  - **commit-id**: The commit id of the change
  - **commit-timestamp**: (optional) The commit timestamp
  - **directory-name**:  The directory name where the repository is cloned
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug
  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource
  - **ibmcloud-apikey-secret-key**: (Default: `apikey`) field in the secret that contains the api key used to login to ibmcloud
  - **maven-exclude-scopes**: (Default: `""`) Specifies which scopes to exclude dependencies in scanning. Example: `test,compile`
  - **gradle-exclude-configs**: (Default: `""`) Specifies which gradle configurations to exclude dependencies in scanning. Example: `runtimeClasspath,testCompileClasspath`
  - **nodejs-create-package-lock**: (Default: `false`) Enable CRA discovery to build the package-lock.json file for node.js repos
  - **python-create-requirements-txt**: (Default: `false`) Enable CRA discovery to build the requirements.txt file for python repos 

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

#### Implicit / data from the pipeline

**Base image pulls secrets (optional)**

To provide pull credentials for the base image you use in your Dockerfile, for example for a UBI image from Red Hat registry, add these variables to your pipeline on he pipeline UI. The Task will look for them and if they are present, it will add an entry to the proper `config.json` for docker.

- **build-baseimage-auth-user** The username to the registry (Type: `text`)
- **build-baseimage-auth-password** The password to the registry (Type: `SECRET`)
- **build-baseimage-auth-host** The registry host name (Type: `text`)
- **build-baseimage-auth-email** An email address to the registry account (Type: `text`)

### Results

- **status**: Status of cra discovery task, possible value are - success|failure

### Usage

Example usage in a pipeline.
``` yaml
    - name: cra-discovery-scan
      runAfter:
        - cra-fetch-repo
      taskRef:
        name: cra-discovery
      workspaces:
        - name: artifacts
          workspace: artifacts
      params:
        - name: repository
          value: $(params.repository)
        - name: revision
          value: $(params.branch)
        - name: commit-id
          value: $(params.commit-id)
        - name: pipeline-debug
          value: $(params.pipeline-debug)
        - name: directory-name
          value: $(params.directory-name)
        - name: commit-timestamp
          value: $(params.commit-timestamp)
        - name: continuous-delivery-context-secret
          value: "secure-properties"
        - name: ibmcloud-apikey-secret-key
          value: "apikey"
        - name: maven-exclude-scopes
          value: $(params.maven-exclude-scopes)
        - name: gradle-exclude-configs
          value: $(params.gradle-exclude-configs)
        - name: nodejs-create-package-lock
          value: $(params.nodejs-create-package-lock)
        - name: python-create-requirements-txt
          value: $(params.python-create-requirements-txt)
```

## cra-bom

This task is being deprecated. It is recommended to use the `cra` task in it's place.

Bill-of-Material (BoM) for a given repository captures pedigree of all the dependencies and it is collected at different granularities. For instance, it captures list of base images used in the build, list of packages from the base images, list of application packages installed over base image. The BoM essentially acts as a ground truth for our analytic results and can potentially be used to enforce policy gates.

### Inputs

#### Parameters

  - **ibmcloud-api**: (Default: `https://cloud.ibm.com`) The ibmcloud api url
  - **repository**: The full URL path to the repo with the deployment files to be scanned
  - **revision**: (Default: `master`) The branch to scan
  - **commit-id**: The commit id of change
  - **pr-url**: (Default: "") The pull request html url
  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource
  - **ibmcloud-apikey-secret-key**: (Default: apikey) field in the secret that contains the api key used to login to ibmcloud
  - **resource-group**: (Default: `""`) target resource group (name or id) for the ibmcloud login operation
  - **git-access-token**: (Default: `""`) (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
  - **target-branch**: (Default: `""`) The target branch for comparison
  - **target-commit-id**: (Default: `""`) The target commit id for comparison
  - **project-id**: (Default: `""`) Required id for GitLab repositories
  - **scm-type**: (Default: `github-ent`) Source code type used (github, github-ent, gitlab)
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug

#### Implicit
The following inputs are coming from tekton annotation:
 - **PIPELINE_RUN_ID**: ID of the current pipeline run

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

### Results

- **status**: status of cra bom task, possible value are-success|failure
- **evidence-store**: filepath to store bom task evidence

### Usage

```yaml
    - name: cra-bom
      taskRef:
        name: cra-bom
      runAfter:
        - cra-discovery-scan
      workspaces:
        - name: artifacts
          workspace: artifacts
        - name: secrets
          workspace: artifacts          
      params:
        - name: ibmcloud-api
          value: $(params.ibmcloud-api)
        - name: repository
          value: $(params.repository)
        - name: revision
          value: $(params.branch)
        - name: pr-url
          value: $(params.pr-url)
        - name: commit-id
          value: $(params.commit-id)
        - name: continuous-delivery-context-secret
          value: "secure-properties"
        - name: ibmcloud-apikey-secret-key
          value: "apikey"
        - name: resource-group
          value: $(params.resource-group)
        - name: git-access-token
          value: ""
        - name: target-branch
          value: $(params.target-branch)
        - name: target-commit-id
          value: $(params.target-commit-id)      
        - name: scm-type
          value: $(params.scm-type)
        - name: project-id
          value: $(params.project-id)    
        - name: pipeline-debug
          value: $(params.pipeline-debug)
```

## cra-cis-check

This task is being deprecated. It is recommended to use the `cra` task in it's place.

Runs configuration checks on kubernetes deployment manifests.

Docker CIS provides prescriptive guidance for establishing a secure configuration posture for Docker container.
Code Risk Analyzer takes these security configurations as point of reference and identifies security controls that can be
checked in the deployment artifacts (*.yaml) for kubernetes applications.
In addition, this task also provided security `risk` for every control failure.

We identified following controls from CIS Docker 1.13.0 that we can implement in DevSecOps. Some additional controls are added based on open source references of [KCCSS](https://github.com/octarinesec/kccss)



|ID | Rule | Risk |
|---------|---------|:----------:|
|5.3|Ensure containers do not have CAP_SYS_ADMIN capability|High|
|5.3|Ensure containers do not have CAP_NET_RAW capability|High|
|5.4|Ensure privileged containers are not used|High|
|5.5|Ensure sensitive host system directories are not mounted on containers|Medium|
|5.7|Ensure privileged ports are not mapped within containers|Low|
|5.9|Ensure the host's network namespace is not shared|Medium|
|5.10|Ensure memory usage for container is limited|Medium|
|5.11|Ensure CPU priority is set appropriately on the container|Medium|
|5.12|Ensure the container's root filesystem is mounted as read only|Medium|
|5.15|Ensure the host's process namespace is not shared|Medium|
|5.16|Ensure the host's IPC namespace is not shared|Medium|
|5.31|Ensure the Docker socket is not mounted inside any containers|High|
|-|Ensure containers do not allow unsafe allocation of CPU resources|Medium|
|-|Ensure containers do not allow privilege escalation|Medium|
|-|Ensure containers do not expose unsafe parts of /proc|Medium|
|-|Ensure containers are not exposed through a shared host port|Medium|



### Inputs

#### Parameters

  - **ibmcloud-api**: (Default: `https://cloud.ibm.com`) The ibmcloud api url
  - **repository**: The full URL path to the repo with the deployment files to be scanned
  - **revision**: (Default: `master`) The branch to scan
  - **commit-id**: The commit id of change
  - **pr-url**: The pull request url
  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource
  - **ibmcloud-apikey-secret-key**: (Default: apikey) field in the secret that contains the api key used to login to ibmcloud
  - **resource-group**: (Default: `""`) target resource group (name or id) for the ibmcloud login operation
  - **git-access-token**: (Default: `""`) (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
  - **project-id**: (Default: `""`) Required id for GitLab repositories
  - **directory-name**: The directory name where the repository is cloned
  - **scm-type**: (Default: `github-ent`) Source code type used (github, github-ent, gitlab)
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug
  

#### Implicit
The following inputs are coming from tekton annotation:
 - **PIPELINE_RUN_ID**: ID of the current pipeline run

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

### Results

- **status**: status of cra bom task, possible value are-success|failure
- **evidence-store**: filepath to store bom task evidence 

### Usage

Example usage in a pipeline.
``` yaml
    - name: cra-cis-check
      taskRef:
        name: cra-cis-check
      runAfter:
        - cra-discovery-scan
      workspaces:
        - name: secrets
          workspace: artifacts
        - name: artifacts
          workspace: artifacts
      params:
        - name: ibmcloud-api
          value: $(params.ibmcloud-api)
        - name: repository
          value: $(params.repository)
        - name: revision
          value: $(params.branch)
        - name: pr-url
          value: $(params.pr-url)
        - name: commit-id
          value: $(params.commit-id)
        - name: continuous-delivery-context-secret
          value: "secure-properties"
        - name: ibmcloud-apikey-secret-key
          value: "apikey"
        - name: resource-group
          value: $(params.resource-group)
        - name: git-access-token
          value: ""
        - name: directory-name
          value: $(params.directory-name)
        - name: scm-type
          value: $(params.scm-type)
        - name: project-id
          value: $(params.project-id)    
        - name: pipeline-debug
          value: $(params.pipeline-debug)
```

## cra-vulnerability-remediation
This task finds out vulnerabilities for all application package dependencies, container base images and os packages.

### Inputs

#### Parameters

  - **ibmcloud-api**: (Default: `https://cloud.ibm.com`) The ibmcloud api url
  - **repository**: The full URL path to the repo with the deployment files to be scanned
  - **revision**: (Default: `master`) The branch to scan
  - **commit-id**: The commit id of change
  - **pr-url**: The pull request url
  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource
  - **ibmcloud-apikey-secret-key**: (Default: apikey) field in the secret that contains the api key used to login to ibmcloud
  - **resource-group**: (Default: `""`) target resource group (name or id) for the ibmcloud login operation
  - **git-access-token**: (Default: `""`) (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
  - **project-id**: (Default: `""`) Required id for GitLab repositories
  - **scm-type**: (Default: `github-ent`) Source code type used (github, github-ent, gitlab)
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug
  - **exclude-dev**: (Default: `false`) Specifies whether to exclude dev dependencies in scanning
  - **repo-dir**: (Default: `/artifacts`) Specifies the path to the repository or .cracveomit file

#### Implicit
The following inputs are coming from tekton annotation:
 - **PIPELINE_RUN_ID**: ID of the current pipeline run

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

### Results

- **status**: status of cra bom task, possible value are-success|failure
- **evidence-store**: filepath to store bom task evidence 

### Usage

Example usage in a pipeline.
``` yaml
    - name: cra-vulnerability-scan
      runAfter:
        - cra-discovery-scan
      taskRef:
        name: cra-vulnerability-remediation
      workspaces:
        - name: artifacts
          workspace: artifacts
        - name: secrets
          workspace: artifacts
      params:
        - name: ibmcloud-api
          value: $(params.ibmcloud-api)
        - name: repository
          value: $(params.repository)
        - name: revision
          value: $(params.branch)
        - name: pr-url
          value: $(params.pr-url)
        - name: commit-id
          value: $(params.commit-id)
        - name: continuous-delivery-context-secret
          value: "secure-properties"
        - name: ibmcloud-apikey-secret-key
          value: "apikey"
        - name: resource-group
          value: $(params.resource-group)
        - name: git-access-token
          value: ""
        - name: scm-type
          value: $(params.scm-type)
        - name: project-id
          value: $(params.project-id)    
        - name: pipeline-debug
          value: $(params.pipeline-debug)
        - name: exclude-dev
          value: $(params.exclude-dev)
        - name: repo-dir
          value: $(params.repo-dir)
```

## cra-comm-editor
This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.

### Inputs

#### Parameters

  - **repository**: The full URL path to the repo with the deployment files to be scanned
  - **pr-url**: (Default: `""`) The pull request url
  - **project-id**: (Default: `""`) Required id for GitLab repositories
  - **comment-fp**: The file path where the comments are stored
  - **scm-type**: Source code type used (github, github-ent, gitlab)

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

### Usage

Example usage in a pipeline.
``` yaml
    - name: cra-comm-editor
      taskRef:
        name: cra-comm-editor
      workspaces:
        - name: artifacts
          workspace: artifacts
      params:
        - name: repository
          value: $(params.repository)
        - name: pr-url
          value: $(params.pr-url)
        - name: project-id
          value: $(params.project-id)    
        - name: comment-fp
          value: $(params.comment-fp)
        - name: scm-type
          value: $(params.scm-type)
```

## cra-terraform-scan
This task scans ibm-terraform-provider files for compliance issues.

Currently supported compliance checks:

| SCC Goal ID | Alert | 
|---------|:----------|
| 3000001 | Ensure IBMid password policy requires at least one uppercase letter | 
| 3000002 | Ensure IBMid password policy requires at least one lowercase letter | 
| 3000003 | Ensure IBMid password policy requires at least one number | 
| 3000004 | Ensure IBMid password policy requires minimum length of 12 characters | 
| 3000005 | Ensure IBMid password policy prevents password reuse below the minimum of # | 
| 3000006 | Ensure IBMid password contains only printable ASCII characters (in the range 33 - 126) | 
| 3000007 | Ensure IBMid password password doesn't contain spaces or any of following characters: ;:(?)<>" | 
| 3000008 | Ensure the usage of a password meter that coaches users to create stronger passwords | 
| 3000009 | Ensure IAM roles are used to create IAM policies for IBM resources | 
| 3000010 | Ensure a support role has been assigned in IAM to manage cases in the IBM Cloud Support Center | 
| 3000011 | Ensure that IBM Cloud API keys are not created during the initial setup of IAM users | 
| 3000015 | Ensure IAM users are attached to access groups | 
| 3000016 | Ensure IAM policies for users are attached only to groups or roles | 
| 3000030 | Ensure IAM policies for service IDs are attached only to groups or roles | 
| 3000022 | Ensure Cloud Object Storage public access is disabled in IAM settings (not applicable to ACLs managed using S3 APIs) | 
| 3000028 | Ensure permissions for service ID creation are limited and configured in IAM settings | 
| 3000029 | Ensure IAM-enabled services have no more than # users with the IAM administrator role | 
| 3000031 | Check whether Identity and Access Management (IAM) is enabled with audit logging | 
| 3000032 | Ensure IAM-enabled services have no more than # service IDs with the IAM administrator role | 
| 3000033 | Ensure IAM-enabled services have at least # users with the IAM manager role | 
| 3000038 | Check whether account has no more than # service IDs with admin privileges | 
| 3000034 | Ensure IAM-enabled services have at least # service IDs with the IAM manager role | 
| 3000035 | Ensure account access is managed only by IAM access groups | 
| 3000101 | Ensure Cloud Object Storage is enabled with encryption | 
| 3000102 | Ensure Cloud Object Storage is enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000229 | Ensure Certificate Manager certificates that are generated by the service are renewed automatically before they expire | 
| 3000103 | Check whether Cloud Object Storage is accessible only through HTTPS | 
| 3000104 | Ensure Cloudant is accessible only through HTTPS | 
| 3000105 | Ensure Cloud Object Storage is accessible only through private endpoints | 
| 3000106 | Ensure Cloud Object Storage bucket access is restricted by using IAM and S3 access control | 
| 3000107 | Ensure Cloud Object Storage network access is restricted to a specific IP range | 
| 3000108 | Ensure Cloud Object Storage is enabled with customer-managed encryption and Keep Your Own Key (KYOK) | 
| 3000201 | Ensure Databases for MongoDB is enabled with encryption | 
| 3000202 | Ensure Databases for MongoDB is enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000203 | Ensure Databases for MongoDB is accessible only through HTTPS | 
| 3000204 | Ensure Databases for MongoDB is accessible only through private endpoints | 
| 3000206 | Ensure Databases for Redis is enabled with encryption | 
| 3000207 | Ensure Databases for Redis is enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000208 | Ensure Databases for Redis is accessible only through HTTPS | 
| 3000209 | Ensure Databases for Redis is accessible only through private endpoints | 
| 3000211 | Ensure Databases for Elasticsearch encryption is enabled | 
| 3000212 | Ensure Databases for Elasticsearch encryption is enabled with BYOK | 
| 3000213 | Ensure Databases for Elasticsearch is accessible only through HTTPS | 
| 3000214 | Ensure Databases for Elasticsearch is enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000216 | Ensure Databases for etcd is enabled with encryption | 
| 3000217 | Ensure Databases for etcd is enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000218 | Ensure Databases for etcd is accessible only through HTTPS | 
| 3000219 | Ensure Databases for etcd is accessible only through private endpoints | 
| 3000221 | Ensure Databases for PostgreSQL is enabled with encryption | 
| 3000222 | Ensure Databases for PostgreSQL is enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000223 | Ensure Databases for PostgreSQL is accessible only through HTTPS | 
| 3000224 | Ensure Databases for PostgreSQL is accessible only through private endpoints | 
| 3000205 | Ensure network access for MongoDB is restricted to specific IP range | 
| 3000210 | Ensure Databases for Redis network access is restricted to specific IP range | 
| 3000215 | Ensure Databases for Elasticsearch network access is restricted to a specific IP range | 
| 3000220 | Ensure Databases for etcd network access is restricted to a specific IP range | 
| 3000225 | Ensure Databases for PostgreSQL network access is restricted to a specific IP range | 
| 3000231 | Ensure Key Protect has high availability | 
| 3000232 | Ensure Kubernetes Service is configured with role-based access control (RBAC) | 
| 3000233 | Ensure Hyper Protect Crypto Services instance has at least # crypto units | 
| 3000234 | Ensure Hyper Protect Crypto Services instance is enabled with a dual authorization deletion policy | 
| 3000235 | Check whether Hyper Protect Crypto Services encryption keys that are generated by the service are rotated automatically at least every # months | 
| 3000242 | Ensure Databases for Redis has no more than # users with the IAM administrator role | 
| 3000243 | Ensure Databases for PostreSQL has no more than # users with the IAM administrator role | 
| 3000244 | Ensure Databases for MongoDB has no more than # users with the IAM administrator | 
| 3000245 | Ensure Databases for Elasticsearch has no more than # users with the IAM administrator role | 
| 3000109 | Ensure Databases for Cloudant has no more than # users with the IAM administrator role | 
| 3000247 | Ensure Key Protect has no more than # users with the IAM administrator role | 
| 3000246 | Ensure Databases for etcd has no more than # users with the IAM administrator role | 
| 3000248 | Ensure Kubernetes Service has no more than # users with the IAM administrator role | 
| 3000249 | Ensure Databases for EnterpriseDB has no more than # users with the IAM administrator role | 
| 3000251 | Ensure Databases for Elasticsearch has no more than # service IDs with the IAM administrator role | 
| 3000252 | Ensure Key Protect has no more than # service IDs with the IAM administrator role | 
| 3000253 | Ensure Databases for etcd has no more than # service IDs with the IAM administrator role | 
| 3000254 | Ensure Kubernetes Service has no more than # service IDs with the IAM administrator role | 
| 3000255 | Ensure Databases for EnterpriseDB has no more than # service IDs with the IAM administrator role | 
| 3000312 | Ensure Databases for MongoDB has no more than # service IDs with the IAM administrator role | 
| 3000313 | Ensure Databases for Redis has no more than # service IDs with the IAM administrator role | 
| 3000314 | Ensure Databases for PostgreSQL has no more than # service IDs with the IAM administrator role | 
| 3000110 | Ensure Cloudant has no more than # service IDs with the IAM administrator role | 
| 3000111 | Ensure Cloudant has at least # users with the IAM manager role | 
| 3000112 | Ensure Cloudant has at least # service IDs with the IAM manager role | 
| 3000256 | Ensure Databases for Redis has at least # users with the IAM manager role | 
| 3000257 | Ensure Databases for Redis has at least # service IDs with the IAM manager role | 
| 3000258 | Ensure Databases for PostreSQL has at least # users with the IAM manager role | 
| 3000259 | Ensure Databases for PostgreSQL has at least # service IDs with the IAM manager role | 
| 3000260 | Ensure Databases for MongoDB has at least # users with the IAM manager role | 
| 3000261 | Ensure Databases for MongoDB has at least # service IDs with the IAM manager role | 
| 3000262 | Ensure Databases for Elasticsearch has at least # users with the IAM manager role | 
| 3000263 | Ensure Databases for Elasticsearch has at least # service IDs with the IAM manager role | 
| 3000264 | Ensure Databases for etcd has at least # users with the IAM manager role | 
| 3000265 | Ensure Databases for etcd has at least # service IDs with the IAM manager role | 
| 3000266 | Ensure Key Protect has at least # users with the IAM manager role | 
| 3000267 | Ensure Key Protect has at least # service IDs with the IAM manager role | 
| 3000268 | Ensure Kubernetes Service has at least # users with the IAM manager role | 
| 3000269 | Ensure Kubernetes Service has at least # service IDs with the IAM manager role | 
| 3000270 | Ensure Databases for EnterpriseDB has at least # users with the IAM manager role | 
| 3000271 | Ensure Databases for EnterpriseDB has at least # service IDs with the IAM manager role | 
| 3000113 | Ensure Cloudant access is managed only by IAM access groups | 
| 3000272 | Ensure Databases for Redis access is managed only by IAM access groups | 
| 3000273 | Ensure Databases for PostgreSQL access is managed only by IAM access groups | 
| 3000274 | Ensure Databases for MongoDB access is managed only by IAM access groups | 
| 3000275 | Ensure Databases for Elasticsearch access is managed only by IAM access groups | 
| 3000276 | Ensure Databases for etcd access is managed only by IAM access groups | 
| 3000277 | Ensure Key Protect access is managed only by IAM access groups | 
| 3000278 | Ensure Kubernetes Service access is managed only by IAM access groups | 
| 3000279 | Ensure Databases for EnterpriseDB access is managed only by IAM access groups | 
| 3000114 | Ensure Cloud Object Storage buckets are enabled with IBM Activity Tracker | 
| 3000115 | Ensure Cloud Object Storage buckets are enabled with IBM Cloud Monitoring | 
| 3000116 | Ensure Cloud Object Storage bucket resiliency is set to cross region | 
| 3000301 | Ensure IBM Activity Tracker is provisioned in multiple regions in an account | 
| 3000302 | Ensure IBM Activity Tracker trails are integrated with LogDNA logs | 
| 3000303 | Ensure IBM Activity Tracker logs are encrypted at rest | 
| 3000304 | Ensure IBM Cloud Monitoring has no more than # users with the IAM administor role | 
| 3000308 | Ensure IBM Activity Tracker has no more than # users with the IAM administrator role | 
| 3000309 | Ensure IBM Activity Tracker has no more than # service IDs with the IAM administrator role | 
| 3000310 | Ensure IBM Cloud Monitoring has no more than # service IDs with the IAM administrator role | 
| 3000315 | Ensure IBM Cloud Monitoring has at least # users with the IAM manager role | 
| 3000316 | Ensure IBM Cloud Monitoring has at least # service IDs with the IAM manager role | 
| 3000317 | Ensure IBM Activity Tracker has at least # users with the IAM manager role | 
| 3000318 | Ensure IBM Activity Tracker has at least # service IDs with the IAM manager role | 
| 3000319 | Ensure IBM Cloud Monitoring access is managed only by IAM access groups | 
| 3000320 | Ensure IBM Activity Tracker access is managed only by IAM access groups | 
| 3000401 | Ensure Cloud Internet Services (CIS) has web application firewall enabled | 
| 3000402 | Ensure Cloud Internet Services (CIS) has DDoS protection enabled | 
| 3000403 | Ensure Cloud Internet Services (CIS) has TLS v1.2 set for all inbound traffic | 
| 3000404 | Ensure Virtual Private Cloud (VPC) security groups have no inbound rules that specify source IP 0.0.0.0/0 to SSH port 22 | 
| 3000405 | Ensure Virtual Private Cloud (VPC) security groups have no inbound rules that specify source IP 0.0.0.0/0 to RDP ports 3389 | 
| 3000406 | Ensure Virtual Private Cloud (VPC) has no rules in the default security group | 
| 3000408 | Ensure Flow Logs for VPC are enabled | 
| 3000410 | Ensure Virtual Private Cloud (VPC) security groups have no inbound ports open to the internet (0.0.0.0/0) | 
| 3000411 | Ensure Virtual Private Cloud (VPC) security groups have no outbound ports open to the internet (0.0.0.0/0) | 
| 3000412 | Ensure all virtual server instances have at least one Virtual Private Cloud (VPC) security group attached | 
| 3000413 | Ensure all network interfaces of a virtual server instance have at least one Virtual Private Cloud (VPC) security group attached | 
| 3000418 | Ensure account is configured with at least one VPN | 
| 3000419 | Ensure VPN for VPC has Internet Key Exchange (IKE) policy encryption that is not set to 'triple\_des' | 
| 3000420 | Ensure VPN for VPC has Internet Key Exchange (IKE) policy authentication that is set to 'sha256' | 
| 3000421 | Ensure VPN for VPC has a Diffie-Hellman group set to at least group # | 
| 3000422 | Ensure VPN for VPC has IPsec policy encryption that is not set to 'triple\_des' | 
| 3000423 | Ensure VPN for VPC has IPsec policy authentication that is set to 'sha256' | 
| 3000424 | Ensure VPN for VPC has an IPsec policy that does not have Perfect Forward Secrecy (PFS) disabled | 
| 3000425 | Ensure VPN for VPC authentication is configured with a strong pre-shared key with at least 24 alphanumeric characters | 
| 3000426 | Ensure VPN for VPC has a Dead Peer Detection policy that is set to 'restart' | 
| 3000404 | Ensure that application end-to-end traffic is encrypted | 
| 3000427 | Ensure Application Load Balancer for VPC has public access disabled | 
| 3000428 | Ensure Application Load Balancer for VPC is configured with multiple members in the pool | 
| 3000429 | Ensure Application Load Balancer for VPC listener is configured with default pool | 
| 3000430 | Ensure Application Load Balancer for VPC has health check configured when created | 
| 3000431 | Ensure Application Load Balancer for VPC has a health check protocol that is either HTTP or HTTPS | 
| 3000432 | Ensure Application Load Balancer for VPC pool uses the HTTPS protocol for HTTPS listeners | 
| 3000433 | Ensure Application Load Balancer for VPC is configured to convert HTTP client requests to HTTPS | 
| 3000434 | Ensure Application Load Balancer for VPC uses HTTPS (SSL & TLS) instead of HTTP | 
| 3000437 | Check whether Block Storage for VPC is enabled with customer-managed encryption and Keep Your Own Key (KYOK) | 
| 3000444 | Ensure Security Groups for VPC contains no outbound rules in security groups that specify source IP 8.8.8.8/32 to DNS port 53 | 
| 3000445 | Ensure Security Groups for VPC doesn't allow SSH for the default security group | 
| 3000446 | Ensure Security Groups for VPC doesn't allow PING for the default security group | 
| 3000447 | Ensure Virtual Private Cloud (VPC) classic access is disabled | 
| 3000449 | Ensure Virtual Private Cloud (VPC) has no public gateways attached | 
| 3000451 | Ensure Virtual Private Cloud (VPC) network access control lists don't allow ingress from 0.0.0.0/0 to any port | 
| 3000441 | Ensure Virtual Private Cloud (VPC) network access control lists don't allow ingress from 0.0.0.0/0 to port 22 | 
| 3000442 | Ensure Virtual Private Cloud (VPC) network access control lists don't allow ingress from 0.0.0.0/0 to port 3389 | 
| 3000452 | Ensure Virtual Private Cloud (VPC) network access control lists don't allow egress from 0.0.0.0/0 to any port | 
| 3000453 | Ensure Virtual Servers for VPC instance has the minimum # interfaces | 
| 3000454 | Ensure Virtual Servers for VPC instance doesn't have a floating IP | 
| 3000455 | Ensure Virtual Servers for VPC instance has all interfaces with IP-spoofing disabled | 
| 3000456 | Ensure Virtual Servers for VPC resource group other than Default is selected | 
| 3000457 | Ensure Virtual Servers for VPC boot volumes are enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000458 | Ensure Virtual Servers for VPC boot volumes are enabled with customer-managed encryption and Keep Your Own Key (KYOK) | 
| 3000459 | Ensure Virtual Servers for VPC data volumes are enabled with customer-managed encryption and Bring Your Own Key (BYOK) | 
| 3000460 | Ensure Virtual Servers for VPC data volumes are enabled with customer-managed encryption and Keep Your Own Key (KYOK) | 
| 3000461 | Ensure Virtual Servers for VPC is provisioned from an encrypted image | 
| 3000462 | Ensure Virtual Servers for VPC is provisioned from customer-defined list of images | 
| 3000463 | Ensure Virtual Servers for VPC instances are identifable by the workload they are running based on the Auto Scale for VPC instance group definition | 
| 3000464 | Ensure Application Load Balancer for VPC has application port of the workload that is identifiable by the Auto Scale for VPC instance group definition | 
| 3000467 | Ensure Virtual Private Cloud (VPC) has no subnet with public gateway attached | 
| 3000469 | Ensure Application Load Balancer for VPC is configured with at least one VPC security group | 
| 3000623 | Ensure Container Registry has no more than # users with the IAM administrator role | 
| 3000628 | Ensure Container Registry has no more than # service IDs with the IAM administrator role | 
| 3000635 | Ensure Container Registry has at least # users with the IAM manager role | 
| 3000636 | Ensure Container Registry has at least # service IDs with the IAM manager role | 
| 3000639 | Ensure Container Registry access is managed only by IAM access groups | 
| 3000706 | Ensure App ID user data is encrypted | 
| 3000305 | Ensure Event Streams is accessible through public endpoints | 
| 3000306 | Ensure Event Streams is accessible only through private endpoints | 
| 3000307 | Ensure Event Streams network access is restricted to a specific IP range | 

### Inputs

#### Parameters

  - **ibmcloud-api**: (Default: `https://cloud.ibm.com`) The ibmcloud api url
  - **repository**: The full URL path to the repo with the deployment files to be scanned
  - **revision**: (Default: `master`) The branch to scan
  - **tf-dir**: (Default `""`) The directory where the terraform main entry files are found.
  - **ibmcloud-apikey-secret-key**: (Default: apikey) field in the secret that contains the api key used to login to ibmcloud
  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource  
  - **directory-name**: The directory name where the repository is cloned
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug
  - **policy-config-json**: (Default `""`) Configure policies thresholds
  - **pr-url**: The pull request url
  - **commit-id**: The commit id of change
  - **project-id**: (Default: `""`) Required id for GitLab repositories
  - **scm-type**: (Default: `github-ent`) Source code type used (github, github-ent, gitlab)
  - **resource-group**: (Default: `""`) target resource group (name or id) for the ibmcloud login operation
  - **git-access-token**: (Default: `""`) (optional) token to access the git repository. If this token is provided, there will not be an attempt to use the git token obtained from the authorization flow when adding the git integration in the toolchain
  - **tf-var-file**: (Default: `""`) Comma seperated list of tf-var files to be passed to terraform




#### Implicit
The following inputs are coming from tekton annotation:
 - **PIPELINE_RUN_ID**: ID of the current pipeline run

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

### Results

- **status**: status of cra terraform scan task, possible value are-success|failure
- **evidence-store**: filepath to store terraform scan task evidence 

### Usage

Example usage in a pipeline.
``` yaml
    - name: cra-terraform-scan   
      taskRef:
        name: cra-terraform-scan
      workspaces:
        - name: artifacts
          workspace: artifacts
        - name: secrets
          workspace: artifacts
      params:
        - name: repository
          value:  $(tasks.extract-repository-url.results.extracted-value)
        - name: revision
          value: $(params.commit-id)
        - name: scm-type
          value: $(params.scm-type)
        - name: commit-id
          value: $(params.commit-id)
        - name: project-id
          value: $(params.project-id)
        - name: directory-name
          value: ""
        - name: pipeline-debug
          value: $(params.pipeline-debug)
        - name: tf-dir
          value: $(params.tf-dir)
        - name: policy-config-json
          value: $(params.policy-config-json)
        - name: pr-url
          value: $(params.pr-url)
        - name: tf-var-file
          value: $(params.tf-var-file)
```

### Configuring CRA Terraform scan
Read more about using [terraform scan profile](terraform-profile.md)
