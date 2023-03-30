import os
import shutil
import tkinter as tk
from tkinter import filedialog
import cv2

class PhotoSorter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Sorter")
        self.folder_path = None
        self.names = []
        self.name_index = 0
        self.image_index = 0
        self.selected_name = tk.StringVar()
        self.selected_name.set("")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.label = tk.Label(self.root, text="请在右侧输入人名后按 Enter 键确认")
        self.label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(side=tk.LEFT)
        self.name_entry.bind("<Return>", self.add_name)
        self.name_list = tk.Listbox(self.root, listvariable=self.selected_name)
        self.name_list.pack(side=tk.LEFT)
        self.name_list.bind("<<ListboxSelect>>", self.select_name)
        self.select_button = tk.Button(self.root, text="选择文件夹", command=self.select_folder)
        self.select_button.pack(side=tk.BOTTOM)

    def select_folder(self):
        """选择需要处理的文件夹"""
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.names = []
            self.name_index = 0
            self.image_index = 0
            self.selected_name.set("")
            self.name_list.delete(0, tk.END)
            self.load_image()

    def add_name(self, event):
        """将输入的人名添加到列表中"""
        name = self.name_entry.get().strip()
        if name and name not in self.names:
            self.names.append(name)
            self.name_entry.delete(0, tk.END)
            self.selected_name.set(tuple(self.names))
            self.name_list.selection_clear(0, tk.END)
            self.name_list.selection_set(self.name_index)
            self.name_index += 1

    def select_name(self, event):
        """选择人名后更新界面"""
        name_index = self.name_list.curselection()
        if name_index:
            self.name_index = name_index[0]
            self.load_image()

    def load_image(self):
        """加载下一张照片并显示"""
        if self.folder_path and self.image_index < len(os.listdir(self.folder_path)):
            image_path = os.path.join(self.folder_path, sorted(os.listdir(self.folder_path))[self.image_index])
            image = cv2.imread(image_path)
            self.canvas.delete("all")
            self.canvas.image = tk.PhotoImage(data=cv2.imencode('.png', image)[1].tobytes())
            self.canvas.create_image(0, 0, anchor="nw", image=self.canvas.image)
            self.label.configure(text=f"当前人名：{self.names[self.name_index]}")
