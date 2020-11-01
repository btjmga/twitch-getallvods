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
    g_oa_response = session.post(url_get_oauth, params=params_get_oauth)
    g_oa_reponse_json = g_oa_response.json()
    return g_oa_reponse_json["access_token"]


def get_userid(
    g_us_username, g_us_headers
):  # This method gets twitch user id using username
    g_us_params = {"login": g_us_username}
    g_us_userid = "https://api.twitch.tv/helix/users"
    g_us_response = session.get(
        g_us_userid, params=g_us_params, headers=g_us_headers
    )
    g_us_response_json = g_us_response.json()
    return g_us_response_json["data"][0]["id"]


def populate_lists(
    p_li_json,
    p_li_title_list,
    p_li_url_list,
):  # this method comes from previous get_videos method
    for i in range(0, len(p_li_json["data"])):
        p_li_video_desc = (
            p_li_json["data"][i]["title"] + " " + p_li_json["data"][i]["created_at"]
        )
        p_li_video_desc_parse = re.sub(
            "[^A-Za-z0-9]+", " ", p_li_video_desc
        )
        p_li_title_list.append(p_li_video_desc_parse)
        p_li_url_list.append(p_li_json["data"][i]["url"])


def get_videos(
    g_vi_userid,
    g_vi_headers,
    g_vi_title_list,
    g_vi_url_list,
    cursor=None,
):  # This method gets all vod urls and creates 2 lists - vod names and urls
    g_vi_params = {("user_id", g_vi_userid)}
    if cursor is not None:
        g_vi_params = list(g_vi_params) + list({("after", cursor)})
    g_vi_url = "https://api.twitch.tv/helix/videos"
    g_vi_response = session.get(
        g_vi_url, params=g_vi_params, headers=g_vi_headers
    )
    g_vi_response_json = g_vi_response.json()
    populate_lists(g_vi_response_json, g_vi_title_list, g_vi_url_list)
    if "cursor" in g_vi_response_json["pagination"]:
        get_videos(
            g_vi_userid,
            g_vi_headers,
            g_vi_title_list,
            g_vi_url_list,
            g_vi_response_json["pagination"]["cursor"],
        )


def download_videos(
    d_vi_description, d_vi_url
):  # This method lets you download all vods 1 by 1
    d_vi_user_input = input("Do you want to download all VODs? (y/n): ")
    if d_vi_user_input == "y":
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
    elif d_vi_user_input == "n":
        return 0
    else:
        print("Wrong choice, start again")
        download_videos(d_vi_description, d_vi_url)
