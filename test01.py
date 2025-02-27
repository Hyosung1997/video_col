from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient


def process_video():
    # 1. 读取视频
    video_origin = VideoFileClip("clip.mp4", audio=False).subclip(0, 30)  # 截取10-30秒
    # 2. 裁剪视频 (左, 上, 右, 下)
    video = video_origin.crop(x1=video_origin.w/2 - (video_origin.h/16*9/2), y1=0, x2=video_origin.w/2 + (video_origin.h/16*9/2), y2=video_origin.h)
    # 3. 旋转视频90度
    # video = video.rotate(90)
    # 水平翻转视频
    video = video.fx(vfx.mirror_x)
    # 4. 调整播放速度（0.8倍速）
    # video = video.fx(vfx.speedx, 0.8)
    # 5. 添加背景音乐
    audio = AudioFileClip("bg_music.mp3").subclip(0, video.duration)
    final_clip = video.set_audio(audio)
    # 6. 添加字幕
    txt_clip = (TextClip("“才感盛夏，忽而已秋”", fontsize=30, color='white', font=r'./font/simfang.ttf')
                .set_position('center')
                .set_duration(20)  # 显示前5秒
                .set_start(10))
    # 7. 添加图片水印
    img_clip = (ImageClip("sign_.png")
                .set_duration(final_clip.duration)
                .resize(width=150)  # 调整宽度
                .margin(right=10, top=10, opacity=0)  # 右侧10像素，顶部10像素
                .set_pos(("right", "top")))
    # 8. 创建渐变动画
    gradient = color_gradient(video_origin.size, p1=(0, 0), p2=(video_origin.w, 0),
                              col1=[0, 0, 0], col2=[255, 255, 0], offset=0.5)
    gradient_clip = ImageClip(gradient, duration=2).set_start(5).crossfadein(1)
    # 合并所有元素
    final = CompositeVideoClip([final_clip, txt_clip, img_clip, gradient_clip])
    # 导出视频
    final.write_videofile("output.mp4",
                          codec='libx264',
                          audio_codec='aac',
                          fps=60,
                          threads=4)  # 使用多线程加速

if __name__ == "__main__":
    process_video()
