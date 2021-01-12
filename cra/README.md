# Code Risk Analyzer

Tasks to scan your codebase using the Code Risk Analyzer scanners

#### Tasks

- [cra-discovery](#cra-discovery)
- [cra-bom](#cra-bom)
- [cra-cis-check](#cra-cis-check)
- [cra-vulnerability-remediation](#cra-vulnerability-remediation)
- [cra-comm-editor](#cra-comm-editor)



## cra-discovery

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

### Workspaces

- **artifacts**: The output volume to check out and store task scripts & data between tasks

#### Implicit / data from the pipeline

**Base image pulls secrets (optional)**

To provide pull credentials for the base image you use in your Dockerfile, for example for a UBI image from Red Hat registry, add these variables to your pipeline on he pipeline UI. The Task will look for them and if they are present, it will add an entry to the proper `config.json` for docker.

- **baseimage-auth-user** The username to the registry (Type: `text`)
- **baseimage-auth-password** The password to the registry (Type: `SECRET`)
- **baseimage-auth-host** The registry host name (Type: `text`)
- **baseimage-auth-email** An email address to the registry account (Type: `text`)

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
```

## cra-bom
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







