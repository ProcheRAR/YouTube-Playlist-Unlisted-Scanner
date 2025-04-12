from googleapiclient.discovery import build

# Replace with your YouTube Data API key
API_KEY = 'YOUR_API_KEY'

# Initialize YouTube API service
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_playlist_videos(playlist_id):
    """Fetch all video IDs and titles from a YouTube playlist."""
    videos = []
    next_page_token = None

    # Handle pagination for playlists with >50 videos
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # Maximum allowed per API request
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract video metadata
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_title = item['snippet']['title']
            videos.append((video_id, video_title))

        # Check for more pages
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def check_video_availability(video_id):
    """Verify if a video is unlisted via its privacy status."""
    request = youtube.videos().list(
        part='status',
        id=video_id
    )
    response = request.execute()

    # Handle potential missing video edge case
    if response.get('items'):
        status = response['items'][0]['status']
        return status['privacyStatus'] == 'unlisted'
    return False

def main():
    # Get playlist ID from user input
    playlist_url = input("Enter playlist URL: ")
    playlist_id = playlist_url.split('list=')[1]

    # Retrieve and analyze videos
    videos = get_playlist_videos(playlist_id)
    print(f"Found {len(videos)} videos in playlist.")

    # Identify unlisted content
    unlisted_videos = []
    for video_id, video_title in videos:
        if check_video_availability(video_id):
            unlisted_videos.append((video_id, video_title))

    # Display results
    if unlisted_videos:
        print("\nUnlisted videos detected:")
        for video_id, video_title in unlisted_videos:
            print(f"Title: {video_title}\nURL: https://www.youtube.com/watch?v={video_id}\n")
    else:
        print("\nAll playlist videos are publicly accessible.")

if __name__ == "__main__":
    main()
