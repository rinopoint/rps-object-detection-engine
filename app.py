from typing import List, Dict, Any
from ultralytics import YOLO
import argparse
import os
import json
import os

def arguments() -> argparse.Namespace:
  """
  Parse command line arguments.

  Returns:
    argparse.Namespace: The parsed arguments.
  """
  parser = argparse.ArgumentParser(description='YOLOv8s')
  parser.add_argument('--confidence', "-c", default=0.5, type=float, help='confidence threshold')
  return parser.parse_args()

def load_models(input_config: Dict[str, Any], each_client: str, model: Dict[str, YOLO], classes: Dict[str, List[str]], class_names: Dict[str, List[str]]) -> None:
  """
  Load YOLOv8 models for each client and model specified in the configuration file.

  Args:
    input_config (dict): The configuration file.
    each_client (str): The name of the client.
    model (dict): The dictionary of YOLOv8 models.
    classes (dict): The dictionary of classes for each model.
    class_names (dict): The dictionary of class names for each model.
  """
  for original_model in input_config["clients"][each_client]:
    each_model = original_model
    print(f"Loading model: {each_model}")
    if each_model == "default":
      each_model = "yolov8s"
    model_name = f"{each_model}.pt"
    if not os.path.exists(model_name) and each_model != "yolov8s":
      print(f"Model: {model_name} not found. Skipping")
      continue
    model[each_model] = YOLO(model_name)
    classes[each_model] = input_config["clients"][each_client][original_model]
    class_names[each_model] = model[each_model].model.names

def predict_objects(image_path: str, model: YOLO, specified_classes: List[str], confidence: float, class_names: List[str]) -> Dict[str, Any]:
  """
  Predict object classes and probabilities for an image.

  Args:
    image_path (str): The path to the input image.
    model (YOLO): The YOLOv8 model.
    specified_classes (list): The list of classes to predict.
    confidence (float): The confidence threshold.
    class_names (list): The list of class names.

  Returns:
    dict: The dictionary of predicted object classes and probabilities.
  """
  results = model.predict(image_path, classes=specified_classes, conf=confidence)
  output_dict = {"classes": []}
  for result in results[0]:
    pred_confidence = result.boxes.conf.cpu().numpy()
    class_id = result.boxes.cls.cpu().numpy().astype(int)
    class_name = class_names[(int(class_id[0]))]
    output_dict["classes"].append({
      "className": class_name,
      "probability": round(float(pred_confidence[0]), 2)
    })
  return output_dict

def process_images(input_config: Dict[str, Any], confidence: float) -> None:
  """
  Process images for each client and model specified in the configuration file.

  Args:
    input_config (dict): The configuration file.
    confidence (float): The confidence threshold.
  """
  base_output_path = input_config["output_path"]
  os.makedirs(base_output_path, exist_ok=True)
  base_client_path = input_config["client_path"]
  list_of_clients = os.listdir(base_client_path)

  for each_client in list_of_clients:
    if each_client not in input_config["clients"]:
      print(f"Client: {each_client} not found in config file. Skipping")
      continue
    model = {}
    class_names = {}
    classes = {}
    load_models(input_config, each_client, model, classes, class_names)

    each_client_path = os.path.join(base_client_path, each_client)
    for each_client_group in os.listdir(each_client_path):
      output_group_path = os.path.join(base_output_path, each_client, each_client_group)
      os.makedirs(output_group_path, exist_ok=True)
      each_client_group_path = os.path.join(each_client_path, each_client_group)
      for each_image in os.listdir(each_client_group_path):
        image_path = os.path.join(each_client_group_path, each_image)
        image_name, image_extension = os.path.splitext(each_image)
        json_path = os.path.join(output_group_path, f"{image_name}.json")
        if image_extension.lower() not in [".jpg", ".jpeg", ".png"]:
          print(f"Image: {each_image} doesn't have a valid extension. Skipping")
          continue
        output_dict = {
          "client": each_client,
          "groupName": each_client_group,
          "models": {},
        }
        for each_model in input_config["clients"][each_client]:
          if each_model == "default":
            each_model = "yolov8s"
          if each_model not in model:
            print(f"Model: {each_model} not found. Skipping")
            continue
          specified_classes = classes.get(each_model)
          if specified_classes == []:
            specified_classes = None
          original_model= each_model if each_model != "yolov8s" else "default"
          output_dict["models"].update({
            original_model: predict_objects(image_path, model[each_model], specified_classes, confidence, class_names[each_model])
          })
        with open(json_path, 'w') as outfile:
          json.dump(output_dict, outfile, indent=4)

if __name__ == '__main__':
  args = arguments()
  confidence = args.confidence
  with open("config.json") as f:
    input_config = json.load(f)
  process_images(input_config, confidence)
