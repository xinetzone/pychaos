# tkinterx

[![GitHub issues](https://img.shields.io/github/issues/xinetzone/pychaos)](https://github.com/xinetzone/pychaos/issues) [![GitHub forks](https://img.shields.io/github/forks/xinetzone/pychaos)](https://github.com/xinetzone/pychaos/network) [![GitHub stars](https://img.shields.io/github/stars/xinetzone/pychaos)](https://github.com/xinetzone/pychaos/stargazers) [![GitHub license](https://img.shields.io/github/license/xinetzone/pychaos)](https://github.com/xinetzone/pychaos/blob/master/LICENSE) [![HitCount](http://hits.dwyl.io/xinetzone/pychaos.svg)](http://hits.dwyl.io/xinetzone/pychaos) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cv) ![repo size](https://img.shields.io/github/repo-size/xinetzone/pychaos.svg) [![contributors](https://img.shields.io/github/contributors/xinetzone/pychaos.svg)](https://github.com/xinetzone/pychaos/graphs/contributors) [![watcher](https://img.shields.io/github/watchers/xinetzone/pychaos.svg)](https://github.com/xinetzone/pychaos/watchers)

Use tkinter to create a handy GUI tool.

## PyPI support available

You can install the latest version using the following command:

```sh
pip install tkinterx
```

The following command is used when called:

```python
import tkinterx
```

## A sample: Record your personal information

```python
class Window(WindowMeta):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

    def create_widget(self):
        self.add_row('Please enter your name:', 'name')
        self.add_row('Please enter your age:', 'age')
        self.add_row('Enter your information saving path:', 'save_path')

    def save(self, path):
        table = self.table.todict()
        with open(path, 'w') as fp:
            json.dump(table, fp)

    def run(self):
        self.withdraw()
        name = self.table['name']
        age = self.table['age']
        save_path = str(self.table['save_path'])
        if '' in [name, age, save_path]:
            showwarning(self)
        else:
            self.save(save_path)
            askokcancel(self)


class Root(Tk):
    def __init__(self):
        super().__init__()
        self.label_var = StringVar()
        self.create_widgets()
        self.layout()

    def create_buttons(self):
        style = ttk.Style()
        style.configure("C.TButton",
                        foreground="green",
                        background="white",
                        relief='raise',
                        justify='center',
                        font=('YaHei', '10', 'bold'))
        self.table_button = ttk.Button(self, text='Fill in your name and age:',
                                       command=self.ask_table,
                                       style="C.TButton")

    def create_widgets(self):
        self.create_buttons()
        self.label = ttk.Label(self, textvariable=self.label_var)

    def ask_table(self):
        bunch = ask_window(self, Window)
        name, age = bunch['name'], bunch['age']
        self.label_var.set(f"{name}: {age}")

    def layout(self):
        self.table_button.pack()
        self.label.pack()


if __name__ == "__main__":
    root = Root()
    root.geometry('300x200')
    root.mainloop()
```

Interface presentation:

![Figure 1: record your personal information](images/name_age.png)

For more information: [Chinese Manual](https://www.jianshu.com/nb/45403586).
