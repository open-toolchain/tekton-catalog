# These tasks have been deprecated and are no longer supported.
# Signing - Docker Content Trust related tasks

# Tasks

- **[signing-dct-init](#signing-dct-init)**: This task initialize Docker Content Trust GUN/repository
- **[signing-dct-sign](#signing-dct-sign)**: This task performs a Docker Content Trust signature on a given image
- **[signing-dct-enforcement-policy](#signing-dct-enforcement-policy)**: This task installs [Container Image Security Enforcement](https://cloud.ibm.com/docs/Registry?topic=Registry-security_enforce) on a given cluster.

## Install the Tasks
- Add a github integration to your toolchain with the repository containing the tasks (https://github.com/open-toolchain/tekton-catalog)
- Add this github integration to the Definitions tab of your Continuous Delivery tekton pipeline, with the Path set to `signing/dct`

## signing-dct-init

## signing-dct-sign

## signing-dct-enforcement-policy
