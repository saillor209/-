import json
import os

def print_settings():
    print(f"{log_auto_scroll}, {video_input_path}")

## 모든 설정을 기본 값으로 설정하는 함수
def set_preferences(preset = "default"):
    global log_auto_scroll, video_input_path, video_output_path, ffmpeg_calc_method, ffmpeg_hwaccel, ffmpeg_codec, realcugan_model  # 전역변수 설정
    if preset == "default":
        ## GUI 설정
        log_auto_scroll = True
        ## 경로 설정
        video_input_path = "./.Videos"
        video_output_path = "./.Results"
        ## FFmpeg 설정
        ffmpeg_calc_method = "cpu"  # cpu (hwaccel = False) / cuda (Nvidia) / qsv (Intel Quick Sync)
        if ffmpeg_calc_method == "cpu": ffmpeg_hwaccel = False
        else: ffmpeg_hwaccel = True  # 연산 주체가 cpu라면 하드웨어 가속은 False가 되어야 합니다.
        ffmpeg_codec = "264"  # 264 (H.264) / 265 (H.265)
        ### realcugan 설정 ###
        realcugan_model = "model_pro"  # model_pro / model_se
    else:
        with open(f"./configs/{preset}.json", "r", encoding="utf-8") as f:
            config = json.load(f)  # JSON 내용을 딕셔너리로 변환
        log_auto_scroll = config["log_auto_scroll"]
        video_input_path = config["video_input_path"]
        video_output_path = config["video_output_path"]
        ffmpeg_calc_method = config["ffmpeg_calc_method"]
        ffmpeg_codec = config["ffmpeg_codec"]
        realcugan_model = config["realcugan_model"]

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

if not os.path.exists("configs"):  # configs 경로 없으면 생성
    os.makedirs("configs")

if not os.path.exists("./configs/config.json"):  # config.json 파일 미존재 시 기본값
    set_preferences()
else:  # config.json 파일 존재 시 불러오기
    set_preferences("config")