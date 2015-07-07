// JavaScript Document
$(document).ready(function(e) {
	/*
	var myLinks = document.getElementsByTagName('a');
	for(var i = 0; i < myLinks.length; i++){
	　　myLinks[i].addEventListener('touchstart', function(){this.className = "hover";}, false);
	　　myLinks[i].addEventListener('touchend', function(){this.className = "";}, false);
	}*/


	//Login, Regist, Edit Password
	$("#form-resetpw").hide();//默认隐藏忘记密码操作
	$("#form-regist").hide();//默认隐藏注册操作
	$("#forgetpw").click(function() {
		$("#form-login").hide();
		$("#form-resetpw").show();        
    });//点击”忘记密码“到注册页
	$("#haspwlogin").click(function() {
		$("#form-resetpw").hide();
		$("#form-login").show();        
    });//点击”已获取到新密码“到登录页
	$("#toregist").click(function() {
		$("#form-login").hide();
		$("#form-regist").show();        
    });//点击”立即加入“到注册页
	$("#hasnamelogin").click(function() {
		$("#form-regist").hide(); 
		$("#form-login").show();       
    });//点击”已有账户“到登录页
	
	//快速导航
	$(".submenu").hide();	
	$("#submenu").on("tap",function(){ 
		$(".submenu").toggle(); 
	});
	
});