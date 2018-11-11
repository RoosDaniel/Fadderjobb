$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $('body').toggleClass("mobile", $(document).width() < 992);
    $(window).on("resize", function () {
        $('body').toggleClass("mobile", $(document).width() < 992);
    });
});
