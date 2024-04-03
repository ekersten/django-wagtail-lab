from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from grapple.helpers import register_streamfield_block
from grapple.models import GraphQLImage, GraphQLRichText, GraphQLString
from wagtail import blocks
from wagtail.admin.staticfiles import versioned_static
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.images.blocks import ImageChooserBlock
from wagtail.telepath import register
from wagtail.templatetags.wagtailcore_tags import richtext


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


class TabbedStructBlock(blocks.StructBlock):
    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix, errors)
        return context

    class Meta:
        form_classname = "tabbed-struct-block"
        form_template = "blocks/tabbed_struct_block.html"
        tabs = {}


class TabbedStructBlockAdapter(StructBlockAdapter):
    js_constructor = "website.blocks.TabbedStructBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + [versioned_static("js/tabbed-struct-block.js")],
            css={"all": (versioned_static("css/tabbed-struct-block.css"),)},
        )


register(TabbedStructBlockAdapter(), TabbedStructBlock)


class CardBlock(TabbedStructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()
    image = ImageChooserBlock()
    background_color = blocks.CharBlock(default="#FFFFFF")

    class Meta:
        label = "Card"
        label_format = "Card: {title}"
        template = "blocks/card.html"
        tabs = {
            _("Content"): ("title", "content", "image"),
            _("Background"): ("background_color",),
        }


class CardsDeckBlock(TabbedStructBlock):
    title = blocks.CharBlock()
    footer = blocks.CharBlock()
    cards = blocks.StreamBlock(
        [
            ("card", CardBlock()),
        ]
    )
    background_color = blocks.CharBlock(default="#FFFFFF")

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
