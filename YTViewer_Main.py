import tkinter as tk
from tkinter import messagebox
from pytube import Channel

class YouTubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Viewer")
        self.root.geometry("600x800")

        self.label = tk.Label(root, text="Zadajte URL YouTube kanálu:")
        self.label.pack(pady=10)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=10)

        self.fetch_button = tk.Button(root, text="Načítať videá", command=self.fetch_videos)
        self.fetch_button.pack(pady=10)

        self.video_listbox = tk.Listbox(root, width=80, height=20)
        self.video_listbox.pack(pady=10)

    def fetch_videos(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Chyba", "Prosím, zadajte korektnú URL kanálu.")
            return

        try:
            channel = Channel(url)
            self.video_listbox.delete(0, tk.END)
            for video in channel.videos:
                self.video_listbox.insert(tk.END, video.title)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodarilo sa načítať videá: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeApp(root)
    root.mainloop()
