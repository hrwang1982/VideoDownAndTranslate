from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os


def create_audio_from_text(text, filename):
    tts = gTTS(text, lang='zh')
    tts.save(filename)
    return filename


def create_image_from_text(text, filename, image_size=(1280, 720), font_size=50):
    image = Image.new('RGB', image_size, color=(255, 255, 255))
    font = ImageFont.truetype("arial.ttf", font_size)
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
    draw.text(text_position, text, fill=(0, 0, 0), font=font)
    image.save(filename)
    return filename


def create_video_clip(text, image_path, duration):
    audio_filename = create_audio_from_text(text, 'temp_audio.mp3')
    audio_clip = AudioFileClip(audio_filename)
    image_clip = ImageClip(image_path, duration=audio_clip.duration).set_audio(audio_clip)

    return image_clip


def create_recipe_video(steps, images, output_filename):
    clips = []
    for step, image in zip(steps, images):
        clip = create_video_clip(step, image, duration=5)
        clips.append(clip)

    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(output_filename, fps=24)

    # Clean up temporary files
    for clip in clips:
        clip.audio.close()
    os.remove('temp_audio.mp3')


# Example usage
steps = [
    "首先，准备好鸡胸肉、花生、青椒、红椒、姜蒜等食材。",
    "将鸡胸肉切丁，用淀粉和酱油腌制。",
    "热锅凉油，放入姜蒜爆香。",
    "加入鸡丁翻炒至变色，然后加入青红椒继续翻炒。",
    "加入酱汁和花生，翻炒均匀。",
    "最后，出锅装盘，美味的宫保鸡丁就做好了。"
]

# 示例图像文件路径，可以替换为实际的图片路径
images = [
    "step1.jpg",
    "step2.jpg",
    "step3.jpg",
    "step4.jpg",
    "step5.jpg",
    "step6.jpg"
]

create_recipe_video(steps, images, 'gongbao_jiding.mp4')
