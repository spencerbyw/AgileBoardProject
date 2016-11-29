
var currentBoard;
var model;

function setModel(data){
    model = data;
}
function getModel(){
    return model;
}
function setCurrentBoard(name){
    currentBoard = name;
}

function getCurrentBoard(){
    return currentBoard;
}

//Create DOM objects and refresh page content
function categoryCreator(idVal,name,catDesc,cardList){
    var headerCode = "<span title='"+catDesc+"'>"+name+"</span>"; 
    if(idVal != "bl"){
     headerCode += "<input type='button' onclick='deleteCatConf("+idVal+")' value='X' style='float:right;'/>";
    }
    var header = $("<div>",{ class: "list-header",html:headerCode});
    if(idVal != "bl"){
        var ul = $("<ul>",{id:"cat_"+idVal,class:"card-list-sortable"});
    }else{
        var ul = $("<ul>",{id:"cat_"+idVal,class:"card-list-no-drag"});
    }
    if(cardList != undefined){
        for(var i = 0; i < cardList.length;i++){
            var cardObj = cardList[i];
            if(checkFilter(cardObj.id)){
                var li = $("<li>",{id:"cat_"+idVal+"_card_"+cardObj.id,class:"card-list-item"});
                var card = $("<div>",{class:"card"});
                var cardHeader = $("<div>",{class:"card-header",text:cardObj.title});
                var assignee = cardObj.assignedto;
                if(assignee == null){
                    assignee = "Unassigned";
                }else{
                    assignee = assignee.name;
                }
                var cardBodyText = "<b>Assignee:</b> " + assignee + "<br/>";
                var date = cardObj.due_date;
                date = date.replace("00:00:00 GMT","");
                cardBodyText+=  "<b>Due:</b> " + date + "<br/>";
                cardBodyText+=  "<b>Priority:</b> " + cardObj.priority + "<br/>";
                cardBodyText+= "<b>Task:</b><br/>"+cardObj.description +"<br/>";
                var cardBody = $("<div>",{class:"card-body",html:cardBodyText});
            
                var assign = $("<select>",{onchange:"assignCardTo("+cardObj.id+",this.value)",class:'form-control card-base assign-select'});
                var members = getModel().team.members;
                var defOpt = $("<option>",{value:"sel",text:"Assign to.."});
                assign.append(defOpt);
            for(var j = 0; j < members.length;j++){
                    var opt = $("<option>",{value:members[j].email,text:members[j].name});
                    assign.append(opt);
                }
                var deleteButton = $("<input>",{type:"button",value:"delete",onclick:"deleteCardConf("+cardObj.id+")",class:"card-base card-delete"});
                var cardBase = $("<div>",{class:"card-base-wrapper"});
                cardBase.append(deleteButton);
                cardBase.append(assign);

                $(card).append(cardHeader);
                $(card).append(cardBody);
                if(idVal != "bl"){
                $(card).append(cardBase);
                }else{
                    var assignButton = $("<input>",{type:"button",value:"Assign",onclick:"assignFromBl("+cardObj.id+")",class:"assign-from-bl-button"});
                    $(card).append(assignButton);
                }
                $(li).append(card);
                $(ul).append(li);
            }
        }
    }
    var outer = $("<div>",{id:"list_"+idVal,class:"card-list"}).append(header).append(ul);
    return outer;
}

function populateBoard(board){
        setCurrentBoard(board.title);
        document.getElementById("brand").innerHTML = board.title;
        $("#brand").attr("title",board.description);
        var categories = board.categories;
        var lists = "";
        document.getElementById("listContainer").innerHTML="";        
        for(var i = 0; i < categories.length;i++){
            var catName = categories[i].title;
            var cards = categories[i].cards;
            var id = categories[i].id;
            var catDesc = categories[i].description;
            $('#listContainer').append(categoryCreator(id,catName,catDesc,cards));
        }
        var width = (categories.length) * 390;
        if(width > $(window).width()){
            $("#listContainer").css("width",width);
        }
        document.getElementById("backLogListContainer").innerHTML="";
         $('#backLogListContainer').append(categoryCreator("bl","Backlog",board.backlog));
        initUI();   
}

//Refresh board after changes
function refreshBoard(){
    var user = getCookie("user");
    var pass = getCookie("pass");
      $.getJSON("http://abp.spencerbywater.com/userboard/user="+user+"&pwd="+pass, function(obj) {
        setModel(obj);
        var board = obj.team.board;
        populateBoard(board);
      });
}

//Load board on name, or trigger new board dialog
function loadBoard(boardName){
    if(boardName=="select"){
        return;
    }
    if(boardName == "newboard"){
        $( "#newBoardDialog" ).dialog(newBoardOpt).dialog( "open" );
        event.preventDefault();
        return;
    }
  var boards = model.boards;
  for(var i = 0; i < boards.length; i++){
      var b = boards[i];
      if(b.title == boardName){
          populateBoard(b);
          return;
        }
    }
}