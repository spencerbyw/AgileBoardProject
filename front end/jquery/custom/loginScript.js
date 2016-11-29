

function verify(){
    var user = getCookie("user");
    var pass = getCookie("pass");
    if(user == ""){
        showLogin();
    }else{
            $.getJSON("http://abp.spencerbywater.com/userboard/user="+user+"&pwd="+pass, function(obj) {
            if(obj.error != undefined){
                $("#email").css("background-color", "#ff6666");
                $("#password").css("background-color", "#ff6666");
                return;
            }
            setModel(obj);
            var board = obj.team.board;
            $("#boardDropdown").show();
            $( "#loginDialog" ).dialog(loginOpt).dialog( "close" );
            populateBoard(board);
        });
    }
}

function checkLogin(){
    var e = document.getElementById("email");
    var p = document.getElementById("password");
    $(e).css("background-color", "");
      $.getJSON("http://abp.spencerbywater.com/userboard/user="+e.value+"&pwd="+p.value, function(obj) {
       if(obj.error != undefined){
            $("#email").css("background-color", "#ff6666");
            $("#password").css("background-color", "#ff6666");
            return;
        }
        setModel(obj);
        var board = obj.team.board;
        $("#boardDropdown").show();
        $( "#loginDialog" ).dialog(loginOpt).dialog( "close" );
        setCookie("user",e.value,1);
        setCookie("pass",p.value,1);
        populateBoard(board);
    }).error(function(){
         $(e).css("background-color", "#ff6666");
         $(p).css("background-color", "#ff6666");
    });
}

function logout(){
    setCookie("user","",0);
    setCookie("pass","",0);
   location.reload();
}