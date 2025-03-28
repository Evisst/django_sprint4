from django.shortcuts import render
from .models import Category
from django.shortcuts import get_object_or_404
from .utils import post_filter


def index(request):
    template_name = 'blog/index.html'
    context = {'post_list': post_filter()[0:5]}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    post_list = post_filter().filter(category__title=category.title)
    context = {'category': category, 'post_list': post_list}

    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(post_filter(), pk=id)
    context = {'post': post}
    return render(request, template_name, context)
