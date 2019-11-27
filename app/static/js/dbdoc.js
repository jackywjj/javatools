/**
 * Created by jacky on 19/04/26.
 */
$(document).ready(function () {
	$('#table_prefix').on('change', function () {
		var table_prefix = $(this).val();
		window.location.href = "/dbdoc?table_prefix=" + table_prefix;
	});
	$('#generateContent').on('click', function () {
		var table_prefix = $('#table_prefix').val();
		if (table_prefix == '') {
			alert('Please choose table prefix.');
			$('#table_prefix').focus();
			return false;
		}
		$.ajax({
			url:"/dbdoc/content",
			method:"get",
			data:"table_prefix="+table_prefix,
			success:function(data){
				var jsonData = JSON.parse(data);
				var contentHtml = jsonData.contentHtml;
				$('#doc_content').html(contentHtml);
			}
		});
	});
	$('#generateTableContent').on('click', function () {
		var table_prefix = $('#table_prefix').val();
		var table_name = $('#table_name').val();
		if (table_prefix == '') {
			alert('Please choose table prefix.');
			$('#table_prefix').focus();
			return false;
		}
		if (table_name == '') {
			alert('Please choose table name.');
			$('#table_name').focus();
			return false;
		}
		$.ajax({
			url:"/dbdoc/table",
			method:"get",
			data:"table_prefix="+table_prefix +"&table_name="+table_name,
			success:function(data){
				var jsonData = JSON.parse(data);
				var contentHtml = jsonData.contentHtml;
				$('#doc_table').html(contentHtml);
			}
		});
	});
	$('#generateAllTableContent').on('click', function () {
		var table_prefix = $('#table_prefix').val();
		if (table_prefix == '') {
			alert('Please choose table prefix.');
			$('#table_prefix').focus();
			return false;
		}
		$.ajax({
			url:"/dbdoc/table/all",
			method:"get",
			data:"table_prefix="+table_prefix,
			success:function(data){
				var jsonData = JSON.parse(data);
				var contentHtml = jsonData.contentHtml;
				var contentHtmlSrc =  jsonData.contentHtmlSrc;
				$('#doc_table_all').html(contentHtml);
				$('#content_hidden').val(contentHtmlSrc);
			}
		});
	});
	$('#clearContent').on('click', function () {
		$('#doc_content').html("");
		$('#doc_table').html("");
		$('#doc_table_all').html("");
		$('#content_hidden').val("");
	});
	$('#copyToClipBoard').on('click', function () {
		$('#content_hidden').select();

		if (document.queryCommandSupported("copy")) {
			document.execCommand("copy");
			alert("复制完成。")
		}
	});
});