$(document).ready(function(){
  $(":text").focus(function() {
    $(this).select();
  });

  $("#search-clear").click(function() {
    $(":text").val("");
  });

  $("#license-filter").change(function() {
    $("#member_filter").submit();
  });

  $("#membership-filter").change(function() {
    $("#member_filter").submit();
  });

  $("#rank-filter").change(function() {
    $("#member_filter").submit();
  });

  $("#city-filter").change(function() {
    $("#dojo-filter").submit();
  });

  $("#country-filter").change(function() {
    $("#dojo-filter").submit();
  });

  $("#language").change(function() {
    $("#setlang").submit();
  });

  $("#clean_up_expired_sessions").click(function() {
    $("#clean_up_session_form").submit();
  });

});

