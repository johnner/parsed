#coding:utf-8

import requests as r
import json

VK_audio_url = 'http://vk.com/audio'


def run_async(func):
    """
        run_async(func)
            function decorator, intended to make "func" run in a separate
            thread (asynchronously).
            Returns the created Thread object
    """
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


class Parsed:
    """Parser class"""
    #yeah, actually it should be dynamic. FIXME
    SID = '1ffacc8452f911ee22889e05449ce6c6cfcef0367cb3da463ef87'

    def __init__(self, vk_id):
        self.vk_id = str(vk_id)
        audios = self.getAudioJSON(self.SID)
        # make json valid and remove slashes cause it can break downloading
        self.audios = self.fix_json(audios)
        self.process_playlist()
        #print json_data

    def process_playlist(self):
        try:
            all = json.loads(self.audios)
            for track in all.get('all'):
                file = {
                    'link': track[2],
                    'author': track[5],
                    'name': track[6]
                }
                try:
                    self.download(file)
                except:
                    print 'file process problem'
        except:
            print 'JSON format error'

    @run_async
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
        '''Create normalized file name
        consist of author and track name
        '''
        author = self.normalize_name(file.get('author'))
        name = self.normalize_name(file.get('name'))
        return 'music/' + author + ' - ' + name + '.mp3'

    def normalize_name(self, name):
        '''remove bullshit from the name
        '''
        return name.replace('/', ' ').replace('\\', ' ')

    def fix_json(self, json):
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
                    'remixlang=0',
                    'remixsid=' + sid,
                    'remixflash=11.9.900',
                    'remixseenads=2'
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
        return res.content[48:].decode('1251')


if __name__ == '__main__':
    p = Parsed(vk_id=825978)
