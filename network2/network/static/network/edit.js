document.addEventListener('DOMContentLoaded', function() {
    getPencils()
});

function getPencils() {
    const pencils = document.querySelectorAll(".pencil")
    
    for (let i=0; i <pencils.length; i++) {
        pencils[i].addEventListener("click", () => showForm(parseInt(pencils[i].dataset.id)))
    }
}

function showForm(post_id) {
    console.log(post_id)

    // when clicked, get post content, hide content div and show textarea div & prepopulate text box with post content
    post_content = document.querySelector(`#post-content-${post_id}`).innerHTML;
    document.querySelector(`#textarea-${post_id}`).innerHTML = post_content;

    document.querySelector(`#post-content-div-${post_id}`).style.display = 'none';
    document.querySelector(`#edit-content-div-${post_id}`).style.display = 'block';

    // add event listener on save edits button and submit post req
    document.querySelector(`#save-edit-btn-${post_id}`).addEventListener('click', () => {
        // get edited content
        new_content = document.querySelector(`#textarea-${post_id}`).value;

        // get csrf token
        const csrftoken = getCookie('csrftoken');
        
        // submit post to db
        fetch(`/edit_post/${post_id}`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                new_content: new_content
            })
        })
        .then(response => response.json())
        .then(message => {
            console.log(message["message"])
        })

        // reset js and update post content
        document.querySelector(`#post-content-${post_id}`).innerHTML = new_content;
        document.querySelector(`#post-content-div-${post_id}`).style.display = 'block';
        document.querySelector(`#edit-content-div-${post_id}`).style.display = 'none';
    });

    // add event listener on cancel edits button
    document.querySelector(`#cancel-edit-btn-${post_id}`).addEventListener('click', () => {

        document.querySelector(`#textarea-${post_id}`).value = post_content;
        document.querySelector(`#post-content-div-${post_id}`).style.display = 'block';
        document.querySelector(`#edit-content-div-${post_id}`).style.display = 'none';

    });

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}