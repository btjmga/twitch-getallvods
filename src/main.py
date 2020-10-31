from twitch_getallvods import *

# static variables
clientID = ""
clientSecret = ""
username = ""

# dynamic variables
token = get_oauth(clientID, clientSecret)
headers = {"Authorization": "Bearer " + token, "Client-Id": clientID}
userID = get_userid(username, headers)
videos_titles = []
videos_urls = []

get_videos(
    userID, headers, videos_titles, videos_urls
)  # populate videos_titles and videos_urls

download_videos(videos_titles, videos_urls)  # download? yes/no
