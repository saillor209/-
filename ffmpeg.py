import os
import subprocess
import glob
import preferences
# import math

# ffmpeg 경로 저장
ffmpeg_path = "./assets/ffmpeg/bin/ffmpeg.exe"
ffprobe_path = "./assets/ffmpeg/bin/ffprobe.exe"

# preferences에서 저장된 설정 받아오기
def get_preferences():
    input = preferences.video_input_path
    output = preferences.video_output_path
    # 하드웨어 가속 세팅
    if preferences.ffmpeg_hwaccel == True:  
        calc = preferences.ffmpeg_calc_method
    else:
        calc = None
    # 코덱 세팅
    if preferences.ffmpeg_hwaccel == True and preferences.ffmpeg_codec == "265":
        codec = "evc"
    else: codec = "264"

    if preferences.ffmpeg_calc_method == "cpu":
        codec = f"libx{preferences.ffmpeg_codec}"
    elif preferences.ffmpeg_calc_method == "cuda":
        codec = f"h{codec}_nvenc"
    elif preferences.ffmpeg_calc_method == "qsv":
        codec = f"h{codec}_qsv"

    return input, output, calc, codec

### 비디오의 프레임 나누기 ###
def split():
    # get_preferences
    input_path, _, calc_method, _ = get_preferences()

    # glob을 사용하여 다양한 확장자의 비디오 파일을 찾음
    video_files = glob.glob(os.path.join(input_path, '*.mp4')) + \
              glob.glob(os.path.join(input_path, '*.avi')) + \
              glob.glob(os.path.join(input_path, '*.mov')) + \
              glob.glob(os.path.join(input_path, '*.mkv')) + \
              glob.glob(os.path.join(input_path, '*.webm'))

    for video in video_files:
        # 비디오 파일 이름 받기
        video_name = os.path.basename(video)
    
        # 출력 폴더 경로 지정 (./.temp 안에 비디오 이름으로 폴더 생성)
        frame_out_path = os.path.join("./.temp", f"{video_name}")
    
        # 출력 폴더가 없으면 생성
        if not os.path.exists(frame_out_path):
            os.makedirs(frame_out_path)


        ## FPS값 추출 ##
        command_find_fps = [
            ffprobe_path, 
            '-v', 'error', 
            '-select_streams', 'v:0', 
            '-show_entries', 'stream=r_frame_rate', 
            '-of', 'default=noprint_wrappers=1', video
        ]

        print("[FFmpeg]", " ".join(command_find_fps))
        result = subprocess.run(command_find_fps, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
        # r_frame_rate 값 추출 (형식: r_frame_rate=numerator/denominator)
        r_frame_rate = result.stdout.strip().split('=')[1]  # 例: 'r_frame_rate=30000/1001'에서 '30000/1001'만 추출
    
        # 분자와 분모로 나누어 FPS 계산
        numerator, denominator = map(int, r_frame_rate.split('/'))
        # fps = math.ceil(numerator / denominator)  # 분자, 분모 나눈 후 소수점 올림 (math.ceil = 올림, math.floor = 내림)
        #   ㄴ 이거 굳이 정수로 안해도 프레임 잘 뽑아내던데 굳이 해야하나????
        fps = numerator / denominator
        print(f"[FFmpeg] FPS of the video is {fps}")


        ## 비디오의 프레임을 이미지 파일로 저장 ##
        command_split =[
            ffmpeg_path,
            "-i", video,  # 입력 비디오 파일
            "-vf", f"fps={fps}",  # Frames Per Second
            os.path.join(frame_out_path, '%06d.jpg')  # 저장할 이미지 형식 (6자리 숫자 이미지 파일)
            ]
        if calc_method != None:  # calc_method가 None이 아닐 때만 추가
            command_split.insert(1, "-hwaccel")
            command_split.insert(2, calc_method)
        
        # 로그
        print("Splitting the video based on the frame rate.")
        print(f"[FFmpeg] {' '.join(command_split)}")

        subprocess.run(command_split)  # FFmpeg_split 명령어 실행