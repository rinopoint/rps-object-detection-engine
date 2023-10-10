#!/bin/bash

INPUT_CLIENTS_DIR="input/clients/"
OUTPUT_CLIENTS_DIR="output/clients/"
CLIENT="rps"
GROUP_NAME="my-group-of-images-10-10-2023"
IMAGE_FILE_URLS=$INPUT_CLIENTS_DIR/$CLIENT/$GROUP_NAME

echo ""
echo "===================="
echo "General Requirements"
echo "===================="
echo "- Configuration by client"
echo "- Configuration should include the ability to specify 1-n: coco dataset classes"
echo "- Configuration should include the ability to specify 1-n: custom dataset classes"
echo "- What else should we make configurable?" 
echo ""


echo "================================="
echo "Requirement #1 - Object Detection"
echo "================================="
echo "Use Case: Process images in directories organized by client and group names. Per image, ouptut a json file with all the descovered data about the image." 
echo ""
echo "-> Input URL Format: input/clients/<CLIENT>/<GROUP NAME>/<Image Files>" 

count=0;
for FILE in `ls "$IMAGE_FILE_URLS/"`; do
  if [[ $count == 1 ]] 
  then 
    break;
  fi

  filePrefix="${FILE%%.*}"

  echo "-> Example Image File: $FILE"
  echo "-> Ouptut JSON Filename: $OUTPUT_CLIENTS_DIR/$GROUP_NAME/$GROUP_NAME--$filePrefix.json"
  echo "-> Output JSON - Obj Mock/Example: { client: "rps", groupName: "my-group-of-images-10-10-2023", classes: [ { className: "motorcycles", probability: 0.59 }, { className: "skateboard", probability: 0.99 }] }"

  ((count=count+1))
done


echo ""
echo "===================================="
echo "Requirement #2 - Train Object, Human"
echo "===================================="
echo "Use Case: A script that trains a new custom class based on a directory of images." 
echo ""


