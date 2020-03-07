from django.shortcuts import render, get_object_or_404
from .models import Blog
from taggit.models import Tag
from .forms import CommentForm


def blog_list(request, tag_slug=None):
    tags = Tag.objects.all()
    blogs = Blog.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        blogs = blogs.filter(tags__in=[tag])
    context = {'tags': tags, 'tag': tag, 'blogs': blogs, 'title': 'Статьи'}
    return render(request, 'blog/list.html', context)

def blog_detail(request, article_slug):
    article = get_object_or_404(Blog, slug=article_slug)
    comments = article.comments.all()
    sent = False
    if request.method == 'POST' and 'comment' in request.POST:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            cd = comment_form.cleaned_data
            sent = True
    else:
        comment_form = CommentForm()
    context = {'article': article, 'title': 'Статьи', 'comments': comments,
    'sent': sent, 'comment_form': comment_form}
    return render(request, 'blog/detail.html', context)
