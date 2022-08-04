$(document).ready(function(){
  // No links pls
  $('.ui-button.inactive').click(function(){
    e.preventDefault();
  });
  
  $('#close').click(function(){
    $('.ui-panel').removeClass('bounceInDown').addClass('bounceOutUp');
  });
});