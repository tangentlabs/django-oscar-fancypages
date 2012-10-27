var fancypages = fancypages || {};

fancypages.assets = {
    init: function () {
        var uploadProgress = $('#upload-progress');
        $('#fileupload').fileupload({
            dataType: 'json',
            done: function (e, data) {
                if (data.result.success) {
                    console.log('markup', data.result.images);
                    $("#asset-gallery").append(data.result.images[0].thumbnailMarkup);
                    uploadProgress.addClass("hide");
                } else {
                    parent.oscar.messages.error(data.reason);
                }
            },
            progressall: function (e, data) {
                var progress = parseInt(data.loaded / data.total * 100, 10);

                uploadProgress.removeClass("hide");

                $('.bar', uploadProgress).css('width', progress + '%');
            },
            start: function () {
                $('.bar', uploadProgress).css('width', '0%');
            }
        });

        $("[data-behaviours~=selectable-asset]").live('click', function (ev) {
            ev.preventDefault();
            console.log('clicked an asset', $(this));

            parent.fancypages.dashboard.setSelectedAsset(
                $(this).data('asset-type'),
                $(this).data('asset-id'),
                //FIXME: this should probably be the actual image url
                $('img', this).attr('src')
            );
        });
    }
};
