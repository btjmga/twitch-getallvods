import requests


MyClientID = '###'
MyClientSecret = '###'
MyUsername = '###'

session = requests.Session()


def get_OAuth(client_id, client_secret):  # function to retrieve OAuth token needed to interact witch Twitch API
    params_get_oauth = {
        'client_id': client_id,  # client_id is available after registering an app
        'client_secret': client_secret,  # client_secret is available after registering an app
        'grant_type': 'client_credentials',  # Twitch API client credentials flow
        'scope': 'clips:edit'  # lowest possible scope since Twitch API for getting videos does not require any scope
    }
    url_get_oauth = 'https://id.twitch.tv/oauth2/token'  # URL to get OAuth token
    response_get_oauth = session.post(url_get_oauth, params=params_get_oauth)  # get the OAuth token
    response_get_oauth_json = response_get_oauth.json()  # parse json data
    return (response_get_oauth_json["access_token"])  # return the token


oauth_var = get_OAuth(MyClientID, MyClientSecret)  # define variable for speed

# authorization header
headers = {
    'Authorization': 'Bearer ' + oauth_var,
    'Client-Id': MyClientID
}


def get_userid(username):  # function to retrieve user id of given user
    params_get_userid = {'login': username}  # params for request.get
    url_get_userid = 'https://api.twitch.tv/helix/users'  # URL to request data
    response_get_userid = session.get(url_get_userid, params=params_get_userid, headers=headers)  # get the userid
    reponse_get_userid_json = response_get_userid.json()  # parse and interpret the data
    return (reponse_get_userid_json["data"][0]["id"])


userid_var = get_userid(MyUsername)  # define variable for speed


def get_videos(cursor=None):  # functiont to retrieve all vod URLs possible, kinda slow for now
    params_get_videos = {('user_id', userid_var)}  # params for request.get
    if cursor is not None:  # check if there was a cursor value passed
        params_get_videos = list(params_get_videos) + list({('after', cursor)})  # add another param for pagination
    url_get_videos = 'https://api.twitch.tv/helix/videos'  # URL to request data
    response_get_videos = session.get(url_get_videos, params=params_get_videos, headers=headers)  # get the data
    reponse_get_videos_json = response_get_videos.json()  # parse and interpret data
    for i in range(0, len(reponse_get_videos_json['data'])):  # parse and interpret data
        print(reponse_get_videos_json['data'][i]['url'])  # parse and interpret data
    if 'cursor' in reponse_get_videos_json['pagination']:  # check if there are more pages
        get_videos(reponse_get_videos_json['pagination']['cursor'])  # iterate the function until there are no more pages

