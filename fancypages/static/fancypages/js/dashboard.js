var fancypages = fancypages || {};

fancypages.dashboard = {
    preview: {
        init: function () {
            var tooltip = '<div class="tool-tip top">Insert here</div>';
            $('.sortable').sortable({
                cursor: 'move',
                handle: '.move',
                connectWith: ".connectedSortable",
                cursorAt: { top:0, left: 0 },
                activate: function( event, ui ) {
                  $('body').addClass('widget-move');
                  $('.ui-sortable-placeholder').prepend(tooltip);
                },
                deactivate: function( event, ui ) {
                  $('body').removeClass('widget-move');
                },
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
            }).disableSelection();

            //load the form to select a new widget to add to the container
            //and display it in a modal
            $("a[data-behaviours~=load-modal]").click(function (ev) {
                return fancypages.dashboard.loadModal(this);
            });

            // Listen on modal cancel buttons and hide and remove the modal
            // when clicked.
            $("button[data-behaviours~=remove-modal]").live('click', function (ev) {
                ev.preventDefault();
                fancypages.dashboard.removeModal(this);
                $(this).parents('div[id$=_modal]').remove();
            });

            $("a[data-behaviours~=update-editor-field]").click(function (ev) {
                ev.preventDefault();
                var target = $(this).data('target');
                var src = $(this).data('src');
                $(target).val(src);
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

            // Add a new tab to the selected tabbed block widget
            $('[data-behaviours~=add-tab]').live('click', function (ev) {
                ev.preventDefault();

                $.getJSON($(this).data('action'), function (data) {
                    if (data.success) {
                        parent.fancypages.dashboard.reloadPreview();
                    } else {
                        parent.oscar.messages.error(data.reason);
                    }
                }).error(function () {
                    parent.oscar.messages.error(
                        "An error occured trying to add a new tab. Please try it again."
                    );
                });
            });
        },

        getPreviewField: function (elem) {
            previewDoc = fancypages.dashboard.getPreviewDocument();
            var widgetId = elem.parents('form').data('widget-id');
            return $('#widget-' + widgetId, previewDoc);
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

            //load the content of a modal via ajax
            //and display it in a modal
            $("a[data-behaviours~=load-modal]").click(function (ev) {
                return fancypages.dashboard.loadModal(this);
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
            if (!fieldElem) { 
                return false;
            }
            var widgetId = $(this).parents('form').data('widget-id');
            var fieldName = $(fieldElem).attr('id').replace('id_', '');

            var previewDoc = fancypages.dashboard.getPreviewDocument();
            var previewField = $('#widget-' + widgetId + '-' + fieldName, previewDoc);
            previewField.html($(fieldElem).val());
        });

        fancypages.dashboard.UpdateSize();

        // Function setting the height if window resizes
        $(window).resize(fancypages.dashboard.UpdateSize);

        // Initialise all the asset related stuff
        $("#asset-modal").live('shown', function () {
            var assetManager = $("#asset-manager");
            assetManager.attr('src', assetManager.data("src")).load(function () {
                var modalHeight = $(window).height() - 100;
                $('.slide-pane', fancypages.dashboard.getAssetDocument()).css('height', modalHeight - 100);
                $('.slide-pane', fancypages.dashboard.getAssetDocument()).jScrollPane({
                    horizontalDragMaxWidth: 0
                });
            });

            $(this).css({
                width: $(window).width() - 100,
                height: $(window).height() - 100,
                top: 100,
                left: 100,
                marginLeft: '-50px',
                marginTop: '-50px'
            });
        });
    },

    loadModal: function (elem) {
        var target = $(elem).data('target');
        var url = $(elem).attr('href');

        return $(target).load(url, function (response, status, xhr) {
            if (status == "error") {
                parent.oscar.messages.error(
                    "Unable to load contents of url: " + url
                );
            }
            fancypages.dashboard.preview.init();
        });
    },

    removeModal: function (elem) {
        var modalElem = $(elem).parents('#delete-modal');
        modalElem.remove();
    },

    scrollToWidget: function (widget) {
        // Scrolls IFrame to the top of editing areas
        if (widget.offset()) {
            var destination = widget.offset().top - 20;
            var previewDoc = fancypages.dashboard.getPreviewDocument();

            $('html:not(:animated),body:not(:animated)', previewDoc).animate({ scrollTop: destination}, 500, 'swing');
        }
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
            var widget = $(this).closest('.widget');
            var widgetUrl = "/dashboard/fancypages/widget/update/" + $(widget).data('widget-id') + "/";

            fancypages.dashboard.scrollToWidget(widget);

            // Add Class to widget editing
            $('.widget', previewDoc).removeClass('editing');
            widget.addClass('editing');

            fancypages.dashboard.loadWidgetForm(widgetUrl, $(widget).data('container-name'), {
                success: function () {
                    // attach slider to column width slider
                    var sliderSelection = $('#id_left_width');
                    sliderSelection.after('<div id="left-width-slider"></div>');
                    sliderSelection.css('display', 'none');
                    var slider = $('#left-width-slider');

                    var maxValue = sliderSelection.data('max');
                    var minValue = sliderSelection.data('min');

                    slider.slider({
                        range: "min",
                        value: sliderSelection.val(),
                        min: minValue,
                        max: (maxValue - 1),
                        slide: function (ev, ui) {
                            var previewField = fancypages.dashboard.preview.getPreviewField($(this));

                            var leftColumn = $('.column-left', previewField);
                            leftColumn[0].className = leftColumn[0].className.replace(/span\d+/g, '');
                            leftColumn.addClass('span' + ui.value);

                            var rightColumn = $('.column-right', previewField);
                            rightColumn[0].className = rightColumn[0].className.replace(/span\d+/g, '');
                            rightColumn.addClass('span' + (maxValue - ui.value));

                            sliderSelection.attr('value', ui.value);
                        }
                    });
                }
            });
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
            $('.editor').animate({backgroundColor: "#444"}, 500);
            fancypages.dashboard.UpdateSize();
        });

        $('body', previewDoc).css('margin-bottom', '600px').addClass('edit-page');

        fancypages.dashboard.carouselPosition();
        
        fancypages.dashboard.mouseWidgetHover();
        
    },

    /**
     * Load the the widget form for the specified url
     */
    loadWidgetForm: function (url, containerName, options) {
        $.ajax(url).done(function (data) {
            var widgetWrapper = $('div[id=widget_input_wrapper]');
            widgetWrapper.html(data);
            $('#page-settings').hide();

            fancypages.dashboard.editor.init();
            $('.editor').animate({backgroundColor: "#555"}, 500)
                        .delay(500)
                        .animate({backgroundColor: "#444"}, 500);

            fancypages.dashboard.UpdateSize();

            if (options && 'success' in options) {
                options.success();
            }
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
                $('.editor').animate({backgroundColor: "#444"}, 500);
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
            fancypages.dashboard.UpdateSize();
        });
    },

    setSelectedAsset: function (assetType, assetId, assetUrl) {
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

    getAssetDocument: function (elem) {
        return $('#asset-manager').contents();
    },

    editingWidget: function () {
        var widgetId = $('div[id=widget_input_wrapper]').find('form').data('widget-id'),
            previewDoc = fancypages.dashboard.getPreviewDocument(),
            editingWidget = $('body', previewDoc).find('#widget-' + widgetId);

        // Add Class to widget editing by removing others first
        $('.widget', previewDoc).removeClass('editing');
        editingWidget.addClass('editing');

        fancypages.dashboard.scrollToWidget(editingWidget);
    },
    
    mouseWidgetHover: function () {
        var previewDoc = fancypages.dashboard.getPreviewDocument(),
            widgetHover = $('.widget', previewDoc);
        widgetHover.on('mouseenter', function(e){
          $(e.target).parents('.widget').removeClass('widget-hover');
          $(this).addClass('widget-hover');
        });
        widgetHover.on('mouseleave', function(){
          $(this).removeClass('widget-hover');
        });
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
            $('#page-preview').attr('src', $('#page-preview').attr('src')).load(function () {
                $('div[data-behaviours~=loading]').fadeOut(300);
                fancypages.dashboard.editingWidget();
            });
        }, 300);
    },

    // Function setting the height of the IFrame and the Sidebar
    UpdateSize: function () {
        var pageHeight = $(window).height(),
            navBarTop = $('.navbar-accounts').outerHeight(),
            subBarTop = $('.navbar-primary').outerHeight(),
            buttonsTop = $('.button-nav').outerHeight(),
            buttonsBottom = $('.form-actions.fixed').outerHeight(),
            sumHeight = pageHeight - navBarTop - subBarTop;

        $('#page-preview').css('height', sumHeight);
        $('.sidebar-content').css('height', sumHeight - buttonsTop - buttonsBottom);
        $('.sidebar-content').jScrollPane();
    },
    /*
    * Checks for carousels, initiates viewable items based on where the
    * carousel is
    */
    carouselPosition: function () {
        var previewDoc = fancypages.dashboard.getPreviewDocument(),
            es_carousel = $('.es-carousel-wrapper', previewDoc);

        $('.sidebar .es-carousel-wrapper', previewDoc).each(function () {
            var es_carouselHeight = $(this).find('.products li:first').height();
            $(this).find('.products').css('height', es_carouselHeight);
            $(this).elastislide({
                minItems: 1,
                onClick: true
            });
        });

        $('.tab-pane .es-carousel-wrapper', previewDoc).each(function () {
            var es_carouselHeight = $(this).find('.products li:first').height();
            $(this).find('.products').css('height', es_carouselHeight);
            $(this).elastislide({
                minItems: 4,
                onClick: true
            });
        });
    }
};
