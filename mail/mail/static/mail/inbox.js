document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // get request users inbox and display emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    emails.forEach(email => {
      // create parent div
      const preview = document.createElement('div');
      preview.classList.add('email-preview');
      if (email.read === false) {
        preview.classList.add('email-unread')
      }
      else {
        preview.classList.add('email-read')
      }

      // create child element for sender
      const sender = document.createElement('strong');
      sender.innerHTML = email["sender"];
      sender.classList.add('email-preview-sender');
      preview.appendChild(sender);
      
      // create child element for subject
      const subject = document.createElement('strong');
      subject.innerHTML = email["subject"];
      subject.classList.add('email-preview-subject');
      preview.appendChild(subject);

      // create child element for timestamp
      const timestamp = document.createElement('strong');
      timestamp.innerHTML = email["timestamp"];
      timestamp.classList.add('email-preview-timestamp');
      preview.appendChild(timestamp);

      // if clicked read email
      preview.addEventListener('click', function(){ read_email(email); });

      // add email to emails view
      document.querySelector('#emails-view').append(preview);
    })
  })
  }

  function send_email() {
    // get values from form
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);

        // Load sent mailbox
        load_mailbox('sent');
    });
    return false;
  }

  function read_email(email) {
    // Show read view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#read-view').style.display = 'block';

    // default open mail name
    document.querySelector('#read-view').innerHTML = `<h3>Now reading...</h3>`;

    // mark as read
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
    // add catch

    // create display for email info
    const sender = document.createElement('small');
    sender.innerHTML = `from: ${email.sender}`

    const recipients = document.createElement('small');
    recipients.innerHTML = `to: ${email.recipients}`

    const subject = document.createElement('h4');
    subject.innerHTML = `${email.subject}`

    const timestamp = document.createElement('small');
    timestamp.innerHTML = `${email.timestamp}`
    timestamp.id = "email-timestamp";

    const body = document.createElement('div');
    body.innerHTML = `${email.body}`

    const pagebreak = document.createElement('hr');

    const subjectdiv = document.createElement('div');
    subjectdiv.id = "email-subject";
    subjectdiv.appendChild(subject);

    const upperdiv = document.createElement('div');
    upperdiv.appendChild(sender);
    upperdiv.appendChild(timestamp);

    const lowerdiv = document.createElement('div');
    lowerdiv.appendChild(recipients);

    // add display info to read-view
    document.querySelector('#read-view').append(subjectdiv, upperdiv, lowerdiv, pagebreak, body);

    console.log(`The id of this email is ${email.id}`);
  }