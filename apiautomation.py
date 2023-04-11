import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import cs50

db = cs50.SQL("sqlite:///videos.db")

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "googleclient.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=8080)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    x = input("Which video queries do you want to store in a database?") # Apple for this project
    
    token = ""
    for _ in range(10):
        request = youtube.search().list(
            part="id,snippet",
            q=x,
            type="video",
            maxResults=50,
            pageToken=token
        )
        response = request.execute()
        token = response["nextPageToken"]
        
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"].replace('&quot;', '"').replace('&#39;', "'").replace('&amp;', '&')
            video_description = item["snippet"]["description"]
            video_thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
            channel_title = item['snippet']['channelTitle']
            
            try:
                db.execute("INSERT INTO videos (video_id, title, description, thumbnail,channel) VALUES (?, ?, ?, ?,?)", video_id, video_title, video_description, video_thumbnail, channel_title)
            except ValueError:
                print("oopsie")

if __name__ == "__main__":
    main()
