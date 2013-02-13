  //Reset carousels dependant on container width
function resetCarousel() {
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
}
// initialise fitVids plugin for resizing IFRAME YouTube videos
function initFitvids() {
  $('.widget-video').fitVids();
}

//Check if Mobile
function checkMobile() {
  var breakpoint = 767,
      mobile = (sw > breakpoint) ? false : true;

  if (!mobile) { //If Not Mobile
    resetCarousel();
  } else { //Hide 
    
  }
}

$(document).ready(function() {
    initFitvids();
    sw = document.documentElement.clientWidth;
    sh = document.documentElement.clientHeight;
    checkMobile();    
});