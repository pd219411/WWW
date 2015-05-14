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
