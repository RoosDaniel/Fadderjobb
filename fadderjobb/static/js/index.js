$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    const $body = $('body');

    $body.toggleClass("mobile", $body.width() < 992);

    $(window).on("resize", function () {
        $body.toggleClass("mobile", $body.width() < 992);
    });
});
