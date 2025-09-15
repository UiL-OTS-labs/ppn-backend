$(function () {
    let asInitVals = [];
    let oTable = $('.dt_custom').DataTable({
        order: [[0, 'asc'], [2, 'asc']],
        lengthMenu: [
            [10, 20, 50, -1],
            ["10", "20", "50", "\u221e"]
        ],
        responsive: true,
        pageLength: -1,
        paginationType: "full_numbers",
    });


    $("tfoot input").keyup(function () {
        /* Filter on the column (the index) of this element */
        let columnIndex = $("tfoot th").index($(this).parent());

        oTable.column(columnIndex).search(this.value).draw();
    });

    /*
    * Support functions to provide a little bit of 'user friendlyness' to the textboxes in
    * the footer
    */
    $("tfoot input").each(function (i) {
        asInitVals[i] = this.value;
    });

    $("tfoot input").focus(function () {
        if (this.className == "search_init") {
            this.className = "";
            this.value = "";
        }
    });

    $("tfoot input").blur(function (i) {
        if (this.value == "") {
            this.className = "search_init";
            this.value = asInitVals[$("tfoot input").index(this)];
        }
    });

    $('.icon-remove-participant').click(function () {
        return confirm(gettext('timeslot:warning:confirm_remove_participant'));
    });

    $('.download-button').click(function () {
        return confirm(gettext('timeslot:warning:download_csv'));
    });

});