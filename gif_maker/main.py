import tkinter as tk
from tkinter import filedialog, messagebox, ttk  # Adjusted import here
from moviepy.editor import VideoFileClip
# Ensure the correct import path for resize; if the below doesn't work, check moviepy documentation
from moviepy.video.fx.resize import resize
from PIL import Image, ImageTk
import os
from PIL import Image as pil
from pkg_resources import parse_version
if parse_version(pil.__version__)>=parse_version('10.0.0'):
    Image.ANTIALIAS=Image.LANCZOS

class GIFMakerApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.fps = 10  # Default fps value
        self.scale = 0.5  # Default scale value

    def setup_ui(self):
        self.root.title("GIF Maker")

        # Frame for video selection and settings
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=20)

        # Button to select video
        self.select_video_btn = tk.Button(settings_frame, text="Select Video", command=self.select_video)
        self.select_video_btn.grid(row=0, column=0, padx=10)

        # Entry for FPS
        self.fps_label = tk.Label(settings_frame, text="FPS:")
        self.fps_label.grid(row=0, column=1)
        self.fps_entry = tk.Entry(settings_frame)
        self.fps_entry.insert(0,"10")  # Display default fps value
        self.fps_entry.grid(row=0, column=2)

        # Entry for Scaling Factor
        self.scale_label = tk.Label(settings_frame, text="Scale:")
        self.scale_label.grid(row=0, column=3)
        self.scale_entry = tk.Entry(settings_frame)
        self.scale_entry.insert(0, "0.5")  # Display default scale value
        self.scale_entry.grid(row=0, column=4)

        # Button to preview GIF
        self.preview_btn = tk.Button(settings_frame, text="Preview", command=self.preview_gif)
        self.preview_btn.grid(row=0, column=5, padx=10)

        # Button to convert video to GIF
        self.convert_btn = tk.Button(settings_frame, text="Convert to GIF", command=self.convert_video)
        self.convert_btn.grid(row=0, column=6)

        # Label for displaying preview
        self.preview_label = tk.Label(self.root)
        self.preview_label.pack()

        self.video_path = ""
        self.output_path = ""

    def select_video(self):
        self.video_path = filedialog.askopenfilename(title="Select a video", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
        if self.video_path:
            self.select_video_btn.config(text=os.path.basename(self.video_path))

    def preview_gif(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please select a video first.")
            return

        try:
            fps = float(self.fps_entry.get())
            scale = float(self.scale_entry.get())
        except ValueError:
            messagebox.showerror("Error", "FPS and Scale must be numbers.")
            return

        clip = VideoFileClip(self.video_path).subclip(0, 5)  # Use a 5-second clip for preview
        clip = clip.fx(resize, scale).set_fps(fps)
        preview_path = "preview.gif"
        clip.write_gif(preview_path, fps=fps)
        self.show_preview(preview_path)

    def show_preview(self, preview_path):
        img = Image.open(preview_path)
        imgtk = ImageTk.PhotoImage(image=img)
        self.preview_label.config(image=imgtk)
        # Keep a reference to the image to prevent garbage collection
        # Note: Some static type checkers might not recognize this usage as valid, but it is necessary for tkinter
        self.preview_label.image = imgtk

    def convert_video(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please select a video first.")
            return

        try:
            fps = float(self.fps_entry.get())
            scale = float(self.scale_entry.get())
        except ValueError:
            messagebox.showerror("Error", "FPS and Scale must be numbers.")
            return

        self.output_path = os.path.splitext(self.video_path)[0] + ".gif"
        clip = VideoFileClip(self.video_path)
        clip = clip.fx(resize, scale).set_fps(fps)

        progress = tk.Toplevel(self.root)
        progress.title("Converting...")
        tk.Label(progress, text="Conversion in progress...").pack()
        progress_bar = ttk.Progressbar(progress, orient="horizontal", length=200, mode="indeterminate")  # Adjusted import here
        progress_bar.pack(pady=10)
        progress_bar.start()

        clip.write_gif(self.output_path, fps=fps)

        progress_bar.stop()
        progress.destroy()

        messagebox.showinfo("Done", "Conversion finished! GIF saved as: " + self.output_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = GIFMakerApp(root)
    root.mainloop()