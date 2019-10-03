from django.db import models


class ContentImportMixin(models.Model):

    def parse_document(self, document):
        """
        Parse a document (the nature of which depends on the importer used)
        and return a dictionary in the form:
        {
            'title': <document_title>,
            'elements': <stream_elements>
        }

        Where <stream_elements> is an iterable of StreamElement objects.
        """
        raise NotImplementedError

    class Meta:
        abstract = True
