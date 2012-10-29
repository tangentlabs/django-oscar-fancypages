$(document).ready(function() {
  
  $('.sidebar .es-carousel-wrapper').each(function(){
    var es_carouselHeight = $(this).find('.products li:first').height();
    $(this).find('.products').css({
      height: es_carouselHeight,
      overflow: 'hidden'
    });
    $(this).elastislide({
        minItems: 1,
        onClick:  true
    });
  });
  
});


