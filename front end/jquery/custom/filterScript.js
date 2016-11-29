var cardList;

function filterCards(){
    var user = $("#filterUser").val();
    var pri = $("#filterPriority").val();
    var pd = $("#filterPassedDue").is(':checked');
    if(user != "sel" || pri != "any" || pd == true){
        var url = "http://abp.spencerbywater.com/filteredcards?board_title="+getCurrentBoard();
        var q = true;
        if(user != "sel"){
            url += "&assignee=" + user;
        }
        if(pri != "any"){
                url += "&priority=" + pri;
        }
        if(pd){
                url += "&past_due=" + pd;
        }
         $.ajax({
            url: url,
            type: 'get',
            data: null,
            success: function (data) {
                cardList = data;
                refreshBoard();
                 $( "#filterDialog" ).dialog( "close" );
            },
            error: function () {
                alert("There was a problem filtering cards.")
            }
        });
    }
}

function checkFilter(id){
    if(cardList == undefined){
        return true;
    }
    for(var i = 0; i < cardList.length; i++){
        if(cardList[i].id == id){
            return true;
        }
    }
    return false;
}

function clearFilter(){
    cardList = undefined;
    refreshBoard();
}