import os
import subprocess
import glob
import preferences

# ffmpeg 경로 받기
ffmpeg_path = "./assets/ffmpeg/bin/ffmpeg.exe"

# preferences에서 지정된 설정 받아오기
def get_preferences():
    input = preferences.video_input_path
    output = preferences.video_output_path

### 비디오의 프레임 나누기 ###
def split():
    # 인코더, 디코더 지정

    # preferences.py에서 input, output 받기
    input_path = preferences.video_input_path
    output_path = preferences.video_output_path

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
    
        # FFmpeg 명령어로 비디오의 프레임을 이미지 파일로 저장
        command =[
            ffmpeg_path,
            '-i', video,  # 입력 비디오 파일
            '-vf', 'fps=1',  # 초당 1프레임 추출
            os.path.join(output_folder, '%06d.jpg')  # 저장할 이미지 형식 (6자리 숫자 이미지 파일)
            ]
        
        subprocess.run(command)  # FFmpeg 명령어 실행