#!/bin/bash

INPUT_CLIENTS_DIR="input/clients/"
OUTPUT_CLIENTS_DIR="output/clients/"
CLIENT="rps"
GROUP_NAME="my-group-of-images-10-10-2023"
IMAGE_FILE_URLS=$INPUT_CLIENTS_DIR/$CLIENT/$GROUP_NAME

echo "Test Data: $IMAGE_FILE_URLS"
echo "URL Format: input/clients/<CLIENT>/<GROUP NAME>/<Image Files>" 

count=0;
for FILE in `ls "$IMAGE_FILE_URLS/"`; do
  filePrefix="${FILE%%.*}"

  echo ""
  echo "Process Image File: $FILE"
  echo "Process & Create JSON File: $OUTPUT_CLIENTS_DIR/$GROUP_NAME/$GROUP_NAME--$filePrefix.json"
  echo "JSON Obj Mock/Example: { client: "rps", groupName: "my-group-of-images-10-10-2023", classes: [ { className: "motorcycles", probability: 0.59 }, { className: "skateboard", probability: 0.99 }] }"

  if [[ $count == 9 ]] 
  then 
    echo ""
    echo "Stopping after 10 images... Fake Demo"
    break;
  fi

  ((count=count+1))
done


