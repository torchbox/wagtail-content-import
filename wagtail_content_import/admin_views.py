from wagtail.admin.modal_workflow import render_modal_workflow


def confirm_dialog(request):
    return render_modal_workflow(
        request,
        'wagtail_content_import/confirm_dialog.html',
        None,
        {},
        json_data={'step': 'dialog'}
    )
