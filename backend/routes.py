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
    print(data)
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for x in data:
        if x["id"] == id:
            return (x,200)

    return ({"message":"picture not found"},404)



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    body = request.get_json()
    for pic in data:
        if pic['id'] == body['id']:
            return({'Message':f"picture with id {pic['id']} already present"}, 302)
    
    data.append(body)
    return ({"id": body['id']},201)

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    body = request.get_json()
    for i in range(len(data)):
        if data[i]['id'] == id:
            data[i] = body
            return jsonify(data[i])
            
    return ({"message":"picture not found"}, 404)



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in range(len(data)):
        if data[i]['id'] == id:
            data.pop(i)
            return ({"message":"no content"},204)

    return ({"message":"picture not found"}, 404)