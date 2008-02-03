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

  $("#setlang").change(function() {
    $(this).submit();
  });
});
