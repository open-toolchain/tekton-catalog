# Code Risk Analyzer

Tasks to scan your codebase using the Code Risk Analyzer scanners

## Tasks

- **[cra-discovery](#cra-discovery)**: This task accesses various source artifacts from the repository and performs deep discovery to identify all dependencies (including transitive dependencies).
- **[cra-bom](#cra-bom)**: This task creates a Bill-of-Material (BoM) for a given repository that captures pedigree of all the dependencies and it is collected at different granularities.
- **[cra-cis-check](#cra-cis-check)**: This tasks runs configuration checks on kubernetes deployment manifests.
- **[cra-vulnerability-remediation](#cra-vulnerability-remediation)**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.
- **[cra-comm-editor](#cra-comm-editor)**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.
- **[cra-terraform-scan](#cra-terraform-scan)**: This task scans ibm-terraform-provider files for compliance issues.

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `cra`

## Usages

- The `sample` sub-directory contains a listener to configure on Pull Request (or Merge Request for Gitlab/GRIT) EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the CRA tasks.

  See the documentation [here](./sample/README.md)

- The `sample-cra-ci` sub-directory contains a listener to configure on commit pushed EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the CRA tasks.

  See the documentation [here](./sample-cra-ci/README.md)


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
  - **exclude-scopes**: (Default: `""`) Specifies which scopes to exclude dependencies in scanning. Example: `test,compile`

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
        - name: exclude-scopes
          value: $(params.exclude-scopes)
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
|ID | Rule | 
|---------|---------|
|1| Ensure IAM does not allow too  many admins per account
|2| Ensure https for all inbound traffic via VPC LBaaS
|3| Ensure no VPC security groups allow incoming traffic from 0.0.0.0/0 to port 22 (ssh)
|4| Ensure no security groups have ports open to internet(0.0.0.0/0)
|5| Ensure VPC flowlogs logging is enabled in all VPCs
|6| Ensure no VPC security groups allow incoming traffic  from 0.0.0.0/0 to port RDP
|7| Ensure that COS Storage Encryption is set to On
|8| Ensure COS bucket is linked to LogDNA
|9| Ensure network access for COS is restricted to specific IP range
|10| Ensure certificates are automatically renewed before expiration. (This lifecycle applies to Certificate Manager generated certificates only)
|11| Ensure that Database for ElasticSearch Encryption is set to On
|12| Ensure that Database for ETCD Encryption is set to On
|13| Ensure that Database for MongoDB Encryption is set to On
|14| Ensure that Database for Radis Encryption is set to On
|15| Ensure that Database for PostgreSQL Encryption is set to On
|16| Ensure that Database for RabittMQ Encryption is set to On
|17| Ensure that Web application firewall is set to On in CIS
|18| Ensure ActivityTracker is provisioned
|19| Ensure Activity Tracker is provisioned in multiple regions for that account
|20| Ensure no all-resource IAM service policy
|21| Ensure IAM service policy is restricted using resource groups
|22| Ensure CIS is provisioned
|23| Ensure DDOS protection is set to On in CIS
|24| Ensure IAM does not authorize CIS to read from COS
|25| Ensure SSL is configured properly (using full/strict/origin_pull only)
|26| Ensure TLS 1.2 for all inbound traffic via CIS
|27| Ensure DNS record is protected
|28| Ensure IAM does not allow too many account managers per account
|29| Ensure IAM does not allow too many IAM admins per account
|30| Ensure IAM does not allow too many all resource managers per account
|31| Ensure IAM does not allow too many all resource readers per account
|32| Ensure IAM does not allow too many KMS managers per account
|33| Ensure IAM does not allow too many COS managers per account
|34| Ensure IAM users are attached to access groups
|35| Ensure CIS load balancer is provisioned
|36| Ensure CIS load balancer is  properly configured
|37| Ensure VPC has atleast one security group attached
|38| Ensure that Databases for ElasticSearch encryption is enabled with BYOK
|39| Ensure that Databases for MongoDB encryption is enabled with BYOK
|40| Ensure that Databases for PostgreSQL encryption is enabled with BYOK
|41| Ensure that Databases for RabbitMQ encryption is enabled with BYOK
|42| Ensure that Databases for ETCD encryption is enabled with BYOK
|43| Ensure that Databases for Redis encryption is enabled with BYOK
|44| Ensure that network access is set for ElasticSearch to be exposed on Private end Points only
|45| Ensure that network access is set for MongoDB to be exposed on Private end Points only
|46| Ensure that network access is set for PostgreSQL to be exposed on Private end Points only
|47| Ensure that network access is set for RabbitMQ to be exposed on Private end Points only
|48| Ensure that network access is set for ETCD to be exposed on Private end Points only
|49| Ensure that network access is set for Redis to be exposed on Private end Points only
|50| Ensure network access for Redis is restricted to specific IP range
|51| Ensure network access for ETCD is restricted to specific IP range
|52| Ensure network access for RabitMQ is restricted to specific IP range
|53| Ensure network access for PostgreSQL is restricted to specific IP range
|54| Ensure network access for MongoDB is restricted to specific IP range
|55| Ensure network access for ElasticSearch is restricted to specific IP range
|56| Ensure that COS Storage Encryption is set to On with BYOK
|57| Ensure that Database for ETCD Encryption is set to On


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
