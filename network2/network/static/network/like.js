document.addEventListener('DOMContentLoaded', function() {
    getHearts()
    
    // preload class sets all animation durations to 0s so no animations run on page load, after 0.3s animations can run
    setTimeout(() => {
        document.body.classList.remove("preload")
    },300)
});

function getHearts() {
    const hearts = document.querySelectorAll(".heart")
    
    for (let i=0; i <hearts.length; i++) {
        hearts[i].style.animationPlayState = 'paused';
        hearts[i].addEventListener("click", () => submitForm(parseInt(hearts[i].dataset.id)))
    }
}

function submitForm(post_id) {
    // get csrf token
    const csrftoken = getCookie('csrftoken');

    // get like count
    let like_count = parseInt(document.querySelector(`#like-count-${post_id}`).innerHTML);
    
    // submit post request to server to toggle like status on post
    fetch(`/toggle_like/${post_id}`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => response.json())
    .then(message => {
        if (message["message"] === "Like removed") {
            // decrease number of likes
            like_count -= 1;
            document.querySelector(`#like-count-${post_id}`).innerHTML = like_count;

            // edit button display and animation playstate
            like_button = document.querySelector(`#liked-${post_id}`)
            like_button.classList.remove("fa-heart")
            like_button.classList.add("fa-heart-o")
            like_button.style = "font-size:24px";

            // animation
            like_button.animationPlayState = 'running';

            // then repause
            like_button.animationPlayState = 'paused';

            console.log(message);
        }
        else if (message["message"] === "Like created") {
            // increase number of likes
            like_count += 1;
            document.querySelector(`#like-count-${post_id}`).innerHTML = like_count;

            // edit button display
            like_button = document.querySelector(`#liked-${post_id}`)
            like_button.classList.remove("fa-heart-o")
            like_button.classList.add("fa-heart")
            like_button.style = "font-size:24px;color:red";

            // animation
            like_button.animationPlayState = 'running';

            // then repause
            like_button.animationPlayState = 'paused';

            console.log(message);
        }
        else {
            console.error("Invalid message response from server.")
        }
        
    })
    .catch(error => {
        console.error(error);
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