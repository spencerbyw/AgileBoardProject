//Add new board to a given team
function addNewBoard(boardName, description){
    var data = {
        "id": 0,
        "title": boardName,
        "description": description,
        "categories": []
        };
    getModel().boards[getModel().boards.length] = data;
    loadBoard(boardName);
    var opt = $("<option>",{value:boardName,text:boardName});
    $("#boardDropdown").append(opt);
    $( "#newBoardDialog" ).dialog( "close" );
}

function addNewCategory(title, description){
    var boardTitle = getCurrentBoard();
    var url = "http://abp.spencerbywater.com/category?board_title="+boardTitle+"&cat_title="+title+"&cat_desc="+description;
     $.ajax({
        url: url,
        type: 'post',
        data: null,
        success: function (data) {
             $( "#newCategoryDialog" ).dialog( "close" );
             refreshBoard();
        },
        error: function(){
            alert("There was a problem adding the category.")
        }
    });
}

function  addNewCard(title,description,date,priority){
    var boardTitle = getCurrentBoard();
    var url = "http://abp.spencerbywater.com/newcard/board_title="+boardTitle+"&priority="+priority+"&description="+description+"&title="+title+"&due_date="+date;
     $.ajax({
        url: url,
        type: 'post',
        data: null,
        success: function (data) {
            $( "#newCardDialog" ).dialog( "close" );
             refreshBoard();
        },
        error: function(){
            alert("There was a problem adding the card.")
        }
    });
       
}

function deleteCard(cardId){
    $.ajax({
        url: "http://abp.spencerbywater.com/card/"+cardId,
        type: 'delete',
        data: null,
        success: function (data) {
            refreshBoard();
        },
        error: function(){
            alert("There was a problem deleting the card.")
        }
    });
}

function deleteCat(catId){
      $.ajax({
        url: "http://abp.spencerbywater.com/category/"+catId,
        type: 'delete',
        data: null,
        success: function (data) {
            refreshBoard();
        },
        error: function(){
            alert("There was a problem deleting the category.")
        }
    });
}

function assignCardTo(cardId,user){
        if(user =="sel"){
            return;
        }
        $.ajax({
        url: "http://abp.spencerbywater.com/assigncard/email="+user+"&card_id="+cardId,
        type: 'put',
        data: null,
        success: function (data) {
            refreshBoard();
        },
        error: function(){
            alert("There was a problem assigning the card.")
        }
    });
}

function assignFromBacklog(){
    var cardId = assignId;
    var user = $("#ablUser").val();
    var cat = $("#ablCat").val();
    $( "#assignFromBacklogDialog" ).dialog( "close" );
    $.ajax({
        url: "http://abp.spencerbywater.com/assigncard/email=" + user + "&card_id=" + cardId,
        type: 'put',
        data: null,
        success: function (data) {
            moveCard(cardId,cat,true);
        },
        error: function () {
            alert("There was a problem assigning the card.")
        }
    });
}

function moveCard(cardId,cat,refresh){
    $.ajax({
        url: "http://abp.spencerbywater.com/movecard/card_id=" + cardId + "&category_id=" + cat,
        type: 'put',
        data: null,
        success: function (data) {
            if(refresh){
                refreshBoard();
            }
        },
        error: function () {
            alert("There was a problem assigning the card.")
        }
    });
}

 function addMember(name,email,pass,role,pos){
    $.ajax({
        url: "http://abp.spencerbywater.com/adduser/name="+name+"&email="+email+"&role="+role+"&pwd="+pass+"&ent_type="+pos,
        type: 'post',
        data: null,
        success: function (data) {
            return;
        },
        error: function () {
            alert("There was a problem adding the memeber.")
        }
    });
 }

 function addMemberToTeam(email,teamName){
        $.ajax({
        url: "http://abp.spencerbywater.com/addusertoteam/team_name="+teamName+"&email="+email,
        type: 'put',
        data: null,
        success: function (data) {
            return;
        },
        error: function () {
            //alert("There was a problem adding the memeber to the team.")
        }
    });
 }

 function createTeam(teamName,leaderEmail){
       $.ajax({
        url: "http://abp.spencerbywater.com/addteam/name="+teamName+"&email="+leaderEmail,
        type: 'post',
        data: null,
        success: function (data) {
            return;
        },
        error: function () {
            alert("There was a problem creating the team.")
        }
    });
 }

 function createBoardOnTeam(teamName,title,bDesc){
       $.ajax({
        url: "http://abp.spencerbywater.com/board/team_name="+teamName+"&board_title="+title+"&board_desc="+bDesc,
        type: 'post',
        data: null,
        success: function (data) {
          return;
        },
        error: function () {
            alert("There was a problem creating the board.")
        }
    });
 }

function addNewTeam(name,email,pass,role,pos,tName,bName,bDesc){
    addMember(name,email,pass,role,pos);
    createTeam(tName,email);
    addMemberToTeam(email,tName);
    createBoardOnTeam(tName,bName,bDesc);
    setCookie("user",email,1);
    setCookie("pass",pass,1);
    verify();
}
