# Useful function for user input. Especially from vscode.
import os
from .util import *

def multiline_input():
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)


def dialog_input(title='title', prompt='input', default=None):
    """
    Example:
    >>> strinput("RIG CONFIG", "Insert RE com port:", default="COM")
    """
    import tkinter as tk
    from tkinter import simpledialog
    root = tk.Tk()
    root.withdraw()
    ans = simpledialog.askstring(title, prompt, initialvalue=default)
    return ans

class TextInputPopup:
    def __init__(self, root):
        import tkinter as tk
        self.root = root
        self.root.title("Input")
        self.user_input = ""

        # 创建一个 Text 组件用于多行文本输入
        self.text = tk.Text(self.root, height=10, width=50)
        self.text.pack()

        # 创建一个确定按钮，当点击时会调用 self.close 方法
        self.button = tk.Button(self.root, text="Confirm", command=self.close)
        self.button.pack()

    def close(self):
        # 获取 Text 组件中的所有文本并去除尾部的换行符
        self.user_input = self.text.get("1.0", "end-1c")
        self.root.destroy()

    def show(self):
        self.root.mainloop()
        return self.user_input  # 返回用户输入的内容

def dialog_input_multiline():
    import tkinter as tk
    root = tk.Tk()
    popup = TextInputPopup(root)
    user_input = popup.show()
    return user_input


def vscode_input(path,prompt, default = None):
    print(prompt)
    if default is not None:
        write_file(path, default)
    else:
        # truncate
        os.system(f"> {path}")
    os.system(f"code -r -w {path}")
    return read_file(path)

def open_in_vscode(path):
    os.system(f"code -r {path}")

def input_with_default(prompt, default):
    res = input(prompt)
    if len(res.strip()) == 0:
        return default
    return res

def input_sth(prompt):
    res = ''
    while len(res.strip()) <= 0:
        res = input(prompt)
    return res.strip()
