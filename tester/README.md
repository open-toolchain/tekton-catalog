# Tester related tasks

# Tasks

- **[tester-run-tests](#tester-run-tests)**: This task allows to invoke a script to execute test

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `tester`

## tester-run-tests

This task allows to invoke a script to execute tests

### Parameters

* **pipeline-secret**: (optional) name of the kubernetes secret containing secured values to be available for the tests (default to `secure-properties`)
* **pipeline-configmap**: (optional) name of the kubernetes configmap containing values to be available for the tests (default to `environment-properties`)
* **tests-image**: (optional) Container image to be used for tests script execution. Default to "icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.9"
* **shuttle-properties-file**: (optional) name of the properties file that contain properties to include in the environment for the `tests-script` execution.
* **tests-script**: (optional) _tests_ script to be executed
* **fail-on-test-errors**: flag (`"true"` | `"false"`) to indicate if the task should be marked as fail or successfull if _tests_ script is failing with exit not equal to 0. Default to "true"
* **pipeline-debug**: (optional) turn on task script context debugging

### Workspaces

* **artifacts**: A workspace containing artifacts/elements

### Results

* **tests-exit-code**: The exit-code of the tests script
