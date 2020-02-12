(function() {
    const GOOGLE_API_SCOPE = 'https://www.googleapis.com/auth/documents.readonly https://www.googleapis.com/auth/drive.readonly';

    class GooglePicker {
        constructor(authOptions, createPageUrl, csrfToken) {
            this.authOptions = authOptions;
            this.createPageUrl = createPageUrl;
            this.csrfToken = csrfToken;

            this.googleApisLoaded = false;
            this.showOnReady = false;

            // Load auth and picker APIs
            gapi.load('client:auth2:picker', () => {
                gapi.client.init({
                    apiKey: this.authOptions.pickerApiKey,
                    clientId: this.authOptions.clientId,
                    discoveryDocs: ['https://docs.googleapis.com/$discovery/rest?version=v1'],
                    scope: GOOGLE_API_SCOPE
                }).then(() => {
                    this.googleApisLoaded = true;

                    if (this.showOnReady) {
                        this.show();
                    }
                }).catch(error => {
                    console.error(error);
                });
            });
        }

        authenticate() {
            const googleAuth = gapi.auth2.getAuthInstance();

            if (googleAuth.isSignedIn.get()) {
                return Promise.resolve(googleAuth.currentUser.get().getAuthResponse());
            }

            return googleAuth.signIn({ scope: GOOGLE_API_SCOPE }).then((result) => {
                return result.getAuthResponse();
            });
        }

        picker(oauthToken, callback) {
            let docsView = new google.picker.DocsView(google.picker.ViewId.DOCUMENTS);
            docsView.setMimeTypes("application/vnd.google-apps.document");
            docsView.setSelectFolderEnabled(true);
            docsView.setIncludeFolders(true);


            let sharedDrivesView = new google.picker.DocsView(google.picker.ViewId.DOCUMENTS);
            sharedDrivesView.setMimeTypes("application/vnd.google-apps.document");
            sharedDrivesView.setSelectFolderEnabled(true);
            sharedDrivesView.setIncludeFolders(true);
            sharedDrivesView.setEnableDrives(true);


            let picker = new google.picker.PickerBuilder()
                .enableFeature(google.picker.Feature.SUPPORT_DRIVES)
                .setAppId(this.authOptions.appId)
                .setDeveloperKey(this.authOptions.pickerApiKey)
                .setOAuthToken(oauthToken)
                .addView(docsView)
                .addView(sharedDrivesView)
                .setCallback(callback)
                .build();

            picker.setVisible(true);
        }

        show() {
            if (!this.googleApisLoaded) {
                console.warn("Google APIs aren't loaded yet");
                this.showOnReady = true;
                return;
            }

            this.authenticate()
                .then(auth => {
                    return this.picker(auth.access_token, (data) => {
                        if (data.action == google.picker.Action.PICKED) {
                            gapi.client.docs.documents.get({
                                documentId: data.docs[0].id
                            }).then((response) => {
                                // POST the JSON content of the document to the create page view
                                // Use a hidden form so the browser reloads with the result of this request
                                let form = document.createElement('form');
                                form.action = this.createPageUrl;
                                form.method = 'POST';
                                form.style.visibility = 'hidden';
                                document.body.appendChild(form);

                                let csrfTokenField = document.createElement('input');
                                csrfTokenField.type = 'hidden';
                                csrfTokenField.name = 'csrfmiddlewaretoken';
                                csrfTokenField.value = this.csrfToken;
                                form.appendChild(csrfTokenField);

                                let googleDocField = document.createElement('input');
                                googleDocField.type = 'hidden';
                                googleDocField.name = 'google-doc';
                                googleDocField.value = response.body;
                                form.appendChild(googleDocField);

                                form.submit();
                            });
                        }
                    });
                });
        }
    }

    window.GooglePicker = GooglePicker;
})();
