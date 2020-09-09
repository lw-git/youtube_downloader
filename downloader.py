import tkinter as tk
import youtube_dl
import threading


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Youtube Downloader')
    root.resizable(False, False)
    root.geometry('300x300+100+100')
    Application(root)
    root.mainloop()
