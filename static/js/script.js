// Current Date

const dateElement = document.getElementById("currentDate");

if(dateElement){

    const today = new Date();

    dateElement.innerHTML =
    today.toLocaleDateString(
        "en-IN",
        {
            day:"numeric",
            month:"long",
            year:"numeric"
        }
    );
}