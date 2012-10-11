var fancypages = fancypages || {};
fancypages.dashboard = {
    pages: {
        init: function (){
            $('a[data-toggle="tab"]').on('shown', function (e) {
                //e.target // activated tab
                //e.relatedTarget // previous tab
            });

            var previewDoc = fancypages.dashboard.pages.getPreviewDocument();

            // initialise drop-down to create a new widget
            $('form[id$=add_widget_form]', previewDoc).submit(function(ev) {
                ev.preventDefault();

                var selection = $("select", this);
                var containerName = $(this).attr('id').replace('_add_widget_form', '');

                var widgetUrl = $(this).attr('action')+selection.val()+"/create/";
                fancypages.dashboard.pages.loadWidgetForm(widgetUrl, containerName);
            });

            // initialise all update widgets
            $('form[id$=update_widget_form]').each(function(idx, form){
                var selection = $("select", form);
                var containerName = $(form).attr('id').replace('_update_widget_form', '');

                var widgetUrl = "/dashboard/fancypages/widget/update/"+selection.val()+"/";
                fancypages.dashboard.pages.loadWidgetForm(widgetUrl, containerName);

                selection.change(function(ev) {
                    var widgetUrl = "/dashboard/fancypages/widget/update/"+$(this).val()+"/";
                    fancypages.dashboard.pages.loadWidgetForm(widgetUrl, containerName);
                });
            });


            $('.edit-button', previewDoc).click(function(ev) {
                var widget = $(this).parents('.widget');

                var widgetUrl = "/dashboard/fancypages/widget/update/"+$(widget).data('widget-id')+"/";

                fancypages.dashboard.pages.loadWidgetForm(widgetUrl, $(widget).data('container-name'));
            });

            $('form[data-behaviours~=widget-create]').live('submit', function(ev){
                ev.preventDefault();
                fancypages.dashboard.pages.submitWidgetForm($(this));
            });

            $('form[data-behaviours~=widget-update]').live('submit', function(ev){
                ev.preventDefault();
                fancypages.dashboard.pages.submitWidgetForm($(this));
            });

            // attach live update listener to all regular input field
            $('div[data-behaviours~=field-live-update]').live('change keyup', function(ev){
                ev.preventDefault();

                var fieldElem = $('input', this);
                var widgetId = $(this).parents('form').data('widget-id');
                var fieldName = $(fieldElem).attr('id').replace('id_', '');

                var previewDoc = fancypages.dashboard.pages.getPreviewDocument();
                var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
                previewField.html($(fieldElem).val());
            });
        },

        loadWidgetForm: function(url, containerName) {
            $.ajax(url).done(function(data){
                var widgetWrapper = $('div[id=widget_input_wrapper]');
                widgetWrapper.html(data);

                fancypages.dashboard.pages.initialiseRichtextEditor(widgetWrapper);
            });

        },

        submitWidgetForm: function(elem) {
            $.ajax({
                type: "POST",
                url: elem.attr('action'),
                data: elem.serialize()
            }).done(function(data) {
                $('div[id=widget_input_wrapper]').html("");
                $('#page-preview').attr('src', $('#page-preview').attr('src'));
            });
        },

        getPreviewDocument: function(elem) {
            return $('#page-preview').contents();
        },

        initialiseRichtextEditor: function(wrapperElement) {
            wrapperElement = wrapperElement || document;
            // initialise wysihtml5 rich-text for editor
            $('.wysihtml5-wrapper', wrapperElement).each(function(elem) {
                var editor = new wysihtml5.Editor($('textarea', this).get(0), {
                    toolbar:      $(".wysihtml5-toolbar", this).get(0),
                    parserRules:  wysihtml5ParserRules
                });

                editor.observe("load", function() {
                    editor.composer.element.addEventListener("keyup", function() {
                        var fieldElem = $(editor.textarea.element);

                        var widgetId = $(fieldElem).parents('form').data('widget-id');
                        var fieldName = $(fieldElem).attr('id').replace('id_', '');

                        var previewDoc = fancypages.dashboard.pages.getPreviewDocument();
                        var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
                        previewField.html($(fieldElem).val());
                    });
                });
                editor.on("change", function() {
                    var fieldElem = $(editor.textarea.element);

                    var widgetId = $(fieldElem).parents('form').data('widget-id');
                    var fieldName = $(fieldElem).attr('id').replace('id_', '');

                    var previewDoc = fancypages.dashboard.pages.getPreviewDocument();
                    var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
                    previewField.html($(fieldElem).val());
                });
                editor.on("aftercommand:composer", function() {
                    var fieldElem = $(editor.textarea.element);

                    var widgetId = $(fieldElem).parents('form').data('widget-id');
                    var fieldName = $(fieldElem).attr('id').replace('id_', '');

                    var previewDoc = fancypages.dashboard.pages.getPreviewDocument();
                    var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
                    previewField.html($(editor.composer.element).html());
                });
            });
        }
    }
};
