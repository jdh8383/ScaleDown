# ScaleDown

This Python script is used to monitor a directory and transcode any newly added video files into a new file with lower resolution. The specific transcoding parameters and file naming conventions can be modified by changing the code accordingly.

## Requirements
- Python 3.6+
- ffmpeg binaries
- ffmpeg-python
- watchdog

## Installation
1. Clone the repository.
2. Install Python 3.6 or above if not already installed.
3. Install ffmpeg binaries on your OS.
4. Pip install ffmpeg-python watchdog.

## Usage
1. Open the terminal and navigate to the repository directory.
2. Set the `path` variable in `settings.py` to the directory you want to watch for new video files.
3. Run the script by executing the command: `python app.py`.
4. The script will watch the specified directory for new video files.
5. When a new video file is detected, the script will transcode it to a lower resolution (480p) and save it in the same directory with the suffix `.mp4`.
6. The original file will be left untouched.

## License
This project is licensed under the MIT License - see the LICENSE file for details.