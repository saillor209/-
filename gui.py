import webbrowser
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.filedialog import *
from datetime import *
import ffmpeg
import preferences

# 프로그램 종료시 실행되는 함수
def close_program():
    preferences.save_config()
    root.destroy()

# 로그 출력 함수
def print_log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_message = f"\n{timestamp}\n{message}"
    
    log_text.config(state="normal")  # 편집 가능하게 설정
    log_text.insert(END, log_message)  # 로그 추가
    log_text.config(state="disabled")  # 다시 읽기 전용으로 설정
    if preferences.log_auto_scroll: log_text.yview(END)  # yviw(END) = 스크롤을 가장 아래로 이동

# 새 윈도우를 중앙에 오도록 위치 계산해주는 함수
def center_calc(window_width, window_height, offset):

    # root 창의 위치와 크기 가져오기
    root_x = root.winfo_x()  # root 창의 X 좌표
    root_y = root.winfo_y()  # root 창의 Y 좌표
    root_width = root.winfo_width()  # root 창의 가로 크기
    root_height = root.winfo_height()  # root 창의 세로 크기
    
    # 중앙 좌표 계산
    x_position = root_x + (root_width - window_width) // 2
    y_position = root_y + (root_height - window_height) // 2 + offset  # offset = 보정값(낮을수록 창이 올라감)
    return window_width, window_height, x_position, y_position

# 해상도
window_width = 640
window_height = 480

root = Tk()  # 메인 GUI 창 생성

# 메인 디스플레이 해상도 가져오기
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 중앙 좌표 계산
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")  # 창의 위치 설정
root.resizable(False, False)  # 창 크기 조절 불가능

ico = ("./assets/hk4e_global.ico")
root.iconbitmap(ico)  # 아이콘 지정

root.title("Upscaler")  # 창 제목 설정

## 로그 출력 창 (ScrolledText)
# bg="배경색상", fg="폰트색상", insertbackground="배경에 들어온 커서 색상", width=문자가로, height=문자세로, state="편집가능여부"
log_text = ScrolledText(root, bg="black", fg="white", insertbackground="white", width=10, height=10, state="normal")
# padx=가로여백, pady=세로여백, fill=빈공간 채우는 방식, expand=창에 따른 위젯 크기 조정
log_text.pack(padx=12, pady=12, fill=BOTH, expand=True)
log_text.insert(END, f"{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")}\nHi")
log_text.config(state="disabled")
if preferences.log_auto_scroll: log_text.yview(END)

   ### Front Panel ###

# Front Panel - Clear
def clear_log():
    log_text.config(state="normal")
    log_text.delete("1.0", END)  # 첫 번째 문자(1.0)부터 끝(END)까지 삭제
    log_text.insert(END, f"{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")}\nThe log has been cleared.")
    log_text.config(state="disabled")

# 로그 테스트 버튼
log_button = Button(root, text="log_test", command=lambda: print_log("Hi"))
log_button.pack(side=LEFT, padx=(12, 0), pady=(0, 12))
# 스탑 버튼(아직 기능이 없음 ㅋㅋ)
stop_button = Button(root, text="Stop", command=print_log)
stop_button.pack(side=LEFT, padx=(12, 0), pady=(0, 12))
# Clear Log
clear_button = Button(root, text="Claer", command=clear_log)
clear_button.pack(side=RIGHT, padx=(0, 12), pady=(0, 12))
# 오토 스크롤 체크박스(어작 기능이 업음 ㅋㅋㅋ)
auto_scroll_checkbox = Checkbutton(root, text="Auto Scroll", variable=preferences.log_auto_scroll)
auto_scroll_checkbox.pack(side=RIGHT, padx=(0, 12), pady=(0, 12))

# 메뉴 바
menu_bar = Menu(root)  # 메뉴 바 생성
root.config(menu=menu_bar)  # 메뉴 바를 창에 적용

    ### File 메뉴 ###

# File - Prefernces method
def file_preference():
    width, height, x, y = center_calc(500, 400, 25)
    prefer = Toplevel(root)
    prefer.geometry(f"{width}x{height}+{x}+{y}")
    prefer.resizable(False, False)
    prefer.transient(root)
    prefer.grab_set()
    prefer.iconbitmap(ico)
    prefer.title("Preferences")
    prefer.mainloop()

# FIle 메뉴 생성
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Preferences", command=file_preference)
file_menu.add_separator() # 구분선 생성
file_menu.add_command(label="Quit", command=close_program)

    ### Edit 메뉴 ###

# Select input path...
def edit_select_input_path():
    path = askdirectory(title="Select the path of the video...")
    preferences.video_input_path = path
    print_log(f"The input path \"{path}\" has been selected.")

# Select output path...
def edit_select_output_path():
    path = askdirectory(title="Select the path of the video...")
    preferences.video_output_path = path
    print_log(f"The output path \"{path}\" has been selected.")

def input_print():
    print(preferences.video_input_path)
    print(preferences.video_output_path)

# Edit 메뉴 생성
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Select input path...", command=edit_select_input_path)
edit_menu.add_command(label="Select output path...", command=edit_select_output_path)
edit_menu.add_separator()
edit_menu.add_command(label="test", command=input_print)

    ### Help 메뉴 ###

# Help - Information... 실행
def help_information():
    width, height, x, y = center_calc(400, 130, 15)
    about = Toplevel(root)
    about.geometry(f"{width}x{height}+{x}+{y}")
    about.resizable(False, False)
    about.transient(root)  # 메인 창과 연관되도록 설정
    about.grab_set()  # info 창이 닫히기 전까지 다른 창 클릭 방지
    about.iconbitmap(ico)
    about.title("Information...")
    # 텍스트 라벨
    text = Label(about, text="This software is licensed under GNU AGPL version 3.\nCopyright (C) 2025 saillor209.\nSource code is available on GitHub.")
    text.pack(padx=12, pady=(12, 0))
    # Close 버튼
    close = Button(about, text="Close", command=about.destroy)
    close.pack(side=BOTTOM, pady=(0, 12))

    about.mainloop()

# Help - Report Bugs... 실행
def help_bug():
    webbrowser.open("https://github.com/saillor209/Upscaler/issues")  # 기본 웹 브라우저에서 URL 열기

# Help 메뉴 생성
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Report Bugs...", command=help_bug)
help_menu.add_separator()
help_menu.add_command(label="Information...", command=help_information)

    ### Debug 메뉴 ###

def tet():
    preferences.set_default()
    print(preferences.video_input_path)
    preferences.print_settings()

# Debug 메뉴 생성
debug_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Debug", menu=debug_menu)
debug_menu.add_command(label="preferences.set_default", command=tet)
debug_menu.add_separator()
# ffmpeg.split 테스트!!!!!!!!!!!!!
debug_menu.add_command(label="ffmpeg.split", command=ffmpeg.split)
# ffmpeg.get_preferences 테스트!!!!!!!!!!!!!
debug_menu.add_command(label="ffmpeg.get_preferences", command=ffmpeg.get_preferences)


root.protocol("WM_DELETE_WINDOW", close_program)  # 종료 시 close_program() 실행
root.mainloop()  # 창 유지