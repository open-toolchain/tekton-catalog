This `sample` sub-directory contains an EventListener and Pipeline definition that you can include in your Tekton pipeline configuration to run an example of the `slack-post-message` task.

1) Create or update a Toolchain so it includes:
   - a Slack integration
   - the repository containing this tekton task
   - a Tekton pipeline definition

   ![Toolchain overview](./sample-toolchain-overview.png)

2) Add the definitions of this task and the sample (`slack` and `slack/sample` paths)

   ![Tekton pipeline definitions](./sample-tekton-pipeline-definitions.png)

3) Add the environment properties as needed:

   - `domain` (optional) the Slack domain to send the message to.
   - `channel` (optional) the channel to post to (overrides the dafault channel as set in the Slack webhook).
   - `message-format` (optional) the format of the message (text or JSON).
   - `message-script` (optional) Shell script that provides messsage content.
   - `message` (optional) the message to post to Slack.

**Note:** when using JSON format, the message is posted as-is to Slack.

   ![Tekton pipeline environment properties](./sample-tekton-pipeline-environment-properties.png)


4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline

6) The message is posted to Slack

   ![sample message](./sample-message.png)

7) Optional: check the execution log

   ![Tekton pipeline sample trigger](./sample-log.png)

8) Optional: Create a message using snippet

   a) Define the snippet in the `message-script` environment property of the pipeline

       message-script: `echo 'Message sent from PipelineRun' ${PIPELINE_RUN_NAME}; echo 'uid:' ${PIPELINE_RUN_ID}; echo 'buildNumber:' ${BUILD_NUMBER};`

      Note: this could also be done in the trigger-template or pipeline definition

      ![Tekton pipeline sample trigger](./sample-snippet-environment-property.png)


   b) After running the pipeline, a new message like the following should have been posted to the Slack channel

      ![sample message using snippet](./sample-snippet-message.png)

   c) Check the execution log

      ![Tekton pipeline sample snippet message](./sample-snippet-log.png)
