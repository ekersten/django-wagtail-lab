# Generated by Django 4.2.7 on 2023-11-27 14:21

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsitePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('title_and_paragraph', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('paragraph', wagtail.blocks.TextBlock())]))], use_json_field=True)),
            ],
            options={
                'verbose_name': 'Website Page',
                'verbose_name_plural': 'Website Pages',
            },
            bases=('wagtailcore.page',),
        ),
    ]
