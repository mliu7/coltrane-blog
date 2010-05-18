from django.db.models import get_model
from django import template

from coltrane.models import Category

register = template.Library()


#class TagsForModelNode(Node):
#    def __init__(self, model, context_var, counts):
#        self.model = model
#        self.context_var = context_var
#        self.counts = counts

#    def render(self, context):
#        model = get_model(*self.model.split('.'))
#        if model is None:
#            raise TemplateSyntaxError(_('tags_for_model tag was given an invalid model: %s') % self.model)
#        context[self.context_var] = Tag.objects.usage_for_model(model, counts=self.counts)
#        return ''


class CategoriesForModelNode(template.Node):
    def __init__(self, model, context_var, counts):
        self.model = model
        self.context_var = context_var
        self.counts = counts
    def render(self, context):
        model = get_model(*self.model.split('.'))
        if model is None:
            raise TemplateSyntaxError(_('categories_for_model tag was given an invalid model: %s') % self.model)
        manager = self.model._default_manager
        if self.model.__name__ == 'Entry':
            manager = self.model.live
        context[self.varname] = manager.all()
        return ''

class LatestContentNode(template.Node):
    def __init__(self, model, num, varname):
        self.model = model
        self.num = int(num)
        self.varname = varname
        
    def render(self, context):
        manager = self.model._default_manager
        if self.model.__name__ == 'Entry':
            manager = self.model.live
        context[self.varname] = manager.all()
        return ''

#def do_tags_for_model(parser, token):
#    """
#    Retrieves a list of ``Tag`` objects associated with a given model
#    and stores them in a context variable.

#    Usage::

#       {% tags_for_model [model] as [varname] %}

#    The model is specified in ``[appname].[modelname]`` format.

#    Extended usage::

#       {% tags_for_model [model] as [varname] with counts %}

#    If specified - by providing extra ``with counts`` arguments - adds
#    a ``count`` attribute to each tag containing the number of
#    instances of the given model which have been tagged with it.

#    Examples::

#       {% tags_for_model products.Widget as widget_tags %}
#       {% tags_for_model products.Widget as widget_tags with counts %}

#    """
#    bits = token.contents.split()
#    len_bits = len(bits)
#    if len_bits not in (4, 6):
#        raise TemplateSyntaxError(_('%s tag requires either three or five arguments') % bits[0])
#    if bits[2] != 'as':
#        raise TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
#    if len_bits == 6:
#        if bits[4] != 'with':
#            raise TemplateSyntaxError(_("if given, fourth argument to %s tag must be 'with'") % bits[0])
#        if bits[5] != 'counts':
#            raise TemplateSyntaxError(_("if given, fifth argument to %s tag must be 'counts'") % bits[0])
#    if len_bits == 4:
#        return TagsForModelNode(bits[1], bits[3], counts=False)
#    else:
#        return TagsForModelNode(bits[1], bits[3], counts=True)

def do_categories_for_model(parser, token):
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits not in (4, 6):
        raise TemplateSyntaxError(_('%s tag requires either three or five arguments') % bits[0])
    if bits[2] != 'as':
        raise TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    if len_bits == 6:
        if bits[4] != 'with':
            raise TemplateSyntaxError(_("if given, fourth argument to %s tag must be 'with'") % bits[0])
        if bits[5] != 'counts':
            raise TemplateSyntaxError(_("if given, fifth argument to %s tag must be 'counts'") % bits[0])
    if len_bits == 4:
        return CategoriesForModelNode(bits[1], bits[3], counts=False)
    else:
        return CategoriesForModelNode(bits[1], bits[3], counts=True)

def do_latest_content(parser, token):
    """
    Gets the most recent items from a model and stores it into a template variable.

    Usage: {% get_latest_content coltrane.link 5 as latest_links %}
    """
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'get_latest_content' tag takes exactly four arguments")
    model_args = bits[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to 'get_latest_content' must be an 'application name'.'model name' string")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid model: %s" % bits[1])
    return LatestContentNode(model, bits[2], bits[4])


register.tag('get_latest_content', do_latest_content)

@register.inclusion_tag('coltrane/tags/categories.html')
def print_event_categories():
    """Return all the categories"""
    return {'categories': Category.objects.all()}

@register.inclusion_tag('coltrane/tags/categories.html')
def print_link_categories():
    """Return all the categories"""
    return {'categories': Category.objects.all()}
