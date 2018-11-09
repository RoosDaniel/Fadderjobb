$(function () {
    $(".filter-checkbox").find("input[type=checkbox]").on("change", function () {
        const $this = $(this);
        const $container = $this.parents(".filter-checkbox-container");

        // Deselect all other
        $container.find("input[type=checkbox]").not($this).prop("checked", false);

        const $label = $this.siblings(".form-check-label");
        const $caret = $container.find(".filter-checkbox-caret");

        if ($this.prop("checked")) {  // Move to selected
            $caret.offset($label.offset());
            $caret.css({width: $label.outerWidth(), opacity: 1});

            if ($label.hasClass("form-check-label-yes")) {
                $caret.css({backgroundColor: "#63bf69"});
            } else {
                $caret.css({backgroundColor: "#ff4c2f"});
            }
        } else {  // Deselect
            $caret.offset($container.offset());
            $caret.css({opacity: 0});
        }
    });

    initialMoveCaret();
});

function initialMoveCaret() {
    $(".filter-checkbox").find("input[type=checkbox]:checked").each(function () {
        const $this = $(this);
        const $container = $this.parents(".filter-checkbox-container");
        const $label = $this.siblings(".form-check-label");
        const $caret = $container.find(".filter-checkbox-caret");

        $caret.toggleClass("noanimate");

        $caret.offset($label.offset());
        $caret.css({width: $label.outerWidth(), opacity: 1});

        if ($label.hasClass("form-check-label-yes")) {
            $caret.css({backgroundColor: "#63bf69"});
        } else {
            $caret.css({backgroundColor: "#ff4c2f"});
        }

        $caret.toggleClass("noanimate");
    });
}
