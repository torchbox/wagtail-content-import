(function() {
    class MicrosoftPicker {
        constructor(authOptions, createPageUrl, csrfToken) {
            this.authOptions = authOptions;
            this.createPageUrl = createPageUrl;
            this.csrfToken = csrfToken;

            this.showOnReady = false;
        }

        post_url(response) {
                                // POST the download url of the document to the create page view
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

                                let microsoftDocField = document.createElement('input');
                                microsoftDocField.type = 'hidden';
                                microsoftDocField.name = 'microsoft-doc';
                                microsoftDocField.value = response.value[0]["@microsoft.graph.downloadUrl"];
                                form.appendChild(microsoftDocField);

                                form.submit();
        }


        show() {
                OneDrive.open({
                                clientId: "4ae1526e-127e-4092-aae7-cda7dd01d3ab",
                                action: "download",
                                advanced: {
                                            redirectUri: "http://localhost:8000/testauth/"
                                            },
                                success: response => {this.post_url(response)},
                                cancel: function() { /* cancel handler */ },
                                error: function(error) { /* error handler */ }
                                });
                }
        }

    window.MicrosoftPicker = MicrosoftPicker;
})();
