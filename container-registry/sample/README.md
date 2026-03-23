# Containerize Task example usage
The `sample` sub-directory contains an `buildkit-no-resources` EventListener definition that you can include in your tekton pipeline configuration to run an example usage of the `icr-containerize` and `icr-check-va-scan`. This pipeline definition uses the task's parameter `image-url` to provide the information on image to build and scan.

It also contains a `buildkit-no-image-url` EventListener definition which is the providing the same example but without the needs to set parameter `image-url`. The information on the IBM Cloud container registry and image to build is provided using parameters `registry-region`, `registry-namespace` and `image-name`.

**Note:** this sample also relies on the clone-repo task to clone the application to containerize.

1) Create or update a toolchain to include:

   - the git repository that you want to clone, which can be private
   - the repository containing this tekton task
   - a [Tekton pipeline definition](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines#create_tekton_pipeline)

   ![Toolchain overview](./images/container-registry-sample-toolchain-overview.png)

2) Add the definitions:

   - for the `git-clone-repo` (`git` path)
   - for this task and the sample (`container-registry` and `container-registry/sample` paths)

   ![Tekton pipeline definitions](./images/container-registry-sample-tekton-pipeline-definitions.png)

3) Add the environment properties:

   - `apikey` to provide an API key used for the ibmcloud login/access
   - `repository` to indicate the git repository url to clone (correspoding to the one integrated in the toolchain)
   - `image-url` to indicate the URL of the image to push to the IBM Cloud Container Registry

   ![Tekton pipeline environment properties](./images/container-registry-sample-tekton-pipeline-environment-properties.png)

4) Create a manual trigger to start the sample listener

   ![Tekton pipeline sample trigger](./images/container-registry-sample-tekton-pipeline-sample-triggers.png)

5) Run the pipeline

6) After the pipeline ran successfully, if you look at the IBM Cloud container registry content referenced within the Image url definition, you will see an image with the expected tags:
   ```
    $ ibmcloud cr images
    Listing images...

    Repository                              Tag                                                     Digest         Namespace        Created         Size    Security status
    de.icr.io/jauninb-tekton/my-new-image   1.0.0-dev                                               5107dea95bd0   jauninb-tekton   6 minutes ago   54 MB   No Issues
    de.icr.io/jauninb-tekton/my-new-image   1.0.0-master-e8e9fa6b7827d7898d04a218fa69f327db7fc2b4   5107dea95bd0   jauninb-tekton   6 minutes ago   54 MB   No Issues

    OK
   ```
## Detailed Description

This pipeline and relevant trigger(s) can be configured using the properties described below.

See https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines&interface=ui#configure_tekton_pipeline for more information.

### buildkit-no-image-url

**EventListener**: buildkit-no-image-url


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` (**secured property**) | [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and git intergation toolcard like `Git Repos and Issue Tracking` service if used). | - | Yes | secret |
| `branch` | the branch for the git repo | `master` | No | string |
| `image-name` | the image name | - | Yes | string |
| `path-to-dockerfile` | - | `.` | No | string |
| `pipeline-debug` | - | `0` | No | string |
| `properties-file` | - | - | Yes | string |
| `push-to-registry` | - | `true` | No | string |
| `registry-namespace` | the container registry namespace | - | Yes | string |
| `registry-region` | the container registry region | - | Yes | string |
| `repository` | the git repo | - | Yes | string |


### buildkit-no-resources

**EventListener**: buildkit-no-resources


| Properties | Description | Default | Required | Type |
|------------|-------------|---------|----------|------|
| `apikey` (**secured property**) | [IBM Cloud Api Key](https://cloud.ibm.com/iam/apikeys) used to access to the toolchain (and git intergation toolcard like `Git Repos and Issue Tracking` service if used). | - | Yes | secret |
| `branch` | the branch for the git repo | `master` | No | string |
| `disable-caching` | Disable caching layers when building images. Value can be 0 or 1. Default to 0 | `0` | No | string |
| `image-url` | the url of the image to build | - | Yes | string |
| `path-to-dockerfile` | the path to the Dockerfile that is used for the build (default to `.` meaning current directory) | `.` | No | string |
| `pipeline-debug` | Pipeline debug mode. Value can be 0 or 1. Default to 0 | `0` | No | string |
| `properties-file` | name of the properties file that will be created (if needed) or updated (if existing) as an additional
 outcome of this task in the workspace. This file will contains the git related information (`GIT_URL`, `GIT_BRANCH` and `GIT_COMMIT`)
 and image registry-related information (`REGISTRY_URL`, `REGISTRY_NAMESPACE`, `REGISTRY_REGION`, `IMAGE_NAME`, `IMAGE_TAGS` and `IMAGE_MANIFEST_SHA`) | - | Yes | string |
| `push-to-registry` | option to push the built image to registry or not. Default is `true` | `true` | No | string |
| `repository` | the git repo | - | Yes | string |
