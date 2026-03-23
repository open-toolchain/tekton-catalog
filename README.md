# Open-Toolchain Tekton Catalog

Catalog of [Tekton Tasks](https://tekton.dev/docs/pipelines/tasks/#overview) usable in [Continuous Delivery Tekton Pipelines](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines)

**Notes**:
- These tasks are usable with Continuous Delivery Tekton Pipeline Worker Agent (Tekton definition with apiVersion: v1). These tasks have been updated  following migration path described in https://github.com/tektoncd/pipeline/blob/v0.11.2/docs/migrating-v1alpha1-to-v1.md
- If you want `v1alpha1` resources, you need to reference the [`tekton_pipeline0.10.1`](https://github.com/open-toolchain/tekton-catalog/releases/tag/tekton_pipeline0.10.1) tag (or
[`tekton_pipeline0.10.1_workspace`](https://github.com/open-toolchain/tekton-catalog/releases/tag/tekton_pipeline0.10.1_workspace) tag to have `v1alpha1` resources using workspaces).
- When moving from from tag `tekton_pipeline0.10.1`, `tekton_pipeline0.10.1` and/or branch `tkn_v1` to use `master`branch of this catalog, take a look at [breaking changes section](./README.md#breaking-changes)

# Tasks

## Cloud Foundry related tasks

- **[cf-deploy-app](./cloudfoundry/README.md#cf-deploy-app) [deprecated]**: This task allows to perform a deployment of a Cloud Foundry application using ibmcloud cf commands.

## IBM Cloud Container Registry related tasks

- **[icr-check-va-scan](./container-registry/README.md#icr-check-va-scan)**: This task verifies that a [Vulnerability Advisor scan](https://cloud.ibm.com/docs/services/Registry?topic=va-va_index) has been made for the image and processes the outcome of the scan.
- **[icr-containerize](./container-registry/README.md#icr-containerize)**: This task builds and pushes (optionaly) an image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started). This task relies on [Buildkit](https://github.com/moby/buildkit) to perform the build of the image.
- **[icr-cr-build](./container-registry/README.md#icr-cr-build) [deprecated]**: The [`ibmcloud cr build`](https://cloud.ibm.com/docs/container-registry-cli-plugin?topic=container-registry-cli-plugin-containerregcli#bx_cr_build) command is deprecated. If you use the [icr-cr-build](./container-registry/README.md#icr-cr-build) Tekton task, you can migrate to one of the three above Tekton tasks to build container images. For more information about this replacement, see the [IBM Cloud™ Container Registry is Deprecating Container Builds](https://www.ibm.com/cloud/blog/announcements/ibm-cloud-container-registry-deprecating-container-builds) blog post.
- **[icr-execute-in-dind-cluster](./container-registry/README.md#icr-execute-in-dind-cluster)**: This task runs `docker` commands (build, inspect...) against a Docker engine running in a Kubernetes cluster (a Docker DinD instance will be deployed if none is available on the build cluster), and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).
- **[icr-execute-in-dind](./container-registry/README.md#icr-execute-in-dind)**: This task runs `docker` commands (build, inspect...) against a Docker engine running as a sidecar container, and pushes the resulting image to the [IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).

## IBM Cloud Code Risk Analyzer scanners related tasks

- **[cra-bom](./cra/README.md#cra-bom) [deprecated]**: This task creates a Bill-of-Material (BoM) for a given repository that captures pedigree of all the dependencies and it is collected at different granularities.
- **[cra-cis-check](./cra/README.md#cra-cis-check) [deprecated]**: This tasks runs configuration checks on kubernetes deployment manifests.
- **[cra-comm-editor](./cra/README.md#cra-comm-editor) [deprecated]**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.
- **[cra-discovery](./cra/README.md#cra-discovery) [deprecated]**: This task accesses various source artifacts from the repository and performs deep discovery to identify all dependencies (including transitive dependencies).
- **[cra-terraform-scan-v2](./cra/README.md#cra-terraform-scan-v2) [deprecated]**: This task uses `ibmcloud cli` and the `cra` plugin to scan ibm-terraform-provider files for compliance issues.
- **[cra-terraform-scan](./cra/README.md#cra-terraform-scan) [deprecated]**: This task scans ibm-terraform-provider files for compliance issues. To configure CRA Terraform scan, Read more about using [terraform scan profile](./terraform-profile.md)
- **[cra-v2-cra](./cra/README.md#cra-v2-cra) [deprecated]**: This task accesses various source artifacts from a repository and performs deep discovery to identify all dependencies (including transitive dependencies). A Bill-of-Material (BoM) is generated that captures pedigree of all dependencies, collected at different granularities. The BoM is scanned to discover and report any known vulnerabilities in OS and Application pacakges. Finally, configuration checks on kubernetes deployment manifests are performed to uncover any issues.
- **[cra-vulnerability-remediation](./cra/README.md#cra-vulnerability-remediation) [deprecated]**: This task creates comments on Pull Requests and opens issues regarding bill of material and discovered vunerabilities.

## IBM Cloud Devops Insights related tasks

- **[doi-evaluate-gate](./devops-insights/README.md#doi-evaluate-gate) [deprecated]**: This task evaluates [DevOps Insights gate policy](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-evaluate-gates-cli)
- **[doi-publish-buildrecord](./devops-insights/README.md#doi-publish-buildrecord) [deprecated]**: This task publishes build record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-publish-deployrecord](./devops-insights/README.md#doi-publish-deployrecord) [deprecated]**: This task publishes deploy record to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-di_working)
- **[doi-publish-testrecord](./devops-insights/README.md#doi-publish-testrecord) [deprecated]**: This task publishes test record(s) to [DevOps Insights](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-publishing-test-data)

## Git related tasks

- **[git-clone-repo](./git/README.md#git-clone-repo)**: This Task fetches the credentials needed to perform git operations on a repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using) and then uses it to clone (and/or perform the appropriate checkout if pull request parameters are given) of the repository. The output of this task is the repository cloned into the directory on the workspace `workspace`.
- **[git-set-commit-status](./git/README.md#git-set-commit-status)**: This task is setting a git commit status for a given git commit (revision) in a git repository repository integrated in a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using).

## IBM Cloud Kubernetes Service related tasks

- **[iks-contextual-execution](./kubernetes-service/README.md#iks-contextual-execution)**: This task is executing bash snippet/script in the context of a Kubernetes cluster configuration.
- **[iks-deploy-to-kubernetes](./kubernetes-service/README.md#iks-deploy-to-kubernetes)**: This task allows to perform scripts typically doing deployment of a Kubernetes application with `ibmcloud ks` cli and `kubectl` cli configured for a given cluster.
- **[iks-fetch-config](./kubernetes-service/README.md#iks-fetch-config)**: This task is fetching the configuration of a [IBM Cloud Kubernetes Service cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) that is required to perform `kubectl` commands.

## Linter related tasks

- **[linter-docker-lint](./linter/README.md#linter-docker-lint)**: This task performs a lint on the given Dockerfile using [Hadolint](https://github.com/hadolint/hadolint)

## Slack related tasks

- **[slack-post-message](./slack/README.md#slack-post-message)**: This Task posts a message to the Slack channel(s) integrated with your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack). The task retrieves a Slack integration(s) from the Toolchain, filtered on the Slack domain (if passed as a parameter) and posts the message to the corresponding channel(s). The message can be: - passed as a parameter - a static Slack formatted JSON payload - a static text message (that will be converted to Slack JSON payload) - dynamically injected - by a bash script - based on the output of previous task(s) stored in the PVC - default message if not set ![Default value](./sample/default-message.png)

## SonarQube related tasks

- **[sonarqube-run-scan](./sonarqube/README.md#sonarqube-run-scan)**: This task starts a SonarQube scan for the code in a workspace using the SonarQube server integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/devsecops?topic=ContinuousDelivery-sonarqube) and upload the test results to DevOps Insights (optional)

## Tester related tasks

- **[tester-run-tests](./tester/README.md#tester-run-tests)**: This task allows to invoke a script to execute test

## Open-Toolchain related tasks

- **[toolchain-build](./toolchain/README.md#toolchain-build)**: This task perform build operation on the given workspace. Default build operations managed are maven build for instance.
- **[toolchain-extract-value](./toolchain/README.md#toolchain-extract-value)**: This task extracts values from the desired config map with a given jq expression.
- **[toolchain-publish-deployable-mapping](./toolchain/README.md#toolchain-publish-deployable-mapping)**: This task creates or updates a toolchain deployable mapping for a [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using). This task relies toolchain endpoints described in [IBM Toolchain API] (https://otc-swagger.us-south.devops.dev.cloud.ibm.com/swagger-ui?url=https://otc-api.us-south.devops.dev.cloud.ibm.com/spec/swagger.json#/toolchain_deployable_mappings).

# Breaking Changes

## when moving from tag "tekton_pipeline0.10.1"

- These tasks are using **kebab-case style for EVERY parameters names**. So parameter `pathToContext` (in previous versions of the tasks) has been renamed as `path-to-context`, parameter `clusterName` has been renamed to `cluster-name` and so on...
- `communication` folder has been renamed to `slack` folder
- Some tasks has been renamed to match the following name format `<category alias>-<task>` where category alias is depending on the folder containing the tasks:

  | Folder/Category | Category alias |
  |--------|----------------|
  | cloudfoundry | cf |
  | container-registry | icr |
  | devops-insights | doi |
  | git | git |
  | kubernetes-service | iks |
  | slack | slack |
  | toolchain | toolchain |

  The task new names are listed in the following table:

  | Folder | Old task name | New task name |
  |--------|---------------|---------------|
  | container-registry | containerize-task | icr-containerize |
  | container-registry | cr-build-task | icr-cr-build |
  | container-registry | execute-in-dind-task | icr-execute-in-dind |
  | container-registry | execute-in-dind-cluster-task | icr-execute-in-dind-cluster |
  | container-registry | vulnerability-advisor-task | icr-check-va-scan |
  | git | clone-repo-task | git-clone-repo |
  | git | set-commit-status | git-set-commit-status |
  | kubernetes-service | fetch-iks-cluster-config | iks-fetch-config |
  | kubernetes-service | kubernetes-contextual-execution | iks-contextual-execution |
  | slack | post-slack | slack-post-message |

- Tasks that use workspace(s) may have changed the expected workspace name. Here is the list of the breaking changes for the expected workspace name

  | Folder | Task | Old workspace name | New workspace name | Description |
  | -- | -- | -- | -- | -- |
  | container-registry | icr-containerize | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-cr-build | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-execute-in-dind | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-execute-in-dind-cluster | workspace | source | A workspace containing the source (Dockerfile, Docker context) to create the image |
  | container-registry | icr-check-va-scan | workspace | artifacts | Workspace that may contain image information and will have the va report from the VA scan after this task exection |
  | git | git-clone-repo | workspace | output | Workspace where the git repository will be cloned into |
  | git | git-set-commit-status | workspace | artifacts | Workspace that may contain git repository information (ie build.properties). Should be marked as optional when Tekton will permit it |
  | kubernetes-service | iks-fetch-config | workspace | cluster-configuration | A workspace where the kubernetes cluster config is exported |
  | kubernetes-service | iks-contextual-execution | workspace | cluster-configuration | A workspace that contain the kubectl cluster config to be used |

## when moving from tag "tekton_pipeline0.10.1" and/or branch "tkn_v1"

- Tasks that are expecting a secret to retrieve apikey and/or secret values have been updated to use the default secret `secure-properties` injected by Continuous Delivery Tekton Pipeline support. The updated tasks are:
  - icr-check-va-scan
  - icr-containerize
  - icr-cr-build
  - icr-execute-in-dind
  - icr-execute-in-dind-cluster
  - git-clone-repo
  - git-set-commit-status
  - iks-fetch-config

  Note: As a reminder, in previous version (before `secure-properties` injection by CD tekton support), the default was set to `cd-secret`

# Criteria for Code Submission
To ensure code quality, protected branches will be enabled soon, and every PR that is to be merged to master will run CI tasks for code quality. These could (and should) be set up for local development environments as well.

Code quality checks currently enabled:
- yaml lint - using yamllint-rules.yaml as configuration file: `yamllint --config-file yamllint-rules.yaml .`
- tekton task lint: `tekton-lint '**/*.yaml'`
- Tasks definition validation: [check_tasks.sh](./.ci/check_tasks.sh)
