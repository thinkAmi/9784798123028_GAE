var map;
var lastDate;
var markersArray = [];
var tid;

/* HTMLが読み込まれたら実行される関数を準備する */
$(function(){
    /* 名古屋駅を示す位置オブジェクトを作成 */
    var latlng = new google.maps.LatLng(35.170914, 136.882052);
    
    /* 倍率、中心位置、地図の種類(ROADMAP)をオプションとして用意する */
    var myOptions = {
        zoom : 16,
        center : latlng,
        mapTypeId : google.maps.MapTypeId.ROADMAP
    };
    
    
    /* 地図オブジェクトを <div id="map"> の中に作成する */
    map = new google.maps.Map(document.getElementById("map"), myOptions);
    
    
    /* p238-239にて追加 */
    /* 位置情報の一覧を取得する */
    refresh();
    
    
    /* タグ名で検索ボタンを押下した時の処理 */
    $("#search").click(function(){
    
        if (tid != null) {
            clearTimeout(tid);
        }
        
        $('#places').empty();
        
        for (i in markersArray){
            markersArray[i].setMap(null);
        }
        
        markerArray = [];
        lastDate = null;
        refresh();
    });
});



function refresh(){
    var data = {};
    if (lastDate != null){
        /* 前回更新日付があれば、その値を渡す */
        data.lastDate = lastDate;
    }
    
    data.tag = $('#tag').val();
    
    /* サーバーと通信する処理を登録する */
    $.ajax({
        type : 'GET',
        url : '/placesjson',
        data : data,
        cache : false,
        dataType : 'json',
        success : function(json) {
            /* 通信に成功した */
            /* 何もしないと日付の昇順になるため、reverse()で降順にする */
            $.each(json.reverse(), function(i, place){
                addMarker(place);
            });
            
            dd = new Date()
            /* getMonth()は 0-11 */
            lastDate = (dd.getFullYear() + "-" + paddingZero(dd.getMonth() + 1) + "-" + paddingZero(dd.getDate()) + " " + paddingZero(dd.getHours()) + ":" + paddingZero(dd.getMinutes()) + ":" + paddingZero(dd.getSeconds()));
        },
        error: function(xml, status, error){
        },
        
        complete : function () {
            /* 通信が終了した */
            
            tid = setTimeout(refresh, 10000);
        }
    });

}



function addMarker(place){
    /* マーカーを追加する */
    var myLatLng = new google.maps.LatLng(place.lat, place.lng);
    
    var marker = new google.maps.Marker({
        map: map,
        position: myLatLng
    });
    
    
    markersArray.push(marker);
    
    

    /* 位置情報を追加する */
    div = $('<div class="place">'
        + '<a class="nickname" href="">nickname</a>'
        + '<span class="message">message</span>'
        + '<div class="elapseTime"><span>elapseTime</span>'
        + ' <a href="#" onclick="javascript:deleteMarker(' + place.entityID + ');">削除</a></div>'
        + '</div>'
        );
        
    $('a.nickname', div).attr('href',
                              'javascript:setCenter(' + place.lat + ',' + place.lng + ');')
                        .text(place.nickname);
                              
    $('span.message', div).text(place.message);
    $('div.elapseTime span', div).text(place.elapseTime);
    $('#places').prepend(div);
    
    
    /* マーカーを地図の中心に移動する */
    setCenter(place.lat, place.lng);

}


/* マーカーを削除する */
function deleteMarker(entityID) {
    var data = {};
    data.entityID = entityID;
    $.ajax({
        type : 'GET',
        url : '/delete',
        data : data,
        cache : false,
        complete : function() {
            /* 削除されたら画面を再描画する */
            window.location.reload();
        }
    });
}



/* 地図の中心を移動する */
function setCenter(lat, lng){
    map.setCenter(new google.maps.LatLng(lat, lng));
}



/*  targetが一桁の場合、先頭にゼロを一つパディングする */
function paddingZero(target){
    if(target < 10){
        return "0" + target;
    }
    else{
        return target;
    }
}
