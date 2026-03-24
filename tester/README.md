# Tester related tasks

## Available Tasks
- **[tester-run-tests](#tester-run-tests)**: This task allows to invoke a script to execute test

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `tester`

## Details
### tester-run-tests

This task allows to invoke a script to execute test

#### Parameters

* **pipeline-secret**: Name of the secret containing the continuous delivery pipeline context secrets. Note: the `secure-properties` secret is injected in the Tekton Pipeline environment by Continuous Delivery Tekton Pipeline support. See [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment#tekton_envprop) (default to `secure-properties`)
* **pipeline-configmap**: name of the configmap containing values for the task (default to `environment-properties`)
* **tests-image**: Container image to be used for _tests_ script execution. (default to `icr.io/continuous-delivery/pipeline/pipeline-base-ubi:3.79`)
* **shuttle-properties-file**: file containing properties
* **tests-script**: _tests_ script to be executed
* **fail-on-test-errors**: flag ("true" | "false") to indicate if the task should be marked as fail or successfull if _tests_ script is failing with exit not equal to 0. (default to `true`)
* **pipeline-debug**: Pipeline debug mode (default to `0`)

#### Workspaces

* **artifacts**: A workspace backing by a volume

#### Results
* **tests-exit-code**: The exit-code of the tests script
* **test-result-file-paths**: semi-colon list of test result output file paths
* **test-types**: semi-colon separated list of of test types. Order should match file output paths in test-result-file-paths
