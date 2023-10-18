# RPS-object-detection-engine

Current project is just mocked 

General Requirements
====================
- Configuration by client
- Configuration should include the ability to specify 1-n: coco dataset classes
- Configuration should include the ability to specify 1-n: custom dataset classes
- What else should we make configurable?


Requirement #1 - Object Detection
=================================
Use Case: Process images in directories organized by client and group names. Per image, ouptut a json file with all the descovered data about the image.

-> Input URL Format: input/clients/<CLIENT>/<GROUP NAME>/<Image Files>
-> Example Image File: 00001.jpg
-> Ouptut JSON Filename: output/clients//my-group-of-images-10-10-2023/my-group-of-images-10-10-2023--00001.json
-> Output JSON - Obj Mock/Example: { client: rps, groupName: my-group-of-images-10-10-2023, classes: [ { className: motorcycles, probability: 0.59 }, { className: skateboard, probability: 0.99 }] }

# How to run
## Prerequisites
- Python 3.7+ (https://www.python.org/downloads/)
- pip (https://pip.pypa.io/en/stable/installing/)

## Install dependencies
```bash
pip install ultralytic==8.0.20
```

## Modify the config file

```json
{
  "client_path": "input/clients", 
  "output_path": "output/clients",
  "clients": {
    "rps": {
      "default": [ 0, 1, 3 ],
      "car": [ 0, 1, 5, 7 ],
      "person": [ 0, 1, 2, 3, 4, 5, 6, 7 ]
    },
    "client2": {
      "face": [],
      "skateboard": [ 0, 1, 2, 3, 4, 5, 6, 7 ]
    }
  }
}
```

- Open `config.json` and modify the `client_path` and `output_path` to point to the correct directories on your machine.
- `client_path` is the path to the directory containing all the client directories.
- `output_path` is the path to the directory where the output json files will be saved.
- add all the `client` names to the `clients` dict
- add all the model names to the `client` dict
- add all the `classes` to the `model` value

  - Empty array means all the classes will be used.
  - default model is pretrained yolov8s.pt
  - in above sample config, `rps` client has 3 models: `default`, `car`, `person`
  - in your directory u should have models named `car.pt`, `person.pt`
  - So whichever model u want to use, just add the model name to the `client` dict with the list of classes u want to use for that model.

## Run the script
```bash
python app.py -c 0.5
```

- `-c` is the confidence threshold. Default is 0.5

## Output
- The output json files will be saved in the `output_path` directory.
- The output json file name will be the same as the input image file name.
- The output json file will contain the `client` name, `model` name, `classes` and `probability` for each class.

## Example
- Input image file: `input/clients/rps/my-group-of-images-10-10-2023/00001.jpg`
- Output json file: `output/clients/rps/my-group-of-images-10-10-2023/00001.json`

```json
{
    "client": "rps",
    "groupName": "my-group-of-images-10-10-2023",
    "models": {
        "default": {
            "classes": [
                {
                    "className": "person",
                    "probability": 0.52
                }
            ]
        },
        "car": {
            "classes": []
        },
        "person": {
            "classes": [
                {
                    "className": "person",
                    "probability": 0.52
                }
            ]
        }
    }
}
```

Requirement #2 - Train Object, Human
====================================
Use Case: A script that trains a new custom class based on a directory of images.

