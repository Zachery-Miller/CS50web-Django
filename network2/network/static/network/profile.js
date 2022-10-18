document.addEventListener('DOMContentLoaded', function() {
    set_button_visibilty();

    document.getElementById('follow-form').addEventListener('submit', follow);
    document.getElementById('unfollow-form').addEventListener('submit', unfollow);
});

function set_button_visibilty() {
// get profile user whose page you are viewing
    const profile_user = document.querySelector('#profile-user').textContent

// get request if active user is following profile user and display appropriate button

    fetch(`/check_follow/${profile_user}`)
    .then(response => response.json())
    .then(following => {
        if (following["following"] === true) {
            document.querySelector('#follow-form').style.display = 'none';
            document.querySelector('#unfollow-form').style.display = 'block';
        }
        else {
            document.querySelector('#follow-form').style.display = 'block';
            document.querySelector('#unfollow-form').style.display = 'none';
        }
})

}

function follow(e) {
    // prevent page reload on form submit
    e.preventDefault();

    // get profile user whose page you are viewing
    const profile_user = document.querySelector('#profile-user').textContent;
    
    //get csrf token from cookie
    const csrftoken = getCookie('csrftoken');

    fetch(`/profile/${profile_user}/follow`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
    })
    .catch(error => {
        console.error(error);
    });

    // adjust button display
    document.querySelector('#follow-form').style.display = 'none';
    document.querySelector('#unfollow-form').style.display = 'block';
}

function unfollow(e) {
    e.preventDefault();

    // get profile user whose page you are viewing
    const profile_user = document.querySelector('#profile-user').textContent;

    //get csrf token from cookie
    const csrftoken = getCookie('csrftoken');

    fetch(`/profile/${profile_user}/unfollow`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
    })
    .catch(error => {
        console.error(error);
    });

    // adjust button display
    document.querySelector('#follow-form').style.display = 'block';
    document.querySelector('#unfollow-form').style.display = 'none';
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