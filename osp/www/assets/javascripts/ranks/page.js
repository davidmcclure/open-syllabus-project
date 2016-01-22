

import $ from 'jquery';


$('.action.ranks').click(function() {
  $('body').animate({
    scrollTop: $('#ranks').offset().top
  });
});
