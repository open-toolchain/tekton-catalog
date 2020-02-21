## Git event trigger with clone task sample usage ##

This `sample-git-trigger` sub-directory contains several EventListener definitions that you can include in your CD tekton pipeline configuration to run an example showing usage of the `clone-repo-task` in the context of CD tekton pipeline triggered by git event (Commit push or PullRequest push/update)

This sample illustrates the PullRequest support provided by the `git-clone-task` to obtain git repository content that would be the same as what you would obtain after a merge action on the given PullRequest (or Merge Request for a Gitlab or GRIT server)

1) Create a toolchain (or update a toolchain) to include:

   - a github.com repository that you want to clone
   - (optional) a GRIT repository that you want to clone
   - (optional) a BitBucket repository that you want to clone
   - the repository containing this tekton task
   - a tekton pipeline definition

   ![Toolchain overview](./sample-git-trigger-toolchain-overview.png)

2) Add the definitions of this task and the sample (`git` and `git/sample-git-trigger` paths)

   ![Tekton pipeline definitions](./sample-git-trigger-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `apikey` to provide an API key used for the ibmcloud login/access
   - `repositoryForManualTrigger` to indicate the git repository url to clone (correspoding to the one integrated in the toolchain) when using the ManualTrigger

   ![Tekton pipeline environment properties](./sample-git-trigger-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to manually start the `event-listener-pr-processing-manual` listener

   ![Tekton pipeline sample-git-trigger trigger](./sample-git-trigger-tekton-pipeline-manual-trigger.png)

5) Run the pipeline by starting the Manual Trigger 

   ![Tekton pipeline sample-git-trigger manual run](./sample-git-trigger-tekton-pipeline-manual-trigger-start.png)

   ![Tekton pipeline sample-git-trigger manual run done](./sample-git-trigger-tekton-pipeline-manual-trigger-done.png)

6) Check the logs of the pipeline run execution

   ![Tekton pipeline sample-git-trigger manual run view](./sample-git-trigger-tekton-pipeline-run-manual-trigger-view.png)

