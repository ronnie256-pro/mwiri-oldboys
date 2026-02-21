from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class FeaturedNews(models.Model):
    SLOT_UPCOMING = 'upcoming'
    SLOT_COMMUNITY = 'community'
    SLOT_CHOICES = [
        (SLOT_UPCOMING, 'Upcoming Events'),
        (SLOT_COMMUNITY, 'Community Impact'),
    ]

    slot = models.CharField(max_length=32, choices=SLOT_CHOICES)

    # generic relation to any article-like model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    article = GenericForeignKey('content_type', 'object_id')

    title = models.CharField(max_length=255, blank=True, help_text='Optional override title; if blank the article title is used')
    hero_image = models.ImageField(upload_to='updates/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Featured News'
        verbose_name_plural = 'Featured News'

    def __str__(self):
        return f"{self.get_slot_display()} - {self.get_title() or str(self.article) if self.article else 'Unlinked'}"

    def get_title(self):
        if self.title:
            return self.title
        if self.article and hasattr(self.article, 'title'):
            return getattr(self.article, 'title')
        return ''

    def get_url(self):
        # Prefer article.get_absolute_url, fallback to resolving a 'news_detail' pattern with the object id
        if self.article:
            if hasattr(self.article, 'get_absolute_url'):
                try:
                    return self.article.get_absolute_url()
                except Exception:
                    pass
        from django.urls import reverse
        try:
            return reverse('news_detail', args=[self.object_id])
        except Exception:
            return '#'
