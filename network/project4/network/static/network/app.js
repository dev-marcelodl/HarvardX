let user_auth = "";

document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#item_all_posts').addEventListener('click', () => load_posts()); 
    if (document.querySelector('#item_following_posts') !== null)
        document.querySelector('#item_following_posts').addEventListener('click', () => load_following_posts());     
    if (document.querySelector('#item_profile') !== null)
        document.querySelector('#item_profile').addEventListener('click', () => load_profile(""));    
    if (document.querySelector('#btn_post') !== null)
        document.querySelector('#btn_post').addEventListener('click',  () => new_post());
    load_posts();
    
});

function new_post() {

  let vcontent = document.querySelector('#post-content').value;

  document.querySelector('#post-content').value = '';

  if (vcontent.length <= 0)
  {
    Swal.fire("Enter the post content");
    return;
  }

  fetch('/posts', {
    method: 'POST',
    body: JSON.stringify({
        content: vcontent
    })
  })
  .then(response => response.json())
  .then(result => {
      if(result.hasOwnProperty('error')){
        Swal.fire({
          icon: 'error',         
          text: result.error
        })
      }
      else
      {
        Swal.fire({
          icon: 'success',        
          text: result.message
        })
        load_posts("");
      }
  }); 

}

function nav_view(page, func, user_profile)
{
  
  document.querySelector('#nav-view').style.display = 'block';
  document.querySelector('#nav-view').innerHTML = "";
   
  const div = document.createElement('div');

  div.setAttribute("data-iden",page.page);

  if (page.has_previous)   
      div.innerHTML += ' <button style="margin:2px;" class="btn btn-primary" style="padding: 0px; margin:0px;" id="btn_next" data-page="'+(page.current-1)+'" >Previous</button>';      
  
  if (page.has_next)
  {
      div.innerHTML += ' <button style="margin:2px;" class="btn btn-primary" style="padding: 0px; margin:0px;" id="btn_next" data-page="'+(page.current+1)+'" >Next</button>';    
  }
           
  document.querySelector('#nav-view').append(div);  

  document.querySelectorAll('#btn_next').forEach(button => {
    button.onclick = function() {        
      page = this.dataset.page;  

      if (func=="load_posts")
         load_posts(page);             
      else if (func=="load_following_posts")
         load_following_posts(page);        
      else if (func=="load_profile")
         load_profile(user_profile, page);       
    }}); 
}

function load_posts(page) {
  
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#profile-info').style.display = 'none';   
    document.querySelector('#posts-view').innerHTML = "";

    let url = '/posts';

    if (page != null)
    {
      url = '/posts?page='+page;
    }

    fetch(url)
    .then(response => response.json())
    .then(json_result => {
        if (json_result.length <= 0)
        {
          document.querySelector('#posts-view').innerHTML += '<br><br><h5 style="margin:30px; color: blue">No one has posted anything yet.<h5>';
        }
        else
        {     
          user_auth = json_result.user_auth;                               
          json_result.posts.forEach(add_view_post);
          nav_view(json_result.page,'load_posts');
        }
    });
  
  }

  function load_following_posts(page) {
  
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#profile-info').style.display = 'none';   
    document.querySelector('#posts-view').innerHTML = "";

    let url = '/following_posts';

    if (page != null)
    {
      url = '/following_posts?page='+page;
    }

    fetch(url)
    .then(response => response.json())
    .then(json_result => {
        if (json_result.length <= 0)
        {
          document.querySelector('#posts-view').innerHTML += '<br><br><h5 style="margin:30px; color: blue">No one has posted anything yet.<h5>';
        }
        else
        {    
          user_auth = json_result.user_auth;    
          json_result.posts.forEach(add_view_post);
          nav_view(json_result.page,'load_following_posts');
        }
    });
  
  }
  
  function load_profile(user_profile, page) {
  
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#posts-view').innerHTML = "";
    document.querySelector('#profile-info').style.display = 'none'; 
    document.querySelector('#new-post').style.display = 'none';     

    let url = '/profile/'+user_profile;

    if (page != null)
    {
      url = '/profile/'+user_profile+'?page='+page;
    }

    fetch(url)
    .then(response => response.json())
    .then(json_result => { 
        if (json_result.length <= 0)
        {
          document.querySelector('#posts-view').innerHTML += '<br><br><h5 style="margin:30px; color: blue">No one has posted anything yet.<h5>';
        }
        else
        {    
          user_auth =json_result.user_auth;    
          json_result.posts.forEach(add_view_post);
          add_view_profile_info(json_result.profile[0]);
          nav_view(json_result.page,'load_profile',user_profile);
        }
    });
      
  }

  function add_view_profile_info(profile) {

    document.querySelector('#profile-info').style.display = 'block';
    document.querySelector('#profile-info').innerHTML = "";
   
    const div_profile = document.createElement('div');
    //'<div class="card flex-row">'+profile.count_followers + "-" +profile.count_following+

    let html = '<div class="card flex-row" style="background-color:white" >'+
     '<img style="width:148px; height: 128px; padding: 5px; margin:20px"  src="'+profile.picture+'" alt="Picture"  />'+
     '<div class="card-body">'+     
      '  <h4 style="font-weight: bold; color:blue">'+profile.username+'</h6>'+
      '  <p style="font-weight: bold">Followers: '+profile.count_followers+'</p>'+
      '  <p style="font-weight: bold">Following: '+profile.count_following+'</p>';     

    if ((user_auth.length > 0) && (profile.username != user_auth)) {
      if(profile.followers.indexOf(user_auth) !== -1) 
         html += ' <button class="btn btn-primary" style="padding: 5px; margin:0px;" id="btn_follow" data-iden="'+profile.username+'" data-setfollow="N">Unfollow</button>';          
      else
         html += ' <button class="btn btn-primary" style="padding: 5px; margin:0px;" id="btn_follow" data-iden="'+profile.username+'" data-setfollow="Y">Follow</button>';           
    }
    html +=  '</div></div>'+
      '</div><p>'  

    div_profile.innerHTML = html;
           
    document.querySelector('#profile-info').append(div_profile);

    document.querySelectorAll('#btn_follow').forEach(button => {
      button.onclick = function() {        
        user_profile = this.dataset.iden;
        setfollow = this.dataset.setfollow;

        fetch('/follow/'+user_profile, {
          method: 'PUT',
          body: JSON.stringify({
              follow: setfollow
          })
        }).then(response => {  
    
            setTimeout(function() {
              load_profile(user_profile);
            }, 200);
        });                
     }}); 
 
 };

  function add_view_post(post) {
  
    const div_post = document.createElement('div');

    div_post.setAttribute("data-iden",post.id);
    html = '<div class="card flex-row">'+
    ' <img style="width:64px; height: 48px; padding: 5px; margin:20px"  src="'+post.picture+'" alt="Picture"  />'+
    '<div class="card-body" data-iden="'+post.id+'">'+     
     '  <h6 style="font-weight: bold" id="user_profile" data-iden="'+post.username+'">'+post.username+'</h6>'+
     '  <p style="margin-top: -10px; font-size:12px; color: grey;">'+post.created+'</p>'+
     '  <p id="content_'+post.id+'">'+post.content+'</p>'+
     '  <i class="glyphicon glyphicon-heart" style="color:blue" id="user_like_'+post.id+'" >_'+post.count_likes+'</i>';
    if (user_auth.length > 0) {
      if(post.likes.indexOf(user_auth) !== -1) 
         html += '  <h6 style="font-weight: bold; color:blue" id="user_like" data-iden="'+post.id+'" data-like="N">UnLike</h6>';
      else
         html += '  <h6 style="font-weight: bold; color:blue" id="user_like" data-iden="'+post.id+'" data-like="Y">Like</h6>';

      if(post.username == user_auth)
         html += '  <h6 style="font-weight: bold; color:blue" id="edit_post" data-iden="'+post.id+'">Edit</h6>';
   
    }
     
     html += '</div>'+
     '</div><p>'; 

    div_post.innerHTML = html;
     
    document.querySelector('#posts-view').append(div_post);

    document.querySelectorAll('#user_profile').forEach(button => {
    button.onclick = function() {        
      user_profile = this.dataset.iden;  
      load_profile(user_profile);             
    }}); 

    document.querySelectorAll('#user_like').forEach(button => {
      button.onclick = function() {        
        post_id = this.dataset.iden; 
        setlike = this.dataset.like; 

        fetch('/like/'+post_id, {
          method: 'PUT',
          body: JSON.stringify({
              like: setlike
          })
        })
        .then(response => response.json())
        .then(json_result => {
            document.querySelector('#user_like_'+post_id).innerHTML = "_"+json_result.count_likes;
            if (setlike == "Y")
            {
              this.innerHTML = "UnLike";
              this.setAttribute("data-like","N");
            }
            else
            {
              this.innerHTML = "Like" 
              this.setAttribute("data-like","Y");
            }
        });
      }; 
    });

    document.querySelectorAll('#edit_post').forEach(button => {
      button.onclick = function() {        
        post_id = this.dataset.iden; 
        if (this.innerHTML == "Edit")
        {
          this.innerHTML = "Save";
          document.querySelector('#content_'+post_id).innerHTML = '<textarea style="width:100%; height:5px; overflow: auto; min-height: 5em; resize: none;" TextMode="MultiLine" id="edit_content_'+post_id+'" >'+document.querySelector('#content_'+post_id).innerHTML+'</textarea>';
        }
        else
        {
              
          data_save = document.querySelector('#edit_content_'+post_id).value;

          fetch('/edit_post/'+post_id, {
            method: 'POST',
            body: JSON.stringify({
                content: data_save
            })
          })
          .then(response => {
            this.innerHTML = "Edit";
            
            document.querySelector('#content_'+post_id).innerHTML = "";
            document.querySelector('#content_'+post_id).innerHTML = data_save;
          });
         
        }
      }      
      
    });
   
 
 };
  