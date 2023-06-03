document.addEventListener("DOMContentLoaded", (e) => {
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
    });
}