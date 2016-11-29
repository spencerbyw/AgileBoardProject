function initUI(){

    $(document).toolTip();
    //Initialize sortables
     $( ".card-list-sortable" ).sortable({
      connectWith: ".card-list-sortable",
      stop: listSortHandler
    }).disableSelection();

    //New category dialog link
    $( "#newCategoryLink" ).click(function( event ) {
        $( "#newCategoryDialog" ).dialog(newBoardOpt).dialog( "open" );
        event.preventDefault();
    });

    //New card dialog link
    $( "#newCardLink" ).click(function( event ) {
        $( "#newCardDialog" ).dialog(newCardOpt).dialog( "open" );
        event.preventDefault();
    });
    //tool dialog link
    $( "#filterLink" ).click(function( event ) {
            var members = getModel().team.members;
            var defOpt = $("<option>",{value:"sel",text:"Anyone"});
            document.getElementById('filterUser').innerHTML = "";
            $('#filterUser').append(defOpt);
           for(var j = 0; j < members.length;j++){
                var opt = $("<option>",{value:members[j].email,text:members[j].name});
                $("#filterUser").append(opt);
            }
        $( "#filterDialog" ).dialog(filterOpt).dialog( "open" );
        event.preventDefault();
    });
    //new member link
    $( "#addMemberLink" ).click(function( event ) {
        $( "#newMemberDialog" ).dialog(newCardOpt).dialog( "open" );
        event.preventDefault();
    });
    
    //New card date picker
     $( "#dueDatePicker" ).datepicker({ dateFormat: 'mm-dd-yy' });

    }

//Show hide backlog
function toggleBacklog(show){
     $(".backlog-drawer").toggle("slide", { direction: "left" }, 300);
     window.setTimeout( marginToggle, 320);
}
function marginToggle(){
        if($(".backlog-drawer").is(":visible")){
            $('.list-container').css("margin-left","400px");
        }else{
            $('.list-container').css("margin-left","0px");
        }
};

//Init
$( function() {
    verify();
    initUI();
} );

//Handler for changes in card list
    function listSortHandler(){
        $(".card-list-sortable").each(function(){
            var col =$(this).attr('id');
            var colNum = col.split("_")[1];
            var list = $(this).sortable("toArray");
            for(var i = 0; i < list.length; i++){
                var card = list[i];
                var idVals = card.split("_");
                if(idVals[1] != colNum){
                    var card = document.getElementById(card);
                    $(card).attr("id","cat_"+colNum+"_card_"+idVals[3]);
                      moveCard(idVals[3],colNum,false);    
                }
            }
        });
    }

//New card dialog
var newCardOpt = {
        autoOpen: false,
        modal: true,
        width: 350,
        height:350,
        title: 'New Card'
};

$( "#newCardLink" ).click(function( event ) {
	$( "#newCardDialog" ).dialog( "open" );
	event.preventDefault();
});


//New board dialog
var newBoardOpt = {
        autoOpen: false,
        modal: true,
        width: 350,
        height:230,
        title: 'New Board'
};



//Log in dialog
var loginOpt = {
        autoOpen: false,
        modal: true,
        width: 250,
        height:185,
        title: 'Sign in'
};

//Tools dialog
var toolOpt = {
    autoOpen: false,
    position: 'center' ,
    title: 'Filtered Cards',
    draggable: false,
    width : "100%",
    height : "600", 
    resizable : false,
    modal : true
};

//backlog assignment dialog
var assignFromBacklogOpt = {
    autoOpen: false,
    title: 'Assign',
    draggable: false,
    width : "300",
    height : "213", 
    resizable : false,
    modal : true
};

//new team
var newTeamOpt = {
    autoOpen: false,
    title: 'Assign',
    draggable: false,
    width : "300",
    height : "400", 
    resizable : false,
    modal : true
};

//filter dialog
var filterOpt = {
    autoOpen: false,
    title: 'Filters',
    draggable: false,
    width : "300",
    height : "230", 
    resizable : false,
    modal : true
};




function showLogin(){
    $( "#loginDialog" ).dialog(loginOpt).dialog( "open" );
}


//middle methods to verify inputs in dialogs and trigger events

function addNewBoardCheck(){
   var description = document.getElementById("boardDescriptionInput").value;
    var title = document.getElementById("boardTitleInput").value;
    if(description == "" || title == ""){    
        return;
    }else{
        addNewBoard(title,description);
    }
}

function addNewCategoryCheck(){
   var description = document.getElementById("categoryDescriptionInput").value;
    var title = document.getElementById("categoryTitleInput").value;
    if(description == "" || title == ""){    
        alert("Missing info!");
        return;
    }else{
        addNewCategory(title,description);
    }
}

function newCardCheck(){
    var title = document.getElementById("newCardTitleInput").value;
    var date = document.getElementById("dueDatePicker").value;
    var priority = document.getElementById("newCardPriority").value;
    var description = document.getElementById("newCardTaskInput").value;
    if(description == "" || title == "" || priority == "" || date ==""){ 
        alert("Missing info!");   
        return;
    }else{
        addNewCard(title,description,date,priority);
    }
    document.getElementById("newCardTitleInput").value = "";
    document.getElementById("dueDatePicker").value = "";
    document.getElementById("newCardPriority").value = "";
    document.getElementById("newCardTaskInput").value = "";
}

function addMemberCheck(){
     //Example: <host>/adduser/name=Bob&email=bob%40bob.com&role=Ninja&pwd=afWIOJf&ent_type=SeniorDev
	var name = $("#newMemberName").val();
    var email = $("#newMemberEmail").val();
    var pass = $("#newMemberPass").val();
    var role = $("#newMemberRole").val();
    var pos = $("#newMemberPos").val();
    if(name == "" || email == "" || pass == "" || role == "" || pos == ""){
        alert("Missing info!");
    }else{
        addMember(name,email,pass,role,pos);
        addMemberToTeam(email,getModel().team.name);
        refreshBoard();
         $( "#newMemberDialog" ).dialog( "close" );
    }
}

function deleteCardConf(cardId){
    var resp = confirm("Are you sure you want to delete this card?");
    if(resp){
        deleteCard(cardId);
    }else{
        return;
    }
}

function deleteCatConf(catId){
    var resp = confirm("Are you sure you want to delete this category and it's cards?");
    if(resp){
        deleteCat(catId);
    }else{
        return;
    }
}

var assignId;
function assignFromBl(cardId){
    assignId = cardId;
    document.getElementById("ablUser").innerHTML = "";
    document.getElementById("ablCat").innerHTML = "";
    var members = getModel().team.members;
    for(var j = 0; j < members.length;j++){
        var opt = $("<option>",{value:members[j].email,text:members[j].name});
        $("#ablUser").append(opt);
    }
    var cats = getModel().team.board.categories;
    for(var i = 0; i < cats.length; i++){
        var catOpt = $("<option>",{value:cats[i].id,text:cats[i].title});
        $("#ablCat").append(catOpt);
    }

    $( "#assignFromBacklogDialog" ).dialog(assignFromBacklogOpt).dialog( "open" );
}

function newTeam(){
      $( "#newTeamDialog" ).dialog(newTeamOpt).dialog( "open" );
}

function newTeamCheck(){
     //Example: <host>/adduser/name=Bob&email=bob%40bob.com&role=Ninja&pwd=afWIOJf&ent_type=SeniorDev
	var name = $("#newTMemberName").val();
    var email = $("#newTMemberEmail").val();
    var pass = $("#newTMemberPass").val();
    var role = $("#newTMemberRole").val();
    var pos = $("#newTMemberPos").val();
    var tName = $("#newTeamName").val();
    var bName = $("#newBoardName").val();
    var bDesc = $("#newBoardDesc").val();
    if(name == "" || email == "" || pass == "" || role == "" || pos == "" || tName == "" || bName == "" || bDesc == ""){
        alert("Missing info!");
    }else{
        addNewTeam(name,email,pass,role,pos,tName,bName, bDesc);
         $( "#newTeamDialog" ).dialog( "close" );
          $( "#loginDialog" ).dialog( "close" );
    }
}