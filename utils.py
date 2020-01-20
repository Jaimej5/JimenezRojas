'''
Download youtube mp3
'''
import hashlib
import os.path
import youtube_dl

DOWNLOADS_PATH = "./downloads/"

class NullLogger:
    '''
    NullLogger
    '''
    def debug(self, msg):
        '''
        debug method
        '''
        pass

    def warning(self, msg):
        '''
        warning method
        '''
        pass

    def error(self, msg):
        '''
        error method
        '''
        pass

_YOUTUBEDL_OPTS_ = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}


def download_mp3(url, destination=DOWNLOADS_PATH):
    '''
    Synchronous download from YouTube
    '''
    options = {}
    task_status = {}

    def progress_hook(status):
        '''
        progress hook
        '''
        task_status.update(status)
    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')

    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([url])
    filename = task_status['filename']
    filename = filename[:filename.rindex('.') + 1]
    return filename + options['postprocessors'][0]['preferredcodec']

def hash_file(file_name):
    '''
    Hash
    '''
    file_hash = hashlib.md5()
    complete_path = DOWNLOADS_PATH + file_name
    with open(complete_path, "rb") as new_file:
        for chunk in iter(lambda: new_file.read(4096), b''):
            file_hash.update(chunk)
    return file_hash.hexdigest()
