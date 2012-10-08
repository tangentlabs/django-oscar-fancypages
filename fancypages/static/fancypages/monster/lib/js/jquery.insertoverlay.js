(function($) {

	var pickerOpen = false;

	var Picker = function(pivot, callback) {
		this.pivot = pivot;
		this.callback = callback;
		this.html = null;

		var self = this;

		pivot.on('click', function(event) {

			if (!pickerOpen) {
				event.stopPropagation();
			}
			event.preventDefault();

			self.show();
		});		
	};

	Picker.prototype.getFields = function() {
		return contact_fields;
	};

	Picker.prototype.build = function() {
		this.html = $('<ul class="dropdown-menu field-picker">');
		var self = this;

		$.each(this.getFields(), function(index, value) {
			var item = $('<li><a></a></li>');
			item.find('a').text(value);
			self.html.append(item);

			item.on('click', function(event) {
				event.preventDefault();
				self.select(value);
			});
		});

		this.html.hide();
		$('body').append(this.html);
	};

	Picker.prototype.reposition = function() {

	};

	Picker.prototype.show = function() {
		if (!pickerOpen) {
			pickerOpen = true
			var self = this;
			if (!this.html) {
				this.build();
			}

			self.html.position({
				of: self.pivot,
				my: 'right top',
				at: 'right bottom'
			});					

			this.html.show();

			self.html.position({
				of: self.pivot,
				my: 'right top',
				at: 'right bottom'
			});					

			$('.scrollparent').on('scroll.fieldoverlay', function(event) {
				self.html.position({
					of: self.pivot,
					my: 'right top',
					at: 'right bottom'
				});
			});

			this.pivot.on('click.fieldoverlay', function(event) {
				event.preventDefault();
			});

			this.pivot.on('mouseover.fieldoverlay', function(event) {
				event.preventDefault();
			});			

			$('body').on('click.fieldoverlay', function(event){
				if (self.html.has(event.target).length === 0){
					self.hide();
				}
			});
	
		}
	};

	Picker.prototype.hide = function() {
		if (this.html) {
			pickerOpen = false;
			$('body').off('.fieldoverlay');
			$(this.pivot).off('.fieldoverlay');
			this.html.remove();
			this.html = null;
			$('.scrollparent').off('scroll.fieldoverlay');
		}
	};

	Picker.prototype.select = function(value) {
		this.hide();
		this.callback(value);
	};

	var defaults = {};

	$.fn.insertOverlay = function(settings) {
		var options = $.extend({}, defaults, settings);

		this.each(function() {
			var elem = $(this);
			var tagName = elem.prop('tagName').toLowerCase();

			if (tagName === 'input' || tagName === 'textarea') {
				var trigger = $('<div class="fieldpicker-trigger">&nbsp;</div>');
				elem.wrap('<div class="input-wrapper" />');
				elem.after(trigger);

				var rPad = parseInt(elem.css('paddingRight'), 10);
				var width = elem.width();

				var triggerWidth = trigger.outerWidth() + 5;

				if (!rPad) {
					rPad = '0';
				}

				rPad += triggerWidth;

				elem.css('paddingRight', rPad + 'px');
				elem.width(width - triggerWidth);

				trigger.position({
					of: elem,
					my: 'right top',
					at: 'right top',
					offset: '-4 4'
				});

				var picker = new Picker(trigger, function(value) {
						elem.val(elem.val() + '[' + value + ']');
						elem.change();
				});
			}
		});
	};

	var wysihtml5Defaults = {};

	$.fn.wysihtml5FieldPicker = function(editor) {
		this.each(function() {
			var elem = $(this);
			var picker = new Picker(elem, function(value) {
          editor.composer.commands.exec("insertHTML", "[" + value + "]");
			});
		});
	};

})(jQuery);