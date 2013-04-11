$(document).ready(function(){
	$('#delete-link').click(function(e){
		e.preventDefault();
		url = $(e.currentTarget).data('url');
		callback = $(e.currentTarget).data('callback');
		$.ajax({
			url:url,
			type:'DELETE',
			success: function(data){
				location.href = callback;
			}
		});
	});

	$('#submit-put').click(function(e){
		e.preventDefault();
		url = $("#url").val();
		console.log(url)
		formData = $('#edit-form').serializeArray(); 
		$.ajax({
			url:url,
			type:'PUT',
			data:$('#edit-form').serializeArray(),
			success: function(data){
				location.href = url;
			}
		});
	});

	$('#process_items').click(function(){
		heads_json = [];
		rows_json = [];
		root_id = $('#directory_id').val()
		total_col = parseInt($("#col-count").val());
		total_row = parseInt($("#row-count").val());
		i = 0;
		while(i < total_col){
			heads_json.push($("#head-"+i).val());
			i++;
		}
		x = 0;
		while(x < total_row){
			y = 0;
			row_data={}
			while(y<total_col){
				col_data = $("#"+x+"-"+y).data("value");
				row_data[y] = col_data;
				y++;
			}
			rows_json.push(row_data);
			x++;
		}
		$.ajax({
			url:"/process",
			type:"POST",
			data:JSON.stringify({"rows":rows_json,head:heads_json,root_id:root_id}),
			contentType: 'application/json',
			success: function(data){
				alert("all data uploaded!");
				window.location = "/";
			}
		});
	});
});