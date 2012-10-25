var fancypages = fancypages || {};

fancypages.assets = {
    init: function () {
        $('#fileupload').fileupload({
            dataType: 'json',
            done: function (e, data) {
                $("#asset-gallery").append(data.result[0].image_markup);
            },
            progressall: function (e, data) {
                var progress = parseInt(data.loaded / data.total * 100, 10);
                var uploadProgress = $('#upload-progress');

                if (progress < 100) {
                    uploadProgress.removeClass("hide");
                } else {
                    uploadProgress.addClass("hide");
                }
                $('.bar', uploadProgress).css('width', progress + '%');
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
