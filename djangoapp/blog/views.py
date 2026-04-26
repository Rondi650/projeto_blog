from typing import cast

from blog.models import Post, PostManager
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

PER_PAGE = 9


def index(request: HttpRequest) -> HttpResponse:
    posts: QuerySet[Post] = cast(PostManager, Post.objects).get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request: HttpRequest, author_pk: int) -> HttpResponse:
    posts: QuerySet[Post] = (
        cast(PostManager, Post.objects).get_published()
        .filter(created_by__pk=author_pk)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request: HttpRequest, slug: str) -> HttpResponse:
    posts: QuerySet[Post] = (
        cast(PostManager, Post.objects).get_published()
        .filter(category__slug=slug)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def tag(request: HttpRequest, slug: str) -> HttpResponse:
    posts: QuerySet[Post] = (
        cast(PostManager, Post.objects).get_published()
        .filter(tags__slug=slug)
    )
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request: HttpRequest, slug: str) -> HttpResponse:
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request: HttpRequest, slug: str) -> HttpResponse:
    post: Post | None = (
        cast(PostManager, Post.objects).get_published()
        .filter(slug=slug)
        .first()
    )

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )
