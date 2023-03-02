/** javascript **/


$(function() {
    // data_table 쿼리문
    // 테이블의 Row 클릭시 값 가져오기

    $("#data_table_view tr").click(function(){
        var str = ""
        var tdArr = new Array();	// 배열 선언

        // 현재 클릭된 Row(<tr>)
        var tr = $(this);
        var td = tr.children();
        // tr.text()는 클릭된 Row 즉 tr에 있는 모든 값을 가져온다.

        // 반복문을 이용해서 배열에 값을 담아 사용할 수 도 있다.
        td.each(function(i){
            tdArr.push(td.eq(i).text());
        });

        // td.eq(index)를 통해 값을 가져올 수도 있다.
        var new_file_name = td.eq(2).text();

        $("#view_file_name").html(new_file_name);
        $("#new_file_name").val(new_file_name);
    });

    // pro_table 쿼리문
    // 테이블의 Row 클릭시 값 가져오기
    $("#pro_table_view tr").click(function(){

        var str = ""
        var tdArr = new Array();	// 배열 선언

        // 현재 클릭된 Row(<tr>)
        var tr = $(this);
        var td = tr.children();
        var arrNumber = new Array(0, 1, 5, 6, 7);
        // tr.text()는 클릭된 Row 즉 tr에 있는 모든 값을 가져온다.

        // 반복문을 이용해서 배열에 값을 담아 사용할 수 도 있다.
        td.each(function(i){
            if($.inArray(i, arrNumber) != -1){
                tdArr.push(td.eq(i).text());
            }
        });

        var modData = tdArr[0]+','+tdArr[1]+','+tdArr[2]+','+tdArr[3]+','+tdArr[4];
        $("#first_tag").html(tdArr[3]);
        $("#second_tag").html(tdArr[4]);
        $("#modData").val(modData);
        $("#data_modify").attr("disabled",false);
    });
});