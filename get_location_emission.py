#!/usr/bin/python3
"""
This script uses the Carbon Awareness SDK to automate the creation
of a impact-framework to use the best rating in a location during the last 24h
"""
import yaml
import subprocess
import json


################## CONFIG ###############
PATH_TO_CONFIG_FILE = "demo.yaml"
OUTPUT_FILE = "output.yaml"
PATH_TO_CASDK = "casdk/caw"
################## CONFIG END ###########

def calculate_grid_carbon_intensity(location: str) -> int:
  process_value = subprocess.run(f"./{PATH_TO_CASDK} emissions -l {location} --best", shell=True, capture_output=True)
  value = json.loads(process_value.stdout)

  return value[0].get("Rating")

with open(PATH_TO_CONFIG_FILE, "r") as file:
  manifest = yaml.safe_load(file)

inputs = manifest["graph"]["children"]["child"]["inputs"]

for input in inputs:
  input["grid_carbon_intensity"] = calculate_grid_carbon_intensity(input["location"])

with open(OUTPUT_FILE, "w") as file:
  file.write(yaml.dump(manifest, sort_keys=False))
