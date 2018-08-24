from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

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

def post_create(request):
    ctx = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            post = Post.objects.create(
                title=title,
                content=content,
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

    return render(request,'post_create.html', ctx)