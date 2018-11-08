$(function() {
   $(".filter-checkbox").find("input[type=checkbox]").on("change", function() {
       const $this = $(this);
       if (!$this.prop("checked")) return;

       $this.parent().parent().parent().find("input[type=checkbox]").prop("checked", false);
       $this.prop("checked", true);
   });
});
