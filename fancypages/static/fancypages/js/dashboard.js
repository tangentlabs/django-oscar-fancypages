var fancypages = fancypages || {};

fancypages.dashboard = {
    preview: {
        init: function () {
            $('.sortable').sortable({
                cursor: 'move',
                handle: '.move',
                placeholder: "ui-state-highlight",
                forcePlaceholderSize: true,
                connectWith: ".connectedSortable",
                update: function (ev, ui) {
                    var dropIndex = ui.item.index();
                    var widgetId = ui.item.data('widget-id');

                    var containerId = ui.item.parents('.sortable').data('container-id');

                    var moveUrl = '/dashboard/fancypages/widget/move/' + widgetId + '/to/';
                    moveUrl += containerId + '/' + dropIndex + '/';

                    $.getJSON(moveUrl, function (data) {
                        if (data.success) {
                            parent.fancypages.dashboard.reloadPreview();
                        } else {
                            parent.oscar.messages.error(data.reason);
                        }
                    }).error(function () {
                        parent.oscar.messages.error(
                            "An error occured trying to move the widget. Please try it again."
                        );
                    });
                }
            });

            //load the form to select a new widget to add to the container
            //and display it in a modal
            $("a[data-behaviours~=load-add-widget]").click(function (ev) {
                var addButton = $(this);
                $.ajax({
                    type: "GET",
                    url: addButton.data('action'),
                    success: function (data) {
                        addButton.after(data);

                        $(data).load(function () {
                            $(this).modal('show');
                        });
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        parent.oscar.messages.error(
                            "Could not get availabe widget for this container. Please try it again."
                        );
                    }
                });
            });

            // Listen on modal cancel buttons and hide and remove the modal
            // when clicked.
            $("button[data-behaviours~=remove-modal]").live('click', function (ev) {
                ev.preventDefault();
                fancypages.dashboard.removeModal(this);
                $(this).parents('div[id$=_modal]').remove();
            });

            // initialise modal for adding widget
            $('form[id$=add_widget_form] input[type=radio]').live('click', function (ev) {
                ev.preventDefault();

                var form = $(this).parents('form');
                var containerName = $(form).attr('id').replace('_add_widget_form', '');
                var addUrl = $(form).attr('action') + $(this).val() + '/';

                $.getJSON(addUrl, function (data) {
                    if (data.success) {
                        parent.fancypages.dashboard.reloadPreview();
                        parent.fancypages.dashboard.loadWidgetForm(data.update_url, containerName);
                    } else {
                        parent.oscar.messages.error(data.reason);
                    }
                }).error(function () {
                    parent.oscar.messages.error(
                        "An error occured trying to add a new widget. Please try it again."
                    );
                });

                $(this).parents('div[id$=_modal]').remove();
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
                previewDoc = fancypages.dashboard.getPreviewDocument();

            var widgetId = $(fieldElem).parents('form').data('widget-id');
            var fieldName = $(fieldElem).attr('id').replace('id_', '');

            var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
            previewField.html($(editor.composer.element).html());
            
            // Add Class to widget editing
            $('.widget', previewDoc).removeClass('editing');
            previewField.parents('.widget').addClass('editing');
        }
    },

    init: function () {
        $('#page-preview').load(function () {
            fancypages.dashboard.addPreviewListeners();
        });

        $('form[data-behaviours~=submit-widget-form]').live('submit', function (ev) {
            ev.preventDefault();
            fancypages.dashboard.removeModal(this);
            fancypages.dashboard.submitWidgetForm($(this));
        });

        // Listen on modal cancel buttons and hide and remove the modal
        // when clicked.
        $("button[data-behaviours~=remove-modal]").live('click', function (ev) {
            ev.preventDefault();
            fancypages.dashboard.removeModal(this);
        });

        // attach live update listener to all regular input field
        $('div[data-behaviours~=field-live-update]').live('change keyup', function (ev) {
            ev.preventDefault();

            var fieldElem = $('input', this);
            var widgetId = $(this).parents('form').data('widget-id');
            var fieldName = $(fieldElem).attr('id').replace('id_', '');

            var previewDoc = fancypages.dashboard.getPreviewDocument();
            var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
            previewField.html($(fieldElem).val())
            
        });

        // Function setting the height of the IFrame and the Sidebar
        function UpdateSize() {
            var pageHeight = $(window).height(),
                navBarTop = $('.navbar-fixed-top').outerHeight(),
                subBarTop = $('.subnav-fixed').outerHeight(),
                buttonsTop = $('.button-nav').outerHeight(),
                sumHeight = pageHeight - navBarTop - subBarTop;
                
            $('#page-preview').css('height', sumHeight);
            $('.sidebar-content').css('height', sumHeight - buttonsTop);
            $('.sidebar-content').jScrollPane();
        }
        UpdateSize();
        // Function setting the height if window resizes
        $(window).resize(UpdateSize);

        // Initialise all the asset related stuff
        $("#asset-modal").live('shown', function () {
            var assetManager = $("#asset-manager");
            assetManager.attr('src', assetManager.data("src"));

            //$(this).css('width', $(window).width() - 100);
            //$(this).css('height', $(window).height() - 100);
        });
    },

    removeModal: function (elem) {
        var modalElem = $(elem).parents('#delete-modal');
        modalElem.remove();
    },

    addPreviewListeners: function () {
        var previewDoc = fancypages.dashboard.getPreviewDocument();

        // initialise all update widgets
        $('form[id$=update_widget_form]').each(function (idx, form) {
            var selection = $("select", form);
            var containerName = $(form).attr('id').replace('_update_widget_form', '');

            var widgetUrl = "/dashboard/fancypages/widget/update/" + selection.val() + "/";
            fancypages.dashboard.loadWidgetForm(widgetUrl, containerName);

            selection.change(function (ev) {
                var widgetUrl = "/dashboard/fancypages/widget/update/" + $(this).val() + "/";
                fancypages.dashboard.loadWidgetForm(widgetUrl, containerName);
            });
        });


        $('.edit-button', previewDoc).click(function (ev) {
            var widget = $(this).parents('.widget');
            var widgetUrl = "/dashboard/fancypages/widget/update/" + $(widget).data('widget-id') + "/";

            // Scrolls IFrame to the top of editing areas
            var destination = widget.offset().top - 20;
            $('html:not(:animated),body:not(:animated)', previewDoc).animate({ scrollTop: destination}, 500, 'swing' );

            fancypages.dashboard.loadWidgetForm(widgetUrl, $(widget).data('container-name'));
        });


        $('div.delete', previewDoc).click(function (ev) {
            var widget = $(this).parents('.widget');

            var deleteUrl = '/dashboard/fancypages/widget/delete/' + $(widget).data('widget-id') + "/";

            $.ajax(deleteUrl)
                .done(function (data) {
                    var widgetWrapper = $('div[id=widget_input_wrapper]');
                    widgetWrapper.after(data);

                    $(data).load(function () {
                        $(this).modal('show');
                    });
                })
                .error(function () {
                    parent.oscar.messages.error(
                        "An error occured trying to delete a widget. Please try it again."
                    );
                });
        });

        // Add / removed page elements for page preview
        $('button[data-behaviours~=preview-check]').on('click', function () {
            $('div[data-behaviours~=loading]').fadeIn(300);
            setTimeout(function () { 
              $('body', previewDoc).toggleClass('preview');
              $('.navbar.accounts', previewDoc).add('.header', previewDoc).fadeToggle('slow');
              $(this).find('i').toggleClass('icon-eye-close');
              $('div[data-behaviours~=loading]').delay(700).fadeOut();
            }, 300);
        });

        // Show Page previews
        $('button[data-behaviours~=page-settings]').on('click', function () {
          $('div[id=widget_input_wrapper]').html("");
          $('#page-settings').show();
          $( '.editor' ).animate({ backgroundColor: "#333" }, 500 );
        });
        
        $('body', previewDoc).css('margin-bottom', '600px');


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
            $( '.editor' ).animate({ backgroundColor: "#444" }, 500 );
        });
    },

    /**
     * Submit the widget form using an AJAX call and create or update the
     * corresponding widget. The form is submitted to the URL specified in
     * the action attribute and is removed from the editor panel right after
     * submission was successful.
     */
    submitWidgetForm: function (form) {
        var submitButton = $('button[type=submit]', form);
        submitButton.attr('disabled', true);
        submitButton.data('original-text', submitButton.text());
        submitButton.text('Processing...');

        if (form.data('locked')) {
            return false;
        }
        form.data('locked', true);
        $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                $('div[id=widget_input_wrapper]').html("");
                parent.fancypages.dashboard.reloadPreview();
                $('#page-settings').show();
                $( '.editor' ).animate({ backgroundColor: "#333" }, 500 );
            },
            error: function () {
                parent.oscar.messages.error(
                    "An error occured trying to delete a widget. Please try it again."
                );
            }
        }).complete(function () {
            submitButton.attr('disabled', false);
            submitButton.text(submitButton.data('original-text'));
            form.data('locked', false);
        });
    },

    setSelectedAsset: function (assetType, assetId, assetUrl) {
        console.log('setting new asset', assetType, assetId, assetUrl);
        $('#asset-modal').modal('hide');

        var assetInput = $("#asset-input");
        $("#id_asset_id", assetInput).attr('value', assetId);
        $("#id_asset_type", assetInput).attr('value', assetType);
        $("img", assetInput).attr('src', assetUrl);
    },

    /**
     * Convenience method to get the current preview document root for handling
     * selectors within the preview page.
     */
    getPreviewDocument: function (elem) {
        return $('#page-preview').contents();
    },

    /**
     * Reload the preview displayed in the iframe of the customise page.
     * A preview reload is necessary (or advised) whenever the content of
     * the page is changed in the database to prevent inconsistencies between
     * the preview and the actual stored content.
     */
    reloadPreview: function () {
        $('div[data-behaviours~=loading]').fadeIn(300);
        setTimeout(function () { 
          $('#page-preview').attr('src', $('#page-preview').attr('src')).load(function(){
            $('div[data-behaviours~=loading]').fadeOut(300);
          }); 
        }, 300);
    }
};


