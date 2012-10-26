var fancypages = fancypages || {};

fancypages.assets = {
    init: function () {
        var uploadProgress = $('#upload-progress');
        $('#fileupload').fileupload({
            dataType: 'json',
            done: function (e, data) {
                $("#asset-gallery").append(data.result[0].image_markup);
                uploadProgress.addClass("hide");
            },
            progressall: function (e, data) {
                var progress = parseInt(data.loaded / data.total * 100, 10);
    
                uploadProgress.removeClass("hide");
               
                $('.bar', uploadProgress).css('width', progress + '%');
            },
            start: function(){
                $('.bar', uploadProgress).css('width', 0 + '%');
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
