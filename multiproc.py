# -*- coding: utf-8 -*-
import requests 
from multiprocessing.dummy import Pool as ThreadPool 
from bs4 import BeautifulSoup as bs
import time 
from random import shuffle, sample

urls = [
    'https://yandex.ru/referats/?t=mathematics&s=8273', 
    'https://yandex.ru/referats/?t=mathematics&s=1111',
    ]
 
class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)

def get_content(link):
    page = requests.get(link)
    soup = bs(page.content, "lxml")
    referat = ""
    referats__text = soup.find("div", { "class" : "referats__text" })
    title = referats__text.find('strong').get_text()
    print title

    tmp_list = title.split(' ')
    shuffle(tmp_list)
    mixed_title = ' '.join(tmp_list)

    for p in referats__text.find_all("p"):
        referat += p.get_text()
    print referat
    return referat

for x in range (100, 200):
    urls += ['https://yandex.ru/referats/?t=mathematics&s=%s' % str(x)]

with Profiler() as p:
    # Make the Pool of workers
    pool = ThreadPool(8) 
    # Open the urls in their own threads
    # and return the results
    results = pool.map(get_content, urls)

    #close the pool and wait for the work to finish 
    pool.close() 
    pool.join() 
#for result in results:
#    print result
