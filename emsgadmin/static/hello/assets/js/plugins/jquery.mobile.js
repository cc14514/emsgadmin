// JavaScript Document
$(document).on("pagecreate","#demo-page",function(){
	$(document).on("swipeleft swiperight","#demo-page",function(e){
		if($(".ui-page-active").jqmDate("panel") !=="open"){
			if(e.type==="swipeleft"){
				$("#right-panel").panel("open");
			}
			else if(e.type==="swiperight"){
				$("#left-panel").panel("open");
			}
		}
	});
});