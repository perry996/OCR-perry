import tkinter as tk
from tkinter import filedialog
import pytesseract
from PIL import Image
import os


def select_folder():
    folder_path = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(tk.END, folder_path)


def process_folder():
    folder_path = entry_path.get()
    file_list = os.listdir(folder_path)
    result_dict = {}

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='eng+chi_sim+digits')
            # 去除识别结果中的空格
            text = text.replace(" ", "")
            result_dict[file_name] = text

    # 创建显示结果的窗口
    result_window = tk.Toplevel(root)
    result_window.title('识别结果')
    result_window.geometry('400x300')

    text_box = tk.Text(result_window, font=('宋体', 11))
    text_box.pack(fill=tk.BOTH, expand=True)

    # 将字典内容按顺序回显到窗体中
    for key, value in result_dict.items():
        text_box.insert(tk.END, f'{key}: {value}\n')

    result_window.mainloop()


# 创建主窗口
root = tk.Tk()
root.title('批量识别')
root.geometry('300x100')


# 创建显示文件夹路径的Entry栏
entry_path = tk.Entry(root, width=30)
entry_path.grid(row=0, column=0, padx=10, pady=10)

# 创建选择文件夹的按钮
select_button = tk.Button(root, text='选择', command=select_folder)
select_button.grid(row=0, column=1, padx=10, pady=10)

# 创建确定按钮
process_button = tk.Button(root, text='确定', command=process_folder)
process_button.grid(row=2, column=0, columnspan=2, pady=10)

# 设置回车触发确定按钮
root.bind('<Return>', lambda event: process_folder())

# 运行主循环
root.mainloop()
