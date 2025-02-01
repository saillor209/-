import webbrowser
from tkinter import *
import ffmpeg

# 해상도
window_width = 800
window_height = 600

ico = ("./assets/hk4e_global.ico")

root = Tk()  # 메인 GUI 창 생성

root.resizable(False, False)  # 창 크기 조절 불가능

# 메인 디스플레이 해상도 가져오기
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 중앙 좌표 계산
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")  # 창의 위치 설정
root.iconbitmap(ico)  # 아이콘 지정
root.title("Tkinter 예제")  # 창 제목 설정

# 텍스트
label = Label(root, text="Hello, Tkinter!")  # 텍스트 라벨 생성
label.pack()  # 화면에 배치

# 새 창 정중앙에 오는 위치 계산해주는 함수수
def center_calc(window_width, window_height):

    # root 창의 위치와 크기 가져오기
    root_x = root.winfo_x()  # root 창의 X 좌표
    root_y = root.winfo_y()  # root 창의 Y 좌표
    root_width = root.winfo_width()  # root 창의 가로 크기
    root_height = root.winfo_height()  # root 창의 세로 크기
    
    # 중앙 좌표 계산
    x_position = root_x + (root_width - window_width) // 2
    y_position = root_y + (root_height - window_height) // 2 + 25  # 25는 보정값
    return window_width, window_height, x_position, y_position

# 메뉴 바
menu_bar = Menu(root)  # 메뉴 바 생성
root.config(menu=menu_bar)  # 메뉴 바를 창에 적용

# File 메뉴 생성
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Quit", command=root.quit)

## ffmpeg 테스트!!!!!!!!!!!!!
file_menu.add_command(label="ffmpegTest", command=ffmpeg.split)

    ## Edit 메뉴 ##
# Edit - Preference 실행
def edit_preference():
    width, height, x, y = center_calc(700, 500)
    prefer = Toplevel(root)
    prefer.resizable(False, False)
    prefer.geometry(f"{width}x{height}+{x}+{y}")
    prefer.iconbitmap(ico)
    prefer.title("Preferences")
    prefer.transient(root)
    prefer.grab_set()

# Edit 메뉴 생성
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Preferences", command=edit_preference)


    ## Help 메뉴 ##
# Help - Information 실행
def help_information():
    width, height, x, y = center_calc(400, 300)
    about = Toplevel(root)
    about.resizable(False, False)
    about.geometry(f"{width}x{height}+{x}+{y}")
    about.iconbitmap(ico)
    about.title("Information...")
    about.transient(root)  # 메인 창과 연관되도록 설정
    about.grab_set()  # info 창이 닫히기 전까지 다른 창 클릭 방지

    about.mainloop()

# Help - Report Bugs... 실행
def help_bug():
    webbrowser.open("https://naver.com")  # 기본 웹 브라우저에서 URL 열기

# Help 메뉴 생성
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Report Bugs...", command=help_bug)
help_menu.add_separator() # 구분선 생성
help_menu.add_command(label="Information...", command=help_information)




root.mainloop()  # 창 유지