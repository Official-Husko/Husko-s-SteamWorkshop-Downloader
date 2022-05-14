// const button = document.querySelector("button"),
//     toast = document.querySelector(".toast");
// const closeIcon = document.querySelector(".close"),
//     progress = document.querySelector(".progress");

// let timer1, timer2;

// button.addEventListener("click", () => {
//     toast.classList.add("active");
//     progress.classList.add("active");

//     timer1 = setTimeout(() => {
//         toast.classList.remove("active");
//     }, 5000); //1s = 1000 milliseconds

//     timer2 = setTimeout(() => {
//         toast.classList.add("active");
//         progress.classList.remove("active");
//     }, 5300);
// });

// closeIcon.addEventListener("click", () => {
//     toast.classList.remove("active");

//     setTimeout(() => {
//         progress.classList.remove("active");
//     }, 300);

//     clearTimeout(timer1);
//     clearTimeout(timer2);
// });




// Works

const closeBtn = document.getElementById('close-btn');
const toast = document.getElementById("toast");

closeBtn.addEventListener('click', () => {
    toast.parentNode.removeChild(toast);
});

setTimeout(function() {
    toast.parentNode.removeChild(toast);
}, 5000);





// setTimeout(function() {
//     let text = document.getElementById("txt-hide");
//     text.parentNode.removeChild(text);
// }, 2000);

// setTimeout(function() {
//     let text1 = document.getElementById("txt-hide-2");
//     text1.parentNode.removeChild(text1);
// }, 2000);






// $("button").click(function() {
//     $('.alert').addClass("show");
//     $('.alert').removeClass("hide");
//     $('.alert').addClass("showAlert");

//   setTimeout(function() {
//     $('.alert').removeClass("show");
//     $('.alert').addClass("hide");
//   },5000);

// });

// $('.close-btn').click( function() {
//     $('.alert').removeClass("show");
//     $('.alert').addClass("hide");
// });