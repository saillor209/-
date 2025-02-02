import json

# 최초 config.json 파일 읽기
with open("./configs/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)  # JSON 내용을 딕셔너리로 변환


### 경로 설정 ###
#video_input_path = "./.Videos"
#video_output_path = "./.Results"

video_input_path = config["video_input_path"]
video_output_path = config["video_output_path"]

### ffmpeg 설정 ###
ffmpeg_hwaccel_method = "soft"  # Default = soft (hwaccel = False) / cuda (Nvidia) / qsv (Intel Quick Sync)
if ffmpeg_hwaccel_method == "soft": ffmpeg_hwaccel = False
else: ffmpeg_hwaccel = True  #  False  # Default = False (하드웨어 가속이 False라면 ffmpeg_hwaccel_method는 Soft가 되어야 합니다.)
ffmpeg_codec = config["ffmpeg_codec"]  # Default = 264 (H.264) / 265 (H.265)

### realcugan 설정 ###
realcugan_model = config["realcugan_model"]  # Default = model_pro / model_se
print(realcugan_model)
print(video_input_path)