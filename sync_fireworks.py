import requests
import json
import time
import os
import subprocess
import shutil
from datetime import datetime, timedelta
import yt_dlp
import sys

# Configuration
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Magic Kingdom Park ID
MK_ID = "75ea578a-adc8-4116-a54d-dccb60765ef9"

# Entity IDs for known fireworks shows
SHOW_ENTITIES = {
    "22b78ed9-a692-47cb-b6a4-6d1224ff67e3": "Happily Ever After",
    "bb28947d-a747-44f0-ac71-1fa8188f4cee": "Minnie's Wonderful Christmastime Fireworks",
    "86c198b0-7c02-4354-814a-27ad70067d45": "Disney Enchantment",
    "fantasy-in-the-sky-id": "Fantasy in the Sky"
}

# Search queries for audio
SHOW_AUDIO_QUERIES = {
    "Happily Ever After": "Happily Ever After Fireworks Full Audio Soundtrack",
    "Minnie's Wonderful Christmastime Fireworks": "Minnie's Wonderful Christmastime Fireworks Full Audio Soundtrack",
    "Disney Enchantment": "Disney Enchantment Fireworks Full Audio Soundtrack",
    "Fantasy in the Sky": "Fantasy in the Sky Fireworks Magic Kingdom Audio"
}

def get_today_show():
    """
    Checks the live data for known fireworks shows for the current day.
    Returns (show_name, start_time_dt) or (None, None).
    """
    url = f"https://api.themeparks.wiki/v1/entity/{MK_ID}/live"
    print(f"Fetching live data from {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        live_data = data.get('liveData', [])
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        for item in live_data:
            entity_id = item.get('id')
            show_name = SHOW_ENTITIES.get(entity_id)
            
            # Also check by name if ID not found (fallback)
            if not show_name:
                name = item.get('name', '')
                if 'Happily Ever After' in name:
                    show_name = "Happily Ever After"
                elif 'Minnie' in name and 'Fireworks' in name:
                    show_name = "Minnie's Wonderful Christmastime Fireworks"
                elif 'Enchantment' in name:
                    show_name = "Disney Enchantment"
            
            if show_name:
                showtimes = item.get('showtimes', [])
                for st in showtimes:
                    start_time_str = st.get('startTime')
                    if start_time_str and start_time_str.startswith(today_str):
                        start_time = datetime.fromisoformat(start_time_str)
                        print(f"Found show: {show_name} at {start_time}")
                        return show_name, start_time
                        
    except Exception as e:
        print(f"Error checking schedule: {e}")
            
    return None, None

def download_audio(show_name):
    """
    Downloads the audio for the show if not already present.
    Returns the path to the audio file.
    """
    # Clean filename
    safe_name = show_name.lower().replace(" ", "_").replace("'", "")
    # Check for any existing audio file with this base name
    for ext in ['.mp3', '.m4a', '.webm', '.wav']:
        filepath = os.path.join(AUDIO_DIR, safe_name + ext)
        if os.path.exists(filepath):
            print(f"Audio already exists: {filepath}")
            return filepath
            
    print(f"Downloading audio for {show_name}...")
    query = SHOW_AUDIO_QUERIES.get(show_name, f"{show_name} fireworks audio")
    search_query = f"ytsearch1:{query}"
    
    # Check if ffmpeg is available
    ffmpeg_available = shutil.which("ffmpeg") is not None
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(AUDIO_DIR, safe_name + '.%(ext)s'),
        'quiet': False,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
    }
    
    if ffmpeg_available:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        print("ffmpeg not found, downloading best available audio format (likely m4a/webm).")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        
        # Find the file we just downloaded
        for ext in ['.mp3', '.m4a', '.webm', '.wav', '.opus', '.mp4']:
            filepath = os.path.join(AUDIO_DIR, safe_name + ext)
            if os.path.exists(filepath):
                return filepath
                
        raise Exception("Download finished but file not found.")
            
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def get_audio_duration(filepath):
    """
    Returns the duration of the audio file in seconds using ffprobe.
    Returns None if ffprobe fails or is not found.
    """
    if not shutil.which("ffprobe"):
        return None
        
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        filepath
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None

def main():
    print("--- Magic Kingdom Fireworks Sync ---")
    show_name, show_time = get_today_show()
    
    if not show_name:
        print("No fireworks show found for today.")
        return
        
    audio_file = download_audio(show_name)
    if not audio_file:
        print("Could not get audio file. Aborting.")
        return
        
    # Calculate wait time
    now = datetime.now(show_time.tzinfo)
    wait_seconds = (show_time - now).total_seconds()
    
    if wait_seconds < 0:
        print(f"Show time {show_time} has already passed.")
        offset = abs(wait_seconds)
        print(f"Show started {timedelta(seconds=int(offset))} ago.")
        
        # Check if we are still within the show duration
        duration = get_audio_duration(audio_file)
        if duration:
            if offset < duration:
                print(f"Jumping to {timedelta(seconds=int(offset))} in the track...")
                try:
                    # Use ffplay to seek
                    # -ss: seek to position
                    # -nodisp: no graphical window
                    # -autoexit: exit when done
                    subprocess.run(['ffplay', '-ss', str(offset), '-nodisp', '-autoexit', audio_file])
                except Exception as e:
                    print(f"Error playing with ffplay: {e}")
            else:
                print("Show has finished (offset > duration).")
        else:
            print("Could not determine audio duration to check if show is still running.")
            # Fallback: try to play if it's within a reasonable time (e.g. 20 mins)
            if offset < 1200: 
                print("Attempting to play from offset anyway...")
                try:
                    subprocess.run(['ffplay', '-ss', str(offset), '-nodisp', '-autoexit', audio_file])
                except Exception as e:
                    print(f"Error playing with ffplay: {e}")
            else:
                print("Show likely finished.")
        return
        
    print(f"Waiting for {show_name} at {show_time}")
    print(f"Time remaining: {timedelta(seconds=int(wait_seconds))}")
    
    # Sleep loop
    while wait_seconds > 0:
        sleep_time = min(wait_seconds, 60)
        time.sleep(sleep_time)
        now = datetime.now(show_time.tzinfo)
        wait_seconds = (show_time - now).total_seconds()
        
        if wait_seconds <= 0.5:
            break
            
    print("It's showtime!")
    try:
        if shutil.which("ffplay"):
             subprocess.run(['ffplay', '-nodisp', '-autoexit', audio_file])
        else:
            subprocess.run(['afplay', audio_file])
    except Exception as e:
        print(f"Error playing audio: {e}")

if __name__ == "__main__":
    main()
