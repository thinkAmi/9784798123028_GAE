$(function() {
    $("#regist").click(function(){
        
        /* 位置情報取得用のオブジェクトを取得する */
        try{
            var geo = navigator.geolocation;
        }
        catch(e){
            /* nop */
            alert("オブジェクトがありません");
            return;
        }
        
        if (geo == null){
            alert("この端末では位置情報が取得できません");
            return;
        }
        
        
        /* 位置情報を取得する */
        var count = 0;
        
        // 精度の低い方
        // 精度の高い方ではどうしても取得できないところもあるので、こちらもコメントアウトで残しておく
        /*
        var watchId = geo.getCurrentPosition(function(position){

            $("#lat").val(position.coords.latitude);
            $("#lng").val(position.coords.longitude);
            
            $("form").submit()
            
            return;
        */
        
        // 精度の高い方
        var watchId = geo.watchPosition(function(position){
            if(position.coords.accuracy < 300){
                geo.clearWatch(watchId);
                $("#lat").val(position.coords.latitude);
                $("#lng").val(position.coords.longitude);
                
                // p218で追加：jQueryによるフォームの送信
                $("form").submit()
                
                return;
            }
            
            if (count++ > 5){
                geo.clearWatch(watchId);
                alert("位置情報の精度が低いため、失敗しました");
                return;
            }
        
        }, function(e) {
            geo.clearWatch(watchId);
            alert("位置情報の取得に失敗しました");
        }, {
            enableHighAccuracy : true
        });
    });
    
    
    
    /* 地図表示ボタンがクリックされた */
    $("#map").click(function(){
        var href = "/map";
        var tag = $("#tag").val();
        
        if (tag != ""){
            href += ("?tag=" + encodeURIComponent(tag));
        }
        
        location.href = href;
        
    });
        
});