import tkinter as tk
from tkinter import scrolledtext

class DebugLogWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Debug Log")
        
        # 로그 출력 창 (ScrolledText)
        self.log_text = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled')
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 테스트 로그 버튼
        self.log_button = tk.Button(root, text="로그 추가", command=self.add_log)
        self.log_button.pack(pady=5)

    def add_log(self, message="디버깅 메시지 출력!"):
        """로그를 추가하는 함수"""
        self.log_text.config(state='normal')  # 편집 가능하도록 변경
        self.log_text.insert(tk.END, message + "\n")  # 메시지 추가
        self.log_text.config(state='disabled')  # 다시 읽기 전용으로 설정
        self.log_text.yview(tk.END)  # 스크롤을 가장 아래로 이동

if __name__ == "__main__":
    root = tk.Tk()
    app = DebugLogWindow(root)
    root.mainloop()