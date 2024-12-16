document.getElementById("mpesa-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const responseMessage = document.getElementById("response-message");

    fetch("{% url 'subscribe' %}", {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            responseMessage.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        } else {
            responseMessage.innerHTML = `<div class="alert alert-success">Transaction successful: ${JSON.stringify(data)}</div>`;
        }
    })
    .catch(error => {
        responseMessage.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
    });
});