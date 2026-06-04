$(function () {

    // Allows auto opening when an anchor was specified in the url
    if (window.location.hash) {
        $('body').find(window.location.hash).collapse('show');
    }

    $(".hide-participants").click(function () {
        return confirm(gettext('datamanagement:home:warning:hide_participants'));
    });

    $(".delete-invites").click(function () {
        return confirm(gettext('datamanagement:home:warning:delete_invites'));
    });

    $(".delete-comments").click(function () {
        return confirm(gettext('datamanagement:home:warning:delete_comments'));
    
    });

    $('#select-all-anonymize').click(function() {
        $('#anonymize-table input[type="checkbox"]').prop('checked', this.checked);
    });

    $('#select-all-delete').click(function() {
        $('#delete-table input[type="checkbox"]').prop('checked', this.checked);
    });
    
    $('#bulk-anonymize-btn').click(function() {
        return confirm(gettext('datamanagement:home:warning:bulk_anonymize'));
    });

    $('#bulk-delete-btn').click(function() {
        return confirm(gettext('datamanagement:home:warning:bulk_delete'));
    });

});