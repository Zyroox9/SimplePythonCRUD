from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)
import urllib.request

try:
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.platforma
    mongo.server_info()

except:
    print("ERROR - cannot connect to db")

#############################################

@app.route("/reports", methods=["GET"])
def get_some_reports():
    try:
        data = list(db.reports.find())
        for user in data:
            user ["_id"] = str(user["_id"])
        return Response(response = json.dumps(data), status=500, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message": "cannot reas users"}), status=200, mimetype="application/json")


@app.route("/reports", methods = ["POST"])
def add_report():
    try:
        report = {"email": request.form["email"], "time": request.form["time"], "score": request.form["score"], "q1ID": request.form["q1ID"], "q1Ans": request.form["q1Ans"], "q1Pts": request.form["q1Pts"]}
        dbResponse = db.reports.insert_one(report)
        return Response(response = json.dumps({"message": "Test added", "id":f"{dbResponse.inserted_id}"}), status=200, mimetype="application/json")

    except Exception as ex:
        print("********************")
        print(ex)
        print("********************")
        return Response(response = json.dumps({"message": "Error, test not added", "id":f"{dbResponse.inserted_id}"}), status=500, mimetype="application/json")

@app.route("/reports/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"email": request.form["email"],
            "score": request.form["score"],
            "q1ID": request.form["q1ID"],
            "q1Ans": request.form["q1Ans"],
            "q1Pts": request.form["q1Pts"]}}
        )

        if dbResponse.modified_count == 1:
            return Response(response = json.dumps({"message": "User updated"}), status=200, mimetype="application/json")
        else:
            return Response(response = json.dumps({"message": "Nothing to update"}), status=200, mimetype="application/json")

    except Exception as ex:
        print("********************")
        print(ex)
        print("********************")
        return Response(response = json.dumps({"message": "Sorry, cannot update user"}), status=500, mimetype="application/json")


@app.route("/reports/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(response = json.dumps({"message": "Report deleted", "id": f"{id}"}), status=200, mimetype="application/json")
        return Response(response = json.dumps({"message": "Report doesn't exist", "id": f"{id}"}), status=200, mimetype="application/json")

    except Exception as ex:
        print("********************")
        print(ex)
        print("********************")
        return Response(response = json.dumps({"message": "Sorry, cannot delete a report"}), status=500, mimetype="application/json")

############################################
if __name__ == "__main__":
    app.run(port = 80, debug = True)
