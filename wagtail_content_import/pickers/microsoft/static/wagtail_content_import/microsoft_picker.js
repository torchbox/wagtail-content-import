(function() {
    class MicrosoftPicker {
        constructor(redirectUri, clientId, createPageUrl, csrfToken) {
            this.redirectUri = redirectUri;
            this.clientId = clientId;
            this.createPageUrl = createPageUrl;
            this.csrfToken = csrfToken;
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
                clientId: this.clientId,
                action: "download",
                advanced: {
                    redirectUri: this.redirectUri,
                    filter: '.docx'
                    },
                success: response => {this.post_url(response)},
                cancel: function() { /* cancel handler */ },
                error: function(error) { /* error handler */ }
                });
        }
    }

    window.MicrosoftPicker = MicrosoftPicker;
})();
