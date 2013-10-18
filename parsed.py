#coding:utf-8

import requests
from BeautifulSoup import BeautifulSoup 

VK_audios = 'http://vk.com/audios'

class Parsed:
    '''
    Parser class
    '''

    def __init__(self, vk_id):
        self.vk_id = str(vk_id)
        rq = self.make_request()
        soup = BeautifulSoup(rq.text)
        print soup.prettify()
		
        #BeautifulSoup or pyQuery

		
    def make_request(self):
	'''Request playlist
	'''
        r = requests.get(VK_audios + self.vk_id)
        return r

if __name__ == '__main__':
    p = Parsed(vk_id=825978)
