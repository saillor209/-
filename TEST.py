from tkinter import *
from tkinter import filedialog

root = Tk()
root.withdraw()  # 메인 윈도우는 숨김

# 폴더 선택 대화상자 열기
folder_path = filedialog.askdirectory(title="폴더를 선택하세요")

# 선택한 폴더 경로 출력
if folder_path:
    print("선택한 폴더의 경로:", folder_path)
else:
    print("폴더가 선택되지 않았습니다.")

root.mainloop()