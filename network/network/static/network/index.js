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
    load_posts();

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
      });

      load_posts();
      return false;
}

function load_posts() {
    // make sure contents box is empty on reload of all posts
    const myElement = document.getElementById('post-content');

    if (myElement) {
        myElement.value = "";
    }
    else {
        console.log("Cannot clear content of form as form does not appear in DOM.");
    }
}