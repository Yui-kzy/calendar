import tkinter as tk

# 建立主視窗
root = tk.Tk()
root.title("我的 Tkinter 應用")

# 新增一個標籤
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
label.pack(pady=20)

# 進入主迴圈
root.mainloop()