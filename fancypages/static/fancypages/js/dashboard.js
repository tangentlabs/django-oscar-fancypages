var fancypages = fancypages || {};
fancypages.dashboard = {
    pages: {
        init: function (){
            $('a[data-toggle="tab"]').on('shown', function (e) {
                //e.target // activated tab
                //e.relatedTarget // previous tab
            });

            // initialise drop-down to create a new widget
            $('form[id$=add_widget_form]').submit(function(ev) {
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


            $('form[data-behaviours~=widget-create]').live('submit', function(ev){
                ev.preventDefault();
                fancypages.dashboard.pages.submitWidgetForm($(this));
            });

            $('form[data-behaviours~=widget-update]').live('submit', function(ev){
                ev.preventDefault();
                fancypages.dashboard.pages.submitWidgetForm($(this));
            });

            fancypages.dashboard.pages.addStyleSheet();

            previewDoc = fancypages.dashboard.pages.getPreviewDocument();
            $('.edit-button', previewDoc).click(function(ev) {
                var widget = $(this).parents('.widget');
                console.log('clicked a button', widget);

                var widgetUrl = "/dashboard/fancypages/widget/update/"+$(widget).data('widget-id')+"/";

                fancypages.dashboard.pages.loadWidgetForm(widgetUrl, $(widget).data('container-name'));
            });
        },

        loadWidgetForm: function(url, containerName) {
            console.log('trying to get data');
            $.ajax(url).done(function(data){
                var widgetWrapper = $('div[id=widget_input_wrapper]');
                console.log('data received', widgetWrapper);
                widgetWrapper.html(data);
            });
        },

        submitWidgetForm: function(elem) {
            $.ajax({
                type: "POST",
                url: elem.attr('action'),
                data: elem.serialize()
            }).done(function(data) {
                $('iframe').attr('src', $('iframe').attr('src'));
            });
        },

        getPreviewDocument: function(elem) {
            return $('iframe').contents();
        },

        addStyleSheet: function() {
            var contents = fancypages.dashboard.pages.getPreviewDocument();

            var head = contents.find("head");
            var body = contents.find("body");
            head.append($("<link/>", {
                rel: "stylesheet",
                href: "/static/fancypages/monster/src/css/monster.css",
                type: "text/css"
            }));
        }
    }
};
