// ==UserScript==
// @name         BaoMiTong Course - One-click course rating
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  A one-click-rating feature to rate courses on BaoMiTong
// @author       q8f13
// @match        http://online.edu-bm.com/classModule/video/*
// ==/UserScript==

function main() {
	$(document).ready(changeCommentBtn);
}
function changeCommentBtn() {
	// get the first game in list
	var btn = $('a.addBtn');
	// unshift the discount one
	// var discountList = $('div.discount_prices').closest('div.wishlistRow');
	// first.before(discountList);
	// // highlight them
	// discountList.css('border', '3px solid #4c6b22');

    function dummy(){
        alert("dummy");
    }

    $(".addBtn").click(function(){
		dummy();
	});

    $('li.exercise').after('<input type="button" id="dummy" value="Dummy" class="btn self-btn bg s_btn" style="background-color:grey;" />');

    $('#dummy').click(function(){
        // dummy();
        instant_comment();
    });

    function inject_auto_comment(){
        var txt = txt.replace('var historyId = $(".zjplaying").attr("stsid");')
        return 'var historyId = $(".zjplaying").attr("stsid"); alert("replaced");';
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function updateStatus(status){
		var historyId = $(".zjplaying").attr("stsid");
		$.ajax({
			url: rootPath + "/userHistory/updateStatus",
			type:"post",
			data:{"id":historyId,"studyStatus":status},
			dataType:"json",
			success:function(data){
				if(data.msg == "success"){
					if(status == 3){
						studyStatus = true;
						$(".zjplaying").attr("ststatus",status);
						$(".studyOk").data("status",1);
						$(".learning").css("background-image","url('" + rootPath + "/stylesheets/video/img/shi.png')");
						$(".study.zjplaying").find(".constant_width div:eq(0)").attr("class","zj_time_full");
						debugger
                        window.opener.changeLidStatus($("#lecId").val())
					}else{
						$(".zjplaying").attr("ststatus",status);
						$(".studyOk").data("status",0);
						$(".learning").css("background-image","url('" + rootPath + "/stylesheets/video/img/kong.png')");
						$(".study.zjplaying").find(".constant_width div:eq(0)").attr("class","zj_time_half");
					}
				}else if(data.msg == "notlogin"){

				}else{
					$('<div class="c-fa">'+ data.msg +'</div>').appendTo('body').fadeIn(100).delay(1000).fadeOut(200,function(){
						$(this).remove();});
				}
			}
		});

        dummy();
	}

    function instant_comment(){
        var comment = $.trim($("#textInfor").val());
		if(!comment){
			comment = '此用户未发布评论内容~';
		}
		var lecId = $("#comment").attr("data-id");
		var teacherId = $("#teacherId").val();
		var id = $(".myping").data("id");

		var arrayIds = '',arrayScore = '';
		var scoreCount = 0;
		var starsLength = $(".clickStars").length;
		for(var i = 0;i < starsLength;i++){
			var ids = $(".clickStars span").eq(i).attr("id");
			var score = $(".clickStars").eq(i).find("i.active").length;
			arrayIds += ids+',';
			arrayScore += score+',';
			scoreCount += score;
		}

        arrayScore = '5,5,5,5,5,5,5,5,';
		scoreCount = 40;
        // alert(arrayScore);
        // alert(scoreCount);

		if(scoreCount == 0){
			$.msg("请针对课程评分")
			return;
		}
		var hideUser = $(".niMing i").hasClass('active') == true ? 1:0;

		if(res != null){
			res.abort();
		}

		res = $.ajax({
			url:rootPath + "/video/addComment",
			type:"post",
			async: false,
			data:{"id":id,"delFlag":0
				,"videoChapterId":$("#chapterId").val()
				,"source":$("#videoId").val()
				,"arrayIds":arrayIds
				,"arrayScore":arrayScore
				,"hideUser":hideUser
				,"comment":comment,"videoLectureId":lecId
				,"teacherId":teacherId,"classTypeId":$("#classTypeId").val()
				,"commid":$("#comId").val()},
			dataType:"json",
			success:function(data) {
				if(data.msg == "success"){
					$("#commentContent").val("");
					$(".pingFenBox,.textBox").slideUp(200);
					$(".myping p").html(data.commentStr);
					$(".myping i").html(data.lickreateTime);
					$(".myping").data("id", data.id);
					$(".myping").slideDown(200);
					$(".ping .num").html("140/140");
				}else{
					$('<div class="c-fa">'+ data.msg +'</div>').appendTo('body').fadeIn(100).delay(2000).fadeOut(200,function(){
						$(this).remove();});
				}
				var scorehtml = '';
				var score = getnum((scoreCount == 0 ? 0 :scoreCount/starsLength));
				var scoreMath = score.toString().split(".");
				if(score >= 0 && score < 1){
					scorehtml += '<span>';
					if(scoreMath[1] == "1"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "2"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 6px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "3"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 7px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "4"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 8px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "5"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 9px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "6"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 10px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "7"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 11px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "8"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 12px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "9"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else{
						scorehtml += '<i class="noChose"></i> ';
					}
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i> ';
					scorehtml += ' </span>';
				}else if(score >= 1 && score < 2){
					scorehtml += '<span>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml += '</i>';
					if(scoreMath[1] == "1"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "2"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 6px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "3"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 7px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "4"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 8px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "5"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 9px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "6"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 10px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "7"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 11px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "8"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 12px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "9"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else{
						scorehtml += '<i class="noChose"></i> ';
					}
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i> ';
					scorehtml += ' </span>';
				}else if(score >= 2 && score < 3){
					scorehtml += '<span>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					if(scoreMath[1] == "1"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "2"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 6px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "3"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 7px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "4"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 8px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "5"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 9px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "6"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 10px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "7"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 11px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "8"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 12px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "9"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else{
						scorehtml += '<i class="noChose"></i> ';
					}
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i> ';
					scorehtml += ' </span>';
				}else if(score >= 3 && score < 4){
					scorehtml += '<span>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml += '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml += '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml += '</i>';
					if(scoreMath[1] == "1"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "2"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 6px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "3"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 7px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "4"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 8px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "5"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 9px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "6"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 10px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "7"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 11px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "8"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 12px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "9"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else{
						scorehtml += '<i class="noChose"></i> ';
					}
					scorehtml += '<i class="noChose"></i> ';
					scorehtml += ' </span>';
				}else if(score >= 4 && score < 5){
					scorehtml += '<span>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					if(scoreMath[1] == "1"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "2"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 6px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "3"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 7px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "4"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 8px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "5"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 9px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "6"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 10px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "7"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 11px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "8"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 12px;"></i>';
						scorehtml += '</i>';
					}else if(scoreMath[1] == "9"){
						scorehtml += '<i class="noChose">';
						scorehtml += '<i class="nochoseStar" style="width: 5px;"></i>';
						scorehtml += '</i>';
					}else{
						scorehtml += '<i class="noChose"></i> ';
					}
					scorehtml += ' </span>';
				}else if(score >= 5){
					scorehtml += '<span>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += '<i class="noChose">';
					scorehtml += '<i class="nochoseStar"></i>';
					scorehtml +=  '</i>';
					scorehtml += ' </span>';
				}else {
					scorehtml += '<span>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += '<i class="noChose"></i>';
					scorehtml += ' </span>';
				}
			$(".myping .students-star").html(scorehtml);
			}
		});
    }

	
}
main();
