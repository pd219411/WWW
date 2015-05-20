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

var loading;
var ajax_requests = 0;


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

function GetCancelButton($row) {
	return $row.find("[name=" + CancelButtonName() + "]");
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

function SetStatus($row, success, status_message) {
	var $temp = $row.find("[name=status]").find("div");
	console.log($temp);
	$temp.html(status_message);
	if (success) {
		$temp.attr("class", "daszek_success");
	} else {
		$temp.attr("class", "daszek_failure");
	}
}

function AjaxStart() {
	++ajax_requests;
	if (ajax_requests == 1) {
		loading.play();
	}
}

function AjaxComplete() {
	--ajax_requests;
	if (ajax_requests == 0) {
		loading.stop();
		loading.canvas.getContext('2d').clearRect(0, 0, loading.canvas.width, loading.canvas.height);
	}
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
			GetKartDoGlosowania($row).attr("readonly", true);
			GetWyborcow($row).attr("readonly", true);

			var $submit = $row.find("[name=button2]").find("button");
			$submit.attr("class", "daszek_hidden");

			var $cancel = $row.find("[name=button3]").find("button");
			$cancel.attr("class", "daszek_hidden");

			$row.attr("data-readonly", "true");
}

function enable_edit($row, json) {
			console.log(GetDataModyfikacji($row).attr("value"));
			GetDataModyfikacji($row).attr("value", json["data_modyfikacji"]);
			console.log(GetDataModyfikacji($row).attr("value"));

			var $temp = GetKartDoGlosowania($row);
			$temp.val(json["kart_do_glosowania"]);
			$temp.attr("readonly", false);

			$temp = GetWyborcow($row);
			$temp.val(json["wyborcow"]);
			$temp.attr("readonly", false);

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

			$row.removeAttr("data-readonly");
}


function query_post($row) {
	var obwod_id = $row.attr("data-id");
	var post_data = {};
	post_data["id"] = obwod_id;

	AjaxStart();

	$.ajax({
		url : query_url(),
		type : "POST",
		data : post_data,
		success : function(json) {
			console.log("handle_success query");
			console.log(json);
			enable_edit($row, json);
			SetStatus($row, true, "OK");
			AjaxComplete();
		},
		error : function(xhr, errmsg, err) {
			console.log("handle_error query");
			SetStatus($row, false, errmsg + " " + err);
			AjaxComplete();
		}
	});
};

function submit_post($row) {
	var obwod_id = $row.attr("data-id");

	AjaxStart();

	var post_data = {};
	post_data["id"] = obwod_id;
	post_data["data_modyfikacji"] = GetDataModyfikacji($row).val();
	post_data["kart_do_glosowania"] = GetKartDoGlosowania($row).val();
	post_data["wyborcow"] = GetWyborcow($row).val();

	$.ajax({
		url : submit_url(),
		type : "POST",
		data : post_data,
		success : function(json) {
			console.log("handle_success submit");
			console.log(json);
			disable_edit($row);
			if (json["success"]) {
				SetStatus($row, true, "OK");
			} else {
				SetStatus($row, false, "TODO: message from json");
			}
			AjaxComplete();
		},
		error : function(xhr, errmsg, err) {
			console.log("handle_error submit");
			disable_edit($row);
			SetStatus($row, false, errmsg + " " + err);
			AjaxComplete();
		}
	});
};

$("tr.editrow").mouseover(function() {
	if ($(this).attr("data-readonly")) {
		var $temp = GetEditButton($(this));
		$temp.attr("class", "daszek_visible");
	}
});

$("tr.editrow").mouseout(function() {
	if ($(this).attr("data-readonly")) {
		var $temp = GetEditButton($(this));
		$temp.attr("class", "daszek_hidden");
	}
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

///////////////////////
$(document).ready(function() {
	loading = new Sonic({
		width: 100,
		height: 40,
		padding: 5,

		stepsPerFrame: 5,
		trailLength: 1,
		pointDistance: .01,
		strokeColor: '#00CC00',
		step: 'fader',
		multiplier: 2,

		setup: function() {
			this._.lineWidth = 5;
		},

		path: [
			['arc', 10, 10, 10, -270, -90],
			['bezier', 10, 0, 40, 20, 20, 0, 30, 20],
			['arc', 40, 10, 10, 90, -90],
			['bezier', 40, 0, 10, 20, 30, 0, 20, 20]
		]
	});

	document.body.appendChild(loading.canvas);
});
