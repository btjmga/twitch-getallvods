import re
import subprocess
import requests
import streamlink

session = requests.Session()


def get_oauth(client_id, client_secret):  # This method gets the auth token
    params_get_oauth = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "clips:edit",
    }
    url_get_oauth = "https://id.twitch.tv/oauth2/token"
    response_get_oauth = session.post(url_get_oauth, params=params_get_oauth)
    response_get_oauth_json = response_get_oauth.json()
    return response_get_oauth_json["access_token"]


def get_userid(username, headers):  # This method gets twitch user id using username
    params_get_userid = {"login": username}
    url_get_userid = "https://api.twitch.tv/helix/users"
    response_get_userid = session.get(
        url_get_userid, params=params_get_userid, headers=headers
    )
    reponse_get_userid_json = response_get_userid.json()
    return reponse_get_userid_json["data"][0]["id"]


def get_videos(
    userid_var, headers, videos_title_list, videos_url_list, cursor=None
):  # This method gets all vod urls and creates 2 lists - vod names and urls
    params_get_videos = {("user_id", userid_var)}
    if cursor is not None:
        params_get_videos = list(params_get_videos) + list({("after", cursor)})
    url_get_videos = "https://api.twitch.tv/helix/videos"
    response_get_videos = session.get(
        url_get_videos, params=params_get_videos, headers=headers
    )
    reponse_get_videos_json = response_get_videos.json()
    for i in range(0, len(reponse_get_videos_json["data"])):
        videos_desc_from_json = (
            reponse_get_videos_json["data"][i]["title"]
            + " "
            + reponse_get_videos_json["data"][i]["created_at"]
        )
        videos_desc_from_json_no_special_chars = re.sub(
            "[^A-Za-z0-9]+", " ", videos_desc_from_json
        )
        videos_title_list.append(videos_desc_from_json_no_special_chars)
        videos_url_list.append(reponse_get_videos_json["data"][i]["url"])
    if "cursor" in reponse_get_videos_json["pagination"]:
        get_videos(
            userid_var,
            headers,
            videos_title_list,
            videos_url_list,
            reponse_get_videos_json["pagination"]["cursor"],
        )


def download_videos(
    video_desc, video_url
):  # This method lets you download all vods 1 by 1
    user_input = input("Do you want to download all VODs? (y/n): ")
    if user_input == "y":
        for i in range(0, len(video_url)):
            stream = streamlink.streams(video_url[i])["best"].url
            download = subprocess.Popen(
                ["streamlink","--hls-segment-threads", "4", "-o", video_desc[i] + ".mkv", stream, "best"]
            )
            download.wait()
    elif user_input == "n":
        return 0
    else:
        print("Wrong choice, start again")
        download_videos(video_desc, video_url)