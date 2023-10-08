import os
import cv2
import json
import requests

from flask import Blueprint, Flask, render_template, redirect, request, session, url_for
from flask_session import Session

from src import app_blueprint
from src.bard_prompt import summarize_about_body_of_water

def get_summarised_water_info(location_name):
  location_name_in_cache = location_name.lower().replace(" ", "-")
  was_cached = True

  results = None

  with open(os.path.join(os.environ["output_path"], "cached_queries.json"), "r") as json_file:
    cache = json.loads(json_file.read())
    
    cached_file_path = cache.get(location_name_in_cache, None)
    cached_file_name = location_name_in_cache + ".json"
    if cached_file_path is None:
      summarised_info = summarize_about_body_of_water(location_name)
      data = {
        "Endangered species" : summarised_info[0],
        "Water origins" : summarised_info[1],
        "Water quality" : summarised_info[2],
        "Precautionary actions" : summarised_info[3],
      }

      results = data

      was_cached = False
      with open(os.path.join(os.environ["output_path"], cached_file_name), "w") as cache_file:
        cache_file.write(json.dumps(data, indent=2))
        cache[location_name_in_cache] = cached_file_name
    else: 
      with open(os.path.join(os.environ["output_path"], cached_file_name), "r") as cache_file:
        results = json.loads(cache_file.read())
  
  if was_cached:
    with open(os.path.join(os.environ["output_path"], "cached_queries.json"), "w") as json_file:
      json_file.write(json.dumps(cache, indent=2))

  return results

def convert_location_name_to_coords(location_name):
  base_url = "https://nominatim.openstreetmap.org/search"
  params = {
      "q": location_name,
      "format": "json",
  }

  response = requests.get(base_url, params=params)
  data = response.json()
  print(data)

  # Access the geocoding results
  for result in data:
    print(result["display_name"], result["lat"], result["lon"])
  
  if len(data) == 0:
    data.append({
      "display_name": "Unknown",
      "lat": "0",
      "lon": "0",
    })

  return data

@app_blueprint.route('/', methods = ['POST', "GET"])
def homepage():
  if request.method == "POST":
    request_json = request.get_json()

    location_name = request_json["location_name"]

    return {
      "link" : url_for("whatsmywater.water_map_view", location_name = location_name)
    }
  else :
    return render_template(
      "index.html", 
      app_name=os.environ["app_name"],
      app_name_display=os.environ["app_name_display"],
    )

@app_blueprint.route('/water_map_view/<location_name>')
def water_map_view(location_name = None):
  if not location_name:
    location_name = "Putrajaya Lake"

  location_search_results = convert_location_name_to_coords(location_name)
  longitude = location_search_results[0]["lon"]
  latitude = location_search_results[0]["lat"]

  return render_template(
    "water_map_view.html", 
    app_name=os.environ["app_name"],
    app_name_display=os.environ["app_name_display"],
    latitude=latitude,
    longitude=longitude,
    location_name=location_name,
  )

@app_blueprint.route('/endangered_species/<location_name>')
def endangered_species(location_name = None):
  if not location_name:
    location_name = "Putrajaya Lake"

  data = get_summarised_water_info(location_name)
  contents = data["Endangered species"]

  return render_template(
    "endangered_species.html", 
    app_name=os.environ["app_name"],
    app_name_display=os.environ["app_name_display"],
    contents=contents,
  )


@app_blueprint.route('/water_origins/<location_name>')
def water_origins(location_name = None):
  if not location_name:
    location_name = "Putrajaya Lake"

  data = get_summarised_water_info(location_name)
  contents = data["Water origins"]

  return render_template(
    "water_origins.html", 
    app_name=os.environ["app_name"],
    app_name_display=os.environ["app_name_display"],
    contents=contents,
  )


@app_blueprint.route('/water_quality/<location_name>')
def water_quality(location_name = None):
  if not location_name:
    location_name = "Putrajaya Lake"

  data = get_summarised_water_info(location_name)
  contents = data["Water quality"]

  return render_template(
    "water_quality.html", 
    app_name=os.environ["app_name"],
    app_name_display=os.environ["app_name_display"],
    contents=contents,
  )


@app_blueprint.route('/precautionary_actions/<location_name>')
def precautionary_actions(location_name = None):
  if not location_name:
    location_name = "Putrajaya Lake"

  data = get_summarised_water_info(location_name)
  contents = data["Precautionary actions"]

  return render_template(
    "precautionary_actions.html", 
    app_name=os.environ["app_name"],
    app_name_display=os.environ["app_name_display"],
    contents=contents,
  )