from wagtail.admin.modal_workflow import render_modal_workflow


def confirm_dialog(request):
    return render_modal_workflow(
        request,
        html_template='wagtail_content_import/confirm_dialog.html',
        js_template=None,
        template_vars={},
        json_data={'step': 'dialog'}
    )
