### 경로 설정 ###
video_input_path = "./.Videos"
video_output_path = "./.Results"

### ffmpeg 설정 ###
ffmpeg_hwaccel_method = "soft"  # Default = Soft (hwaccel = False) / cuda (Nvidia) / qsv (Intel Quick Sync)
if ffmpeg_hwaccel_method == "soft": ffmpeg_hwaccel = False
else: ffmpeg_hwaccel = True  #  False  # Default = False (하드웨어 가속이 False라면 ffmpeg_hwaccel_method는 Soft가 되어야 합니다.)
ffmpeg_codec = "265"  # Default = 264 (H.264) / 265 (H.265)