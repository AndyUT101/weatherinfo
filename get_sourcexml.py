import os
import urllib3
import threading
from time import localtime, gmtime, strftime
from multiprocessing import Queue
import _thread
from datetime import datetime
WORKER = 5

xml_url = {
	"warning_tc": "http://rss.weather.gov.hk/rss/WeatherWarningSummaryv2_uc.xml",
	"warning_eng": "http://rss.weather.gov.hk/rss/WeatherWarningSummaryv2.xml",
	"current_tc": "http://rss.weather.gov.hk/rss/CurrentWeather_uc.xml",
	"current_eng": "http://rss.weather.gov.hk/rss/CurrentWeather.xml",
	"forecast9day_tc" : "http://rss.weather.gov.hk/rss/SeveralDaysWeatherForecast_uc.xml",
	"forecast9day_eng" : "http://rss.weather.gov.hk/rss/SeveralDaysWeatherForecast.xml",
}


dir_path = os.path.dirname(os.path.abspath(__file__))
export_timestamp = strftime("%Y%m%d%H%M", localtime())

def create_crawleredfile(project_name, urlpath):
	project_path = dir_path + "\\"+ project_name

	http = urllib3.PoolManager()
	r = http.request('GET', urlpath)
	#print (r.data)

	if not os.path.exists(project_path):
		os.makedirs(project_path)

	with open(project_path +"\\export_" + export_timestamp + ".txt", "wb") as file:
	    file.write(r.data)


def process_queueproject():
	global dir_path, export_timestamp, q

	if q.qsize() != 0:
		init_queue_datetime = datetime.now()

		project_name = q.get()
		urlpath = xml_url[project_name]
		project_path = dir_path + "\\" + project_name

		http = urllib3.PoolManager()
		r = http.request('GET', urlpath)
		# print (r.data)

		if not os.path.exists(project_path):
			os.makedirs(project_path)

		with open(project_path + "\\export_" + export_timestamp + ".txt", "wb") as file:
			file.write(r.data)

		end_queue_datetime = datetime.now()
		queue_delta = end_queue_datetime - init_queue_datetime
		print ("Export Project \"{0}\" spent: {1}".format(project_name, queue_delta.total_seconds()))

	#print (q.qsize())

#create_crawleredfile("warning_tc", xml_url["xml_url_warning_tc"])

init_datetime = datetime.now()

q = Queue()
for xml_urlkey in xml_url:
	q.put(xml_urlkey)

#for i in (0, WORKER):
#	_thread.start_new_thread(process_queueproject, ())

while (q.qsize() != 0):
	process_queueproject()

end_datetime = datetime.now()


delta = end_datetime - init_datetime
print ("Overall time spent: {0}".format(delta.total_seconds()))