# Code Risk Analyzer

Tasks to scan your codebase using the Code Risk Analyzer scanners

## Tasks

- **[cra](#cra)**: This task accesses various source artifacts from a repository and performs deep discovery to identify all dependencies (including transitive dependencies). A Bill-of-Material (BoM) is generated that captures pedigree of all dependencies, collected at different granularities. The BoM is scanned to discover and report any known vulnerabilities in OS and Application pacakges. Finally, configuration checks on kubernetes deployment manifests are performed to uncover any issues.

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `cra-v2`

## Usages

- The `sample` sub-directory contains a listener to configure on Pull Request (or Merge Request for Gitlab/GRIT) EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the CRA tasks.

  See the documentation [here](./sample/README.md)


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

  - **continuous-delivery-context-secret**: (Default: `secure-properties`) Reference name for the secret resource
  - **ibmcloud-apikey-secret-key**: (Default: `apikey`) field in the secret that contains the api key used to login to ibmcloud
  - **repository**: The full URL path to the repo with the deployment files to be scanned
  - **branch**: (Default: `master`) The branch to scan
  - **revision**: The git revision/commit for the git repo
  - **pipeline-debug**: (Default: `0`) 1 = enable debug, 0 no debug
  - **ibmcloud-api**: (Default: `https://cloud.ibm.com`) The ibmcloud api url
  - **ibmcloud-region**: (Optional) The ibmcloud target region
  - **pr-repository**: The forked git repo from where the PR is made
  - **pr-branch**: The branch in the forked git repo from where the PR is made
  - **registry-region**: (Optional) The ibmcloud container registry region
  - **resource-group**: (Optional) Target resource group (name or id) for the ibmcloud login operation
  - **custom-script**: (Optional) A custom script to be ran prior to CRA scanning
  - **env-props**: (Optional) A custom configuration of environment properties to source before execution, ex. 'export ABC=123 export DEF=456'
  - **fileignore**: (Optional) Filepath to .fileignore
  - **output**: (Default: `false`) Prints command result to console
  - **path**: (Default: `/artifacts`) Directory where the repository is cloned
  - **strict**: (Optional) Enables strict mode for scanning
  - **toolchainid**: The ibmcloud target toolchain to be used
  - **verbose**: (Optional) Enable verbose log messages
  - **asset-type**: (Default: `all`) Security checks to run (apps, image, os, all)
  - **bom-report**: (Default: `bom.json`) Filepath to store generated Bill of Materials
  - **docker-build-flags**: (Optional) Customize docker build command for build stage scanning
  - **gradle-exclude-configs**: (Optional) Exclude gradle configurations, ex. 'runtimeClasspath,testCompileClasspath'
  - **maven-exclude-scopes**: (Optional) Exclude maven scopes, ex. 'test,compile'
  - **nodejs-create-package-lock**: (Default: `false`) Enable the task to build the package-lock.json for node.js projects
  - **prev-report**: (Optional) Filepath to previous BoM report to skip Dockerfile or application manifest scans
  - **deploy-report**: (Default: `deploy.json`) Filepath to store generated Deploy Analytic report
  - **cveignore**: (Optional) File path to cveignore
  - **exclude-dev**: (Default: `false`) Exclude dev dependencies during vulnerability scan
  - **vulnerability-report**: (Default: `vulnerability.json`) Filename to store generated Vulnerability report
  - *cra-scan-image***: (Default: `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.2`) Image to use for `scan` task

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
        - name: pipeline-debug
          value: $(params.pipeline-debug)
        - name: ibmcloud-api
          value: $(params.ibmcloud-api)
        - name: ibmcloud-region
          value: $(params.ibmcloud-region)
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
        - name: prev-report
          value: $(params.prev-report)
        - name: docker-build-flags
          value: $(params.docker-build-flags)
        - name: gradle-exclude-configs
          value: $(params.gradle-exclude-configs)
        - name: maven-exclude-scopes
          value: $(params.maven-exclude-scopes)
        - name: nodejs-create-package-lock
          value: $(params.nodejs-create-package-lock)
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
