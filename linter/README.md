# Linter related tasks

- **[linter-docker-lint](#linter-docker-lint)**: This task performs a lint on the given Dockerfile using [Hadolint](https://hub.docker.com/r/hadolint/hadolint)

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `linter`

## linter-docker-lint
This task performs a lint on the given Dockerfile using [Hadolint](https://github.com/hadolint/hadolint)

### Parameters

* **path-to-dockerfile**: (optional) The path to the Dockerfile that is used for the build (default to `.` meaning current directory)
* **dockerfile**: (optional) The name of the Dockerfile. Default to `Dockerfile`.
* **path-to-hadolint-config**: (optional) The path to the hadolint configuration file.
* **hadolint-ignored-rules**: (optional) Comma separated list of ignored rules for the lint.
* **trusted-registries**: (optional) Comma separated list of trusted repositories that can be used in Dockerfiles.
* **fail-on-lint-errors**: (optional) flag (`"true"` | `"false"`) to indicate if the task should fail or continue if issues are found in the Dockerfile lint. Default to "true"
* **hadolint-image**: (optional) image containing hadolint. Default to `hadolint/hadolint:v1.18.0-alpine`
* **pipeline-debug**: (optional) Pipeline debug mode. Value can be 0 or 1. Default to 0

### Workspaces

* **workspace**: A workspace containing the Dockerfile to lint
