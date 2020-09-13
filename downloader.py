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
                            command=self.get_info)
        self.b1.pack()
        self.b2 = tk.Button(root, text='Download', width=15,
                            command=self.download)
        self.b2.pack()
        self.b3 = tk.Button(root, text='From clipboard', width=15,
                            command=self.from_clipboard)
        self.b3.pack()

    def from_clipboard(self):
        clipboard = self.clipboard_get()
        self.link.set(clipboard)

    def info_thread(self, ydl, videos):
        video_info = ydl.extract_info(videos, download=False)
        for f in video_info['formats']:
            if f.get('ext') == 'mp4':
                x = f.get('format')
                self.formats[x] = f.get('format_id')
                self.listbox.insert(tk.END, x)

    def get_info(self):
        self.listbox.delete(0, tk.END)
        videos = self.link.get()
        with youtube_dl.YoutubeDL() as ydl:
            it = threading.Thread(target=self.info_thread,
                                  args=[ydl, videos])
            it.start()

    def download(self):
        if self.listbox.curselection() is None:
            return

        video_format = self.formats.get(
            self.listbox.get(self.listbox.curselection())
        )
        ydl_opts = {
            'format': f'{video_format}+bestaudio'
        }
        videos = [self.link.get()]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            dt = threading.Thread(target=self.download_thread,
                                  args=[ydl, videos])
            dt.start()

    def download_thread(self, ydl, videos):
        ydl.download(videos)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Youtube Downloader')
    root.resizable(False, False)
    root.geometry('300x300+100+100')
    Application(root)
    root.mainloop()
