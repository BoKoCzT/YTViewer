import pytube
import vlc
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class YouTubePlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Player")

        # Vytvorenie vstupného poľa pre URL
        self.url_label = ttk.Label(root, text="YouTube URL:")
        self.url_label.pack(side=tk.TOP)

        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(side=tk.TOP)

        self.load_button = ttk.Button(root, text="Load", command=self.load_video)
        self.load_button.pack(side=tk.TOP)

        # Vytvorenie tlačidiel pre ovládanie prehrávania
        self.play_button = ttk.Button(root, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT)

        self.pause_button = ttk.Button(root, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_video)
        self.stop_button.pack(side=tk.LEFT)

        self.save_button = ttk.Button(root, text="Save Video", command=self.save_video)
        self.save_button.pack(side=tk.LEFT)

        # Vytvorenie widgetu pre prehrávanie videa
        self.video_frame = ttk.Frame(root)
        self.video_frame.pack(expand=True, fill="both")

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.player.set_hwnd(self.video_frame.winfo_id())

        # Vytvorenie menu pre výber rozlíšenia
        self.resolution_var = tk.StringVar(root)
        self.resolution_menu = ttk.OptionMenu(root, self.resolution_var, "Select Resolution")
        self.resolution_menu.pack(side=tk.TOP)

    def load_video(self):
        url = self.url_entry.get()
        yt = pytube.YouTube(url)
        self.streams = yt.streams.filter(progressive=True, file_extension='mp4')
        resolutions = [stream.resolution for stream in self.streams]
        self.resolution_var.set(resolutions[0])
        self.resolution_menu['menu'].delete(0, 'end')
        for res in resolutions:
            self.resolution_menu['menu'].add_command(label=res, command=tk._setit(self.resolution_var, res))

    def play_video(self):
        selected_resolution = self.resolution_var.get()
        stream = next(stream for stream in self.streams if stream.resolution == selected_resolution)
        media = self.instance.media_new(stream.url)
        self.player.set_media(media)
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()

    def save_video(self):
        url = self.url_entry.get()
        yt = pytube.YouTube(url)
        stream = next(stream for stream in self.streams if stream.resolution == self.resolution_var.get())
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            stream.download(output_path=folder_selected)
            tk.messagebox.showinfo("Download Complete", "Video has been downloaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    player = YouTubePlayer(root)
    root.mainloop()
