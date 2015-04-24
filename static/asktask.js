$(document).bind('ready', function () {
  $( ".q_widget" ).draggable({
    helper: "clone",
    cursor: "move",
    revert: "invalid"
  });

  $("#layout").droppable({
    accept: ".q_widget",
    drop: function(event, ui){
      console.log(event);
      console.log(ui);
    } 
  });
});