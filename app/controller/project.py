from flask import *
from app.flask_twitter.TwitterPlugin import *
import json
import urllib

project = Module(__name__)

@project.route('/twitter/callback')
@twitter_callback
def callback():
    resp = make_response(redirect("/"));
    return (resp);

@project.route("/")
@twitter_login
def index(api):
    resp = make_response(render_template("index.html"));
    key = request.cookies["twackey"];
    secret = request.cookies["twsckey"];
    resp.set_cookie("twackey", key, max_age=60 * 60 * 24 * 30);
    resp.set_cookie("twsckey", secret, max_age=60 * 60 * 24 * 30);

    return (resp);

@project.route("/post", methods=["POST"])
@twitter_login
def post(api):
    text = request.form["text"];
    api.update_status(text);

    return ("OK");

@project.route("/get_timeline")
@twitter_login
def get_timeline(api):
    tl = api.home_timeline();
    
    max_id = int(request.args["max_id"]);
    tl.reverse();
    result = [{"id": str(i.id), "text": i.text, "user": i.user.screen_name}  for i in tl if (max_id < i.id)];
    return (json.dumps(result));


@project.route("/fav", methods=["POST"])
@twitter_login
def fav(api):
    id = int(request.form["id"]);
    
    try:
        api.create_favorite(id=id);
    except:
        return ("NG");
    return ("OK");


@project.route("/retweet", methods=["POST"])
@twitter_login
def retweet(api):
    id = int(request.form["id"]);
    
    try:
        api.retweet(id=id);
    except:
        return ("NG");

    return ("OK");


@project.route("/image/<user>")
def get_image(user):
    resp = make_response();
    resp.headers["Content-Type"] = "image/jpeg; charset=utf-8";
    resp.data = urllib.urlopen("https://api.twitter.com/1/users/profile_image?size=normal&screen_name=%s" % user).read();
    return (resp);

