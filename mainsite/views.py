# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from mainsite import models
# Create your views here.
def index(request, pid=None, del_pass=None):
    # get_template
    template = get_template('index.html')
    # get data from database(Post/Mood)
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()
    try:
        #request.GET: grab info from "index.html"
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message =  '如要張貼訊息，則每一個欄位都要填...'

    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
        except:
            post = None
        if post:
            if post.del_pass == del_pass:
                post.delete()
                message = "資料刪除成功"
            else:
                message = "密碼錯誤"
    elif user_id != None:
        # store data(user_id/user_pass/user_post/user_mood) into database(Post/Mood)  by store api xxx.save()
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message='成功儲存！請記得你的編輯密碼[{}]!，訊息需經審查後才會顯示。'.format(user_pass)

    #render
    html = template.render(locals())
    #response
    return HttpResponse(html)

def listing(request):
    # get_template
    template = get_template('listing.html')
    # get data from database(Post/Mood)
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    #render
    html = template.render(locals())
    #response
    return HttpResponse(html)

def posting(request):
    # get_template
    template = get_template('posting.html')
    # get data from database(Post/Mood)
    moods = models.Mood.objects.all()
    message =  '如要張貼訊息，則每一個欄位都要填...'
    # for post, use RequestContext to  generate render content
    #request_context = RequestContext(request)
    #request_context.push(locals())
    #render
    html = template.render(locals(), request)
    #response
    return HttpResponse(html)    