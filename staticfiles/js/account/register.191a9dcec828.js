console.log('hello');
const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector(".invalid-feedback");
const usernameSuccess = document.querySelector(".usernameSuccess");



const registerForm = document.querySelector("#regform");


const firstArea = document.querySelector(".invalid-feedback");



const emailField = document.querySelector('#emailField');
const emailFeedback = document.querySelector(".emailFeedback");
const emailSuccess = document.querySelector(".emailSuccess");

// const showPasswdToggle = document.querySelector(".showPasswdToggle");
const password1Field = document.querySelector("#password1Field");
const password2Field = document.querySelector("#password2Field");

const signup = document.querySelector(".signup");

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = 'none';
    usernameSuccess.textContent = `Checking ${usernameVal}`;
    usernameSuccess.style.display = 'block';
    if (usernameVal.length > 0) {
        fetch('/account/validate-username', {
            body: JSON.stringify({ 'username': usernameVal }),
            method: 'POST'
        }).then(res => res.json()).then(data => {
            usernameSuccess.style.display = 'none';
            if (data.username_error) {
                signup.disabled = true;
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = 'block';
                feedbackArea.innerHTML = `<p class="danger">${data.username_error}</p>`;
            } else {
                signup.disabled = false;
            }

        });

    }


});



emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedback.style.display = 'none';
    emailSuccess.textContent = `Checking ${emailVal}`;
    emailSuccess.style.display = 'block';
    if (emailVal.length > 0) {
        fetch("/account/validate-email", {
            body: JSON.stringify({ "email": emailVal }),
            method: "POST",
        }).then(res => res.json()).then((data) => {
            console.log("data", data);
            emailSuccess.style.display = 'none';
            if (data.email_error) {
                signup.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedback.style.display = 'block';
                emailFeedback.innerHTML = `<p class="danger">${data.email_error}</p>`;
            } else {
                signup.disabled = false;
            }
        });
    }
});




// const handleToggle = (e) => {
//     if (showPasswdToggle.textContent == 'SHOW') {
//         showPasswdToggle.textContent = 'HIDE';
//         password1Field.setAttribute("type", "password")

//     } else {
//         showPasswdToggle.textContent = 'SHOW';
//         password1Field.setAttribute("type", "text")

//     }
// }

// showPasswdToggle.addEventListener('click', handleToggle); 

