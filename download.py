from flask import Flask, request, send_file, render_template, redirect, url_for
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Specify the folder where downloaded and converted files will be stored
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'download_songs')

# Ensure the folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for download page
@app.route('/download')
def download_page():
    return render_template('download.html')

# Function to download and convert a YouTube video to MP3/MP4 based on link type and bitrate
def download_and_convert(youtube_url, bitrate, format_type, link_type):
    try:
        if format_type == 'mp3':
            quality = 'bestaudio'
            postprocessors = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate if bitrate != 'original' else '0',
            }]
        elif format_type == 'mp4':
            if bitrate == '1080p':
                quality = 'bestvideo[height<=1080]+bestaudio/best'
            elif bitrate == '720p':
                quality = 'bestvideo[height<=720]+bestaudio/best'
            elif bitrate == '480p':
                quality = 'bestvideo[height<=480]+bestaudio/best'
            else:
                quality = 'bestvideo+bestaudio/best'
            postprocessors = []

        ydl_opts = {
            'format': quality,
            'postprocessors': postprocessors,
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'prefer_ffmpeg': True,
        }

        # Handle playlists
        if link_type == 'playlist':
            ydl_opts['noplaylist'] = False  # Download full playlist
        else:
            ydl_opts['noplaylist'] = True  # Download single video

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)

        if format_type == 'mp3':
            file = filename.rsplit('.', 1)[0] + '.mp3'
        else:
            file = filename  # MP4 remains as-is

        return file

    except Exception as e:
        print(f"Error during download and conversion: {e}")
        return None

@app.route('/convert', methods=['POST'])
def convert_video():
    data = request.json
    youtube_url = data.get('youtube_url')
    format_type = data.get('format')
    bitrate = data.get('bitrate')
    link_type = data.get('link_type')

    if bitrate not in ['320', '160', '80', '1080p', '720p', '480p', 'original']:
        return "Invalid bitrate", 400

    # Download and convert the YouTube video to MP3/MP4
    file = download_and_convert(youtube_url, bitrate, format_type, link_type)

    if file:
        return send_file(file, as_attachment=True)
    else:
        return "Failed to download or convert the video. Please try again.", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the port set by Render or default to 5000
    app.run(host="0.0.0.0", port=port)
