

from googleapiclient.discovery import build
from pytube import YouTube
import os

#pip install google-api-python-client pytube


os.environ["http_proxy"] = "http://127.0.0.1:7897"
os.environ["https_proxy"] = "http://127.0.0.1:7897"
# 替换为你的API密钥
API_KEY = 'AIzaSyDzGsBXFVcjwPLv7Cd8P9-dor0E9OO9axM'

# 构建YouTube API服务对象
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 调用YouTube API获取热门视频
request = youtube.videos().list(
    part='snippet,statistics',
    chart='mostPopular',
    regionCode='US',  # 可以根据需要更改地区代码
    maxResults=1
)
response = request.execute()

# 创建下载目录
download_directory = "youtube_downloads"
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# 解析并下载视频
for item in response['items']:
    video_id = item['id']
    title = item['snippet']['title']
    channel = item['snippet']['channelTitle']
    views = item['statistics']['viewCount']
    print(f'Title: {title}, Channel: {channel}, Views: {views}')
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        print(f'Downloading: {title}')
        stream.download(download_directory)
        print(f'Downloaded: {title}')
    except Exception as e:
        print(f'Error downloading {title}: {e}')
