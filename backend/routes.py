from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        urls = []
        for item in data:
            urls.append(item["pic_url"]) 
        return jsonify(urls), 200
    except:
        return ({"message": "data not found"}, 400)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pict in data:
        if pict['id'] == id:
            return jsonify(pict), 200
    return {"message": "ID not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = json.loads(request.data)
    if not picture_data:
        return ({"message": "Invalid Input Paramter"}, 422)
    ava_ids = [item["id"] for item in data]
    if picture_data['id'] in ava_ids:
        return ({"Message": f"picture with id {picture_data['id']} already present"}, 302)
    data.append(picture_data)
    return (jsonify(picture_data), 201)

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pict_data = json.loads(request.data)
    resp_data = data[:]
    if not pict_data:
        return ({"message": "Invaid input parameter"}, 422)
    for pict in resp_data:
        if pict['id'] == id:
            pict['event_state'] = pict_data['event_state']
            return (jsonify(resp_data), 200)
    return ({"message": "picture not found"}, 404)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pict in data:
        if pict['id'] == id:
            data.remove(pict)
            return ({"message": " "}, 204)
    return ({"message": "picture not found"}, 404)
