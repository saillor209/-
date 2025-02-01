import os
import subprocess
import glob
import preferences

# ffmpeg 경로 받기
ffmpeg_path = "./assets/ffmpeg/bin/ffmpeg.exe"

# preferences에서 저장된 설정 받아오기
def get_preferences():
    input = preferences.video_input_path
    output = preferences.video_output_path
    # 하드웨어 가속 세팅
    if preferences.ffmpeg_hwaccel == True:  
        calc = preferences.ffmpeg_hwaccel_method
    else:
        calc = None
    # 코덱 세팅
    if preferences.ffmpeg_hwaccel_method == "soft":
        codec = f"libx{preferences.ffmpeg_codec}"
    elif preferences.ffmpeg_hwaccel_method == "cuda":
        codec = f"h{preferences.ffmpeg_codec}_nvenc"
    elif preferences.ffmpeg_hwaccel_method == "qsv":
        codec = f"h{preferences.ffmpeg_codec}_qsv"

    return input, output, calc, codec

### 비디오의 프레임 나누기 ###
def split():
    # get_preferences
    input_path, output_path, calc_method, codec = get_preferences()

    # glob을 사용하여 다양한 확장자의 비디오 파일을 찾음
    video_files = glob.glob(os.path.join(input_path, '*.mp4')) + \
              glob.glob(os.path.join(input_path, '*.avi')) + \
              glob.glob(os.path.join(input_path, '*.mov')) + \
              glob.glob(os.path.join(input_path, '*.mkv')) + \
              glob.glob(os.path.join(input_path, '*.webm'))

    for video in video_files:
        # 비디오 파일 이름 받기
        video_name = os.path.basename(video)
    
        # 출력 폴더 경로 지정 (output_path 안에 비디오 이름으로 폴더 생성)
        output_folder = os.path.join(f"{output_path}/.temp", f"ffmpeg_split_{video_name}")
    
        # 출력 폴더가 없으면 생성
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

            # FFmpeg 명령어로 비디오의 FPS 정보 얻기
        command_fps = [
        ffmpeg_path,
        "-i", video,
        "-hide_banner"
        ]
    
        # FPS 추출을 위해 FFmpeg 명령어 실행
        fps_output = subprocess.run(command_fps, capture_output=True, text=True)
    
        # FPS 값 파싱 (정규 표현식으로 FFmpeg의 출력에서 FPS 값 추출)
        fps = None
        for line in fps_output.stderr.split('\n'):
            if 'fps' in line:
                # FPS 값을 찾은 경우, 값을 파싱하여 추출
                fps = float(line.split('fps')[0].strip().split()[-1])
            break

    if fps is None:
        print(f"[FFmpeg] Info: FPS not found for {video}. Using default fps=30.")
        fps = 30  # FPS 정보를 찾을 수 없으면 기본값을 30으로 설정
    
        # FFmpeg 명령어로 비디오의 프레임을 이미지 파일로 저장
        command_split =[
            ffmpeg_path,
            "-i", video,  # 입력 비디오 파일
            "-vf", f"fps={fps}",  # Frames Per Second
            os.path.join(output_folder, '%06d.jpg')  # 저장할 이미지 형식 (6자리 숫자 이미지 파일)
            ]
        if calc_method != None:  # calc_method가 None이 아닐 때만 추가
            command_split.insert(1, "-hwaccel")
            command_split.insert(2, calc_method)
        
        print("[FFmpeg] Splitting the video based on the frame rate:", " ".join(command_split))

        subprocess.run(command_split)  # FFmpeg_split 명령어 실행