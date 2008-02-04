$(document).ready(function(){
  $(":text").focus(function() {
    $(this).select();
  });

  $("#id_username").focus();

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

  $("#active_sessions").hide();
  $("#toggle_active_sessions").click(function() {
    $("#active_sessions").toggle();
  });

});

