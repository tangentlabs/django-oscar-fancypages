var fancypages = {
    apiBaseUrl: "/api/v1/",
    /**
     * Get the CSRF token from the session to submit POST data.
     */
    getCsrfToken: function () {
        var cookies = document.cookie.split(';');
        var csrf_token = null;
        $.each(cookies, function (index, cookie) {
            cookieParts = $.trim(cookie).split('=');
            if (cookieParts[0] == 'csrftoken') {
                csrfToken = cookieParts[1];
            }
        });
        return csrfToken;
    },
    /**
     * Remove the modal for an element.
     */
    removeModal: function (elem) {
        var modalElem = $(elem).parents('#delete-modal');
        modalElem.remove();
    }
};

fancypages.utils = {
    /**
     * Borrowed from http://stackoverflow.com/a/321527
     */
    partial: function (func /*, 0..n args */) {
        var args = Array.prototype.slice.call(arguments, 1);
        return function () {
            var allArguments = args.concat(Array.prototype.slice.call(arguments));
            return func.apply(this, allArguments);
        };
    }
};

fancypages.panels = {
    showEditPanel: function (ev) {
        if (ev) {
            ev.preventDefault();
        }
        $('#editor-handle').hide();
        $('#editor-panel').removeClass('editor-hidden');
    },
    hideEditPanel: function (ev) {
        if (ev) {
            ev.preventDefault();
        }
        $('#editor-handle').show();
        $('#editor-panel').addClass('editor-hidden');
    }
};

fancypages.editor = {
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
                    fancypages.editor.updatePreview(editor);
                });
            });
            // Update the preview whenever the editor window fires the 'change' event
            // meaning whenever the focus is set to another element. "change" applies
            // to both the textarea or the composer.
            editor.on("change", function () {
                fancypages.editor.updatePreview(editor);
            });
            // Listen to this event to be able to update the preview when a command
            // such as "bold" or "italic" is applied to the content. This event is
            // used by wysihtml5 internally to update the textarea with the composer
            // content which means the textarea might not be up-to-date when this
            // event is received. Make sure you use the composer content in this
            // case.
            editor.on("aftercommand:composer", function () {
                fancypages.editor.updatePreview(editor);
            });
        });

        //load the content of a modal via ajax
        //and display it in a modal
        $("a[data-behaviours~=load-modal]").click(fancypages.eventHandlers.loadModal);
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
        var fieldElem = $(editor.textarea.element);

        var widgetId = $(fieldElem).parents('form').data('widget-id');
        var fieldName = $(fieldElem).attr('id').replace('id_', '');

        var previewField = $('#widget-' + widgetId + '-' + fieldName);
        $(previewField).html($(editor.composer.element).html());
    }
};

fancypages.dashboard = {
    pages: {
        init: function () {
            var pageSortable = $('#pages-sortable');
            pageSortable.nestedSortable({
                forcePlaceholderSize: true,
                opacity: 0.6,
                isTree: true,
                items: 'li.sortable',
                handle: 'div',
                //toleranceElement: '> div',
                placeholder: 'nested-sortable-placeholder',
                start: function (event, ui) {
                    $(this).data('old-position', ui.item.index());
                },
                update: function (event, ui) {
                    var parentPage = $(ui.item).parents('li');
                    var oldIndex = $(this).data('old-position');
                    var newIndex = ui.item.index();

                    var parentId = 0;
                    if (parentPage.length) {
                        parentId = parentPage.data('page-id');
                    }
                    var moveUrl = fancypages.apiBaseUrl + "page/" + $(ui.item).data('page-id') + '/move';
                    $.ajax({
                        url: moveUrl,
                        type: 'PUT',
                        data: {
                            parent: parentId,
                            new_index: newIndex,
                            old_index: oldIndex
                        },
                        beforeSend: function (xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
                        },
                        success: function (data) {
                            window.location.reload();
                        },
                        error: function () {
                            oscar.messages.error(
                                "An error occured moving the page, please try again."
                            );
                        }
                    });
                    $(this).removeAttr('data-old-position');
                }
            });
            $('.tree li:last-child').addClass('last');

        }
    },

    /**
     * Register event listeners for showing and hiding the
     * editor panel.
     */
    initEditorPanel: function () {
        $('#editor-handle').click(function (ev) {
            ev.preventDefault();
            $(this).hide();
            $('#editor-panel').removeClass('editor-hidden');
        });
        $('#editor-close').click(function (ev) {
            ev.preventDefault();
            $('#editor-handle').show();
            $('#editor-panel').addClass('editor-hidden');
        });
    },

    initialiseEventsOnPageContent: function () {
        // Add a new tab to the selected tabbed block widget
        $('[data-behaviours~=add-tab]').click(fancypages.eventHandlers.addNewTag);
        //load the form to select a new widget to add to the container
        //and display it in a modal
        $("a[data-behaviours~=load-modal]").click(fancypages.eventHandlers.loadModal);

        $('.edit-button').click(fancypages.eventHandlers.editWidget);
        $('div.delete').click(fancypages.eventHandlers.deleteWidget);
    },

    initialiseEventsOnLoadedContent: function () {
        // Listen on modal cancel buttons and hide and remove the modal
        // when clicked.
        $("button[data-behaviours~=remove-modal]").live('click', function (ev) {
            ev.preventDefault();
            fancypages.removeModal(this);
            $(this).parents('div[id$=_modal]').remove();
        });
        // Attach handler to dynamically loaded widget form for 'submit' event.
        $('form[data-behaviours~=submit-widget-form]').live('submit', function (ev) {
            console.log('remove the modal');
            ev.preventDefault();
            fancypages.removeModal(this);
            fancypages.dashboard.submitWidgetForm($(this));
        });
        // Listen on modal cancel buttons and hide and remove the modal
        // when clicked.
        $("button[data-behaviours~=remove-modal]").live('click', function (ev) {
            ev.preventDefault();
            fancypages.removeModal(this);
        });
        // Listen on widget form for content changes in text fields and text
        // areas
        $("a[data-behaviours~=update-editor-field]").live('click', function (ev) {
            ev.preventDefault();
            var target = $(this).data('target');
            var src = $(this).data('src');
            $(target).val(src);
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

            var previewField = $('#widget-' + widgetId + '-' + fieldName);
            previewField.html($(fieldElem).val());
        });
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

    init: function () {
        fancypages.dashboard.initEditorPanel();
        fancypages.dashboard.initialiseSortable();
        fancypages.dashboard.initialiseAddWidgetModal();

        fancypages.dashboard.initialiseEventsOnPageContent();
        fancypages.dashboard.initialiseEventsOnLoadedContent();

        // initialise all update widgets
        $('form[id$=update_widget_form]').each(function (idx, form) {
            var selection = $("select", form);
            var containerName = $(form).attr('id').replace('_update_widget_form', '');
            fancypages.dashboard.loadWidgetForm(selection.val(), containerName);

            selection.change(function (ev) {
                fancypages.dashboard.loadWidgetForm($(this).val(), containerName);
            });
        });

        // Add / removed page elements for page preview
        $('button[data-behaviours~=preview-check]').on('click', function () {
            $('div[data-behaviours~=loading]').fadeIn(300);
            setTimeout(function () {
                $('body').toggleClass('preview');
                $('.navbar.accounts').add('.header').fadeToggle('slow');
                $(this).find('i').toggleClass('icon-eye-close');
                $('div[data-behaviours~=loading]').delay(700).fadeOut();
            }, 300);
        });

        // Show Page previews
        $('button[data-behaviours~=page-settings]').click(function () {
            $('div[id=widget_input_wrapper]').html("");
            $('#page-settings').show();
            $('.editor').animate({backgroundColor: "#444"}, 500);
            fancypages.dashboard.updateSize();
        });

        $('body').css('margin-bottom', '600px').addClass('edit-page');

        fancypages.dashboard.carouselPosition();
        fancypages.dashboard.mouseWidgetHover();

        // Function setting the height if window resizes
        $(window).resize(fancypages.dashboard.updateSize);
        fancypages.dashboard.updateSize();
    },

    initialiseSortable: function () {
        var tooltip = '<div class="tool-tip top">Insert here</div>';
        $('.sortable').sortable({
            cursor: 'move',
            handle: '.move',
            connectWith: ".connectedSortable",
            cursorAt: {
                top: 0,
                left: 0
            },
            activate: function (event, ui) {
                $('body').addClass('widget-move');
                $('.ui-sortable-placeholder').prepend(tooltip);
            },
            deactivate: function (event, ui) {
                $('body').removeClass('widget-move');
            },
            update: function (ev, ui) {
                var dropIndex = ui.item.index();
                var widgetId = ui.item.data('widget-id');
                var containerId = ui.item.parents('.sortable').data('container-id');
                var moveUrl = fancypages.apiBaseUrl + 'widget/' + widgetId + '/move';

                $.ajax({
                    url: moveUrl,
                    type: 'PUT',
                    data: {
                        container: containerId,
                        index: dropIndex
                    },
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
                    },
                    success: function (data) {
                        fancypages.dashboard.reloadPage();
                    },
                    error: function () {
                        oscar.messages.error(
                            "An error occured trying to move the widget. Please try it again."
                        );
                    }
                });
            }
        }).disableSelection();
    },

    initialiseAddWidgetModal: function () {
        // initialise modal for adding widget
        $('form[id$=add_widget_form] input[type=radio]').live('click', function (ev) {
            ev.preventDefault();

            var form = $(this).parents('form');
            var containerName = $(form).attr('id').replace('_add_widget_form', '');

            $.ajax({
                url: $(form).attr('action'),
                type: 'POST',
                dataType: 'json',
                data: {
                    container: $(form).data('container-id'),
                    code: $(this).val()

                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
                },
                success: function (data) {
                    fancypages.dashboard.reloadPage();
                },
                error: function () {
                    oscar.messages.error(
                        "An error occured trying to add a new widget. Please try it again."
                    );
                }
            });
            $(this).parents('div[id$=_modal]').remove();
        });
    },

    scrollToWidget: function (widget) {
        // Scrolls IFrame to the top of editing areas
        if (widget.offset()) {
            var destination = widget.offset().top - 20;
            $('html:not(:animated),body:not(:animated)').animate({scrollTop: destination}, 500, 'swing');
        }
    },

    /**
     * Load the the widget form for the specified url
     */
    loadWidgetForm: function (widgetId, containerName, options) {
        var widgetUrl = fancypages.apiBaseUrl + 'widget/' + widgetId;
        var func =
        $.getJSON(
            widgetUrl,
            {includeForm: true},
            fancypages.utils.partial(fancypages.eventHandlers.displayWidgetForm, options)
        );
    },

    setSelectedAsset: function (assetType, assetId, assetUrl) {
        $('#asset-modal').modal('hide');
        var assetInput = $("#asset-input");
        $("#id_asset_id", assetInput).attr('value', assetId);
        $("#id_asset_type", assetInput).attr('value', assetType);
        $("img", assetInput).attr('src', assetUrl);
    },
    getAssetDocument: function (elem) {
        return $('#asset-manager').contents();
    },

    //editingWidget: function () {
    //    var widgetId = $('div[id=widget_input_wrapper]').find('form').data('widget-id'),
    //        editingWidget = $('body').find('#widget-' + widgetId);

    //    // Add Class to widget editing by removing others first
    //    $('.widget').removeClass('editing');
    //    editingWidget.addClass('editing');

    //    fancypages.dashboard.scrollToWidget(editingWidget);
    //},

    mouseWidgetHover: function () {
        var widgetHover = $('.widget');
        widgetHover.on('mouseenter', function (e) {
            $(e.target).parents('.widget').removeClass('widget-hover');
            $(this).addClass('widget-hover');
        });
        widgetHover.on('mouseleave', function () {
            $(this).removeClass('widget-hover');
        });
    },

    /**
     * Reload the current page and display a loader
     */
    reloadPage: function () {
        $('div[data-behaviours~=loading]').fadeIn(300);
        setTimeout(function () {
            window.location.reload();
        }, 300);
    },

    // Function setting the height of the IFrame and the Sidebar
    updateSize: function () {
        var pageHeight = $(window).height(),
            navBarTop = $('.navbar-accounts').outerHeight(),
            subBarTop = $('.navbar-primary').outerHeight(),
            buttonsTop = $('.button-nav').outerHeight(),
            buttonsBottom = $('.form-actions.fixed').outerHeight(),
            sumHeight = pageHeight - navBarTop - subBarTop;

        $('.sidebar-content').css('height', sumHeight - buttonsTop - buttonsBottom);
        $('.sidebar-content').jScrollPane();
    },
    /*
    * Checks for carousels, initiates viewable items based on where the
    * carousel is
    */
    carouselPosition: function () {
        $('.es-carousel-wrapper').each(function () {
            var es_carouselHeight = $(this).find('.products li:first').height(),
                es_carouselWidth = $(this).closest('.widget-wrapper').width();

            $(this).find('.products').css('height', es_carouselHeight);

            if (es_carouselWidth > 300) {
              $(this).elastislide({
                  minItems: 4,
                  onClick: true
              });
            } else {
              $(this).elastislide({
                  minItems: 1,
                  onClick: true
              });
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
            url: form.attr('action'),
            type: "POST",
            data: form.serialize(),
            success: function (data) {
                $('div[id=widget_input_wrapper]').html("");
                fancypages.dashboard.reloadPage();
                $('#page-settings').show();
                $('.editor').animate({backgroundColor: "#444"}, 500);
            },
            error: function () {
                oscar.messages.error(
                    "An error occured trying to delete a widget. Please try it again."
                );
            }
        }).complete(function () {
            submitButton.attr('disabled', false);
            submitButton.text(submitButton.data('original-text'));
            form.data('locked', false);
            fancypages.dashboard.updateSize();
        });
    }

};
