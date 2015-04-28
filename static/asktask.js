$(document).bind('ready', function () {
  $( ".q_widget" ).draggable({
    helper: "clone",
    cursor: "move",
    revert: "invalid",
    refreshPositions: true
  });

  $(".layout").droppable({
    accept: ".q_widget",
    drop: function(event, ui){
      renderQuestion(ui.draggable.attr('id'), ui.offset.top);
    }
  }).sortable({
    items: "div.quest_element"
  });
});

renderQuestion = function(q_id, offset){
  Sijax.request('add_question', [q_id, window.questionnaire, offset]);
};