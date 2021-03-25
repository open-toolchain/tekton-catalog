#!/bin/bash

# iterate over all the task files to ensure
# - task name is appropriately prefiexed according to folder
# - folder/filename match task name
# - each task parameter has a description
exit_status=0
for file in $(find . -type f -name "*.yaml")
do
  if [[ "$(yq r $file 'kind')" == "Task" ]]; then
    file=$(echo $file | sed 's|^./||')
    folder=$(dirname $file)
    if [[ "$folder" != *"sample"* ]]; then
      if [ "$folder" == "cloudfoundry" ]; then
        prefix="cf"
      elif [ "$folder" == "container-registry" ]; then
        prefix="icr"
      elif [ "$folder" == "devops-insights" ]; then
        prefix="doi"
      elif [ "$folder" == "kubernetes-service" ]; then
        prefix="iks"
      else
        prefix=$(echo $folder | tr -s '/' '-')
      fi    
      fully_qualified_task_name="$(yq r $file 'metadata.name')"
      task_name=${fully_qualified_task_name#"$prefix-"}
      # Check task name only for non sample
      if [[ "$prefix-$task_name" != "$fully_qualified_task_name" ]]; then
        echo "Task name in $file is not appropriate. it should be $prefix-$task_name and not $fully_qualified_task_name"
        exit_status=1
      fi
      # Check file name
      filename=$(basename -s .yaml $file)
      if [[ "task-$task_name" != "$filename" ]]; then
         echo "File $file containing task $fully_qualified_task_name is not well-formed. $filename.yaml should be renamed to task-$task_name.yaml"
        exit_status=1
      fi
      # Check if each Task parameters has a description
      parameters=$(yq r --tojson $file | jq -r '.spec.params | .[] | select(has("description") | not) | .name')
      if  [[ ! -z "$parameters" ]]; then
        echo "Task $fully_qualified_task_name (in $file) is missing description for parameter(s):"
        for parameter in $parameters; do
          echo "- $parameter"
        done
        exit_status=1
      fi
    fi
  fi
done
exit $exit_status
