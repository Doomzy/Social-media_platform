(function() {
	var card = document.querySelector(".signupForm");
	[].slice.apply( document.querySelectorAll('[data-action="flip"]') ).forEach(function(el) {
		el.addEventListener("click", function(evt) {
			evt.preventDefault();
			card.classList.toggle("active");
		});
	});
})();

function editUser(user){
	profile= document.getElementById('about-tab');
	profileInfo= profile.querySelector('.profileInfo');
	editProfileInfo= profile.querySelector('.editProfileInfo');
	if (profileInfo.classList.contains('hidden')){
		profileInfo.classList.remove('hidden');
		editProfileInfo.classList.add('hidden');
	}
	else{
		editProfileInfo.classList.remove('hidden')
		profileInfo.classList.add('hidden')
	}
}

function editPost(id){
	post= document.getElementById('post'+id);
	var editForm= post.querySelector(".postEditForm");
	var postContent= post.querySelector(".postContent");
	if (editForm.classList.contains('hidden')){
		editForm.classList.remove('hidden');
		postContent.classList.add('hidden');
	}
	else{
		postContent.classList.remove('hidden')
		editForm.classList.add('hidden')
	}
}

function editComm(id){
	comment= document.getElementById(id);
	var editForm= comment.querySelector(".commEditForm");
	var commtContent= comment.querySelector(".commContent");
	if (editForm.classList.contains('hidden')){
		editForm.classList.remove('hidden');
		commtContent.classList.add('hidden');
	}
	else{
		commtContent.classList.remove('hidden')
		editForm.classList.add('hidden')
	}
}

function pgpURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$('#img_pgp').css('background-image','url('+e.target.result+')');
		};
		reader.readAsDataURL(input.files[0]);
	}
}

function pfpURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$('#img_pfp').css('background-image','url('+e.target.result+')');
		};
		reader.readAsDataURL(input.files[0]);
	}
}

$('#userSearch').keyup(function(){
	var searchName= $(this).val()
	$.ajax({
		url: "/account/ajax-search/",
		dataType: 'json',
		data:{
			'searchKey': searchName
		},
        success: function (data) {
			if(searchName== ''){
				$('#found').remove()
				$('#notFound').remove()
				$('#userSearchMenu').prepend(`
					<div id="notFound" style="text-align: center; color: #fff001;">
						<h4>Enter a valid username/Name</h4>
					</div>
				`)
			}
          	else {
				$('#notFound').remove()
				$('#found').remove()
				$('#userSearchMenu').prepend(
					`<div id="found">`
					+data.html+
					`</div>`
					)	
          	}
    	}	
	})
})

$("[id^=like]").click(function(){
	var pId= $(this).data('postid');
	var Method= $(this).data('method');
	var Token= $(this).data('token');

	$.ajax({
		url:"/posts/ajax-ctrls/",
		type:'post',
		dataType: 'json',
		headers: { "X-CSRFToken": Token },
		data:{
			'postId':pId,
			'method':Method,
		},
		success: function (data) {
			if (data.status =='liked'){
				$("#like"+data.post+"").addClass("btnNo1");
				$("#like"+data.post+"").removeClass("btnNo2");
				$("#like"+data.post+"").data('method','unlike');

				var count= +$("#likesCount"+data.post+"").text()+1
				$("#likesCount"+data.post+"").text(count);
						}
			if (data.status =='unliked'){
				$("#like"+data.post+"").removeClass("btnNo1");
				$("#like"+data.post+"").addClass("btnNo2");
				$("#like"+data.post+"").data('method','like');
				
				var count= +$("#likesCount"+data.post+"").text()-1
				$("#likesCount"+data.post+"").text(count);
			}
		},
		error: function () {
			alert('something went wrong!');
		}
	})	
})

$("[id^=comment]").click(function(){
	var pId= $(this).data('postid');
	var Method= $(this).data('method');
	var Token= $(this).data('token');
	var content= $("#commArea"+pId+"").val()
	
	$.ajax({
		url:"/posts/ajax-ctrls/",
		type:'post',
		dataType: 'json',
		headers: { "X-CSRFToken": Token },
		data:{
			'postId':pId,
			'method':Method,
			'contnet':content
		},
		success: function(data){
			$("#commList"+data.post+"").append(`
			<div id="commBody `+data.commId+`"> 
				<img class="smImg col-1" style="vertical-align: top; width: 40px; height: 40px;" src="`+data.imgUrl+`" alt="">
				<div class="comment mb-2 d-inline-block">
					<div class="dropdown float-end">
						<span class="align-center" type="button" id="dropdownPostOptn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							<i class="fa fa-ellipsis-h" style="font-size: 2rem;"></i>
						</span>	
						
						<div class="dropdown-menu dropdown-menu-left postEditMenu" aria-labelledby="dropdownPostOptn">
							<button onclick="editComm('commBody`+data.commId+`')" class="dropdown-item">Edit</button>
							<button id="cDel`+data.commId+`" data-token="{{ csrf_token }}" data-commid="`+data.commId+`" data-method="delete" class="dropdown-item" >Delete</button>
						</div>
					</div>
					<a class="profileLink" style="font-size: 1.6rem; " href="{% url 'userProfile:Profile' `+data.username+`%}">  `+data.fullname+` </a>
					<p id="commContent`+data.commId+`" class="mt-2 mx-3 commContent">
						`+content+`
					</p>
					<div class="mt-1 commEditForm hidden">
						<textarea class="commEditContent" maxlength="10000" name="content" id="id_content">`+content+`</textarea>
						<button class="mt-3 btn btnNo2" id="cEdit`+data.commId+`" data-token="{{ csrf_token }}" data-commid="`+data.commId+`" data-method="edit">Save</button>
						<button onclick="editComm('commBody`+data.commId+`')" class="mt-3 btn btnNo1" type="reset">Cancel</button>
					</div>
				</div>
				<br>
			</div>
			`);
			var count= +$("#commsCount"+data.post+"").text()+1
			$("#commsCount"+data.post+"").text(count);
		},
		error: function () {
			alert('something went wrong!');
		}
	})
})

$("[id^=cDel]").click(function(){
	var cId= $(this).data('commid');
	var Method= $(this).data('method');
	var Token= $(this).data('token');

	$.ajax({
		url:"/posts/ajax-ctrls/",
		type:'post',
		dataType: 'json',
		headers: { "X-CSRFToken": Token },
		data:{
			'commId':cId,
			'method':Method,
		},
		success:function(data){
			$('#commBody'+cId+'').remove()
			var count= +$("#commsCount"+data.post+"").text()-1
			$("#commsCount"+data.post+"").text(count);		
		},
		error: function () {
			alert('something went wrong!');
		}
	})
})

$("[id^=cEdit]").click(function(){
	var cId= $(this).data('commid');
	var Method= $(this).data('method');
	var content= $("#commEditArea"+cId+"").val()
	var Token= $(this).data('token');

	$.ajax({
		url:"/posts/ajax-ctrls/",
		type:'post',
		dataType: 'json',
		headers: { "X-CSRFToken": Token },
		data:{
			'commId':cId,
			'content':content,
			'method':Method,
		},
		success:function(data){
			$("#commContent"+data.commId+"").text(data.content)
		},
		error: function () {
			alert('something went wrong!');
		}
	})
})

$("[id^=pDel]").click(function(){
	var pId= $(this).data('postid');
	var Method= $(this).data('method');
	var Token= $(this).data('token');

	$.ajax({
		url:"/posts/",
		type:'post',
		dataType: 'json',
		headers: { "X-CSRFToken": Token },
		data:{
			'postId':pId,
			'method':Method,
		},
		success:function(data){
			$('#post'+data.postId+'').remove()
		},
		error: function () {
			alert('something went wrong!');
		}
	})
})

$("[id^=pEdit]").click(function(){
	var pId= $(this).data('postid');
	var Method= $(this).data('method');
	var content= $("#postEditContent"+pId+"").val()
	var Token= $(this).data('token');

	$.ajax({
		url:"/posts/",
		type:'post',
		dataType: 'json',
		headers: { "X-CSRFToken": Token },
		data:{
			'postId':pId,
			'method':Method,
			'content':content,
			'noMedia':$("#noMedia"+pId+"").is(':checked'),
		},
		success:function(data){
			$("#postContent"+data.postId+"").text(data.content)
			if ($("#noMedia"+pId+"").is(':checked')){
				$("#postMedia"+data.postId+"").remove()
			}
		},
		error: function () {
			alert('something went wrong!');
		}
	})

})