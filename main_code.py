from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pytube import YouTube, Playlist
from tkinter.filedialog import askdirectory
import threading

# Create the main window
root = Tk()
root.title("TrewMedia Downloader")
root.geometry("800x500")
root.configure(bg='#C291DE')

# Define a function to handle the download button click
def download_video():
    # Get the video URL from the text entry box
    url = url_entry.get()
    # Create an object of the YouTube class by passing the video URL as a parameter
    try:
        yt = YouTube(url)
    except:
        messagebox.showerror("Uh Oh!!", "Looks like, You are not connected to the Internet or the URL is invalid")
        return
    # Get the selected video quality from the radio button options
    quality = quality_var.get()
    # Get the video stream with the selected quality
    stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=quality).first()
    # Print the title of the video
    print("Downloading:", yt.title)
    url_label.config(text="Video Title: " + yt.title, font=("Comic Sans MS", 20))
    # Show a file dialog to get the download directory
    save_dir = askdirectory()
    messagebox.showinfo("Starting", "Your Video:\n" + yt.title + "\n" + quality)
    # Download the video to the specified directory in a new thread
    t = threading.Thread(target=download_video_thread, args=(stream, save_dir, yt.title))
    t.start()

# Define a function to handle the download playlist button click
def download_playlist():
    # Get the playlist URL from the text entry box
    url = url_entry.get()
    # Create an object of the Playlist class by passing the playlist URL as a parameter
    try:
        playlist = Playlist(url)
    except:
        messagebox.showerror("Uh Oh!!", "Looks like, You are not connected to the Internet or the URL is invalid")
        return
    # Show a file dialog to get the download directory
    save_dir = askdirectory()
    # Loop through each video in the playlist and download it to the specified directory in a new thread
    for video in playlist.videos:
        # Create an object of the YouTube class by passing the video URL as a parameter
        yt = YouTube(video.watch_url)
        # Get the selected video quality from the radio button options
        quality = quality_var.get()
        # Get the video stream with the selected quality
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=quality).first()
        # Print the title of the video
        print("Downloading:", yt.title)
        url_label.config(text="Video Title: " + yt.title, font=("Comic Sans MS", 20))
        # Download the video to the specified directory in a new thread
        t = threading.Thread(target=download_video_thread, args=(stream, save_dir, yt.title))
        t.start()

# Define a function to download the video in a new thread
def download_video_thread(stream, save_dir, title):
    try:
        # Download the video to the specified directory
        stream.download(output_path=save_dir)
        # Update the status label
        status_label.config(text="Video downloaded successfully to: " + save_dir)
        url_label.config(text="Enter the URL of the video or playlist you want to download", font=("Comic Sans MS", 13), bg='#C291DE')
    except Exception as e:
        # Display an error message if the download fails
        messagebox.showerror("Error", f"Download failed: {e}")
        status_label.config(text="Download failed: " + str(e))


# Define a function to handle the about button click
def about():
    messagebox.showinfo("From the creator", "TrewMedia Downloader\nLanguage: Python\n\nCreated by: Ionderify")	



#GUI Elements

title_label = Label(root, text="TrewMedia Downloader", font=("Comic Sans MS", 22, "bold"), bg='#C291DE')
title_label.pack(pady=20)

url_label = Label(root, text="Enter the URL of the video or playlist you want to download", font=("Comic Sans MS", 13), bg='#C291DE')
url_label.pack(pady=10)

url_entry = Entry(root, font=("Comic Sans MS", 13))
url_entry.pack(pady=10)

quality_label = Label(root, text="Select video quality", font=("Comic Sans MS", 18), bg='#C291DE')
quality_label.pack(pady=10)

quality_var = StringVar()
quality_var.set("720p")

quality_radios = Frame(root, bg='#C291DE')

radio_720p = Radiobutton(quality_radios, text="1080p", variable=quality_var, value="1080p", bg='#C291DE', font=("Comic Sans MS", 16))
radio_720p.pack(side=LEFT, padx=5)

radio_480p = Radiobutton(quality_radios, text="720p", variable=quality_var, value="720p", bg='#C291DE', font=("Comic Sans MS", 16))
radio_480p.pack(side=LEFT, padx=5)

radio_360p = Radiobutton(quality_radios, text="480p", variable=quality_var, value="480p", bg='#C291DE', font=("Comic Sans MS", 16))
radio_360p.pack(side=LEFT, padx=5)

radio_240p = Radiobutton(quality_radios, text="360p", variable=quality_var, value="360p", bg='#C291DE', font=("Comic Sans MS", 16))
radio_240p.pack(side=LEFT, padx=5)

quality_radios.pack()

download_button = Button(root, text="Download Video", font=("Comic Sans MS", 13), command=download_video, bg='#000000', fg='white')
download_button.pack(pady=20)

download_playlist_button = Button(root, text="Download Playlist", font=("Comic Sans MS", 13), command=download_playlist, bg='#000000', fg='white')
download_playlist_button.pack(pady=10)

about_button = Button(root, text="About", font=("Comic Sans MS", 13), command=about, bg='#000000', fg='white')
about_button.pack(pady=10)

status_label = Label(root, text="", font=("Comic Sans MS", 13), bg='#C291DE')
status_label.pack(pady=10)

#mainloop

root.mainloop()
