from django.db import models
from grapple.models import GraphQLStreamfield
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import general_blocks


# Create your models here.
class WebsitePage(Page):
    body = StreamField(general_blocks, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('body'),
    ]

    graphql_fields = [
        GraphQLStreamfield('body'),
    ]

    class Meta:
        verbose_name = "Website Page"
        verbose_name_plural = "Website Pages"
