from cmath import inf
from multiprocessing import context
from re import I
from turtle import title
from django.shortcuts import render

import json
import urllib.request
import string
import random

API_KEY = 'AIzaSyClbdHxbV3ojvOfIArWk2DFx8HWeib_Dm8'

def home(request):
     
     count = 50
     context = {}
     
     # Search Resoult
     if request.method == 'POST':
          searchValue =request.POST['search']
     else:
          searchValue = stringGenerator(3)
          
     context["videos"] = getVideos(50, searchValue)
     return render(request, "main/home.html" , context=context)

def watch(request, id):
     context={}
     context["id"] = id
     context["videos"] = getRelatedVideos(id,5)
    
     video = getVideoData(id)

     context['titleTarget'] = video[1]
     context['publishDateTarget'] = video[3]
     context['descriptionTarget'] = video[4]
     info = getChannleInfo(video[2])
     context['channelInfo_name'] = info[0]
     context['channelInfo_url'] = info[1]
     context['channelInfo_thumb'] = info[2]
     context['channelId'] = video[2]
     return render(request, "main/video.html" , context=context)

def channle(request, id):
     context={}
     context["id"] = id
     context["info"] = getChannleInfo(id)
     return render(request, "main/channle.html" , context=context)

def stringGenerator(size):
     letters = string.ascii_uppercase + string.ascii_lowercase
     ret =  ''.join(random.choice(letters) for i in range(size)) 
     return ret

def getChannleInfo(id):
     urlData = "https://youtube.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}".format(id,API_KEY)
     webURL = urllib.request.urlopen(urlData)
     data = webURL.read()
     encoding = webURL.info().get_content_charset('utf-8')
     results = json.loads(data.decode(encoding))
     for data in results['items']:
          title = ((data['snippet']['title']))
          url = ((data['id']))
          thumb = ((data['snippet']['thumbnails']['default']['url']))
          desc = ((data['snippet']['description']))
          publishedAt =  ((data['snippet']['publishedAt']))
     return [title,url,thumb,desc, publishedAt]

def getRelatedVideos(id,amount):
     urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&relatedToVideoId={}".format(API_KEY,amount,id)
     webURL = urllib.request.urlopen(urlData)
     data = webURL.read()
     encoding = webURL.info().get_content_charset('utf-8')
     results = json.loads(data.decode(encoding))

     videoID = []
     videoTitle =[]
     videoThumb =[]
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

     return zip(videoID,videoTitle,videoThumb)

def getVideos(amount,search):
     urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,amount,search)
     webURL = urllib.request.urlopen(urlData)
     data = webURL.read()
     encoding = webURL.info().get_content_charset('utf-8')
     results = json.loads(data.decode(encoding))
     videoID = []
     videoTitle =[]
     videoThumb =[]
     channelIds =[]

     for data in results['items']:
          id = (data['id']['videoId'])
          title = ((data['snippet']['title']))
          thumb = ((data['snippet']['thumbnails']['medium']['url']))
          channelId = ((data['snippet']['channelId']))
          videoID.append(id)
          videoTitle.append(title)
          videoThumb.append(thumb)
          channelIds.append(channelId)

     return zip(videoID,videoTitle,videoThumb)

def  getVideoData(id):
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

          channelId = ((data['snippet']['channelId'])) 
          publishDateTarget = ((data['snippet']['publishedAt']))
          descriptionTarget = ((data['snippet']['description']))
     
     return [idTarget,titleTarget,channelId,publishDateTarget,descriptionTarget]