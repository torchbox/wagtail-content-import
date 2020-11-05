# Setting Up Google Integration

Wagtail Google Docs integration relies on Google APIs, which you will first need to enable for your project:

1. Navigate to the [Google API Library](https://console.developers.google.com/apis/library). Select a project for your Wagtail site, or create a new one now.

2. Find and enable the [Google Docs](https://console.developers.google.com/apis/library/docs.googleapis.com) and [Google Drive](https://console.developers.google.com/apis/library/drive.googleapis.com) APIs.
    
3. Find and enable the [Google Picker](https://console.developers.google.com/apis/api/picker.googleapis.com) API, and copy its API key to the setting `WAGTAILCONTENTIMPORT_GOOGLE_PICKER_API_KEY`.

4. Open the [Credentials](https://console.developers.google.com/apis/credentials) page in the API Console.

5. Select `Create credentials`, then `OAuth client ID`

6. If you haven't already configured the consent screen, you will need to configure this now.

    1. Under `Scopes for Google APIs`, click `Add scope`.

    2. Add `../auth/documents.readonly` and `../auth/drive.readonly` scopes.

        Note: adding these sensitive scopes means that you will need to submit your project for verification by Google to
        avoid user caps and warning pages during use.
        
    3. Add your domain to `Authorised domains`.

 7. For `Application type`, choose `Web application`

 8. Under `Authorised JavaScript origins`, add your domain.

 9. On the Credentials page, next to your Client ID, click the download item to download a JSON file of your client
    secret.

 10. Copy the text from this file, and use it to set `WAGTAILCONTENTIMPORT_GOOGLE_OAUTH_CLIENT_CONFIG`.

## Note

For users to authenticate with Google and import documents from their Drives, they must either allow third party cookies or add `accounts.google.com` to their allowed domains ([Settings/Privacy and Security/Cookies and other site data in Chrome](chrome://settings/cookies) or [Preferences/Privacy & Security in Firefox](about:preferences#privacy)).
