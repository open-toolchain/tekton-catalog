# Post to Slack task helper
This Task sends a message to the Slack channel(s) integrated to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack).

The task retrieves the Slack integration(s) as set in your Toolchain,
filtered on the Slack domain (if passed as parameter) and post the message to the corresponding channel(s).

The message, passed as a parameter, can be:
- a Slack formatted JSON payload,
- a text message (that will be converted to Slack JSON payload)
- dynamically injected by a bash script
- default message if not set

## Prereq
### Slack
Create a [Slack Webhook](https://api.slack.com/messaging/webhooks).
### Toolchain
Add a [Slack integration](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack) to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using)
## Install the Task
- Add a github integration in your toolchain to the repository containing the task (https://github.com/open-toolchain/tekton-catalog)
- Add that github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `communication`.

## Inputs
None.
### Parameters

* **task-pvc**: the output pvc.
* **domain**: (optional) the Slack domain to send the message to. If not set, the message will be posted to the Slack integration(s) as defined in the Toolchain.
* **channel**: (optional) the Slack channel to send the message to. When set, overrides the default channel as set in the Slack Webhook URL.
* **messageFormat**: (optional) the format of the message. Value: text(default) or JSON.
* **messageScript**: (optional) Shell script that provides messsage content.
* **message**: (optional) the message to send to Slack.
* **exitOnError**: flag (`true` | `false`) to indicate if the task should fail or continue if unable to process the message or post to Slack (default `false`).

![Default value](./sample/default-message.png)


## Output
None.

## Usage
The `sample` sub-directory contains an EventListener definition that you can include in your Tekton pipeline configuration to run an example of the `task-post-slack`

1) Create or update a toolchain so it includes:
   - a Slack integration
   - the repository containing this tekton task
   - a Tekton pipeline definition

   ![Toolchain overview](./sample/sample-toolchain-overview.png)

2) Add the definitions of this task and the sample (`communication` and `communication/sample` paths)

   ![Tekton pipeline definitions](./sample/sample-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `domain` the Slack domain to send the message to.
   - `channel` (optional) the channel to post to (overrides the dafault channel as set in the Slack webhook).
   - `messageFormat` (optional) the format of the message (text or JSON).
   - `message` (optional) the message to post to Slack.

   ![Tekton pipeline environment properties](./sample/sample-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./sample/sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline

6) The message is posted to Slack

   ![sample message](./sample/sample-message.png)

7) Optional: check the execution log

   ![Tekton pipeline sample trigger](./sample/sample-log.png)