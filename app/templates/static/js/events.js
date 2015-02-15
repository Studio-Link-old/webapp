function notifyMe(caller) {
	if (!("Notification" in window)) {
		//alert("This browser does not support desktop notification");
	} else if (Notification.permission === "granted") {
		var notification = new Notification("Studio-Link call from: " + caller);
		notification.onclick = function() {
			window.focus();
		};
	} else if (Notification.permission !== 'denied') {
		Notification.requestPermission(function (permission) {
			// Nothing todo
		});
	}
}

//Long Polling Call Events
function checkCallEvents()
{

    $.ajax({
        type: "GET",
    url: "/events",
    timeout: 30000,
    dataType: "json"
    }).done(function(result) {

        if (result.INCOMING) {
	    notifyMe(result.INCOMING);
            bootbox.confirm("Incoming call from '" + result.INCOMING  + "', accept?", 
                function(result) {
                    if (result) {
                        $.ajax({url: "/calls/answer"});
			setTimeout("window.location = '/calls'", 500);
                    } else {
                        $.ajax({url: "/calls/hangup"});
                    	setTimeout("checkCallEvents()", 5000);
                    }
                }); 
        } else {
            checkCallEvents();
        }
    });
};

jQuery(document).ready(function () {
    setTimeout("checkCallEvents()", 500);
});
