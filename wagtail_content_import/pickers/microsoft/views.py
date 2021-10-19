from django.http import HttpResponse
from django.utils.safestring import mark_safe


def auth(request, *args, **kwargs):
    return HttpResponse(
        mark_safe(
            '<!DOCTYPE html><html lang="en"><script type="text/javascript" src="https://js.live.net/v7.2/OneDrive.js"></script></html>'
        )
    )
