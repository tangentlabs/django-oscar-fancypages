/*!
 * Copyright Andrée Hansson, 2009
 * Licensed under the MIT license
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Contact: E-mail:  peolanha _AT gmail _DOT com
 *          Twitter: peolanha
 *          Website: http://andreehansson.se/
 */
(function ($) {
	$.fn.getCSS = function (compare) {
		var _getStyle = function (el) {
			var

				// Cache
				defView = document.defaultView,

				// Get stylesheet CSS object
				styleObj = !defView ?
					el.currentStyle:
					defView.getComputedStyle(el, null),

				// Return object, will contain property : value for the CSS later
				returnObj = {};

			// Webkit implements getComputedStyle in a different way, convert it to
			// a identical object returned by other browsers, we also filter out all functions
			for ( var i in styleObj ) {
				if ( typeof styleObj[i] !== "function" ) {

					// We check if the key is a integer (which means webkit)
					(+i) ?
						returnObj[ styleObj[i] ] = styleObj.getPropertyValue( styleObj[i] ):
						returnObj[i] = styleObj[i];
				}
			}

			return returnObj;
		};

		var

			// Set a reference to the DOM element
			me = this.get(0),

			// Create a control element that'll be matched against the actual element
			$controlEl = compare ?
				$(compare):
				$("<" + me.tagName + "/>").html('&nbsp;').appendTo( this.parent() ),

			// Grab styles for control and our element
			styleControl = _getStyle( $controlEl.get(0) ),
			styleObj = _getStyle(me),

			// This is a empty object, will contain any CSS that mismatches the control
			// versus our element
			returnObj = {};

		// Loop through all CSS properties, and add the mismatching ones to our returnObj
		for ( var i in styleObj ) {
			if ( styleControl[i] != styleObj[i] && i !== "cssText" ) {
				var iCamel = i.replace(/\-(\w)/g, function ( string, letter ) {
					return letter.toUpperCase();
				});

				returnObj[iCamel] = styleObj[i];
			}
		}

		// Garbage
		if (!compare) {
			$controlEl.remove();
		}

		return returnObj;
	};
})(jQuery);