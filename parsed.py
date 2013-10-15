#coding:utf-8

import requests
import BeautifulSoup as BS
VK_audios = 'http://vk.com/audios'

class Parsed:
    '''
    Parser class
    '''

    def __init__(self, vk_id):
        self.vk_id = str(vk_id)
        rq = self.make_request()
        rq.text
        #BeautifulSoup or pyQuery

    def make_request(self):
        r = requests.get(VK_audios + self.vk_id)
        return r

p = Parsed(vk_id=825978)
