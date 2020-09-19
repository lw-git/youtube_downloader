import tkinter as tk
import youtube_dl
import threading
import sys


class StdoutRedirector():
    def __init__(self, status):
        self.status = status

    def write(self, str_):
        self.status.configure(state='normal')
        last_insert = self.status.tag_ranges('last_insert')
        last_text = ''
        if last_insert:
            last_text = self.status.get(last_insert[0], last_insert[1])

        if '\n' not in str_:
            str_ += '\n'

        if '[download]' in str_ and 'ETA' in last_text:
            self.status.delete(last_insert[0], last_insert[1])

        self.status.tag_remove('last_insert', '1.0', 'end')
        self.status.insert('end', str_, 'last_insert')
        self.status.see('end')
        self.status.configure(state='disabled')

    def flush(self):
        pass


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.formats = {}
        self.video = 'mp4'
        self.link = tk.StringVar()
        self.link.set('http://youtube.com/watch?v=')
        self.link_frame = tk.Frame(root)
        self.link_frame.pack(fill=tk.BOTH)
        self.e1 = tk.Entry(self.link_frame,
                           textvariable=self.link,
                           font='Helvetica 22 bold',
                           justify='center',
                           relief='sunken')
        self.e1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.format_frame = tk.Frame(root)
        self.format_frame.pack(fill=tk.X, expand=1)

        self.listbox = tk.Listbox(self.format_frame,
                                  font='Helvetica 17 bold',
                                  justify='center',
                                  height=7,
                                  bg='lightgray',
                                  relief='sunken')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scroll1 = tk.Scrollbar(self.format_frame, command=self.listbox.yview)
        scroll1.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scroll1.set)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, expand=1)

        buttons = {
            'Get formats': self.get_info,
            'Download': self.download,
            'From clipboard': self.from_clipboard,
            'Clear': self.clear_status
        }

        for text, command in buttons.items():
            tk.Button(self.button_frame, text=text, command=command,
                      font='Helvetica 17 bold', relief='flat').pack(
                side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.status_frame = tk.Frame(root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status = tk.Text(self.status_frame, height=10, bg='black',
                              fg='white', wrap=tk.WORD, relief='sunken')
        self.status.pack(fill=tk.X, side=tk.LEFT, expand=1)

        scroll2 = tk.Scrollbar(self.status_frame, command=self.status.yview)
        scroll2.pack(side=tk.RIGHT, fill=tk.Y)

        self.status.config(yscrollcommand=scroll2.set)

        sys.stdout = StdoutRedirector(self.status)

    def clear_status(self):
        self.status.configure(state='normal')
        self.status.delete('1.0', 'end')
        self.status.configure(state='disabled')

    def from_clipboard(self):
        try:
            clipboard = self.clipboard_get()
        except:
            self.clear_status()
            print('[Error] Clipboard is empty')
        else:
            self.link.set(clipboard)

    def info_thread(self, ydl, videos):
        with ydl:
            try:
                video_info = ydl.extract_info(videos, download=False)
            except:
                print('[Error] Incorrect link')
            else:
                for f in video_info['formats']:
                    print(f)
                    if f.get('ext') == self.video and bool(f.get('width')):
                        x = f'{f.get("width")}x{f.get("height")}'
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
        self.clear_status()
        try:
            video_format = self.formats.get(
                self.listbox.get(self.listbox.curselection())
            )
        except:
            print('[Error] Format not chosen')
        else:
            ydl_opts = {
                'format': f'{video_format}+bestaudio[ext=m4a]/bestaudio'
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
    root.geometry('800x450+100+100')
    Application(root)
    root.mainloop()
