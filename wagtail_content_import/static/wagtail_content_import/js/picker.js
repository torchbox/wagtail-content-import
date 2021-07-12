document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-content-import-picker]').forEach(function (element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            element.dispatchEvent(new Event('openPicker'));
        });
    });
});
