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
        },

        loadWidgetForm: function(url, containerName) {
            $.ajax(url).done(function(data){
                var widgetWrapper = $('div[id='+containerName+'_widget_input_wrapper]');
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
        }
    }
};
