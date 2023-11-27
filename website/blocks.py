from wagtail import blocks


class TitleAndParagraphBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    paragraph = blocks.TextBlock()

    class Meta:
        label = "Title and Paragraph"


general_blocks = [
    ("title_and_paragraph", TitleAndParagraphBlock()),
]
