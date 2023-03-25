function checkExp() {
	// $('.showmsg').remove();
	var str=document.getElementById("username").value;
	mobileExp=/^[0-9]{11}$/
	emailExp = /[a-z0-9]*@[a-z0-9]*\.[a-z0-9]+/gi
	if (mobileExp.test(str) || emailExp.test(str)) {
		return true;
	}
	else {
		alert("手机号或邮箱格式不正确！");
		// $('#message').innerHTML="手机号或邮箱格式不正确！";
		return false;
	}
}

function checkpwdlen(){
	
	var password = document.getElementById("password").value;
	var str = password;
	if(str.length < 8)
	{
		// var showmsg2 = document.getElementById("msg2");
		alert("密码长度不能小于8位！");
		// showmsg2.innerHTML = "密码长度不能小于8位！"
	}
}

function checkpwd(){
	var password = document.getElementById("password").value;
	var password1 = document.getElementById("password1").value;
	if(password1 != password)
	{
		alert("两次输入密码不一致！");
	}
}

function recheck(){
	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;
	var password1 = document.getElementById("password1").value;
	if( username == "" || password == "" || password1 == "")
	{
		alert("用户名或密码不能为空！");
	}
	else{
		$('.showmsg').remove();
		$.ajax({
			url:'/user/register/',
			type:'POST',
			data:$('#reform').serialize(),
			dataType:"JSON",
			success:function(data){
				// alert(data.msg);
				// location.href = "/user/"
				if(data.flag == "0"){
					var msg = document.getElementById("showmsg");
					// msg.className = "showmsg";
					// msg.innerHTML="邮箱或手机号已存在！";
					alert("邮箱或手机号已存在！")
				}
				else{
					alert("注册成功！")
				}
			}
		})
		
	}
}