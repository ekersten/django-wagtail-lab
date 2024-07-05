from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from grapple.helpers import register_streamfield_block
from grapple.models import GraphQLBoolean, GraphQLImage, GraphQLRichText, GraphQLStreamfield, GraphQLString
from wagtail import blocks
from wagtail.admin.staticfiles import versioned_static
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.images.blocks import ImageChooserBlock
from wagtail.telepath import register
from wagtail.templatetags.wagtailcore_tags import richtext
from wagtail_tabbed_structblock.blocks import TabbedStructBlock


@register_streamfield_block
class TitleAndParagraphBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    paragraph = blocks.TextBlock()

    graphql_fields = [
        GraphQLString("title"),
        GraphQLString("paragraph"),
    ]

    class Meta:
        label = "Title and Paragraph"


@register_streamfield_block
class ImageAndRichTextBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    rich_text = blocks.RichTextBlock()

    graphql_fields = [
        GraphQLImage("image"),
        GraphQLRichText("rich_text"),
    ]

    def get_api_representation(self, value, context=None):
        val = super().get_api_representation(value, context)
        val["rich_text"] = str(richtext(value["rich_text"]))
        return val

    class Meta:
        label = "Image and Rich Text"


@register_streamfield_block
class CardBlock(TabbedStructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()
    image = ImageChooserBlock()
    background_color = blocks.CharBlock(default="#FFFFFF")

    graphql_fields = [
        GraphQLString("title"),
        GraphQLRichText("content"),
        GraphQLImage("image"),
        GraphQLString("background_color"),
    ]

    class Meta:
        label = "Card"
        label_format = "Card: {title}"
        template = "blocks/card.html"
        tabs = {
            _("Content"): ("title", "content", "image"),
            _("Background"): ("background_color",),
        }


@register_streamfield_block
class FeaturedCardBlock(TabbedStructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()
    image = ImageChooserBlock()
    background_color = blocks.CharBlock(default="#FFFFFF")
    is_featured = blocks.BooleanBlock(default=False)

    graphql_fields = [
        GraphQLString("title"),
        GraphQLRichText("content"),
        GraphQLImage("image"),
        GraphQLString("background_color"),
        GraphQLBoolean("is_featured"),
    ]

    class Meta:
        label = "Featured Card"
        label_format = "Featured Card: {title}"
        template = "blocks/card.html"
        tabs = {
            _("Content"): ("title", "content", "image"),
            _("Background"): ("background_color",),
            _("Config"): ("is_featured",),
        }


@register_streamfield_block
class CardsDeckBlock(TabbedStructBlock):
    title = blocks.CharBlock()
    footer = blocks.CharBlock()
    cards = blocks.StreamBlock(
        [
            ("card", CardBlock()),
            ("featured_card", FeaturedCardBlock()),
        ]
    )
    background_color = blocks.CharBlock(default="#FFFFFF")

    graphql_fields = [
        GraphQLString("title"),
        GraphQLString("footer"),
        GraphQLString("background_color"),
        GraphQLStreamfield("cards"),
    ]

    class Meta:
        label = "Card Deck"
        template = "blocks/cards_deck.html"
        tabs = {
            _("Content"): ("title",),
            _("Extra"): ("footer",),
            _("Items"): ("cards",),
            _("Background"): ("background_color",),
        }


general_blocks = [
    ("title_and_paragraph", TitleAndParagraphBlock()),
    ("image_and_rich_text", ImageAndRichTextBlock()),
    ("cards_deck", CardsDeckBlock()),
    ("card", CardBlock()),
]
