var fancypages = fancypages || {};

fancypages.dashboard = {
    preview: {
        init: function () {
            $('.sortable').sortable({
                cursor: 'move',
                handle: '.move',
                update: function (ev, ui) {
                    var dropIndex = ui.item.index(),
                        widgetId = ui.item.data('widget-id');

                    $.getJSON('/dashboard/fancypages/widget/move/' + widgetId + '/' + dropIndex + '/', function (data) {
                        if (data.success) {
                            parent.fancypages.dashboard.pages.refreshPreview();
                        } else {
                            alert('ERROR');
                        }
                    });
                }
            });
        }
    },
    editor: {
        init: function () {
            var wrapperElement = $('div[id=widget_input_wrapper]') || document;

            // initialise wysihtml5 rich-text for editor
            $('.wysihtml5-wrapper', wrapperElement).each(function (elem) {

                var editor = new wysihtml5.Editor($('textarea', this).get(0), {
                    toolbar: $(".wysihtml5-toolbar", this).get(0),
                    parserRules: wysihtml5ParserRules
                });

                // This is the only way to get the 'keyup' event from the wysihtml5
                // editor according to https://github.com/jezdez/django_compressor/issues/99
                editor.observe("load", function () {
                    editor.composer.element.addEventListener("keyup", function () {
                        fancypages.dashboard.editor.updatePreview(editor);
                    });
                });
                // Update the preview whenever the editor window fires the 'change' event
                // meaning whenever the focus is set to another element. "change" applies
                // to both the textarea or the composer.
                editor.on("change", function () {
                    fancypages.dashboard.editor.updatePreview(editor);
                });
                // Listen to this event to be able to update the preview when a command
                // such as "bold" or "italic" is applied to the content. This event is
                // used by wysihtml5 internally to update the textarea with the composer
                // content which means the textarea might not be up-to-date when this
                // event is received. Make sure you use the composer content in this
                // case.
                editor.on("aftercommand:composer", function () {
                    fancypages.dashboard.editor.updatePreview(editor);
                });
            });
        },

        /*
         * Update the preview whenever the content in the editor changes. The editor
         * instance provides the details for referencing the corresponding field in
         * the preview.
         *
         * @param {wysihtml5.Editor} Wysihtml5 Editor instance that provide the
         *      content to update the corresponding preview field with.
         */
        updatePreview: function (editor) {
            var fieldElem = $(editor.textarea.element),
                previewDoc = fancypages.dashboard.pages.getPreviewDocument();

            var widgetId = $(fieldElem).parents('form').data('widget-id');
            var fieldName = $(fieldElem).attr('id').replace('id_', '');

            var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
            previewField.html($(editor.composer.element).html());
        }
    },

    pages: {
        init: function () {
            $('#page-preview').load(function () {
                fancypages.dashboard.pages.addPreviewListeners();
            });

            $('form[data-behaviours~=submit-widget-form]').live('submit', function (ev) {
                ev.preventDefault();
                $('button[type=submit]').attr("disabled", true).html("Processing...");
                $('button').attr("disabled", true);
                fancypages.dashboard.pages.removeModal(this);
                fancypages.dashboard.pages.submitWidgetForm($(this));
            });

            // Listen on modal cancel buttons and hide and remove the modal
            // when clicked.
            $("button[data-behaviours~=remove-modal]").live('click', function (ev) {
                ev.preventDefault();
                fancypages.dashboard.pages.removeModal(this);
            });

            // attach live update listener to all regular input field
            $('div[data-behaviours~=field-live-update]').live('change keyup', function (ev) {
                ev.preventDefault();

                var fieldElem = $('input', this);
                var widgetId = $(this).parents('form').data('widget-id');
                var fieldName = $(fieldElem).attr('id').replace('id_', '');

                var previewDoc = fancypages.dashboard.pages.getPreviewDocument();
                var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
                previewField.html($(fieldElem).val());
            });
        },

        removeModal: function (elem) {
            var modalElem = $(elem).parents('#delete-modal');
            modalElem.remove();
        },

        addPreviewListeners: function () {
            var previewDoc = fancypages.dashboard.pages.getPreviewDocument();

            // initialise drop-down to create a new widget
            $('form[id$=add_widget_form]', previewDoc).submit(function (ev) {
                ev.preventDefault();

                var selection = $("select", this);
                var containerName = $(this).attr('id').replace('_add_widget_form', '');

                var widgetUrl = $(this).attr('action') + selection.val() + "/create/";
                fancypages.dashboard.pages.loadWidgetForm(widgetUrl, containerName);
            });

            // initialise all update widgets
            $('form[id$=update_widget_form]').each(function (idx, form) {
                var selection = $("select", form);
                var containerName = $(form).attr('id').replace('_update_widget_form', '');

                var widgetUrl = "/dashboard/fancypages/widget/update/" + selection.val() + "/";
                fancypages.dashboard.pages.loadWidgetForm(widgetUrl, containerName);

                selection.change(function (ev) {
                    var widgetUrl = "/dashboard/fancypages/widget/update/" + $(this).val() + "/";
                    fancypages.dashboard.pages.loadWidgetForm(widgetUrl, containerName);
                });
            });


            $('.edit-button', previewDoc).click(function (ev) {
                var widget = $(this).parents('.widget');
                var widgetUrl = "/dashboard/fancypages/widget/update/" + $(widget).data('widget-id') + "/";

                fancypages.dashboard.pages.loadWidgetForm(widgetUrl, $(widget).data('container-name'));
            });

            $('div.delete', previewDoc).click(function (ev) {
                var widget = $(this).parents('.widget');

                var deleteUrl = '/dashboard/fancypages/widget/delete/' + $(widget).data('widget-id') + "/";

                $.ajax(deleteUrl).done(function (data) {
                    var widgetWrapper = $('div[id=widget_input_wrapper]');
                    widgetWrapper.after(data);

                    $(data).load(function () {
                        $(this).modal('show');
                    });
                });
            });
        },

        /**
         * Load the the widget form for the specified url
         */
        loadWidgetForm: function (url, containerName) {
            $.ajax(url).done(function (data) {
                var widgetWrapper = $('div[id=widget_input_wrapper]');
                widgetWrapper.html(data);
                $('#page-settings').hide();

                fancypages.dashboard.editor.init();
            });
        },

        /**
         * Submit the widget form using an AJAX call and create or update the
         * corresponding widget. The form is submitted to the URL specified in
         * the action attribute and is removed from the editor panel right after
         * submission was successful.
         */
        submitWidgetForm: function (elem) {
            $.ajax({
                type: "POST",
                url: elem.attr('action'),
                data: elem.serialize()
            }).done(function (data) {
                $('div[id=widget_input_wrapper]').html("");
                $('#page-preview').attr('src', $('#page-preview').attr('src'));
                $('#page-settings').show();
            });
        },

        /**
         * Convenience method to get the current preview document root for handling
         * selectors within the preview page.
         */
        getPreviewDocument: function (elem) {
            return $('#page-preview').contents();
        },

        refreshPreview: function () {
            $('#page-preview').attr('src', $('#page-preview').attr('src'));
        }
    }
};
