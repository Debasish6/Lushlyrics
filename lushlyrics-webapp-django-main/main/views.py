from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import playlist_user
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json

# import cardupdate



f = open('card.json', 'r')
CONTAINER = json.load(f)

def default(request):
    global CONTAINER
    if request.method == 'GET':
      if request.user.is_anonymous:
        return redirect('login')

    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})



def playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})


def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})




def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])

def signup_view(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request,user)
      return redirect('default')
  
  else:
    initial_data={'username':'','password1':'','password2':''}
    form = UserCreationForm(initial=initial_data)
  return render(request,'signup.html',{'form':form})

def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request,data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request,user)
      return redirect('default')
  
  else:
    data = {'username':'','password':''}
    form = AuthenticationForm(request,initial=data)
  return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    print("Log out Successfuly")
    return redirect('login')
