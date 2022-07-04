from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from . import db
from .models import User, UserGames
import requests as rq
import subprocess
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from time import sleep

views = Blueprint("views", __name__)

@views.route("/")
def blank():
    return render_template("base.html", user=current_user)

@views.route("/home")
@login_required
def home():
    return render_template("base.html", user=current_user)

@views.route("/games", methods=["GET", "POST"])
@login_required
def games():
    if request.method == "POST":
        game_id = request.form.get("game_id")
        game_name = request.form.get("game_name")
        game_path = request.form.get("game_path")

        game = UserGames.query.filter_by(game_id=game_id, user_id=current_user.id).first()
        if game:
            flash("Game was already added!", category="error")
        elif game_id == "" or game_name == "" or game_path == "":
            flash("Please fill out all fields.", category="error")
        else:
            new_game = UserGames(game_id=game_id, game_name=game_name, game_path=game_path, user_id=current_user.id)
            db.session.add(new_game)
            db.session.commit()

            # Retrieve image directly
            request_image = rq.get(f"https://cdn.akamai.steamstatic.com/steam/apps/{game_id}/header.jpg")
            if request_image.status_code == 200:
                open(f"website/static/headers/{game_id}.jpg", 'wb').write(request_image.content)
            else:
                pass


            flash("Game Added Successfully!", category="success")
            return redirect(url_for("views.games"))

    return render_template("games.html", user=current_user)

@views.route("/downloader", methods=["GET", "POST"])
@login_required
def downloader():
    if request.method == "POST":
        prepared_ids = {
            "key" : "DE24D89C1E9B80E36ED9E3AD3938B7C2",
            "itemcount" : "1"
            }
        url = request.form.get("workshop-link")
        xid = url.strip("https://steamcommunity.com/workshop/filedetails/?id=")
        id = re.match(r"(.*\d+)", xid).group()

        print("POST SENT!")
        id_data = {f"publishedfileids[{0}]": id}
        prepared_ids.update(id_data)
        print(prepared_ids)
        print("Mods prepared: ", str(len(prepared_ids)))
        form_data = MultipartEncoder(prepared_ids)
        #print(form_data)
        data = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data=form_data, headers={'Content-Type': form_data.content_type}).json()
        print("")
        #print(data)
        for mod in data["response"]["publishedfiledetails"]:
            mod_creator_id = mod["creator"]
            mod_size = mod["file_size"]
            mod_image = mod["preview_url"]
            mod_name = mod["title"]
            mod_desc = mod["description"]
            mod_updated = mod["time_updated"]
            mod_subs = mod["lifetime_subscriptions"]
            mod_favs = mod["lifetime_favorited"]
            mod_views = mod["views"]
            print("")
            print("Creator ID: ", mod_creator_id)
            print("Size: ", mod_size)
            print("Image: ", mod_image)
            print("Name: ", mod_name)
            #print("Description: ", mod_desc)
            print("Updated: ", mod_updated)
            print("Subscriptions: ", mod_subs)
            print("Favorites: ", mod_favs)
            print("Views: ", mod_views)
            print("")
            creator_data = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=DE24D89C1E9B80E36ED9E3AD3938B7C2&steamids={mod_creator_id}").json()
            creator_name = creator_data["response"]["players"][0]["personaname"]
            creator_image = creator_data["response"]["players"][0]["avatarfull"]
            print(creator_name)
            print(creator_image)
    else:
        return render_template("downloader.html", user=current_user)

@views.route("/settings")
@login_required
def settings():
    return render_template("settings.html", user=current_user)