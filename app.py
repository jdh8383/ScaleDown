from time import sleep
from os import path
import logging
import ffmpeg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from settings import Settings

# Define log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.INFO, format=LOG_FORMAT)

class Watcher:
    def __init__(self, path) -> None:
        self.path = path

    def run(self):
        # Initialize observer and handler
        observer = Observer()
        handler = VideoFileHandler()
        observer.schedule(handler, self.path, recursive=True)
        observer.start()
        logging.info("App started.")
        try:
            # Avoid unnecessary polling while waiting for events
            while True:
                sleep(3)
        except KeyboardInterrupt:
            observer.stop()
        # Wait for observer to finish its tasks
        observer.join()
        logging.info("App exit.")

class VideoFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Override default on_created method"""
        # Check if the file has been processed
        _, file_name = path.split(event.src_path)
        file_prefix, _ = path.splitext(file_name)
        a, b = path.splitext(file_prefix)
        if b != '':
            # logging.info(f"{event.src_path} is an output file. Skipping")
            return None

        # If it's not a directory and it's a video file
        if not event.is_directory and self.is_video_file(event.src_path):
            # Wait for file writing to finish
            while not self.is_file_complete(event.src_path):
                sleep(1)
            logging.info(f'Found new video file: "{event.src_path}"')
            # Process the file
            self.process_file(event.src_path)
            logging.info(f'"{event.src_path}" processing complete.')

    def is_video_file(self, file):
        """Check if new file is video file"""
        video_ext = ['.mp4', '.mkv', '.avi', 'm4v', '.mov', '.flv']
        _, file_ext = path.splitext(file)
        return file_ext.lower() in video_ext
    
    def is_file_complete(self, file):
        """Check if file has fininshed writing"""
        while True:
            file_early_size = path.getsize(file)
            sleep(2)
            file_now_size = path.getsize(file)
            if file_now_size == file_early_size:
                break
            logging.info(f'"{file}" writing is not complete yet.')
        return True
        
    def process_file(self, file):
        # Set input and output file paths
        input_file = file
        out_file = f"{input_file}" + '.mp4'

        # Get video information
        file_info_dict = ffmpeg.probe(input_file)
        video_info = next(s for s in file_info_dict['streams'] if s['codec_type'] == 'video')
        
        # Check if video height is greater than 480
        if video_info['height'] > 480:
            # Scale video to height of 480 while maintaining aspect ratio
            # Transcode video
            try:
                v = ffmpeg.input(input_file).video.filter('scale', width=-2, height=480)
                a = ffmpeg.input(input_file).audio
                ffmpeg.output(v, a, out_file, acodec='copy').run(capture_stderr=True)
            except ffmpeg.Error as e:
                logging.error(e.stderr.decode())

if __name__ == '__main__':
    settings = Settings()
    w = Watcher(settings.path)
    w.run()
