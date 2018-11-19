$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    const $body = $('body');

    $body.toggleClass("mobile", $body.width() < 992);

    $(window).on("resize", function () {
        $body.toggleClass("mobile", $body.width() < 992);
    });

    $('.darkmode-toggler').on("click", function () {
        Cookies.set("darkmode", Cookies.get("darkmode") !== "true");
        updateDarkMode();
    });
});

function updateDarkMode() {
    const $body = $("body");
    const $toggler = $(".darkmode-toggler");
    const $metaTag = $("meta[name='theme-color']");

    if (Cookies.get("darkmode") === "true") {
        $body.addClass("darkmode");
        $toggler.text("Dag");
        $metaTag.attr("content", "#000");
    } else {
        $body.removeClass("darkmode");
        $toggler.text("Natt");
        $metaTag.attr("content", "#fff");
    }
}
