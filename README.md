# Magic Kingdom Fireworks Sync

This script synchronizes your local audio playback with the daily fireworks show at Magic Kingdom.

## Features

-   **Automatic Schedule Detection**: Checks the daily schedule for Magic Kingdom to find the fireworks show time.
-   **Audio Download**: Automatically downloads the correct audio track for the show (Happily Ever After, Minnie's Wonderful Christmastime Fireworks, Disney Enchantment) from YouTube using `yt-dlp`.
-   **Precise Timing**: Waits until the exact start time of the show to play the audio.
-   **Daily Schedule**: Includes a `launchd` plist to run the script automatically every day at 12:00 PM.

## Prerequisites

-   Python 3
-   `ffmpeg` (optional, but recommended for best audio quality)
-   `yt-dlp` (`pip install yt-dlp`)
-   `requests` (`pip install requests`)

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  (Optional) Install `ffmpeg` via Homebrew:
    ```bash
    brew install ffmpeg
    ```

## Usage

Run the script manually:

```bash
python3 sync_fireworks.py
```

## Scheduling

To run the script daily at 12:00 PM:

1.  Edit `com.user.mkfireworks.plist` and ensure the paths to `python3` and the script are correct.
2.  Copy the plist to your LaunchAgents folder:
    ```bash
    cp com.user.mkfireworks.plist ~/Library/LaunchAgents/
    ```
3.  Load the job:
    ```bash
    launchctl load ~/Library/LaunchAgents/com.user.mkfireworks.plist
    ```
