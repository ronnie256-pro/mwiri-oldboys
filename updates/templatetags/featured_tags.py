from django import template
from updates.models import FeaturedNews

register = template.Library()

@register.simple_tag
def featured_for(slot, limit=1):
    qs = FeaturedNews.objects.filter(slot=slot, active=True).order_by('order')[:int(limit)]
    return list(qs)
