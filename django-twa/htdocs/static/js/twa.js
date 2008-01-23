function Absenden() {
  document.getElementById("setlang").submit();
}

$(document).ready(function(){

  $(":text").focus(function() {
    $(this).select();
  });

  $("#search-clear").click(function() {
    $(":text").val("");
  });

});
