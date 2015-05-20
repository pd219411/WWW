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

function get_edit_span($outer) {
	return $outer.find("[name=" + EditButtonName() + "]");
}

function query_url() {
	$div = $("#ajax-urls");
	return $div.attr("data-query");
}

function disable_edit($row) {
			var $kart_do_glosowania = $row.find("[name=kart_do_glosowania]").find("input");
			$kart_do_glosowania.attr("disabled", true);

			var $wyborcow = $row.find("[name=wyborcow]").find("input");
			$wyborcow.attr("disabled", false);

			var $submit = $row.find("[name=button1]").find("button");
			$submit.attr("name", EditButtonName());
			$submit.html("Edytuj");
			$submit.attr("class", "daszek_hidden");

			var $cancel = $row.find("[name=button2]").find("button");
			$cancel.attr("class", "hidden_visible");
}

function enable_edit($row, json) {
			var $data_modyfikacji = $row.find("[name=data_modyfikacji]").find("input");
			$data_modyfikacji.attr("value", json["data_modyfikacji"]);

			var $kart_do_glosowania = $row.find("[name=kart_do_glosowania]").find("input");
			$kart_do_glosowania.attr("value", json["kart_do_glosowania"]);
			$kart_do_glosowania.attr("disabled", false);
			//var kart_do_glosowania = document.createElement("input");
			//kart_do_glosowania.type = "text";
			//kart_do_glosowania.value = json.kart_do_glosowania;
			//$row.find("[name=kart_do_glosowania]").html(kart_do_glosowania);

			var $wyborcow = $row.find("[name=wyborcow]").find("input");
			$wyborcow.attr("value", json["wyborcow)"]);
			$wyborcow.attr("disabled", false);

			var $submit = $row.find("[name=button1]").find("button");
			$submit.attr("name", SubmitButtonName());
			$submit.html("Zapisz");
			$submit.attr("class", "daszek_visible");

			var $cancel = $row.find("[name=button2]").find("button");
			$cancel.attr("name", CancelButtonName());
			$cancel.html("Anuluj");
			$cancel.attr("class", "daszek_visible");
}


function query_post($row) {
	var obwod_id = $row.attr("data-id");
	var post_data = { id: obwod_id };

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

$("tr.editrow").mouseover(function() {
	var $temp = get_edit_span($(this));
	console.log($temp);
	$temp.attr("class", "daszek_visible");
});

$("tr.editrow").mouseout(function() {
	var $temp = get_edit_span($(this));
	$temp.attr("class", "daszek_hidden");
});

$("button[name=" + EditButtonName() + "]").on('click', function(event) {
	console.log("editspan click");
	console.log(this);
	query_post($(this).closest("tr.editrow"));
});

$("button").on('click', "[name=" + SubmitButtonName() + "]", function(event) {
	console.log("submit click");
}

$("button").on('click', "[name=" + CancelButtonName() + "]", function(event) {
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
