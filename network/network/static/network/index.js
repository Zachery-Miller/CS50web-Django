document.addEventListener('DOMContentLoaded', function() {
    console.log("Page has loaded")

    // add onsubmit handler to new post form
    const myElement = document.getElementById('create-post');

    if (myElement) {
        myElement.onsubmit = create_post;
    }
    else {
        console.log("Cannot add onsubmit handler to form as form does not appear in DOM.");
    }

    // by default load posts and clear new post field
    load_posts('all-posts');

});

function create_post () {
    // get form values
    const content = document.querySelector('#post-content').value;

    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
          load_posts('all-posts');
      });

    return false;
}

function load_posts(page) {
    // make sure contents box is empty on reload of all posts
    const myElement = document.getElementById('post-content');

    if (myElement) {
        myElement.value = "";
    }
    else {
        console.log("Cannot clear content of form as form does not appear in DOM.");
    }

    // empty all posts div
    document.querySelector(`#${page}`).innerHTML = "";
    console.log("cleared div");

    // call api
    fetch(`/show_posts/${page}`)
    .then(response => response.json())
    .then(posts => {

        posts.forEach(post => {
            // create parent div for post
            const postDiv = document.createElement('div');
            postDiv.classList.add('post');

            // create child div and element for poster
            const posterDiv = document.createElement('div');
            const posterStrong = document.createElement('strong');

            posterDiv.appendChild(posterStrong);
            posterStrong.innerHTML = post["poster"];
            postDiv.appendChild(posterDiv);

            // create child div and element for content
            const contentDiv = document.createElement('div');
            const contentStrong = document.createElement('strong');

            contentDiv.appendChild(contentStrong);
            contentStrong.innerHTML = post["content"];
            postDiv.appendChild(contentDiv);

            // create child div and element for timestamp
            const timestampDiv = document.createElement('div');
            const timestampStrong = document.createElement('strong');

            timestampDiv.appendChild(timestampStrong);
            timestampStrong.innerHTML = post["timestamp"];
            postDiv.appendChild(timestampDiv);

            // create child div and element for likes
            const likesDiv = document.createElement('div');
            const likesStrong = document.createElement('strong');

            likesDiv.appendChild(likesStrong);
            likesStrong.innerHTML = `Likes: ${post["likes"]}`;
            postDiv.appendChild(likesDiv);

            // add post to posts view
            document.querySelector(`#${page}`).append(postDiv);

            console.log(post);
        })
    });
}