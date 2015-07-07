function json2str(o) {
	var arr = [];
	var fmt = function(s) {
		 if (typeof s == 'object' && s != null) return json2str(s);
		return /^(string|number)$/.test(typeof s) ? '"' + s + '"' : s;
	}
	for (var i in o) arr.push('"' + i + '":' + fmt(o[i]));
	return '{' + arr.join(',') + '}';
}


//alert
function myAlert(msg,type){
	if(!type){
		type = 'success';
	}
	
	/*
	http://github.hubspot.com/messenger/
	message: The text of the message
	type: info, error or success are understood by the provided themes. You can also pass your own string, and that class will be added.
	theme: What theme class should be applied to the message? Defaults to the theme set for Messenger in general.
	id: A unique id. If supplied, only one message with that ID will be shown at a time.
	singleton: Hide the newer message if there is an id collision, as opposed to the older message.
	actions: Action links to put in the message, see the 'Actions' section on this page.
	hideAfter: Hide the message after the provided number of seconds
	hideOnNavigate: Hide the message if Backbone client-side navigation occurs
	showCloseButton: Should a close button be added to the message?
	closeButtonText: Specify the text the close button should use (default ×)
	 */
	Messenger().post({
		message: msg,
		type: type,
		hideAfter: 3,
		singleton: true,
 		showCloseButton: true
	});
}

$(function() {
	//alert config
	Messenger.options = {
	    extraClasses: 'messenger-fixed messenger-on-top',
	    theme: 'air'
	}
	
	//confirm config
	$.messager.model = {
		ok : {
			text : "确认",
			classed : 'btn-info'
		},
		cancel : {
			text : "取消",
			classed : 'btn-error'
		}
	};
	
});


var app = {};
/*
 * 为页面元素增加 disabled 属性.
 */
app.disabled = function(dom) {
	$(dom).attr({disabled: true});
	$(dom).addClass("disabled");
}

/*
 * 取消页面元素的 disabled 属性.
 */
app.enabled = function(dom) {
	$(dom).removeAttr("disabled");
	$(dom).removeClass("disabled");
}