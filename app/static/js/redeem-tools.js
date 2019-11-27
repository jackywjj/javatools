$(document).ready(function () {
	var startNumber = startRedeemCodeNumber;
	for (i = 0; i < redeemCodeBatch; i++) {
		$('#from_redeem_code_number_'+i).val(startNumber);
		step = parseInt($('#redeem_code_amount_'+i).val());
		endNumber = startNumber + step - 1;
		startNumber = startNumber + step;
		$('#to_redeem_code_number_'+i).val(endNumber);
	}

	$('.amountClass').change(function(){
		redeemIndex = parseInt($(this).attr("element_index"));
		var startNumber = parseInt($('#from_redeem_code_number_'+redeemIndex).val());
		for (i = redeemIndex; i < redeemCodeBatch; i++) {
			$('#from_redeem_code_number_'+i).val(startNumber);
			step = parseInt($('#redeem_code_amount_'+i).val());
			endNumber = startNumber + step - 1;
			startNumber = startNumber + step;
			$('#to_redeem_code_number_'+i).val(endNumber);
		}
	});

	$('#createRedeem').click(function(){
		var start_redeem_code_number = $('#start_redeem_code_number').val();
		var redeem_code_amount = $('#redeem_code_amount').val();
		window.location.href = "/redeem/?start_redeem_code_number=" + start_redeem_code_number + "&redeem_code_amount=" + redeem_code_amount;
	});

	$('.province-class').change(function(){
		redeemIndex = parseInt($(this).attr("element_index"));
		var province_code = $(this).val();
		$.ajax({
			url:"/system/city",
			method:"get",
			data:"province_code="+province_code,
			success:function(data){
				var jsonData = JSON.parse(data);
				var cities = jsonData.cities;
				$('#city_'+redeemIndex).empty();
				$('#city_'+redeemIndex).append("<option value=''>城市</option>")
				for (index in cities) {
					var city_code = cities[index].city_code;
					var city_name = cities[index].city_name;
					$('#city_'+redeemIndex).append("<option value='"+city_code+"'>"+city_name+"</option>");
				}
				$('#agent_'+redeemIndex).empty();
				$('#agent_'+redeemIndex).append("<option value=''>代理商</option>")
			}
		});

		var grade_code = $("#grade_"+redeemIndex).val();
		var province_code = $("#province_"+redeemIndex).val();
		var city_code = $("#city_"+redeemIndex).val();
		$.ajax({
			url:"/system/agent",
			method:"get",
			data:"grade_code="+grade_code+"&province_code="+province_code+"&city_code="+city_code,
			success:function(data){
				var jsonData = JSON.parse(data);
				var agents = jsonData.agents;
				$('#agent_'+redeemIndex).empty();
				$('#agent_'+redeemIndex).append("<option value=''>代理商</option>")
				for (index in agents) {
					var id = agents[index].id;
					var agent_title = agents[index].agent_title;
					$('#agent_'+redeemIndex).append("<option value='"+id+"'>"+agent_title+"</option>");
				}
			}
		});
	});

	$('.agent-class').change(function() {
		redeemIndex = parseInt($(this).attr("element_index"));
		var grade_code = $("#grade_"+redeemIndex).val();
		var province_code = $("#province_"+redeemIndex).val();
		var city_code = $("#city_"+redeemIndex).val();
		$.ajax({
			url:"/system/agent",
			method:"get",
			data:"grade_code="+grade_code+"&province_code="+province_code+"&city_code="+city_code,
			success:function(data){
				var jsonData = JSON.parse(data);
				var agents = jsonData.agents;
				$('#agent_'+redeemIndex).empty();
				$('#agent_'+redeemIndex).append("<option value=''>代理商</option>")
				for (index in agents) {
					var id = agents[index].id;
					var agent_title = agents[index].agent_title;
					$('#agent_'+redeemIndex).append("<option value='"+id+"'>"+agent_title+"</option>");
				}
			}
		});
	});
})