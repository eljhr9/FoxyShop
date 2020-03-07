from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Blog


class LatestArticlesFeed(Feed):
    title = 'FoxyShop Blog'
    link = '/blog/'
    description = 'New articles.'

    def items(self):
        return Blog.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
