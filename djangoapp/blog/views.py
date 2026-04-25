from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpRequest
from blog.models import Post

PER_PAGE = 9


def index(request: HttpRequest):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request: HttpRequest):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request: HttpRequest):
    return render(
        request,
        'blog/pages/post.html',
        {
            # 'page_obj': page_obj,
        }
    )
