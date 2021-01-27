function check() {
    if (checkdescription()) {
        alert("Add a new event successfully!")
        return true
    } else {
        alert("Description can not be none!")
        return false
    }

}

function checkdescription() {
    let t = document.getElementById("event")
    let text = t.value;

    if (text == "" || text == null) {
        return false
    } else {
        return true
    }
}