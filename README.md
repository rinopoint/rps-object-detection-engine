# rps-object-detection-engine

Current project is just mocked 

====================
General Requirements
====================
- Configuration by client
- Configuration should include the ability to specify 1-n: coco dataset classes
- Configuration should include the ability to specify 1-n: custom dataset classes
- What else should we make configurable?

=================================
Requirement #1 - Object Detection
=================================
Use Case: Process images in directories organized by client and group names. Per image, ouptut a json file with all the descovered data about the image.

-> Input URL Format: input/clients/<CLIENT>/<GROUP NAME>/<Image Files>
-> Example Image File: 00001.jpg
-> Ouptut JSON Filename: output/clients//my-group-of-images-10-10-2023/my-group-of-images-10-10-2023--00001.json
-> Output JSON - Obj Mock/Example: { client: rps, groupName: my-group-of-images-10-10-2023, classes: [ { className: motorcycles, probability: 0.59 }, { className: skateboard, probability: 0.99 }] }

====================================
Requirement #2 - Train Object, Human
====================================
Use Case: A script that trains a new custom class based on a directory of images.

