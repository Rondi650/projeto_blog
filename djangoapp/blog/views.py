from typing import cast

from blog.models import Page, Post
from blog.models import PostManager
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

PER_PAGE = 9


class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published() # type:ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


# def index(request: HttpRequest) -> HttpResponse:
#     posts: QuerySet[Post] = cast(PostManager, Post.objects).get_published()

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )


def created_by(request: HttpRequest, author_pk: int) -> HttpResponse:
    user = User.objects.filter(pk=author_pk).first()
    if user is None:
        raise Http404()
    posts: QuerySet[Post] = (
        cast(PostManager, Post.objects).get_published()
        .filter(created_by__pk=author_pk)
    )
    user_full_name = user.username
    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'
    page_title = 'Posts de ' + user_full_name + ' - '

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
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

    if len(page_obj) == 0:
        raise Http404()
    page_title = f'{page_obj[0].category.name} - Categoria - '
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
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

    if len(page_obj) == 0:
        raise Http404()
    page_title = f'{page_obj[0].tags.first().name} - Tag - '
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def search(request: HttpRequest) -> HttpResponse:
    search_value = request.GET.get("search", "").strip()
    posts = (
        cast(PostManager, Post.objects).get_published()
        .filter(
            Q(title__icontains=search_value)
            | Q(excerpt__icontains=search_value)
            | Q(content__icontains=search_value)
        )[:PER_PAGE]
    )
    print(posts.query)

    page_title = f'{search_value[:30]} - Search - '
    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": posts,
            "search_value": search_value,
            "page_title": page_title,
        }
    )


def page(request: HttpRequest, slug: str) -> HttpResponse:
    page_obj = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    if page_obj is None:
        raise Http404()
    page_title = f'{page_obj.title} - Página - '
    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request: HttpRequest, slug: str) -> HttpResponse:
    post_obj: Post | None = (
        cast(PostManager, Post.objects).get_published()
        .filter(slug=slug)
        .first()
    )

    if post_obj is None:
        raise Http404()
    page_title = f'{post_obj.title} - Post - '
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
