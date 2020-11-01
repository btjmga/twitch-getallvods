import re
import subprocess
import requests
import streamlink

session = requests.Session()


def get_oauth(g_oa_client_id, g_oa_client_secret):  # This method gets the auth token
    params_get_oauth = {
        "client_id": g_oa_client_id,
        "client_secret": g_oa_client_secret,
        "grant_type": "client_credentials",
        "scope": "clips:edit",
    }
    url_get_oauth = "https://id.twitch.tv/oauth2/token"
    response_get_oauth = session.post(url_get_oauth, params=params_get_oauth)
    response_get_oauth_json = response_get_oauth.json()
    return response_get_oauth_json["access_token"]


def get_userid(
    g_us_username, g_us_headers
):  # This method gets twitch user id using username
    params_get_userid = {"login": g_us_username}
    url_get_userid = "https://api.twitch.tv/helix/users"
    response_get_userid = session.get(
        url_get_userid, params=params_get_userid, headers=g_us_headers
    )
    reponse_get_userid_json = response_get_userid.json()
    return reponse_get_userid_json["data"][0]["id"]


def populate_lists(
    p_li_json,
    p_li_title_list,
    p_li_url_list,
):  # this method comes from previous get_videos method
    for i in range(0, len(p_li_json["data"])):
        videos_desc_from_json = (
            p_li_json["data"][i]["title"] + " " + p_li_json["data"][i]["created_at"]
        )
        videos_desc_from_json_no_special_chars = re.sub(
            "[^A-Za-z0-9]+", " ", videos_desc_from_json
        )
        p_li_title_list.append(videos_desc_from_json_no_special_chars)
        p_li_url_list.append(p_li_json["data"][i]["url"])


def get_videos(
    g_vi_userid,
    g_vi_headers,
    g_vi_title_list,
    g_vi_url_list,
    cursor=None,
):  # This method gets all vod urls and creates 2 lists - vod names and urls
    params_get_videos = {("user_id", g_vi_userid)}
    if cursor is not None:
        params_get_videos = list(params_get_videos) + list({("after", cursor)})
    url_get_videos = "https://api.twitch.tv/helix/videos"
    response_get_videos = session.get(
        url_get_videos, params=params_get_videos, headers=g_vi_headers
    )
    reponse_get_videos_json = response_get_videos.json()
    populate_lists(reponse_get_videos_json, g_vi_title_list, g_vi_url_list)
    if "cursor" in reponse_get_videos_json["pagination"]:
        get_videos(
            g_vi_userid,
            g_vi_headers,
            g_vi_title_list,
            g_vi_url_list,
            reponse_get_videos_json["pagination"]["cursor"],
        )


def download_videos(
    d_vi_description, d_vi_url
):  # This method lets you download all vods 1 by 1
    user_input = input("Do you want to download all VODs? (y/n): ")
    if user_input == "y":
        for i in range(0, len(d_vi_url)):
            stream = streamlink.streams(d_vi_url[i])["best"].url
            download = subprocess.Popen(
                [
                    "streamlink",
                    "--hls-segment-threads",
                    "4",
                    "-o",
                    d_vi_description[i] + ".mkv",
                    stream,
                    "best",
                ]
            )
            download.wait()
    elif user_input == "n":
        return 0
    else:
        print("Wrong choice, start again")
        download_videos(d_vi_description, d_vi_url)
