let message_timeout = document.getElementById("message-timer");

setTimeout(function()
{

    message_timeout.style.display = "none";

}, 3000);


const toastTrigger = document.getElementById('liveToastBtn');
const toastLiveExample = document.getElementById('liveToast');

if (toastTrigger) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    toastTrigger.addEventListener('click', () => {
    toastBootstrap.show();
    });
}


