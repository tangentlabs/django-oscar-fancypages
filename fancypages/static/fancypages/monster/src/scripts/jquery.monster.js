$.extend($.expr[':'],{
    widget: function(elem, index, match, array){

        var $elem = $(elem);

        if ($elem.attr('m:widget')){
            return true;
        }
        return false;
    }
});

$.fn.extend({
    widgets : function() {
        var node = this;
        var temp = node.find(':widget');

        var result = temp.filter(function(i){
            var parents = $(this).parents(':widget');

            if (parents.length > 0) {
                var index = parents.index(node);

                if (index === 0) { return true; }
                return false;
            }
            return true;
        });

        return result;
    },
    outerHTML: function(s) {
        return (s) ? this.before(s).remove() : $('<div>').append(this.eq(0).clone()).html();
    }
});

$.fn.window = function () {
    var b;
    if (this.length) {
        b = this[0];
        if (b.ownerDocument) b = b.ownerDocument;
        return $(b.defaultView || b.parentWindow);
    }
};