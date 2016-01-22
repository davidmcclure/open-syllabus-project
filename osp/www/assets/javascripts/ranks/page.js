

import $ from 'jquery';


$('.action.ranks').click(function() {

  $('body, html').animate({
    scrollTop: $('#ranks').offset().top
  });

});
