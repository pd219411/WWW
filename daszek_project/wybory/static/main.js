// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// END OF COPY-PASTE ===========================================================


$("form[name=AJAX_FORM]").on('submit', function(event) {
	event.preventDefault();
	console.log("on_submit()");
	$form = $(this);
	create_post($form);
});

// AJAX for posting
function create_post(form) {
	console.log("create_post()");
	console.log(csrftoken);
	console.log($form.attr('action'));
	$url = $form.attr('action');
	var $text = $form.find('#TEST-AJAX-TEXT');
	var post_data = $form.serialize();

	disable_buttons($form);

	$.ajax({
		url : $url,
		type : "POST",
		data : post_data,
		//TODO: does not work complete : enable_buttons($form),
		success : handle_success.bind($form),
		error : handle_error.bind($form)
	});
};

function handle_success(json) {
	console.log("handle_success");
	console.log(json);

	enable_buttons(this);
	if (json.success) {
		status_success(this);
	} else {
		status_error(this);
	}
}

function handle_error(xhr, errmsg, err) {
	console.log("handle_error");
	console.log(xhr.status + " : " + xhr.responseText);

	enable_buttons(this);
	status_error(this);
	//$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+ " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
}

function status_success($form) {
	var $temp = $form.find("[name='STATUS']");
	//var $temp = $("#TEST-AJAX-STATUS");
	$temp.html("Success");
}

function status_error($form) {
	//var temp = document.getElementById("TEST-AJAX-STATUS");
	//temp.innerHTML = "Error!";
	var $temp = $form.find("[name='STATUS']");
	$temp.html("Error!");
}

function disable_buttons($form) {
	var $temp = $form.find("[name='submit-button']");
	$temp.attr("disabled", true);
}

function enable_buttons($form) {
	var $temp = $form.find("[name='submit-button']");
	$temp.attr("disabled", false);
}


///////////////////////////

function EditButtonName() {
	return "editbutton";
}

function SubmitButtonName() {
	return "submitbutton";
}

function CancelButtonName() {
	return "cancelbutton";
}

function GetEditButton($row) {
	return $row.find("[name=" + EditButtonName() + "]");
}

function GetDataModyfikacji($row) {
	return $row.find("[name=data_modyfikacji]");
}

function GetKartDoGlosowania($row) {
	return $row.find("[name=kart_do_glosowania]").find("input");
}

function GetWyborcow($row) {
	return $row.find("[name=wyborcow]").find("input");
}

function GetUrlsDiv() {
	return $("#ajax-urls");
}

function query_url() {
	return GetUrlsDiv().attr("data-query");
}

function submit_url() {
	return GetUrlsDiv().attr("data-submit");
}

function disable_edit($row) {
			GetKartDoGlosowania($row).attr("disabled", true);
			GetWyborcow($row).attr("disabled", true);

			var $submit = $row.find("[name=button2]").find("button");
			$submit.attr("class", "daszek_hidden");

			var $cancel = $row.find("[name=button3]").find("button");
			$cancel.attr("class", "daszek_hidden");
}

function enable_edit($row, json) {
			console.log(GetDataModyfikacji($row).attr("value"));
			GetDataModyfikacji($row).attr("value", json["data_modyfikacji"]);
			console.log(GetDataModyfikacji($row).attr("value"));

			var $temp = GetKartDoGlosowania($row);
			$temp.attr("value", json["kart_do_glosowania"]);
			$temp.attr("disabled", false);

			$temp = GetWyborcow($row);
			$temp.attr("value", json["wyborcow"]);
			$temp.attr("disabled", false);

			var $edit = $row.find("[name=button1]").find("button");
			$edit.attr("class", "daszek_hidden");

			var $submit = $row.find("[name=button2]").find("button");
			$submit.attr("name", SubmitButtonName());
			$submit.html("Zapisz");
			$submit.attr("class", "daszek_visible");

			var $cancel = $row.find("[name=button3]").find("button");
			$cancel.attr("name", CancelButtonName());
			$cancel.html("Anuluj");
			$cancel.attr("class", "daszek_visible");
}


function query_post($row) {
	var obwod_id = $row.attr("data-id");
	var post_data = {};
	post_data["id"] = obwod_id;


	$.ajax({
		url : query_url(),
		type : "POST",
		data : post_data,
		success : function(json) {
			console.log("handle_success");
			console.log(json);
			enable_edit($row, json);
		},
		error : function(xhr, errmsg, err) {
			console.log("handle_error");
		}
	});
};

function submit_post($row) {
	var obwod_id = $row.attr("data-id");
	//var post_data = { id: obwod_id, data_modyfikacji : GetDataModyfikacji };
	var post_data = {};
	post_data["id"] = obwod_id;
	post_data["data_modyfikacji"] = GetDataModyfikacji($row).val();
	post_data["kart_do_glosowania"] = GetKartDoGlosowania($row).val();
	post_data["wyborcow"] = GetWyborcow($row).val();
	console.log(post_data);

	$.ajax({
		url : submit_url(),
		type : "POST",
		data : post_data,
		success : function(json) {
			console.log("handle_success");
			console.log(json);
			disable_edit($row, json);
			//TODO: disable edit and set stat
		},
		error : function(xhr, errmsg, err) {
			console.log("handle_error");
			//TODO: disable edit and set status
		}
	});
};

$("tr.editrow").mouseover(function() {
	var $temp = GetEditButton($(this));
	console.log($temp);
	$temp.attr("class", "daszek_visible");
});

$("tr.editrow").mouseout(function() {
	var $temp = GetEditButton($(this));
	$temp.attr("class", "daszek_hidden");
});

$("button[name=" + EditButtonName() + "]").on('click', function(event) {
	console.log("edit click");
	query_post($(this).closest("tr.editrow"));
});

$("tr.editrow").on('click', "[name=" + SubmitButtonName() + "]", function(event) {
	console.log("submit click");
	submit_post($(this).closest("tr.editrow"));
});

$("tr.editrow").on('click', "[name=" + CancelButtonName() + "]", function(event) {
	console.log("cancel click");
	disable_edit($(this).closest("tr.editrow"));
});


//$("row_entryform[name=AJAX_FORM]").on('submit', function(event) {
//$(this).button show
//}

//static -> form
//1) span <-> hidden input
//2) tr wymienic na nowy wiersz z serwera

//fill form
//1) edytuj zaciaga z serwera AJAXem
