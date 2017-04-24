# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from mainsite import models, forms
from django.core.mail import EmailMessage
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

def contact(request):
    if request.method == 'POST':
        #create form instance from request.POST
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = " THANKS for your letter"
            #get data from  class form
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
            #prepare to send email
            mail_body = u''' 網友姓名：{} \
                                        居住城市：{} \
                                        是否在學：{} \
                                        反應意見：如下 \
                                        {}'''.format(user_name, user_city, user_school, user_message)
            
            # EmailMessage
            email = EmailMessage(   '來自【不吐不快】網站的網友意見', 
                                    mail_body, 
                                    user_email,
                                    ['cse3dadakiller@gmail.com'])
            email.send()
        else:
            message = " error: please check your input infomation"
    else:
        #create form instance
        form = forms.ContactForm()
        
    # get_template
    template = get_template('contact.html')
    # for post, use RequestContext to  generate render content
    #request_context = RequestContext(request)
    #request_context.push(locals())
    #render
    html = template.render(locals(), request)
    #response
    return HttpResponse(html)    

def post2db(request):
    if request.method == 'POST':
        #create PostForm instance from request.POST
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            message = "您的訊息已儲存，要等管理者啟用後才看得到喔。"
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message = '如要張貼訊息，則每一個欄位都要填...'
    else:
        #create PostForm instance
        post_form = forms.PostForm()
    # get_template
    template = get_template('post2db.html')
    #moods = models.Mood.objects.all()
    #render
    html = template.render(locals(), request)
    #response
    return HttpResponse(html)