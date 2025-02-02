import json
import os

def print_settings():
    print(f"{log_auto_scroll}, {video_input_path}")

## 모든 설정을 기본 값으로 설정하는 함수
def set_default():
    global log_auto_scroll, video_input_path, video_output_path, ffmpeg_calc_method, ffmpeg_hwaccel, ffmpeg_codec, realcugan_model
    log_auto_scroll = True
    video_input_path = "./.Videos"
    video_output_path = "./.Results"
    ffmpeg_calc_method = "cpu"
    ffmpeg_hwaccel = False if ffmpeg_calc_method == "cpu" else True
    ffmpeg_codec = "264"
    realcugan_model = "model_pro"

## 프로그램 종료 시 config.json을 저장함.
def save_config(filename="./configs/config.json"):
    data = {
        "log_auto_scroll": log_auto_scroll,
        "video_input_path": video_input_path,
        "video_output_path": video_output_path,
        "ffmpeg_calc_method": ffmpeg_calc_method,
        "ffmpeg_codec": ffmpeg_codec,
        "realcugan_model": realcugan_model
        }
    """주어진 데이터를 JSON 파일에 저장하는 함수"""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

## 최초 preferences 설정
if os.path.exists("./configs/config.json"):  # config.json 파일 존재 시 config.json을 불러옴
    with open("./configs/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)  # JSON 내용을 딕셔너리로 변환
    ## GUI 설정
    log_auto_scroll = config["log_auto_scroll"]
    ## 경로 설정
    video_input_path = config["video_input_path"]
    video_output_path = config["video_output_path"]
    ## FFmpeg 설정
    ffmpeg_calc_method = config["ffmpeg_calc_method"]# cpu (hwaccel = False) / cuda (Nvidia) / qsv (Intel Quick Sync)
    if ffmpeg_calc_method == "cpu": ffmpeg_hwaccel = False
    else: ffmpeg_hwaccel = True  # 연산 주체가 cpu라면 하드웨어 가속은 False가 되어야 합니다.
    ffmpeg_codec = config["ffmpeg_codec"]  # 264 (H.264) / 265 (H.265)
    ### realcugan 설정 ###
    realcugan_model = config["realcugan_model"]  # model_pro / model_se
else: set_default()