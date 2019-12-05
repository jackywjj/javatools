$(document).ready(function () {
	$('#generateJson').click(function(){
		var javacode = $("#javacode").val();
		$.ajax({
			url:"/json/generate/json",
			method:"post",
			data:"javacode="+javacode,
			success:function(data){
				
				var jsonObj = JSON.parse(data);
				var jsonPretty = JSON.stringify(jsonObj, null, '\t');

				$("pre").text(jsonPretty);
			}
		});
	});
})