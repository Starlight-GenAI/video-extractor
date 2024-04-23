import re
import os
import base64
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def extract_video_id(url):
    regex_pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex_pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def get_video_subtitle(video_id):
    try:
        subtitle_list = YouTubeTranscriptApi.get_transcript(video_id)
        subtitle = []
        for title in subtitle_list:
            subtitle.append({'text': title['text'].encode("ascii", "ignore").decode().replace("\n", " "), 'start': title['start'], 'end': title['start'] + title['duration']})
        return subtitle
    except Exception as e:
        raise e

def download(url, id):
    filename = f'{id}_{extract_video_id(url)}.mp4'
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=filename)
        return filename
    except Exception as e:
        raise e

def get_video_in_base64_format(filename):
    try:
        with open(filename, 'rb') as f:
            text = base64.b64encode(f.read())
            os.remove(filename)
        return str(text)
    except Exception as e:
        raise e
        