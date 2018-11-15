$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    const $body = $('body');

    $body.toggleClass("mobile", $body.width() < 992);

    updateDarkMode();

    $(window).on("resize", function () {
        $body.toggleClass("mobile", $body.width() < 992);
    });

    $('.darkmode-toggler').on("click", function () {
        console.log(Cookies.get("darkmode") === "true");
        Cookies.set("darkmode", Cookies.get("darkmode") !== "true");

        updateDarkMode();
    });
});

function updateDarkMode() {
    const $body = $("body");
    const $toggler = $(".darkmode-toggler");

    if (Cookies.get("darkmode") === "true") {
        $body.removeClass("darkmode");
        $toggler.text("Natt");
    } else {
        $body.addClass("darkmode");
        $toggler.text("Dag");
    }
}
