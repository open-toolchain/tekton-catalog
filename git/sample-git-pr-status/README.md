## Git Pull Request event trigger with set PR/MR commit status ##

This `sample-git-pr-status` sub-directory contains several EventListener definitions that you can include in your CD tekton pipeline configuration to run an example demonstrating the usage of the `git-set-commit-status` in the context of a CD Tekton pipeline triggered by a Git Pull Request event (PullRequest push/update).

This sample illustrates the PullRequest support provided by the `git-clone-repo` that results in a Git repository content that would be identical to the one obtained after a merge action on the given PullRequest (or Merge Request for a Gitlab or GRIT server).

It is also showcase the `git-set-commit-status`to create/update Pull Request status check (i.e. set commit status on the last commit of the Pull Request).
The status being sucess or failing according to the commit message (it the commit message contains `fail` then the status is `failed` otherwise it is `success`)

1) Create or update a Toolchain to include:

   - the github.com repository that you want to clone
   - (optional) the GRIT repository that you want to clone
   - (optional) the BitBucket repository that you want to clone
   - the repository containing this Tekton task
   - a Tekton pipeline definition

   ![Toolchain overview](./images/sample-git-pr-status-toolchain-overview.png)

2) Add the definitions of this task and the sample (`git` and `git/sample-git-pr-status` paths)

   ![Tekton pipeline definitions](./images/sample-git-pr-status-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `apikey`: the API key used for the ibmcloud login/access

   ![Tekton pipeline environment properties](./images/sample-git-pr-status-tekton-pipeline-environment-properties.png)

4) Create Git Triggers for the different Git repositories that you have integrated to your Toolchain (corresponding to the repositories integrated to your Toolchain).

   Github:
    - `eventlistener-git-pr-status-github-pr` for Github PullRequest opened/updated event

      ![Tekton pipeline sample-git-trigger Github PullRequest](./images/sample-git-pr-status-github-pullrequest-trigger-configuration.png)

   GRIT/Gitlab:
    - `eventlistener-git-pr-status-grit-mr` for GRIT/Gitlab MergeRequest opened/updated event

   BitBucket:
    - `eventlistener-git-pr-status-bitbucket-pr` for BitBucket PullRequest opened/updated event

5) **Trigger on PullRequest**: in one of your repository that has the above triggers defined, define a new Git branch, push some code changes and create a new PullRequest to the default `master` branch.

   ![Tekton pipeline github new-branch commit](./images/github-sample-new-branch-commit.png)

   ![Tekton pipeline github pullrequest new-branch](./images/github-pull-request-overview.png)

   Observe: a new pipeline run is automatically started, triggered by this PullRequest.

   ![Tekton pipeline sample-git-trigger run on pr event](./images/sample-git-pr-status-github-pr-event-run.png)

   Notes:
   - The `clone-task` execution will produce the same repository content as the "Merge Pull Request" action/button would.
   - The `set-git-commit-status` task execution will use the `inspect-git-commit-message` pipelinerun task execution status to update the PullRequest commit status

   ![Tekton pipeline github pull request run view](./images/sample-git-pr-status-github-pr-event-run-view.png)

   The Pull Request status check is updated as the last commit has a commit status

   ![github pull request status check](./images/sample-git-pr-status-github-pr-status-check.png)

   Note: in case of a commit message containing `fail` the task will result in a failure and the `finally` clause in the pipeline definition will still execute the `set-git-commit-status` task with the appropriate state

   ![Tekton pipeline github pull request run view](./images/sample-git-pr-status-github-pr-event-run-view-failure.png)

   The Pull Request status check is updated to failure corresponding to the last commit status

   ![github pull request status check](./images/sample-git-pr-status-github-pr-status-check-failure.png)

## Detailed Description

This pipeline and relevant trigger(s) can be configured using the properties described below.

See https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines&interface=ui#configure_tekton_pipeline for more information.

### eventlistener-git-pr-status-github-pr

**EventListener**: eventlistener-git-pr-status-github-pr


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` (**secured property**) | the api key used to login to ibmcloud | - | Yes | secret |
| `branch` | the branch for the git repo | `$(event.pull_request.base.ref)` | No | string |
| `context` | - | `commit message check` | No | string |
| `description` | - | `verify the commit message` | No | string |
| `git-access-token` | the token to access the git repository for the clone operations | - | Yes | string |
| `git-credentials-json-file` | - | `output/secrets/thecredentials.json` | No | string |
| `pipeline-debug` | Pipeline debug mode. Value can be 0 or 1. Default to 0 | `0` | No | string |
| `pr-branch` | The source branch for the PullRequest | `$(event.pull_request.head.ref)` | No | string |
| `pr-repository` | The source git repo for the PullRequest | `$(event.pull_request.head.repo.clone_url)` | No | string |
| `pr-revision` | the commit id/sha for the PullRequest | `$(event.pull_request.head.sha)` | No | string |
| `properties-file` | - | `output/thebuild.properties` | No | string |
| `repository` | the git repo | `$(event.pull_request.base.repo.clone_url)` | No | string |
| `triggerName` | name of the trigger | `github-pullrequest` | No | string |


### eventlistener-git-pr-status-grit-mr

**EventListener**: eventlistener-git-pr-status-grit-mr


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` (**secured property**) | the api key used to login to ibmcloud | - | Yes | secret |
| `branch` | the branch for the git repo | `$(event.object_attributes.target_branch)` | No | string |
| `context` | - | `commit message check` | No | string |
| `description` | - | `verify the commit message` | No | string |
| `git-access-token` | the token to access the git repository for the clone operations | - | Yes | string |
| `git-credentials-json-file` | - | `output/secrets/thecredentials.json` | No | string |
| `pipeline-debug` | Pipeline debug mode. Value can be 0 or 1. Default to 0 | `0` | No | string |
| `pr-branch` | The source branch for the PullRequest | `$(event.object_attributes.source_branch)` | No | string |
| `pr-repository` | The source git repo for the PullRequest | `$(event.object_attributes.source.git_http_url)` | No | string |
| `pr-revision` | the commit id/sha for the PullRequest | `$(event.object_attributes.last_commit.id)` | No | string |
| `properties-file` | - | `output/thebuild.properties` | No | string |
| `repository` | the git repo | `$(event.object_attributes.target.git_http_url)` | No | string |
| `triggerName` | name of the trigger | `grit-mergerequest` | No | string |


### eventlistener-git-pr-status-bitbucket-pr

**EventListener**: eventlistener-git-pr-status-bitbucket-pr


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` (**secured property**) | the api key used to login to ibmcloud | - | Yes | secret |
| `branch` | the branch for the git repo | `$(event.pullrequest.destination.branch.name)` | No | string |
| `context` | - | `commit message check` | No | string |
| `description` | - | `verify the commit message` | No | string |
| `git-access-token` | the token to access the git repository for the clone operations | - | Yes | string |
| `git-credentials-json-file` | - | `output/secrets/thecredentials.json` | No | string |
| `pipeline-debug` | Pipeline debug mode. Value can be 0 or 1. Default to 0 | `0` | No | string |
| `pr-branch` | The source branch for the PullRequest | `$(event.pullrequest.source.branch.name)` | No | string |
| `pr-repository` | The source git repo for the PullRequest | `$(event.pullrequest.source.repository.links.html.href)` | No | string |
| `pr-revision` | the commit id/sha for the PullRequest | `$(event.pullrequest.source.commit.hash)` | No | string |
| `properties-file` | - | `output/thebuild.properties` | No | string |
| `repository` | the git repo | `$(event.pullrequest.destination.repository.links.html.href)` | No | string |
| `triggerName` | name of the trigger | `bitbucket-pullrequest` | No | string |
