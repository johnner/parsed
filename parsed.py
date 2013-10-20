#coding:utf-8

import argparse
import requests as r
import json
import threading
import Queue

#number of threads
THREADS_NUM = 5
VK_audio_url = 'http://vk.com/audio'
queue = Queue.Queue()

parser = argparse.ArgumentParser(description='process params')
parser.add_argument('-i', '--id', help='vk.com user id', required=True)
args = parser.parse_args()

class ThreadGrabAudio(threading.Thread):
    """Worker class
    For every download there is a thread which is
    represented by its instance
    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        #queue has tasks?
        while not queue.empty():
            #grab file url from queue
            file = self.queue.get()
            self.download(file)
            self.queue.task_done()

    def download(self, file):
        """Download files asynchronously
        and save them to local directory 'music'
        """
        request = r.get(file.get('link'), stream=True)
        file_name = self.make_filename(file)
        with open(file_name, 'wb') as f:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()

    def make_filename(self, file):
        """Create normalized file name
        consist of author and track name
        """
        author = self.normalize_name(file.get('author'))
        name = self.normalize_name(file.get('name'))
        return 'music/' + author + ' - ' + name + '.mp3'

    def normalize_name(self, name):
        """remove bullshit from the name"""
        return name.replace('/', ' ').replace('\\', ' ')


class Parsed():
    """Parser class
    Creates threading pool to download playlist files
    in parallel
    """
    #yeah, actually it should be dynamic. FIXME
    SID = '1ffacc8452f911ee22889e05449ce6c6cfcef0367cb3da463ef87'

    def __init__(self, vk_id):
        self.vk_id = str(vk_id)

    def run(self):
        pass

    def process_playlist(self):
        audios = self.getAudioJSON(self.SID)
        try:
            all = json.loads(audios)

            for track in all.get('all'):
                file = self.trackToFile(track)
                #populate queue with files for download
                queue.put(file)

            #spawn a thread pool
            for i in range(THREADS_NUM):
                t = ThreadGrabAudio(queue)
                #t.setDaemon(True)
                t.start()

        except Exception, e:
            print e

    def trackToFile(self, track):
        """Converting track (which is array) to file dict
        picking only interesting track info
        """
        return {
            'link': track[2],
            'author': track[5],
            'name': track[6]
        }

    def fix_json(self, json):
        """remove slashes cause it can break downloading"""
        json = json.replace('\'', '"')
        sep_index = json.find('<!>')
        json = json[:sep_index]
        return json

    def getAudioJSON(self, sid):
        """Make request for vk.com audio
        session id must be provided for remixsid cookie param
        """

        res = r.post(
            url=VK_audio_url,
            headers={
                'Cookie': '; '.join([
                    'remixdt=0',
                    'remixtst=8537d36c',
                    'remixlang=0',
                    'remixsid=' + sid,
                    'remixflash=11.9.900',
                    'remixseenads=1'
                ])
            },
            data={
                'act': 'load_audios_silent',
                'al': '1',
                'gid': '0',
                'id': self.vk_id,
                'please_dont_ddos': '2'
            }
        )
        #cut some garbage at the beginning
        #and decode cyrilic symbols in response
        print res
        res = res.content[48:].decode('1251')
        res = self.fix_json(res)
        return res


if __name__ == '__main__':
    #request audio playlist of the user with given id
    if args.id is not None:
        p = Parsed(vk_id=args.id)
        p.process_playlist()
        queue.join()
        print('Playlist successfully downloaded!')
