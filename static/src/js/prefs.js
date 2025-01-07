document.addEventListener("DOMContentLoaded", e => {
  let form = document.getElementById("prefsForm");
  console.log(form);
  form.addEventListener("submit", submit);
});

function submit(e) {
    e.preventDefault();
    fetch("/update-prefs", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"state": e.target.state.value})
    }).then(response => {
        let messageBox = document.getElementById("messageBox");
        if (response.status == 200) {
            messageBox.innerHTML = "<p class='mt-4 text-lg'>Updated preferences</p>"
        } else {
            messageBox.innerHTML = "<p class='tmt-4 text-red-600 text-lg'>Something went wrong</p>"
        }
    });
}