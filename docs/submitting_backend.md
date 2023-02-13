Thanks for being interested in contributing! All contributions should be submitted as pull requests
to the [Wagtail Content Import repository](https://github.com/torchbox/wagtail-content-import).


## Submitting a New Picker

If you're planning on submitting a new picker - apps which enable choosing and importing a file from a
remote source - you'll need to follow this blueprint:

### Overview and File Structure

Inside `wagtail_content_import.pickers`, your app should have the following structure:

- `my_picker`
    - `static`
        - `wagtail_content_import`
            - `MY_PICKER.js`
    - `templates`
        - `wagtail_content_import`
            - `MY_PICKER_js_init.html`
    - `__init__.py`
    - `apps.py`
    - `utils.py`
    - `wagtail_hooks.py`

Where `MY_PICKER` should be replaced with the name of your picker.

- `MY_PICKER.js` provides the JavaScript class for your picker, which will select a file and make
a POST request to the page with relevant data using a hidden form
- `MY_PICKER_js_init.html` creates an instance of that class on the `Create` page, using
  a template filled in with the relevant settings,
  and sets up a listener to call that class's `.show()` method on clicking the relevant import
  button.
- `__init__.py` and `apps.py` set your app's name and label.
- `utils.py` adds your Python picker class, eg `GooglePicker`
- `wagtail_hooks.py` registers your picker using a Wagtail hook, and adds a `before_create_page` hook
to actually take the POST-ed document data and import it, using a parser.

The following examples will follow a picker which needs a variable `AUTH_PARAMETERS` available in the
JavaScript in order to import content.

#### `MY_PICKER.js`

This adds the JavaScript class for your picker, and adds it to the window. It should implement
a method to show the picker, and upon choosing, make a POST request to the page using a hidden form
with relevant data that allows Wagtail to import the document: for the Google picker, this is a JSON
containing the document; for the Microsoft picker, this is a temporary url allowing the file to be downloaded.

Eg:

```javascript
(function() {
    class MyPicker {
        constructor(AUTH_PARAMETERS, importPageUrl, csrfToken) {
        this.AUTH_PARAMETERS = AUTH_PARAMETERS;
        this.importPageUrl = importPageUrl;
        this.csrfToken = csrfToken;
        }

        post_data(response) {
            // POST relevant data to the page
            // Use a hidden form so the browser reloads with the result of this request
            let form = document.createElement('form');
            form.action = this.importPageUrl;
            form.method = 'POST';
            form.style.visibility = 'hidden';
            document.body.appendChild(form);

            let csrfTokenField = document.createElement('input');
            csrfTokenField.type = 'hidden';
            csrfTokenField.name = 'csrfmiddlewaretoken';
            csrfTokenField.value = this.csrfToken;
            form.appendChild(csrfTokenField);

            let myDocField = document.createElement('input');
            myDocField.type = 'hidden';
            myDocField.name = 'my-doc';
            myDocField.value = response.value;
            form.appendChild(myDocField);

            form.submit();
        }


        show() {
          # Open the picker here, and call this.post_data(response) on successfully getting a file
        }
    }

    window.MyPicker = MyPicker;
})();
```

#### `MY_PICKER_js_init.html`

This should provide a Django template which creates an instance of your JS picker class, populated with
the relevant variables, which can be filled in by the Django side using your Python picker class. It must also add a listener to the
relevant import button, such that when it is clicked, it calls `myPicker.show()`.

Eg:

```html
<script type="text/javascript">
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('[data-content-import-picker="my_picker"]').forEach(function (element) {
            let myPicker = new MyPicker({{ AUTH_PARAMETERS }}, element.dataset.importPageUrl, '{{ csrf_token|escapejs }}');

            element.addEventListener('openPicker', function() {
                myPicker.show();
            });
        });
    });
</script>

```

#### `__init__.py` and `apps.py`

`init.py`:

```python
default_app_config = 'wagtail_content_import.pickers.my_picker.apps.WagtailContentImportMyPickerAppConfig'
```

`apps.py`:

```python
from django.apps import AppConfig


class WagtailContentImportMyPickerAppConfig(AppConfig):
    name = 'wagtail_content_import.pickers.my_picker'
    label = 'wagtail_content_import_my_picker'
    verbose_name = "Wagtail Content Import - My Picker"
```

#### `utils.py`

Here, you'll need to create the Python class for your new picker, which will provide the names
and context needed by the `js_init` template.

```python
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail_content_import.pickers import Picker


class MyPicker(Picker):
    name = "my_picker"
    verbose_name = "My Picker"

    def __init__(self, AUTH_PARAMETERS):
        self.AUTH_PARAMETERS = AUTH_PARAMETERS

    def get_context(self):
        return {
            'picker': self,
            'AUTH_PARAMETERS': self.AUTH_PARAMETERS,
        }

    js_template = 'wagtail_content_import/MY_PICKER_js_init.html'

    def render_js_init(self, request):
        return mark_safe(render_to_string(self.js_template, self.get_context(), request=request))

    class Media:
        css = {}
        js = [
            # ANY EXTRA JS YOU NEED HERE
            'wagtail_content_import/MY_PICKER.js',
        ]
```

### `wagtail_hooks.py`

Finally, here you'll need to register your picker, and add a `before create page` hook to actually
import posted content.

Eg:

```python
from django.conf import settings

from wagtail import hooks

from .utils import MyPicker

from ...utils import create_page_from_import, is_importing, set_importing


@hooks.register("before_create_page")
def create_from_my_doc(request, parent_page, page_class):
    if "my-doc" in request.POST and not is_importing(request):
        set_importing(request)
        parsed_doc = # PARSE THE DOCUMENT HERE
        return create_page_from_import(request, parent_page, page_class, parsed_doc)


@hooks.register('register_content_import_picker')
def register_content_import_picker():
    return MyPicker(
        settings.AUTH_PARAMETERS,
    )
```
