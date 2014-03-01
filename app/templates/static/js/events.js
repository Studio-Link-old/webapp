//Long Polling Call Events
function checkCallEvents()
{

    $.ajax({
        type: "GET",
    url: "/calls/events",
    timeout: 30000,
    dataType: "json"
    }).done(function(result) {

        if(result.INCOMING) {
            bootbox.confirm("Are you sure?", function(result) {
                Console.log(result);
            }); 
        }

        checkCallEvents();
    });
};

jQuery(document).ready(function () {
    setTimeout("checkCallEvents()", 2000);
});
