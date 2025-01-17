from flask import Flask, make_response, redirect
from flask import render_template, request, Response
from uuid import uuid4
import json
from data_treatement import identify_user, clear_keys, get_user_list

app = Flask(__name__)

@app.route("/")
def menu():
    resp = make_response(render_template("menu.html"))
    resp.set_cookie("session_id", str(uuid4()))
    return resp

@app.route("/enregistrement")
def enregistrement():
    """
    renvoie l'interface d'enregistrement pour un nouvel utilisateur
    """
    clear_keys("")
    resp = make_response(render_template("enregistrement.html") )
    if not request.cookies.get("session_id"):
        resp.set_cookie("session_id", str(uuid4()))
    return resp

@app.route("/validate", methods=["POST"])
def validate():
    """
    Requete faite quand un utilisateur en cour d'enregistrement clique sur le bouton
    pour signifier qu'il a fini avec les données d'entrainement.   
    """
    clear_keys(request.cookies.get('session_id'))
    return redirect("/")
    

@app.route("/identification")
def identification():

    users = get_user_list()

    clear_keys(request.cookies.get('session_id'))
    resp = make_response(render_template("identification.html", users=users) )
    resp.set_cookie("session_id", str(uuid4()))
    return resp

@app.route("/text-data", methods=["POST"])
def savetext():
    """
    Requete recue a chaque barre espace. 
    """
    
    data = request.json
    
    print("New data from user: ", data["name"])
    with open('keys.json', 'r+') as json_file:
            file = json.load(json_file)
            inserted = False
            for session in file: 
                if session["session_id"] == data["session_id"]:  # La session existe déjà 
                    session["data"].append(data["data"])
                    inserted = True
            if not inserted:                  # Aucune session n'existe pour ce numéro de session. 
                data["data"] = [data["data"]]
                file.append(data)
            json_file.seek(0)
            json.dump(file, json_file, indent=2)  # On remet les données dans le fichier keys. 
    with open(f"input/entire_texts/{data['name']}.txt", "w") as file:
        file.write(data["text"])
    if data["name"] == "IDENTIFY":
        resp = identify_user()
        return resp
    
    return Response( "Recieved", status=200)