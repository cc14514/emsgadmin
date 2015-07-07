// JavaScript Document
/* Popup
=====================================================================================*/	
var popHtml = $(
		'<div data-role="popup" data-overlay-theme="b" data-dismissible="true" style="min-width:200px; min-height:30px; padding:15px;">'+
		'<a href="#" data-rel="back" class="ui-btn ui-corner-all ui-icon-delete ui-btn-icon-notext ui-btn-right">'+'</a>'+
		'<p>'+'</p>'+
		'</div>'
		)
		
	 $('body [data-role="page"]').append(popHtml);
	 	popHtml.trigger("create");
		popHtml.popup();
		
/* Loader
=====================================================================================*/	
	
$(document).on("click",".show-page-loading-msg",function() {
			var $this = $( this ),
				theme = $this.jqmData( "theme" ) || $.mobile.loader.prototype.options.theme,
				msgText = $this.jqmData( "msgtext" ) || $.mobile.loader.prototype.options.text,
				textVisible = $this.jqmData( "textvisible" ) || $.mobile.loader.prototype.options.textVisible,
				textonly = !!$this.jqmData( "textonly" );
				html = $this.jqmData( "html" ) || "";
			$.mobile.loading("show", {
					text: msgText,
					textVisible: textVisible,
					theme: theme,
					textonly: textonly,
					html: html
			});
		})
		.on("click",".hide-page-loading-msg",function() {
			$.mobile.loading("hide");
		});
	
function myAlert(msg){
	popHtml.popup("open");
	popHtml.children("p").text(msg)
}

