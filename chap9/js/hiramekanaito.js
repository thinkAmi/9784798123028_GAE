var sid; // ヒントを開くタイマー用の変数
var seq; // ヒントを開く順番を保存する変数

/* 画面が表示されたら実行される関数 */
$(function() {
    stop();
    makeSeq();
    sid = setInterval(openHint, 4500);
    $("#answerbutton").click(answer);
    $("#answerinput").keypress(function(e) {
        if (e.which == 13)
            answer();
    });
    $("#nextbutton").click(function() {
        location.href = "http://" + location.host + "/index";
    });
    $("#twitterbutton").click(tweet);
});

/* ヒントが開く処理を停止する */
function stop() {
    if (!sid) {
        clearInterval(sid);
        sid = null;
    }
}

/* 16個のヒントをランダムに開く順序を作成する */
function makeSeq() {
    seq = new Array(16);
    var workSeq = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ];
    for ( var i = 0; i < 16; i++) {
        var j = Math.floor(Math.random() * workSeq.length);
        seq[i] = workSeq[j];
        workSeq.splice(j, 1);
    }
}

/* ヒントを1枚開く */
function openHint() {
    if (seq.length <= 0) {
        openAnswer();
    }
    var index = seq[0];
    seq.splice(0, 1);
    $("#" + index + "_close").toggle(false);
    $("#" + index + "_open").toggle(true);
}

/* 入力された解答の確認を行なう。一部があっていれば正解とする */
function answer() {
    var answerinput = $("input#answerinput").val().toUpperCase();
    var answertext = $("input#answertext").val().toUpperCase();
    var answerfurigana = $("input#answerfurigana").val().toUpperCase();
    if ((answertext.indexOf(answerinput) >= 0 && answertext.length <= answerinput.length * 2)
            || (answerfurigana.indexOf(answerinput) >= 0 && answerfurigana.length <= answerinput.length * 2)) {
        openAnswer();
        return;
    }
    $("#message").html($("#message").html() + "X");
}

/* 答えを表示する */
function openAnswer() {
    stop();
    $("table#hints").toggle(false);
    $("table#answer").toggle(true);
    $("input#nextbutton").toggle(true);
    $("input#twitterbutton").toggle(true);
}

/* 問題をtwitterに投稿する画面を開く */
function tweet() {
    var id = $("#id").val();
    // 注：書籍のリストに対して、ハッシュタグを追加しました
    window.open(encodeURI("http://twitter.com/?status=")
            + encodeURI("http://" + location.host + "/index/" + id + " ")
            + encodeURIComponent("#hiramekanaito"));
}
