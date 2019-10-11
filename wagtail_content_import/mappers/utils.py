import requests
from django.core.files.base import ContentFile
from wagtail.images import get_image_model


def to_tuple(element, new_type=None):
    """
    Converts a parser output element {'type': type, 'value': value} into (type, value), changing type to new_type if supplied.
    """
    type = new_type if new_type else element['type']
    return (type, element['value'])


def image_element_to_tuple(element):
    url = element['value']
    image = import_image_from_url(url)
    return ('image', image)


def import_image_from_url(url):
    response = requests.get(url)

    if not response.status_code == 200:
        return

    file_name = url.split("/")[-1]

    Image = get_image_model()
    image = Image(title=file_name)
    image.file.save(file_name, ContentFile(response.content))
    image.save()

    return image