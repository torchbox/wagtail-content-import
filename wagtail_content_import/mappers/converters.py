import re

import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.base import ContentFile
from django.utils.functional import cached_property
from wagtail.admin.rich_text.converters.contentstate import (
    ContentstateConverter)
from wagtail.images import get_image_model
from wagtail.models import Page, Site
from wagtail.rich_text import RichText
from wagtail.rich_text import features as feature_registry
from wagtail.rich_text.rewriters import LinkRewriter

USER_NEEDS_IMAGE_CHOOSE_PERMISSION = None


def get_user_needs_image_choose_permission():
    global USER_NEEDS_IMAGE_CHOOSE_PERMISSION
    if USER_NEEDS_IMAGE_CHOOSE_PERMISSION is None:
        USER_NEEDS_IMAGE_CHOOSE_PERMISSION = Permission.objects.filter(
            content_type__model='image',
            content_type__app_label='wagtailimages',
            codename='choose_image'
        ).exists()
    return USER_NEEDS_IMAGE_CHOOSE_PERMISSION


class BaseConverter:
    """Base class for all converters, which take a intermediate-form {'type': type, 'value': value} element
    and return a (self.block_name, content) StreamField-compatible tuple on __call__"""

    def __init__(self, block_name):
        self.block_name = block_name

    def __call__(self, element, **kwargs):
        raise NotImplementedError


class RichTextConverter(BaseConverter):
    def __init__(self, block_name, features=None):
        self.features = features
        super().__init__(block_name)

    @cached_property
    def contentstate_converter(self):
        if self.features is None:
            features = feature_registry.get_default_features()
        else:
            features = self.features
        return ContentstateConverter(features=features)

    @cached_property
    def site_root_paths(self):
        return Site.get_site_root_paths()

    def convert_external_links(self, html):
        rewriter = LinkRewriter({'external': self.convert_external_link_tag})
        return rewriter(html)

    def convert_external_link_tag(self, attrs):
        # Convert any external link tags that exactly match internal urls to page links
        href = attrs.get('href', '')
        page = self.get_page_for_url(href)
        if page:
            return f'<a linktype="page" id="{page.pk}">'
        return f'<a linktype="external" href="{href}">'

    def get_page_for_url(self, submitted_url):
        # Strip the url of its query/fragment link parameters - these won't match a page
        url_without_query = re.split(r"\?|#", submitted_url)[0]

        if url_without_query != submitted_url:
            # We only want to convert exact matches
            return

        # Start by finding any sites the url could potentially match
        sites = self.site_root_paths

        possible_sites = [
            (path, url_without_query[len(url) + 1:])
            for pk, path, url, language_code in sites
            if submitted_url.startswith(url)
        ]

        # Loop over possible sites to identify a page match
        for root_path, url in possible_sites:
            matched_pages = Page.objects.filter(url_path=root_path + url)
            page = matched_pages.first()
            if page:
                return page

    def __call__(self, element, **kwargs):
        cleaned_html = self.contentstate_converter.to_database_format(
            self.contentstate_converter.from_database_format(element["value"])
        )

        if getattr(settings, "WAGTAILCONTENTIMPORT_CONVERT_EXTERNAL_LINKS", True):
            cleaned_html = self.convert_external_links(cleaned_html)

        return (self.block_name, RichText(cleaned_html))


class TextConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        return (self.block_name, element["value"])


class ImageConverter(BaseConverter):
    def __call__(self, element, user, **kwargs):
        image_name, image_content = self.fetch_image(element["value"])
        title = element.get("title", "")
        image = self.import_as_image_model(
            image_name, image_content, owner=user, title=title
        )
        return (self.block_name, image)

    @staticmethod
    def fetch_image(url):
        response = requests.get(url)

        if not response.status_code == 200:
            return

        file_name = url.split("/")[-1]
        return file_name, response.content

    @staticmethod
    def import_as_image_model(name, content, owner, title=None):
        if not title:
            title = name
        Image = get_image_model()
        image = Image(title=title, uploaded_by_user=owner)
        image.file = ContentFile(content, name=name)
        # Set image file size
        image.file_size = image.file.size

        # Set image file hash
        image.file.seek(0)
        image._set_file_hash(image.file.read())
        image.file.seek(0)

        # Before we save the image, let's check if there are any choosable images with the same hash
        # so we can avoid importing a duplicate

        from wagtail.images.permissions import permission_policy

        if USER_NEEDS_IMAGE_CHOOSE_PERMISSION:
            existing_images = permission_policy.instances_user_has_any_permission_for(
                owner, ['choose']
            )
        else:
            existing_images = Image.objects.all()

        existing_images = existing_images.filter(file_hash=image.file_hash).iterator(chunk_size=1)
        for potential_duplicate in existing_images:
            if not getattr(settings, "WAGTAILCONTENTIMPORT_CHECK_DUPLICATE_IMAGE_CONTENT", False):
                # We don't need to check the file content
                return potential_duplicate
            # Check the file contents actually match - hash collisions are extremely unlikely by default
            # hence the chunk_size=1, but could happen if someone is using a custom image model with
            # some other hashing scheme
            if potential_duplicate.file.size == image.file.size and all(
                a == b for a, b in zip(potential_duplicate.file.chunks(), image.file.chunks())
            ):
                # We've found an existing image in the library
                # so let's not save our new image, and return this one instead
                return potential_duplicate

        image.save()
        return image


class TableConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        table = element["value"]
        text_table = [[cell.get_text() for cell in row] for row in table.rows]
        return (self.block_name, {"data": text_table})
