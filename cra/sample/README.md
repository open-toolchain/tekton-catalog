# Configuring Code Risk Analyzer for Your Code Repositories
To configure Code Risk Analyzer for your repositories, you will need to take the following steps:
- Create an empty Toolchain in Dallas location
- Add DevOps Insights card to your Toolchain
- Add a card for each code repository that you want to scan.  You can start with a single card and add more later.
- Create a Tekton pipeline and configure it.  

Before you start, ensure that you have admin access to your code repositories.

##  Region Considerations
At this time, Code Risk Analyzer is supported only at Dallas location.  Your toolchain must be created Dallas location.

## Create an Empty Toolchain
1. Login to your IBM Cloud account and go to the Toolchains page https://cloud.ibm.com/devops/toolchains?env_id=ibm:yp:us-south.  

2. Click on  `Create Toolchain`

3.  Select `Build your own toolchain` template, change the default toolchain name if desired and click the Create button.

## API Key for the toolchain
You will need an API Key that has access to this toolchain.  For creating an API Key via the User Interface, click on Manage->Access->API Keys.  Click on Create an IBM Cloud API key to create an API Key.  Copy the API Key - you will need it later.

## Add DevOps Insights card to your Toolchain
Click on Add Tool button, select DevOps Insights card and click on Create Integration button.  Now, DevOps Insights card should be added to your toolchain.

## Add a card for your code repository to your Toolchain
Now, you need to add a card for your code repository to the toolchain.  Click on Add tool button then select the GitHub card or the Git Repos and Issue Tracking card to add the card to the toolchain.

## Add a card for the code repository where Tekton tasks have been defined
Click on Add tool button and then click on GitHub card.  Add the existing repository https://github.com/open-toolchain/tekton-catalog.

## Add and Configure a Tekton pipeline to your toolchain
- In this step, you will add a Tekton pipeline to the toolchain. Click on Add tool button and then click on Delivery Pipeline card.  Specify a Pipeline Name. For Pipeline Type, select Tekton.  Click Create Integration.
- Click on the pipeline card so that you can configure the pipeline.
- In this step, you will import Tekton task defintions into your toolchain. On the Definitions tab, click on Add button.  Select tekton-catalog repository.  Select branch `master`. Select path `toolchain` and click on Add button.  Similarly, add the following paths:  `git`,`utils`, `cra` and `cra/sample`.  Now click Validate button and then Save button.

| Repository                | Branch | Path          |
| ------------------------- | ------ | ------------- |
| tekton-catalog	| master   | toolchain     |
| tekton-catalog	| master   | git           |
| tekton-catalog	| master   | utils         |
| tekton-catalog	| master | cra           |
| tekton-catalog	| master | cra/sample    |


- In this step, you will specify the Tekton worker pool for this pipeline. There is a managed worker pool that IBM provides for Dallas location - you can select that.  You can also choose to host a private worker pool.  See {HERE}.

- In this step, you will set up a Trigger for you code repository.  Click on Triggers menu. Click Add trigger button and select Git Repository.  For Repository, select your code repository.  Select the branch for which you want to enable the trigger.  Click on the checkbox for When a pull request is opened or updated.  Select an EventListener.  For GitHub repos, select github-pr-listener.  For Git Repository and Issue Tracking repos, select gitlab-pr-listener.  Click Save butoon.  You can add a trigger for each repo for which you want to run Code Risk Advisor pipeline.

- In this step, you will specify Environment Properties for your pipeline. Click on Environment properties tab. Click on Add button and then click on Secure. Specify Property Name apikey. Now specify the API Key that you generated earlier in the Value field.  Click on Save button.

# Scanning your Pull Requests
After the above set up is complete, follow these steps:
- Open a Pull Request for your repository
- The Code Risk Analyzer pipeline that you configured above will start running automatically. 
- The pipeline first discovers the dependencies that your repository has.  These dependencies could be application packages, container images or OS pacakges. 
- The pipeline then identifies vulnerabilities associated with these dependencies and posts a comment to your Pull Request.
- The pipeline then scans Dockerfiles and Kubernetes yaml files for best practices. It will then post a comment to your Pull Request.
- The pipeline then posts a link to Bill of Materials to your Pull Request.
