var clientId;

/* 画面が表示された時の処理 */
$(function() {
    showMessage("接続していません。名前と称号を入れて接続してください。");

    /* 画面表示時に履歴を読み込む */
    loadHistory();

    /* [接続]ボタンがクリックされたら、getTokenを呼び出す */
    $("#connect").click(getToken);

    /* 新しい絵を描くボタンがクリックされたときの処理 */
    $("#newpicture").click(newPicture);

    $("#showcurrent").click(showCurrent);
});


/* メッセージ欄にメッセージを表示する */
function showMessage(message) {
    $("#message").html(message);
}


/* 保存された絵の一覧を表示する */
function loadHistory(){
    /* すでに表示されている履歴をクリアする */
    $("#history ul li").remove();

    /* 最新の履歴を読み込んで表示する */
    $.get("/history", function(data){
        $.each(data, function(i, history) {
            $("#history ul").append("<li><a href='#' onclick='loadPicture(" + history.id + "); return false;'>"
                                    + history.createDate + "</a></li>");
        })
    });
}

/* 過去の絵を履歴に表示する */
function loadPicture(id){
    showMessage("保存された絵の情報を取得中です...");
    $.ajax({
        type: 'GET',
        url: 'initstrokes/' + id,
        cache: false,
        dataType: 'json',
        success: initializedAsSaved,
        error: function(XMLHttpRequest, status, errorThrown){
            showMessage("保存された絵の情報の取得に失敗しました。");
        },
        complete: function(){}
    });
}

/* 過去の絵を取得する */
function initializedAsSaved(data, status, xhr){
    historycontext.clearRect(0, 0, 640, 400);
    $.each(data, function(i, strokePoints){
        drawStroke(historycontext, JSON.parse(strokePoints));
    });

    $("#mycanvas").hide();
    $('#historycanvas').show();
    showMessage("過去の絵を読み込みました。");
}



/* 接続用トークンを取得する */
function getToken () {
    /* clientIdの作成 */
    var name = $("#name").val();
    var status = $("#status").val();
    if (name == "") {
        showMessage("名前が入力されていません。");
        return;
    }
    clientId = name + "@" + status;


    /* 接続用トークンの取得 */
    showMessage("接続用のトークンを取得しています...");
    $.ajax({
        type: "GET",
        url: "http://" + window.location.host + "/gettoken",
        data: {clientId: clientId},
        cache: false,
        dataType: "text",
        success: connect,
        error: function(XMLHttpRequest, status, errorThrown){
            showMessage("トークンの取得に失敗しました。");
        }
    });
}


/* トークンを使ってチャネルサービスに接続する */
function connect(token){
    showMessage("接続中です...");

    var channel = new goog.appengine.Channel(token);
    var handlers = {
        'onopen': connected,
        'onmessage': onMessage,
        'onerror': function(){ showMessage("接続できませんでした。"); }
    }

    var socket = channel.open(handlers);
}

/* チャネルサービスへの接続が完了した */
function connected(){

    /* 初期データを投入するには、ここをコメントアウトやめる */
    /*
    $("#connect").attr("disabled", "disabled");
    showCurrent();
    showMessage("接続しました。");
    return
    */

    showMessage("現在の絵の情報を取得中です...");
    $.ajax({
        type: 'GET',
        url: 'initstrokes',
        cache: false,
        dataType: 'json',
        success: initialized,
        error: function(XMLHttpRequest, status, errorThrown) {
            showMessage("現在の絵の情報の取得に失敗しました。");
        },
        complete: function(){}
    });
}

/* 現在の絵の情報を取得した */
function initialized(data,status, xhr){
    showMessage("絵を描いています");
    if (data) {
        $.each(data, function(i, strokePoints){
            drawStroke(mycontext, JSON.parse(strokePoints));
        });
    };

    $("#connect").attr("disabled", "disabled");
    showCurrent();
    showMessage("接続しました。");
}


/* 新しい絵を描く */
function newPicture(){
    $.post("/newpicture");
}


/* チャネルサービスからデータが送信された */
function onMessage(message){
    var command = JSON.parse(message.data);
    if (command.name == "addstroke"){
        addStroke(command);
    }
    else if (command.name == "newpicture"){
        reload(command);
    }
}

/* 新しい絵が作成されたリロードする */
function reload(command){
    location.reload(true);
}

/* 送信された描画情報で、描画する */
function addStroke(command){
    strokePoints = JSON.parse(command.content);
    showMessage(strokePoints);
    drawStroke(mycontext, strokePoints);
}

/* 与えられた描画情報を描画する */
function drawStroke(context, strokePoints){
    context.beginPath();
    context.moveTo(strokePoints[0].x, strokePoints[0].y);

    for(i = 1; i < strokePoints.length; i++){
        context.lineTo(strokePoints[i].x, strokePoints[i].y);
    }

    context.stroke();
    context.closePath();
}


/* 最新のキャンバスを表示する */
function showCurrent(){
    $("#mycanvas").show();
    $("#historycanvas").hide();
}


/* キャンバスに絵を描く */
var mode;
var mycontext;
var historycontext;
var points;

/* ブラウザの違いを考慮して、canvas上の座標を取得する */
function getPoint(e){
    var x = e.clientX;
    var y = e.clientY;
    var rect = e.target.getBoundingClientRect();
    x = Math.floor(x - rect.left);
    y = Math.floor(y - rect.top);
    return { x:x, y:y };
}

/* canvasタグを描画する関数を定義する */
$(window).load(function(){
    mode = 0;

    /* 用意するキャンバスは2次元用で、太さ4の赤い線とする */
    mycontext = document.getElementById("mycanvas").getContext("2d");
    mycontext.strokeStyle = "rgba(255, 0, 0, 1)";
    mycontext.lineWidth = 4;

    $("#mycanvas")
        .mousedown(mouseDownHandler)
        .mousemove(mouseMoveHandler)
        .mouseup(mouseUpOrOutHandler)
        .mouseout(mouseUpOrOutHandler)
    ;

    /* 用意する履歴キャンバスは2次元用で、太さ4の灰色の線とする */
    historycontext = document.getElementById("historycanvas").getContext("2d");
    historycontext.strokeStyle = "rgba(64, 64, 64, 1)";
    historycontext.lineWidth = 4;
});


/* マウスボタンが押された時の処理 */
function mouseDownHandler(e){
    mode = 1;
    var point = getPoint(e);
    points = new Array(point);
    mycontext.beginPath();
}

/* マウスを動かした時の処理 */
function mouseMoveHandler(e){
    if (mode < 1) { return; }

    oldPoint = points.pop();
    points.push(oldPoint);

    var newPoint = getPoint(e);
    points.push(newPoint);

    mycontext.moveTo(oldPoint.x, oldPoint.y);
    mycontext.lineTo(newPoint.x, newPoint.y);
    mycontext.stroke();
}

/* マウスが放された、あるいは、マウスカーソルがキャンバスをはみ出した時の処理 */
function mouseUpOrOutHandler(e){
    if (mode < 1) { return; }

    mycontext.closePath();
    mode = 0;

    /* 描画情報をサーバーに送信する */
    var stringPoints = JSON.stringify(points);
    /* 以下で調べると、stringが返ってくる
    showMessage(typeof arrayPoints); */
    $.ajax({
        type: "POST",
        url: "/addstroke",
        data: {"clientId": clientId,
               "stroke": stringPoints
           }
    });
}