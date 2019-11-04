from wagtail.core import hooks

from .utils import MicrosoftPicker


@hooks.register('register_content_import_picker')
def register_content_import_picker():
    return MicrosoftPicker()
