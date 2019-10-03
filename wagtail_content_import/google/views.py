import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from wagtail.admin.forms.search import SearchForm

from .utils import get_auth_url, get_oauth_credentials, save_oauth_credentials, search_documents


logger = logging.getLogger(__name__)


def process_google_oauth(request):
    if request.GET.get('error'):
        logger.error('Google OAuth failed: %s', request.GET['error'])
        messages.error(
            request,
            'An error occurred whilst connecting your Google account, please try again.'
        )
        return HttpResponseRedirect(request.session.get('oauth_failed_redirect_uri', '/'))
    else:
        save_oauth_credentials(request)
        messages.success(request, 'Google account connected.')
        request.session['oauth_completed'] = True
        return HttpResponseRedirect(request.session.get('oauth_complete_redirect_uri', '/'))


class GoogleDocSearchView(View):

    def get(self, request, *args, **kwargs):
        creds = get_oauth_credentials(self.request.user)
        docs = search_documents(creds, q=request.GET.get('q'))
        return render(request, 'wagtail_content_import/google_doc_results.html', {
            'documents': docs,
            'query_string': request.GET.get('q'),
        })


class GoogleDocImportChooserView(TemplateView):
    template_name = 'wagtail_content_import/google_doc_import_chooser.html'

    def get(self, request, *args, **kwargs):
        if not get_oauth_credentials(request.user):
            request.session['oauth_complete_redirect_uri'] = request.get_full_path()
            return HttpResponseRedirect(get_auth_url(request))
        return super().get(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        redirect_url = reverse('cms_news_google_doc_select_parent')
        redirect_url += '?' + urlencode({'google-doc-id': request.POST['docid']})
        return HttpResponseRedirect(redirect_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        creds = get_oauth_credentials(self.request.user)
        ctx['documents'] = search_documents(creds, q=self.request.GET.get('q'))
        ctx['search_form'] = SearchForm(self.request.GET or None, placeholder='Search for documents')
        return ctx
