$(document).ready(function() {
      //Reset carousels dependant on container width
      $('.es-carousel-wrapper').each(function () {
          var es_carouselWidth = $(this).closest('.widget-wrapper').width();
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
});


