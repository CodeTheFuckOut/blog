from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import Post

class LatestPostsFeed( Feed ):
    
    title = "Code The Fuck Out Latest Posts"
    link = "/posts/"
    
    description = "Get our latest tutorials, news and cool projects."

    def items(self):
        return Post.objects.order_by('-timestamp')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:500]

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse( "detail.post", args=[item.pk] )