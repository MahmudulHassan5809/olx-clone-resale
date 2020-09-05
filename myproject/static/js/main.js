jQuery(document).ready(function($) {

    $("a.delete_ad").confirm({
        content: "Ad will be deleted"
    });
    $("a.delete_ad").confirm({
        buttons: {
            hey: function() {
                location.href = this.$target.attr("href");
            }
        }
    });


    $(".collapse.in").each(function() {
        $(this)
        .siblings(".panel-heading")
        .find(".glyphicon")
        .addClass("rotate");
    });

  // Toggle plus minus icon on show hide of collapse element
  $(".collapse")
  .on("show.bs.collapse", function() {
      $(this)
      .parent()
      .find(".glyphicon")
      .addClass("rotate");
  })
  .on("hide.bs.collapse", function() {
      $(this)
      .parent()
      .find(".glyphicon")
      .removeClass("rotate");
  });

});
