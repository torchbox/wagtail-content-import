import json
import uuid

from django.conf import settings
from django.urls import reverse

from dateutil.parser import parse
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

from .models import OAuthCredentials
from .parser import GoogleDocumentParser


def get_flow(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        json.loads(settings.GOOGLE_OAUTH_CLIENT_CONFIG),
        scopes=[
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/documents.readonly'
        ]
    )
    flow.redirect_uri = request.build_absolute_uri('/').strip('/') + reverse('content_import_google:complete_oauth')
    return flow


def get_auth_url(request):
    flow = get_flow(request)
    authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
    return authorization_url


def save_oauth_credentials(request):
    flow = get_flow(request)
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Google only provides a refresh token the first time that consent is provided
    # see https://github.com/googleapis/google-api-python-client/issues/213,
    # so we can't just dump this into the session. We have to persist the refresh
    # token, otherwise the user will have to go through the content flow every time
    # they log out.
    creds, _ = OAuthCredentials.objects.get_or_create(user=request.user)
    creds.data = json.dumps({
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    })
    creds.save()


def get_oauth_credentials(user):
    try:
        stored_creds = user.content_import_google_oauth_credentials
    except OAuthCredentials.DoesNotExist:
        return
    else:
        data = json.loads(stored_creds.data)
        creds = google.oauth2.credentials.Credentials(**data)
        if not creds.valid:
            creds.refresh()
            # Update the stored token, but don't clobber the refresh token as that
            # is not resent
            data['token'] = creds.token
            stored_creds.data = json.dumps(data)
            stored_creds.save()
        return creds


def search_documents(credentials, q=''):
    service = build('drive', 'v3', credentials=credentials)
    name_query = 'and name contains "{}"'.format(q) if q else ''
    query = 'mimeType="application/vnd.google-apps.document" {}'.format(name_query)
    results = service.files().list(
        pageSize=10,
        orderBy='modifiedTime desc',
        fields="nextPageToken, files(id, name, webViewLink, modifiedTime)",
        q=query,
    ).execute()

    files = results.get('files', [])
    # Convert modifiedTime to a datetime object
    for f in files:
        f['modifiedTime'] = parse(f['modifiedTime'])

    return files


def parse_document(credentials, doc_id):
    service = build('docs', 'v1', credentials=credentials)
    document = service.documents().get(documentId=doc_id).execute()
    return GoogleDocumentParser(document).parse()

def create_streamfield_block(block):
    # Add an ID to the block, because wagtail-react-streamfield borks without one
    block['id'] = str(uuid.uuid4())
    return block
