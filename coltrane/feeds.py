from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.contrib.sites.models import Site
try:
    from django.contrib.syndication.feeds import Feed # For old versions of django
except ImportError:
    from django.contrib.syndication.views import Feed

from coltrane.models import Category, Entry, Link


current_site = Site.objects.get_current()


class LatestEntriesFeed(Feed):
    author_name = "Mark Liu"
    #copyright = "http://%s/about/copyright/" % current_site.domain
    description = "Latest entries posted to Mark's Blog"
    description_template = "coltrane/feeds/latest_description.html"
    subtitle = "Latest entries posted to Mark's Blog"
    feed_type = Rss201rev2Feed
    #item_copyright = "http://%s/about/copyright/" % current_site.domain
    item_author_name = "Mark Liu"
    item_author_link = "http://%s/" % current_site.domain
    link = "/feeds/latest/"
    title = "Mark Liu: Blog Posts"
    title_template = "coltrane/feeds/latest_title.html"
    
    def items(self):
        return Entry.live.all()

    def item_pubdate(self, item):
        return item.pub_date
    
    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain, item.pub_date.strftime('%Y-%m-%d'), item.get_absolute_url())
    
    def item_categories(self, item):
        return [c.title for c in item.categories.all()]


class LatestLinksFeed(Feed):
    author_name = "Mark Liu"
    copyright = "http://%s/about/copyright/" % current_site.domain
    description = "Latest entries posted to %s" % current_site.name
    feed_type = Atom1Feed
    item_copyright = "http://%s/about/copyright/" % current_site.domain
    item_author_name = "Mark Liu"
    item_author_link = "http://%s/" % current_site.domain
    link = "/feeds/links/"
    title = "%s: Latest links" % current_site.name
    
    def items(self):
        return Link.objects.all()
    
    def item_pubdate(self, item): 
        return item.pub_date
    
    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain, item.pub_date.strftime('%Y-%m-%d'), item.get_absolute_url())
    
    def item_tags(self, item):
        return [t.title for t in item.tags.all()]


# Page 144 in Practical Django Projects 2nd ed
class CategoryFeed(LatestEntriesFeed):
    def get_object(self, request, category_name):
        if not category_name:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=category_name)
    
    def title(self, obj):
        if obj.slug == 'technical':
            return "Mark Liu: Technical Blog Posts"
        elif obj.slug == 'non-technical':
            return "Mark Liu: Non-Technical Blog Posts"
        else:
            return "%s: Latest entries in category '%s'" % (current_site.name, obj.title)
    
    def description(self, obj):
        return "%s: Latest entries in category '%s'" % (current_site.name, obj.title)
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def items(self, obj):
        return obj.live_entry_set()
