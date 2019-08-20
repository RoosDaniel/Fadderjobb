$(function () {
    const $filterButton = $("#filter-button");

    $(".filter-checkbox").find("input[type=checkbox]").on("change", function () {
        const $this = $(this);
        const $container = $this.parents(".filter-checkbox-wrapper");
        const $label = $this.siblings(".filter-checkbox-label");
        const $caret = $container.find(".filter-checkbox-caret");

        // Deselect all other
        $container.find("input[type=checkbox]").not($this).prop("checked", false);

        if ($this.prop("checked")) {  // Move to selected
            moveCaret($caret, $label);
        } else {  // Deselect
            $caret.offset($container.offset());
            $caret.css({opacity: 0});
        }

        $filterButton.trigger("click");
    });

    $("#filter-jobtype").find(".dropdown-item").on("click", function () {
        const $this = $(this);
        const $container = $this.parents(".filter-dropdown-container");

        if ($this.hasClass("filter-dropdown-reset")) {
            $container.find("button").text(" Välj jobbtyp");
            $container.find("input").val("");
        } else {
            $container.find("button").text(` ${$this.text()}`);
            $container.find("input").val($this.text());
        }

        $filterButton.trigger("click");
    });

    $("#add-filter").find(".dropdown-item").on("click", function () {
        const $this = $(this);

        $this.css({display: "none"});
        $(`#${$this.data("filter-id")}`).toggleClass("hidden");
    });

    $(".filter-remove").on("click", function () {
        const $this = $(this);
        const $container = $this.parents(".filter-checkbox-wrapper");

        $container.find("input[type=checkbox]").not($this).prop("checked", false);

        $container.addClass("hidden");
        $("#add-filter").find(".filter-add").filter(function () {
            return $(this).data("filter-id") == $container.prop("id");
        }).css({display: ""});

        $filterButton.trigger("click");
    });

    setTimeout(initialMoveCaret, 100);
});

function initialMoveCaret() {
    $(".filter-checkbox").find("input[type=checkbox]:checked").each(function () {
        const $this = $(this);
        const $container = $this.parents(".filter-checkbox-wrapper");
        const $label = $this.siblings(".filter-checkbox-label");
        const $caret = $container.find(".filter-checkbox-caret");

        $caret.toggleClass("noanimate", true);
        moveCaret($caret, $label);
        $caret.toggleClass("noanimate", false);
    });
}

function moveCaret($caret, $label) {
    $caret.offset($label.offset());
    $caret.css({width: $label.outerWidth(), opacity: 1, top: 0});
}
