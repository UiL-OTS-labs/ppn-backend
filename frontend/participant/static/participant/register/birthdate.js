var formatBirthdate = function() {
	var val = $("#id_birth_date").val();
	if(val == "" || val == "dd-mm-yyyy") {
		$("#formatted_birthday").hide();
	} else {
		$("#formatted_birthday").show();
		var dateregex = /^((?:0[1-9])|(?:[1-2]\d)|(?:3[0-1]))-(0[1-9]|1[0-2])-(\d{4})$/;
		if((m = dateregex.exec(val)) != null) {
			d = new Date(parseInt(m[3],10), parseInt(m[2],10) - 1, parseInt(m[1],10));
			mindate = new Date(1900,0,1);
			if(d < mindate) {
				$("#formatted_birthday_value").html("<span style='color: red;'>Geboortedatum moet minimaal in het jaar 1900 liggen</span>");	
			} else {
				$("#formatted_birthday_value").html(convertDateToDutchString(d));
			}
		} else {
			$("#formatted_birthday_value").html("<span style='color: red;'>Ongeldige datum</span>");
		}
	}
};

var months = ["januari", "feburari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"];

function convertDateToDutchString(d) {
	return d.getDate() + " " + months[d.getMonth()] + " " + d.getFullYear();
}

jQuery(function($){
    let birth_date_element = $("#id_birth_date");
    birth_date_element.parent().append($('<div>').attr('id', 'formatted_birthday_value'));

	birth_date_element.mask(
		"99-99-9999",
		{
			placeholder:"dd-mm-yyyy",
			completed:formatBirthdate
		}
	);

	birth_date_element.focusout(formatBirthdate);
	formatBirthdate();
});