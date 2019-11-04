(function() {
    class MicrosoftPicker {
        constructor(authOptions, createPageUrl, csrfToken) {
            this.authOptions = authOptions;
            this.createPageUrl = createPageUrl;
            this.csrfToken = csrfToken;

            this.showOnReady = false;
        }

        show() {
            OneDrive.open({
  clientId: "4ae1526e-127e-4092-aae7-cda7dd01d3ab",
  action: "download",
  multiSelect: false,
  advanced: {
    redirectUri: "http://localhost:8000/testauth/"
  },
  success: function(files) { /* success handler */ },
  cancel: function() { /* cancel handler */ },
  error: function(error) { /* error handler */ }
});
        }
    }

    window.MicrosoftPicker = MicrosoftPicker;
})();
