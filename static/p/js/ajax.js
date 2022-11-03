/** javascript **/


// 태깅버튼 비동기 ajax
$(function() {

	$('#tag_btn').click(function() {

		var form = $('#tagging')[0];
		var data = new FormData(form);
		data.append("testFile",$('#testFile').files);
		data.append("filename", $('#testFileNm').text());

		// ajax로 데이터 전송
		$.ajax({
			url: "/tagging/", // ajax로 데이터 교환할 페이지 주소
			processData : false,
			contentType : false,
			method: "POST",
			data: data,
			success: function(data){ //로직 성공시
				$(".tagging").fadeOut();
				$(".modal").fadeOut();

				$("#tag_box").hide();
				$("#download_box").show();
				$("#testFileNm").html(data.filename);
				$("#new_file_name").val(data.filename);
			},
			error: function(data){ //로직 실패시

                var html = "<button type='button' class='btn_Close' onclick='popClose2()'></button><p></p><span>message</span>";
                error_log = html.replace("message", data.responseJSON.error);
                console.log(data.responseJSON.error);
                $(".tagging").html(error_log);
                $(".tagging").fadeIn();
                $(".modal").fadeIn();

			},
			beforeSend: function () { //로딩화면
                var html = "<button type='button' class='btn_Close' onclick='popClose2()'></button><p></p><span>message</span>";
                tagging_message = html.replace("message", "카테고리 태깅중 입니다. <br> 태깅이 완료될 때 까지 현재 창을 유지해 주세요.");
                $(".tagging").html(tagging_message);
				$(".tagging").fadeIn();
				$(".modal").fadeIn();
			},

		});
	});
});