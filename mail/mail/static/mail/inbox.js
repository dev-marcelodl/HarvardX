let last_box = "";

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', new_email);
  document.querySelector('#btn_send_mail').addEventListener('click', send_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
  
});

function new_email() {

  compose_email(null)

}

function compose_email(id) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = ''; 

    if (id != null)
    {
      fetch('/emails/'+id)
      .then(response => response.json())
      .then(email => {
           document.querySelector('#compose-recipients').value = email.sender;
           if (email.subject.includes("Re:"))
              document.querySelector('#compose-subject').value = email.subject;
           else
              document.querySelector('#compose-subject').value = 'Re: '+email.subject;
           document.querySelector('#compose-body').value = '"On '+email.timestamp+' '+email.sender+' wrote: '+email.body+'"';
           
        }
      );
    }

}

function send_email() {

  let vrecipients = document.querySelector('#compose-recipients').value;  
  let vsubject = document.querySelector('#compose-subject').value; 
  let vbody = document.querySelector('#compose-body').value; 

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: vrecipients,
        subject: vsubject,
        body: vbody
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
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
        load_mailbox('sent');
      }
  });
  
}

function load_mailbox(mailbox) {
  last_box = mailbox;

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    if (emails.length <= 0)
    {
      document.querySelector('#emails-view').innerHTML += "<br><br><h5>Empty Mailbox<h5>";
    }
    else
    {
      emails.forEach(add_email_list);
    }
  });

}

function add_email_list(email) {

   // Create new post
   const div_mail = document.createElement('div');
   let bg_color = "";

   if (email.read)   
      bg_color = "bg-custom-1"

   div_mail.setAttribute("data-iden",email.id);
   div_mail.innerHTML = '<div class="card '+bg_color+'" style="width: 100%;">'+
    '<div class="card-body" data-iden="'+email.id+'">'+    
    '  <h7 class="card-subtitle mb-2 text-muted">'+email.timestamp+'</h7>'+
    '  <h6 class="card-text mb-2">From: '+email.sender+'</h6>'+
    '  <h6 class="card-subtitle mb-2">To: '+email.recipients+'</h6>'+
    '  <p class="card-text">Subject: '+email.subject+'</p>'+    
    '</div>'+
    '</div><p>' 
    div_mail.addEventListener('click', function() {      
      load_mail(this.dataset.iden);
  }); 
    
  document.querySelector('#emails-view').append(div_mail);

};

function load_mail(id) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = '';
  
  fetch('/emails/'+id)
  .then(response => response.json())
  .then(email => {
    // Print emails
    
    if (email.archived)
       text_archive = "Unarchive Mail";
    else
       text_archive = "Archive Mail";

    const div_mail = document.createElement('div');   

    div_mail.className = 'post';
    div_mail.innerHTML = '<div class="card" style="width: 100%;">'+
    '<div class="card-body">'+
    '  <h7 class="card-subtitle mb-2 text-muted">'+email.timestamp+'</h7>'+
    '  <h6 class="card-title">From: '+email.sender+'</h6>'+
    '  <h6 class="card-title">To: '+email.recipients+'</h6>'+
    '  <h6 class="card-subtitle mb-2 text-muted">Subject: '+email.subject+'</h6>'+
    '  <p class="card-body">'+email.body+'</p></div></div><p></p>';
    
    if (last_box != 'sent') {
      div_mail.innerHTML +=  '  <button id="btn_reply" data-iden="'+email.id+'">Reply Mail</button>';    
      div_mail.innerHTML +=  '  <button id="btn_archive" data-iden="'+email.id+'" data-archived="'+email.archived+'">'+text_archive+'</button>';    
    }

     document.querySelector('#emails-view').append(div_mail);

     document.querySelectorAll('#btn_archive').forEach(button => {
      button.onclick = function() {        
        id = this.dataset.iden;
        status_archived =  this.dataset.archived;

        if (status_archived=='true')
            set_archived = false;
        else
            set_archived = true; 

        fetch('/emails/'+id, {
          method: 'PUT',
          body: JSON.stringify({
              archived: set_archived
          })
        }).then(response => {         
            setTimeout(function() {
              load_mailbox('inbox');
            }, 200);
          });                
     }}); 

     document.querySelectorAll('#btn_reply').forEach(button => {
      button.onclick = function() {        
        id = this.dataset.iden;
        compose_email(id);               
     }}); 

  });

  fetch('/emails/'+id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  

}