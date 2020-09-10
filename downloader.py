import tkinter as tk
import youtube_dl
import threading


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.formats = {}
        self.link = tk.StringVar()
        self.link.set('http://youtube.com/watch?v=')
        self.e1 = tk.Entry(root, textvariable=self.link, width=50)
        self.e1.pack()
        self.listbox = tk.Listbox(root)
        self.listbox.pack()

        self.b1 = tk.Button(root, text='Get formats', width=15,
                            command=None)
        self.b1.pack()
        self.b2 = tk.Button(root, text='Download', width=15,
                            command=None)
        self.b2.pack()
        self.b3 = tk.Button(root, text='From clipboard', width=15,
                            command=None)
        self.b3.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Youtube Downloader')
    root.resizable(False, False)
    root.geometry('300x300+100+100')
    Application(root)
    root.mainloop()
