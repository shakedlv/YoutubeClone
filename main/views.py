from multiprocessing import context
from django.shortcuts import render

import json
import urllib.request
import string
import random

API_KEY = 'AIzaSyClbdHxbV3ojvOfIArWk2DFx8HWeib_Dm8'

def home(request):
     
     context = {}
     
     count = 50
     random = stringGenerator(3)
     urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,random)
     webURL = urllib.request.urlopen(urlData)
     data = webURL.read()
     encoding = webURL.info().get_content_charset('utf-8')
     results = json.loads(data.decode(encoding))

     videoID = []
     videoTitle =[]
     videoThumb =[]
     for data in results['items']:
          id = (data['id']['videoId'])
          title = ((data['snippet']['title']))
          thumb = ((data['snippet']['thumbnails']['medium']['url']))
          videoID.append(id)
          videoTitle.append(title)
          videoThumb.append(thumb)


     # Search
     if request.method == 'POST':
          searchValue =request.POST['search']
          urlDataSearch = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,searchValue)
          webURLSearch = urllib.request.urlopen(urlDataSearch)
          dataSearch = webURLSearch.read()
          encodingSearch = webURLSearch.info().get_content_charset('utf-8')
          resultsSearch = json.loads(dataSearch.decode(encodingSearch))

          videoID = []
          videoTitle =[]
          videoThumb =[]
          for data in resultsSearch['items']:
               id = (data['id']['videoId'])
               title = ((data['snippet']['title']))
               thumb = ((data['snippet']['thumbnails']['medium']['url']))
               videoID.append(id)
               videoTitle.append(title)
               videoThumb.append(thumb)


     context["videos"] = zip(videoID,videoTitle,videoThumb)

     return render(request, "main/home.html" , context=context)

def watch(request, id):
     context={}
     context["id"] = id

     urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&relatedToVideoId={}".format(API_KEY,5,id)
     print(urlData)
     webURL = urllib.request.urlopen(urlData)
     data = webURL.read()
     encoding = webURL.info().get_content_charset('utf-8')
     results = json.loads(data.decode(encoding))

     videoID = []
     videoTitle =[]
     videoThumb =[]
     for data in results['items']:
          id = (data['id']['videoId'])
          try:
               title = ((data['snippet']['title']))
          except:
               title = "Could not get video title!"
          try:
               thumb = ((data['snippet']['thumbnails']['medium']['url']))
          except:
               thumb = "https://i.ytimg.com/vi/{}/mqdefault.jpg".format(id)
          videoID.append(id)
          videoTitle.append(title)
          videoThumb.append(thumb)

     # Search
     if request.method == 'POST':
          searchValue =request.POST['search']
          urlDataSearch = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,searchValue)
          webURLSearch = urllib.request.urlopen(urlDataSearch)
          dataSearch = webURLSearch.read()
          encodingSearch = webURLSearch.info().get_content_charset('utf-8')
          resultsSearch = json.loads(dataSearch.decode(encodingSearch))

          videoID = []
          videoTitle =[]
          videoThumb =[]
          for data in resultsSearch['items']:
               id = (data['id']['videoId'])
               title = ((data['snippet']['title']))
               thumb = ((data['snippet']['thumbnails']['medium']['url']))
               videoID.append(id)
               videoTitle.append(title)
               videoThumb.append(thumb)

     context["videos"] = zip(videoID,videoTitle,videoThumb)


     urlDataTarget = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}".format(id,API_KEY)
     webURLTarget = urllib.request.urlopen(urlDataTarget)
     dataTarget = webURLTarget.read()
     encodingTarget = webURLTarget.info().get_content_charset('utf-8')
     resultsTarget = json.loads(dataTarget.decode(encodingTarget))


     for data in resultsTarget['items']:
          idTarget = (data['id'])
          try:
               titleTarget = ((data['snippet']['title']))
          except:
               titleTarget = "Could not get video title!"


          publishDateTarget = ((data['snippet']['publishedAt']))
          descriptionTarget = ((data['snippet']['description']))

     context['titleTarget'] = titleTarget
     context['publishDateTarget'] = publishDateTarget
     context['descriptionTarget'] = descriptionTarget
     
     return render(request, "main/video.html" , context=context)


def stringGenerator(size):
     letters = string.ascii_uppercase + string.ascii_lowercase
     ret =  ''.join(random.choice(letters) for i in range(size)) 
     return ret