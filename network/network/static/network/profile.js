document.addEventListener('DOMContentLoaded', function() {
    console.log("Page has loaded.")
    
    // get current user
    const user_username = JSON.parse(document.getElementById('user_username').textContent);
    console.log(`Active user: ${user_username}`);

    // get profile user
    const profile_user_username = JSON.parse(document.getElementById('profile_user_username').textContent);
    console.log(`Profile user: ${profile_user_username}`);

    // call function if not active user looking at their own profile
    if (user_username === profile_user_username) {
        console.log("User looking at their own profile.")
    }
    else {
        load_follow_buttons(profile_user_username);
    }; 
});

function load_follow_buttons(profile_user) {
    // fetch follow information via GET
    fetch(`/check_following/${profile_user}`)
    .then(response => response.json())
    .then(follow => {

        // get follow/unfollow buttons
        const follow_button = document.querySelector('#follow-button');
        const unfollow_button = document.querySelector('#unfollow-button');

        // add event listener
        follow_button.addEventListener('click', () => follow_fxn(profile_user));
        unfollow_button.addEventListener('click', () => unfollow_fxn(profile_user));

        // load buttons based on following or unfollowing condition
        if (follow["following"] === true) {
            follow_button.style.display = 'none';
            unfollow_button.style.display = 'block';
        }
        else {
            follow_button.style.display = 'block';
            unfollow_button.style.display = 'none';
        }       
    });

};

async function follow_fxn(profile_user) {
    console.log("Clicked follow.");

    await fetch(`/profile/${profile_user}/toggle_follow`, {
        method: 'POST',
        body: JSON.stringify({
            profile_user: profile_user,
            toggle: "follow"
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result)
          console.log("Followed user.");
  
      });
      return false;
};

async function unfollow_fxn(profile_user) {
    console.log("Clicked unfollow.");

    await fetch(`/profile/${profile_user}/toggle_follow`, {
        method: 'POST',
        body: JSON.stringify({
            profile_user: profile_user,
            toggle: "unfollow"
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result)
          console.log("Unfollowed user.");
  
      });
      return false;
};
