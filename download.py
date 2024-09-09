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
@app.route('/template')
def download_page():
    return render_template('download.html')

# Function to download and convert a YouTube video to MP3 at the desired bitrate using yt-dlp
def download_and_convert(youtube_url, bitrate):
    try:
        if bitrate == 'original':
            quality = 'bestaudio'
        else:
            quality = 'bestaudio/best'
        
        # Options for yt-dlp, including the output template and postprocessing for audio conversion
        ydl_opts = {
            'format': quality,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate if bitrate != 'original' else '0',
            }],
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Filename template
            'prefer_ffmpeg': True,  # Ensure FFmpeg is used for conversion
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)
        
        # Replace the original extension with .mp3 after conversion
        mp3_file = filename.rsplit('.', 1)[0] + '.mp3'
        return mp3_file
    
    except Exception as e:
        print(f"Error during download and conversion: {e}")
        return None

@app.route('/convert', methods=['POST'])
def convert_video():
    youtube_url = request.form['youtube_url']
    bitrate = request.form['bitrate']
    
    if bitrate not in ['320', '160', '80', 'original']:
        return "Invalid bitrate", 400
    
    # Download and convert the YouTube video to MP3
    mp3_file = download_and_convert(youtube_url, bitrate)
    
    if mp3_file:
        # Serve the MP3 file for download
        return send_file(mp3_file, as_attachment=True)
    else:
        # If an error occurred during the download/conversion, return an error message
        return "Failed to download or convert the video. Please try again.", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the port set by Render or default to 5000
    app.run(host="0.0.0.0", port=port)
