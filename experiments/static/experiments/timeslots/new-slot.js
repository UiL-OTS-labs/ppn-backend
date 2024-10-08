/**
 * This file does the following:
 * - creates a datetimepicker for the timeslot creation
 * - Validates the new timeslot data before submitting the form
 */
$(function () {
    // Create a datetimepicker for the datetime field
    $('#id_datetime').datetimepicker({
        format: 'yyyy-mm-dd hh:ii',
        weekStart: 1, // Monday
        startDate: new Date(), // Today
        autoclose: true,
        keyboard: false, // It's buggy
        pickerPosition: 'top-left',
        forceParse: false, // We validate manually, as to provide better feedback to the user
    });

    // Run validation when the submit button is clicked
    // When it returns false, the form is not submitted.
    $("#save-new-slot").click(function () {
        let datetime = $('#id_datetime');

        try {
            let dt = datetime.val().split(' ');

            // If we could not split into 2 separate values, something is messed up
            if(dt.length !== 2)
            {
                alert(gettext('timeslot:error:invalid_date'));
                return false
            }

            let date = dt[0];
            let time = dt[1];

            if (!validate_date(date))
            {
                alert(gettext('timeslot:error:invalid_date'));
                return false;
            }

            if (!validate_time(time))
            {
                alert(gettext('timeslot:error:invalid_time'));
                return false;
            }

            return true;

        } catch (e) {
            alert(gettext('timeslot:error:cannot_validate_datetime'));
        }


        return false;
    });
});

// This code is lifted from the old application. It's a bit manual, but it works pretty well
const this_year = new Date().getFullYear();

function validate_date(date) {
    /**
     * Validates a date in yyyy-mm-dd format
     */

    if(!/^\d{4}-\d{1,2}-\d{1,2}$/.test(date))
        return false;

    let parts = date.split('-');
    let year = parseInt(parts[0], 10);
    let month = parseInt(parts[1], 10);
    let day = parseInt(parts[2],10);

    if(year < this_year || year > 3000 || month === 0 || month > 12)
        return false;

    let monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

    // Adjust for leap years
    if(year % 400 === 0 || (year % 100 !== 0 && year % 4 === 0))
        monthLength[1] = 29;

    return day > 0 && day <= monthLength[month - 1];
}

function validate_time(time) {
    /**
     * Validates a time in hh:mm format, no seconds allowed!
     */
    if(!/^\d{1,2}:\d{2}$/.test(time))
        return false;

    let parts = time.split(':');
    let hours = parseInt(parts[0], 10);
    let minutes = parseInt(parts[1], 10);

    return !(hours < 0 || hours > 24 || minutes < 0 || minutes > 59);
}
