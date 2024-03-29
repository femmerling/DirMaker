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

  $("#directory_id").change(function(){
    if($("#directory_id").val() === "NewDir"){
      $("#new-dir").show();
    }
  });

	$('#process_items').click(function(){
		$('#notify-message').html('<b>please wait</b><br/>we are uploading your data to the server');
		$('#notify').show();
		$('#spotlight').show();
		heads_json = [];
		rows_json = [];
		root_id = $('#directory_id').val();
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
    var new_root;
    var data_items;
    if ($('#name').val() !== ""){
      new_root = $('#name').val();
    }
    if (root_id === "NewDir"){
      data_items = JSON.stringify({rows:rows_json,head:heads_json,root_name:new_root,root_id:null});
    }else{
      data_items = JSON.stringify({rows:rows_json,head:heads_json,root_name:null,root_id:root_id});
    }
    data_items = 
		$.ajax({
			url:"/process",
			type:"POST",
			data:data_items,
			contentType: 'application/json',
			success: function(data){
				$('#notify-message').html('<b>success</b><br/>all data uploaded successfully<br/><br/><input type="submit" id="success-button" onClick="window.location=\'/\'" value="ok thanks"/>');
			}
		});
	});
});
