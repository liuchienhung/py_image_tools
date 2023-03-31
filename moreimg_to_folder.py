import tkinter as tk
from tkinter import filedialog, simpledialog
import shutil
import os

# 創建GUI窗口
root = tk.Tk()
root.withdraw()

# 讓使用者選擇多個檔案
file_paths = filedialog.askopenfilenames()

# 如果使用者選擇了檔案，就讓他們選擇目標目錄
if file_paths:
    target_directory = filedialog.askdirectory()

    # 如果目標目錄不存在，就讓使用者輸入新的目錄名稱並創建該目錄
    while not os.path.exists(target_directory):
        new_directory = simpledialog.askstring(title="新目錄名稱", prompt="請輸入新的目錄名稱：")
        if new_directory:
            target_directory = os.path.join(target_directory, new_directory)
            os.makedirs(target_directory)
        else:
            break

    # 將所選擇的檔案複製到目標目錄中
    for file_path in file_paths:
        shutil.copy(file_path, target_directory)
