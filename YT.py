from googleapiclient.discovery import build

# Ваш API ключ
API_KEY = 'YOUR_API_KEY'

# Создание сервиса YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_playlist_videos(playlist_id):
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_title = item['snippet']['title']
            videos.append((video_id, video_title))

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def check_video_availability(video_id):
    request = youtube.videos().list(
        part='status',
        id=video_id
    )
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        status = response['items'][0]['status']
        return status['privacyStatus'] == 'unlisted'
    return False

def main():
    playlist_url = input("Введите ссылку на плейлист: ")
    playlist_id = playlist_url.split('list=')[1]

    videos = get_playlist_videos(playlist_id)

    print(f"Найдено {len(videos)} видео в плейлисте.")

    unlisted_videos = []

    for video_id, video_title in videos:
        if check_video_availability(video_id):
            unlisted_videos.append((video_id, video_title))

    if unlisted_videos:
        print("Следующие видео доступны только по ссылке:")
        for video_id, video_title in unlisted_videos:
            print(f"Название: {video_title}, Ссылка: https://www.youtube.com/watch?v={video_id}")
    else:
        print("Все видео в плейлисте доступны публично.")

if __name__ == "__main__":
    main()
