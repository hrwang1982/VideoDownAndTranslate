from moviepy.editor import VideoFileClip
import whisper
from googletrans import Translator
from moviepy.editor import TextClip, CompositeVideoClip
import os

#必须提前完成如下内容：
#1. pip install git+https://github.com/openai/whisper.git
#2. pip install googletrans==4.0.0-rc1
#3. 需要下载ffmpeg，并将可执行程序添加到系统的path路径中
#4. 需要下载安装imagemagick , https://www.imagemagick.org/script/download.php#windows
#   修改moviepy的config_defaults.py模块的配置，将如下内容：
#       IMAGEMAGIC_BINARY = os.getenv('IMAGEMAGICK_BINARY','auto-detect')
#    替换为：
#       IMAGEMAGIC_BINARY =r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'

os.environ["http_proxy"] = "http://127.0.0.1:7897"
os.environ["https_proxy"] = "http://127.0.0.1:7897"

# 加载视频文件
video = VideoFileClip("input_video.mp4")
w, h = video.w, video.h
# 提取音频
audio = video.audio
audio.write_audiofile("extracted_audio.wav")

# 加载 Whisper 模型  --model：tiny、base、small、medium、large，准确率耗时依次递增，首次执行会自动下载
model = whisper.load_model("large")

# 转录音频文件
result = model.transcribe("extracted_audio.wav")
transcribed_text = result["text"]
print("audio text----------------")
print(transcribed_text)

translator = Translator()

segments=result['segments']
l_subtitle= []
for seg in segments:
    start = seg['start']
    end = seg['end']
    text = seg['text']
    translated_text = translator.translate(text, src='en', dest='zh-cn').text
    subtitle= [round(start,2),round(end-start,2),translated_text]
    print(subtitle)
    l_subtitle.append(subtitle)



#print("translated text----------------")
#print(translated_text)

# 创建字幕
txts = []
for start, duration, text in l_subtitle:
    subtitle1 = (TextClip(text, fontsize=24, color='white', font='simhei.ttf', size=(w-20, 80), align='center').set_position('bottom').set_duration(duration).set_start(start))
    txts.append(subtitle1)

#subtitle = subtitle.set_duration(video.duration)
#subtitle = subtitle.set_position(('center', 'bottom'))


# 将字幕添加到视频
final_video = CompositeVideoClip([video, *txts])
final_video.write_videofile("translated_video.mp4", codec="libx264")
