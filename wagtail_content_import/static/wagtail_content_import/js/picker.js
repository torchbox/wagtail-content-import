document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-content-import-picker]').forEach(function (element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();

            if (element.dataset.dialogUrl) {
                ModalWorkflow({
                    url: element.dataset.dialogUrl,
                    onload: {
                        'dialog': function(modal) {
                            document.querySelectorAll('[data-content-import-confirm]').forEach(function (element) {
                                element.addEventListener('click', function(e) {
                                    e.preventDefault();
                                    modal.respond('importClicked');
                                    modal.close();
                                });
                            });
                        },
                    },
                    responses: {
                        importClicked: function() {
                            element.dispatchEvent(new Event('openPicker'));
                        }
                    }
                });
            } else {
                element.dispatchEvent(new Event('openPicker'));
            }
        });
    });
});
