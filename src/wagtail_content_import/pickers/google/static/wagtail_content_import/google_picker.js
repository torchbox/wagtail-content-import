(function() {
    const GOOGLE_API_SCOPE = 'https://www.googleapis.com/auth/documents.readonly https://www.googleapis.com/auth/drive.readonly';

    class GooglePicker {
        constructor(authOptions, importPageUrl, csrfToken) {
            this.authOptions = authOptions;
            this.importPageUrl = importPageUrl;
            this.csrfToken = csrfToken;

            this.clientInitialised = false;
            this.accessToken = localStorage.getItem("contentImportGoogleAccessToken");
        }

        picker() {
            let docsView = new google.picker.DocsView(google.picker.ViewId.DOCS)
                .setMimeTypes("application/vnd.google-apps.document")
                .setSelectFolderEnabled(true)
                .setIncludeFolders(true);

            let sharedDrivesView = new google.picker.DocsView(google.picker.ViewId.DOCS)
                .setMimeTypes("application/vnd.google-apps.document")
                .setSelectFolderEnabled(true)
                .setIncludeFolders(true)
                .setEnableDrives(true);

            const picker = new google.picker.PickerBuilder()
                .setAppId(this.authOptions.appId)
                .setDeveloperKey(this.authOptions.pickerApiKey)
                .setOAuthToken(this.accessToken)
                .addView(docsView)
                .addView(sharedDrivesView)
                .setCallback(this.getPickerCallBack())
                .build();

            picker.setVisible(true);
        }

        getPickerCallBack() {
            // The callback will be executed with `this' not bound to an instance of this class,
            // so bind the required members in a closure
            const { csrfToken, importPageUrl } = this;
            return (data) => {
                if (data.action == google.picker.Action.PICKED) {
                    gapi.client.docs.documents.get({
                        documentId: data.docs[0].id
                    }).then((response) => {
                        // POST the JSON content of the document to the create page view
                        // Use a hidden form so the browser reloads with the result of this request
                        let form = document.createElement('form');
                        form.action = importPageUrl;
                        form.method = 'POST';
                        form.style.visibility = 'hidden';
                        document.body.appendChild(form);

                        let csrfTokenField = document.createElement('input');
                        csrfTokenField.type = 'hidden';
                        csrfTokenField.name = 'csrfmiddlewaretoken';
                        csrfTokenField.value = csrfToken;
                        form.appendChild(csrfTokenField);

                        let googleDocField = document.createElement('input');
                        googleDocField.type = 'hidden';
                        googleDocField.name = 'google-doc';
                        googleDocField.value = response.body;
                        form.appendChild(googleDocField);

                        form.submit();
                    });
                }
            };
        }

        show() {
            if (!window.googlepicker_client_loaded && !window.googlepicker_api_loaded) {
                console.warn("Google APIs aren't loaded yet");
                return;
            }

            if (!this.clientInitialised) {
                gapi.load('client', async () => {
                    await gapi.client.init({
                        apiKey: this.authOptions.pickerApiKey,
                        discoveryDocs: ['https://docs.googleapis.com/$discovery/rest?version=v1'],
                    });
                    this.clientInitialised = true;
                    gapi.load('picker', () => { this.show() });
                });
            } else {
                let tokenClient = google.accounts.oauth2.initTokenClient({
                    client_id: this.authOptions.clientId,
                    scope: GOOGLE_API_SCOPE,
                    callback: async (response) => {
                        if (response.error !== undefined) {
                            throw (response);
                        }
                        localStorage.setItem("contentImportGoogleAccessToken", response.access_token);
                        this.accessToken = response.access_token;
                        this.picker();
                    }
                });

                if (this.accessToken === null) {
                    // Prompt the user to select a Google Account and ask for consent to share their data
                    // when establishing a new session.
                    tokenClient.requestAccessToken({prompt: 'consent'});
                } else {
                    // Skip display of account chooser and consent dialog for an existing session.
                    tokenClient.requestAccessToken({prompt: ''});
                }
            }
        }
    }

    window.GooglePicker = GooglePicker;
})();
