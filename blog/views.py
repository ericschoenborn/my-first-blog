from django.shortcuts import render
from django.utils import timezone
from .models import Post
from blog.functions.jira_data import main

def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #return render(request, 'blog/post_list.html',{'posts':posts})
    posts = main('pharju')
    thing1 = posts[0]
    thing2 = posts[1]
    thing3 = posts[2]
    return render(request, 'blog/post_list.html',{'posts':thing1, 'posts2':thing2, 'posts3':thing3})
