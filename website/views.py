from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_required
from . import db
from .models import User, UserGames
import requests as rq
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime
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
        if request.form.get("workshop-link") == "":
            flash("Please enter a workshop url.", category="error")
            return render_template("downloader.html", user=current_user)
        # Prepare entered item
        prepared_ids = {
            "key" : session['steam_api_key'],
            "itemcount" : "1"
            }
        url = request.form.get("workshop-link")
        xid = url.strip("https://steamcommunity.com/workshop/filedetails/?id=")
        id = re.match(r"(.*\d+)", xid).group()
        id_data = {f"publishedfileids[{0}]": id}
        prepared_ids.update(id_data)
        form_data = MultipartEncoder(prepared_ids)

        # Get File Info
        data = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data=form_data, headers={'Content-Type': form_data.content_type}).json()
        
        # Extract Needed information
        for mod in data["response"]["publishedfiledetails"]:
            mod_creator_id = mod["creator"]
            mod_size_bytes = mod["file_size"]
            mod_image = mod["preview_url"]
            mod_name = mod["title"]
            mod_desc = mod["description"]
            mod_updated = mod["time_updated"]
            mod_subs = mod["lifetime_subscriptions"]
            mod_favs = mod["lifetime_favorited"]
            mod_views = mod["views"]

        # Convert bytes to readable size
        step_to_greater_unit = 1024.
        number_of_bytes = float(mod_size_bytes)
        unit = 'bytes'
        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'KB'
        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'MB'
        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'GB'
        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'TB'
        precision = 1
        number_of_bytes = round(number_of_bytes, precision)
        mod_size = str(number_of_bytes) + ' ' + unit

        # Debug File Print
        print("")
        print("Creator ID: ", mod_creator_id)
        print("Size Bytes: ", mod_size_bytes)
        print("Size: ", mod_size)
        print("Image: ", mod_image)
        print("Name: ", mod_name)
        #print("Description: ", mod_desc)
        print("Updated: ", mod_updated)
        print("Subscriptions: ", mod_subs)
        print("Favorites: ", mod_favs)
        print("Views: ", mod_views)
        print("")

        # Get Creator Data
        creator_data = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={session['steam_api_key']}&steamids={mod_creator_id}").json()
        
        # Extract Creator Info
        creator_name = creator_data["response"]["players"][0]["personaname"]
        creator_image = creator_data["response"]["players"][0]["avatarfull"]
        print("Creator: ", creator_name)
        print("Avatar: ", creator_image)

        mod_data = {
            "mod_image": mod_image,
            "mod_name": mod_name,
            "mod_desc": mod_desc,
            "mod_size": mod_size,
            "mod_updated": datetime.utcfromtimestamp(mod_updated).strftime('%Y-%m-%d %H:%M:%S'),
            "mod_subs": mod_subs,
            "mod_favs": mod_favs,
            "mod_views": mod_views,
            "creator_name": creator_name,
            "creator_image": creator_image
        }

        return render_template("downloader-details.html", user=current_user, mod_data=mod_data)
    else:
        if session['steam_api_key'] == "":
            flash("Please Provide a Steam API Key to download mods", category="error")
            return redirect(url_for("views.settings"))
        return render_template("downloader.html", user=current_user)

@views.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        if request.form.get("delete-account") == "1":
            user = User.query.filter_by(username=session['username']).first()
            db.session.delete(user)
            db.session.commit()
            flash("Account Successfully Deleted!", category="success")
            return redirect(url_for("auth.login"))
    return render_template("settings.html", user=current_user)