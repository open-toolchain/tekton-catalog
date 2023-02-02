# Post to Slack task helper
This Task posts a message to the Slack channel(s) integrated with your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack).

The task retrieves a Slack integration(s) from the Toolchain,
filtered on the Slack domain (if passed as a parameter) and posts the message to the corresponding channel(s).

The message can be:
- passed as a parameter
   - a static Slack formatted JSON payload
   - a static text message (that will be converted to Slack JSON payload)
- dynamically injected
   - by a bash script
   - based on the output of previous task(s) stored in the PVC
- default message if not set

    ![Default value](./sample/default-message.png)

## Prerequisites
### Slack
Create a [Slack Webhook](https://api.slack.com/messaging/webhooks).
### Toolchain
Add a [Slack integration](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-integrations#slack) to your [Continuous Delivery toolchain](https://cloud.ibm.com/docs/services/ContinuousDelivery?topic=ContinuousDelivery-toolchains-using)

## Install the Task
- Add a github integration in your Toolchain to the repository containing the task (https://github.com/open-toolchain/tekton-catalog)
- Add that github integration to the Definitions tab of your Continuous Delivery Tekton pipeline, with the Path set to `slack`.

## Usage

The `sample` sub-directory contains an EventListener and Pipeline definition that you can include in your Tekton pipeline configuration to run an example of the `slack-post-message` task.

  See the documentation [here](./sample/README.md)

## slack-post-message

### Parameters

* **domain**: (optional) the Slack domain to send the message to. If not set, the message will be posted to the Slack integration(s) as defined in the Toolchain.
* **channel**: (optional) the Slack channel to send the message to. When set, overrides the default channel as set in the Slack Webhook URL. Only non-private channel can override the default channel. If the target channel is a private channel, the Slack Webhook URL in the Slack toolchain integration card needs to be updated.
* **message-format**: (optional) the format of the message. Value: text(default) or JSON.
* **message-script**: (optional) Shell script that provides messsage content.
* **message**: (optional) the message to send to Slack.
* **exit-on-error**: flag (`true` | `false`) to indicate if the task should fail or continue if unable to process the message or post to Slack (default `false`).
* **post-to-slack-step-image**: (optional) image to use for the post-to-slack step. Default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.11`

## Workspaces

* **workspace**: A workspace that contain data useful for the script/slack message resolution. Should be marked as optional when Tekton will permit it.

## Outputs
None.

## Usage
