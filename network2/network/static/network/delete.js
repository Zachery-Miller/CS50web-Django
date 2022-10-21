document.addEventListener('DOMContentLoaded', function() {
    getDeletes()
});

function getDeletes() {
    const deletes = document.querySelectorAll(".delete-icon")
    
    for (let i=0; i <deletes.length; i++) {
        deletes[i].addEventListener("click", () => deletePost(parseInt(deletes[i].dataset.id)))
    }
}

function deletePost(post_id) {
    console.log("clicked")

    // get csrf token
    const csrftoken = getCookie('csrftoken');

    // delete from db
    fetch(`/delete_post/${post_id}`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => response.json())
    .then(message => {
        console.log(message["message"])
    })

    // remove from DOM
    post = document.querySelector(`#post-card-div-${post_id}`)
    post.remove();

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