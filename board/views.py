from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post
# Create your views here.

def post_list(request):

    qs = Post.objects.all()
    q = request.GET.get('q','')
    if q:
        qs = qs.filter(title__icontains=q)

    response = render(request, 'board/post_list.html', {
        'post_list' : qs,
        'q' : q,

    })
    return response

def post_detail(request,id):
    post = get_object_or_404(Post,id=id)

    return render(request,'board/post_detail.html',{
        'post' : post
    })

@login_required
def post_create(request):
    ctx = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            post = Post.objects.create(
                title=title,
                content=content,
                name = request.user.get_username()
            )
            url = reverse('board:post_detail', kwargs={
                'id': post.id,
            })
            return redirect(url)
        else:
            error_msg={}
            if not title:
                error_msg.update({'title':'제목을 입력해주세요'})
            if not content:
                error_msg.update({'content': '내용을 입력해주세요'})
            ctx.update({'error':error_msg, })

    return render(request,'board/post_create.html', ctx)

def post_delete(request):
    post = get_object_or_404(Post, id=id)
    post.delete()
   # if request.method == 'POST':

def post_update(request):
    post = get_object_or_404(Post, id=id)
    title = post.title
    content= post.content
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        url = reverse('board:post_detail', kwargs={
            'id': post.id,
        })
        return redirect(url)

    ctx = {
        'post': post,
        'title': title,
        'content': content,
    }
    return render(request, 'post_create.html', ctx)

