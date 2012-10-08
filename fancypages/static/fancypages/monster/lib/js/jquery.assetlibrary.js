(function($) {

    var pickerOpen = false;

    /**
     * returns iframeOverlay
     * @param options like defaults
     */
    var showAssetsLibrary = function(options) {
        var html = $('<div><div id="asset-library-overlay"></div><div id="asset-library"><iframe src="/asset-library/' + options.source + "/" + options.type + '/?embed=true" frameborder="0"></iframe></div></div>');

        var iframeOverlay = html.find('#asset-library-overlay');
        var iframe = html.find('#asset-library');

        iframeOverlay.on('click', function(event) {
            html.fadeOut('250', function(){
                html.remove();
            });
        });

        iframeOverlay.hide();
        iframe.hide();

        $('body').append(html);
        iframeOverlay.fadeIn('250');
        iframe.show();

        return iframeOverlay;
    };

    var AssetPicker = function(elem, trigger, options) {

        this.elem = elem;
        this.trigger = trigger;
        this.options = options;
        var self = this;
        this.iframeOverlay = null;

        this.closePopup  =function() {
            self.iframeOverlay.click();
        };

        this.useAsset = function(asset) {
            if (self.options.type == AssetPicker.TYPE_IMAGE) {
                self.useImage(asset);
            }
            if (self.options.type == AssetPicker.TYPE_SNIPPET) {
                self.useSnippet(asset);
            }
        };

        this.useSnippet = function(snippet) {
            var editor = self.options.editor;
            if (editor) {
                editor.focus();
                editor.composer.commands.exec("insertHTML", snippet.contents());
            } else {
                elem.val(elem.val() + snippet.contents());
                elem.text(elem.text() + snippet.contents());
            }
            elem.removeClass('asset-target');
            elem.change();
            self.closePopup();
        };

        this.useImage = function(image) {
            var success = function(data, textStatus, jqXHR) {
                var partialURL = data.partial_path;
                var finalURL = self.options.assetBaseURL + partialURL;
                self.options.onCopyComplete(self.elem, image, finalURL, partialURL);
                self.closePopup();
            };

            $.post(self.options.copyURL, {
                'image_asset': image.id,
                'destination': self.options.assetPath
            }, success, 'json');
        };

        trigger.on('click', function(event) {
            self.iframeOverlay = showAssetsLibrary(self.options);
            /* Add property to input so that iframe has something to find. Can't use .data() because it's not shared
             between frames */
            self.elem[0].assetCallback = self.useAsset;
            self.elem.addClass('asset-target');
        });
    };

    AssetPicker.TYPE_IMAGE = "image";
    AssetPicker.TYPE_SNIPPET = "snippet";


    AssetPicker.prototype.copy_to_campaign = function(image, callback) {
        var self = this;
        var responseHandler = function(result) {
            if (result.status != 'success') {
                alert("Error");
            } else {
                callback(data.path, data.partial_path);
            }
        };

        $.post(self.options.copyURL, {
            'image_asset': image.id,
            'destination': self.options.assetPath
        }, responseHandler, 'json');
    };

    var defaultCopyComplete = function(elem, asset, newURL, partialURL) {
        elem.val(newURL);
        elem.removeClass('asset-target');
        elem.change();
    };


    var createButtonTrigger = function(elem, label) {
        var trigger = $('<a class="btn btn-info">' + label + '</a>');
        elem.after(trigger);
        var triggerWidth = trigger.outerWidth() + 5;
        var width = elem.width();
        trigger.css({
            marginLeft: '5px'
        });
        elem.width(width - triggerWidth);

        return trigger;
    };

    var createSnippetTriggerWYSI = function(elem) {
        var trigger = $('<li><a class="toolbar-snippets">snippets</a></li>');
        var wysiToolbar = elem.parent('.wysihtml5-wrapper').find('.wysihtml5-toolbar ul');
        wysiToolbar.append(trigger);
        return trigger;
    };

    var createImageTrigger = function(elem) {
        return createButtonTrigger(elem, 'Library');
    };

    var createSnippetTrigger = function(elem) {
        return createButtonTrigger(elem, 'Snippets');
    };

    var createSnippetTriggerNL = function(elem) {
        var trigger = $('<a class="btn btn-mini btn-info">Snippets</a>');
        elem.siblings('.fieldpicker-trigger').after(trigger);
        return trigger;
    };

    var createSnippetTriggerPrintWYSI = function(elem) {
        var trigger = $('<a class="btn btn-small">Snippets</a>');
        elem.parents('.field_html').find('.wysi-toolbar').append(trigger);
        return trigger;

    };

    var defaultCreateTrigger = function(elem) {
        return createImageTrigger(elem);
    };

    var defaults = {
        'type': AssetPicker.TYPE_IMAGE,
        'mode': 'browse',  // select or browse.
        'copyURL': '/asset-library/copy-image-to-campaign/',
        'assetPath': null,
        'assetBaseURL': null,
        'onCopyComplete': defaultCopyComplete,
        'createTrigger': defaultCreateTrigger,
        'source': 'email',
        'editor': null
    };

    $.fn.assetPicker = function(settings) {
        var options = $.extend({}, defaults, settings);

        if (options.type == AssetPicker.TYPE_IMAGE) {
            if (!options.assetPath) {
                throw "You must specify an assetPath to copy selected resources to";
            }
            if (!options.assetBaseURL) {
                throw "You must specify an assetBaseURL";
            }
        }

        this.each(function() {
            var elem = $(this);
            var trigger = options.createTrigger(elem);
            var picker = new AssetPicker(elem, trigger, options);
        });
    };


    window.LibraryTriggers = {
        snippet: createSnippetTrigger,
        snippetNewLine: createSnippetTriggerNL,
        snippetWYSI: createSnippetTriggerWYSI,
        snippetPrintWYSI: createSnippetTriggerPrintWYSI,
        image: createImageTrigger
    };

})(jQuery);