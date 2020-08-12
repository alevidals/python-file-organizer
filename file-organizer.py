from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from datetime import datetime

import time
import os
import json

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png']
PDF_EXTENSIONS = ['.pdf']
ISOS_EXTENSIONS = ['.iso']
IGNORED_EXTENSIONS = ['.crdownload']
COMPRESSED_EXTENSIONS = ['.zip', '.tar']
AUDIO_EXTENSIONS = ['.m4a', '.flac', '.mp3', '.wav', '.wma', '.aac']
VIDEO_EXTENSIONS = ['.avi', '.mp4', '.mov']

folder_to_track = '/home/ale/Descargas'


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for file in os.listdir(folder_to_track):
            if not os.path.isdir(folder_to_track + '/' + file):
                src = folder_to_track + '/' + file
                fileName, file_extension = os.path.splitext(file)
                if checkFileType(file_extension, IMAGE_EXTENSIONS):
                    new_destination = getNewDestination(
                        '/Images', folder_to_track, fileName, file_extension)
                elif checkFileType(file_extension, PDF_EXTENSIONS):
                    new_destination = getNewDestination(
                        '/Pdfs', folder_to_track, fileName, file_extension)
                elif checkFileType(file_extension, ISOS_EXTENSIONS):
                    new_destination = getNewDestination(
                        '/Isos', folder_to_track, fileName, file_extension)
                elif checkFileType(file_extension, AUDIO_EXTENSIONS):
                    new_destination = getNewDestination(
                        '/Audios', folder_to_track, fileName, file_extension)
                elif checkFileType(file_extension, VIDEO_EXTENSIONS):
                    new_destination = getNewDestination(
                        '/Videos', folder_to_track, fileName, file_extension)
                elif checkFileType(file_extension, COMPRESSED_EXTENSIONS):
                    new_destination = getNewDestination(
                        '/Compressed', folder_to_track, fileName, file_extension)
                elif checkFileType(file_extension, IGNORED_EXTENSIONS):
                    break
                else:
                    new_destination = getNewDestination(
                        '/Others', folder_to_track, fileName, file_extension)
                os.rename(src, new_destination)


def checkIfExistsOrCreate(name):
    """ Check if the directory exists, if it doesn't exist create it

    Args:
        name (str): the name of the directory
    """
    if not os.path.isdir(folder_to_track + name):
        os.mkdir(folder_to_track + name)


def checkFileType(extension, types):
    """Check if the given extension is on the types array

    Args:
        extension (str): the extension to check
        types (str): the array of extension to compare

    Returns:
        bool: if the extension exists on the types array
    """
    return extension in types


def getNewDestination(path, folder_to_track, fileName, file_extension):
    """Return the new destination

    Args:
        path (str): the path where the file is going to be save
        folder_to_track (str): the parent folder
        fileName (str): the name of the file
        file_extension (str): the extension of the file

    Returns:
        str: the new destination
    """
    checkIfExistsOrCreate(path)
    actual_time = datetime.now()
    full_file_name = fileName + '_' + str(actual_time.hour) + '-' + \
        str(actual_time.minute) + '-' + \
        str(actual_time.second) + file_extension
    return folder_to_track + path + '/' + full_file_name


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=False)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
