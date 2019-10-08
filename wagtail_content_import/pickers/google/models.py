from django.conf import settings
from django.db import models

from ...models import ContentImportMixin


class OAuthCredentials(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='content_import_google_oauth_credentials'
    )
    # Data is stored as JSON, but we use a TextField for database compatibility
    data = models.TextField(blank=True)


class GoogleContentImportMixin(ContentImportMixin):

    can_import_from_google = True

    def parse_document(self, document):
        raise NotImplementedError

    class Meta:
        abstract = True
