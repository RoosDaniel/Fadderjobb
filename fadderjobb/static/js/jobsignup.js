$(function () {
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
    });

    $(".filter-dropdown-container").find(".dropdown-item").on("click", function () {
        const $this = $(this);
        const $container = $this.parents(".filter-dropdown-container");

        if ($this.hasClass("filter-dropdown-reset")) {
            $container.find("button").text(" Välj jobbtyp");
            $container.find("input").val("");
        } else {
            $container.find("button").text(` ${$this.text()}`);
            $container.find("input").val($this.text());
        }
    });

    initialMoveCaret();
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
    $caret.css({width: $label.outerWidth(), opacity: 1, backgroundColor: "#222", top: 0});
}
