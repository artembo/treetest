from django.shortcuts import render, HttpResponse, get_object_or_404
import requests 
from multiprocessing.dummy import Pool as ThreadPool 
from bs4 import BeautifulSoup as bs
import time 
from random import shuffle 
from tree.models import Referat 

class Profiler(object): 
    def __enter__(self):
        self._startTime = time.time() 
         
    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)

def generate(request):
	urls = []
	if request.method == 'POST':
		threads = int(request.POST['threads'])
		copies = int(request.POST['copies'])
		first = int(request.POST['first'])
		second = int(request.POST['second'])
		third = int(request.POST['third'])
		fourth = int(request.POST['fourth'])

		def get_content(link):
			page = requests.get(link)
			soup = bs(page.content, "lxml")
			referat = ""
			referats__text = soup.find("div", { "class" : "referats__text" })
			title = referats__text.find('strong').get_text()

			for p in referats__text.find_all("p"):
			    referat += p.get_text()

			Referat.objects.create(name=title, text=referat)

			for _ in range(1, copies):

				tmp_list = title.split(' ')
				shuffle(tmp_list)
				mixed_title = ' '.join(tmp_list)

				tmp_list = referat.split(' ')
				shuffle(tmp_list)
				mixed_referat = ' '.join(tmp_list)

				Referat.objects.create(name=mixed_title, text=mixed_referat)


			return referat

		uniques = (first + second + third + fourth) // copies

		print uniques
		for x in range (100, 100 + uniques):
			urls += ['https://yandex.ru/referats/?t=mathematics&s=%s' % str(x)]

		with Profiler() as p:
			# Make the Pool of workers
			pool = ThreadPool(int(threads)) 
			# Open the urls in their own threads
			# and return the results
			results = pool.map(get_content, urls)

			#close the pool and wait for the work to finish 
			pool.close() 
			pool.join() 
		#for result in results:
		#    print result

		full_set = Referat.objects.all()
		first_set = full_set[0:first]
		second_set = full_set[first:(first+second)]
		third_set = full_set[(first+second):(first+second+third)]
		fourth_set = full_set[(first+second+third):(first+second+third+fourth)]
		with Referat.objects.disable_mptt_updates():
			for ind in range(0,second):
				chld = second_set[ind]
				chld.parent = first_set[first - 1 - (ind % first)]
				chld.save()

			for ind in range(0,third):
				chld = third_set[ind]
				chld.parent = second_set[second - 1 - (ind % second)]
				chld.save()

			for ind in range(0,fourth):
				chld = fourth_set[ind]
				chld.parent = third_set[fourth - 1 - (ind % fourth)]
				chld.save()

		Referat.objects.rebuild()


		return HttpResponse('success')
	else:
		return HttpResponse('Please use POST')

def delete(request):
	if request.method == 'POST':
		Referat.objects.all().delete()
		return HttpResponse('All objects have been deleted')

def index(request):
	referats = Referat.objects.all()
	return render(request, 'tree/index.html', { 'referats': referats })

def detail(request, pk):
	referats = Referat.objects.all()
	referat = get_object_or_404(Referat, pk=pk)
	args = {
		'referats': referats,
		'ref': referat,
		'key': pk
	}
	return render(request, 'tree/detail.html', args)