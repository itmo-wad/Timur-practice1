let scrollbot = () => {
    let scrollableEl = document.querySelector(".chat-thread");
    let maxScroll = scrollableEl.scrollTopMax;
    scrollableEl.scrollTo(0, maxScroll);
}

document.addEventListener("load", scrollbot());

document.querySelector("#eraseBtn").onclick = () => {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/erase', true);
    let secret_value = "secret_param=sainou";
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(secret_value)
    xhr.onload = function() {
        document.querySelector("ul").innerHTML = "";
    }
}

document.querySelector('#message').addEventListener('keypress', function (e) {
    // e.preventDefault();
    if (e.key === 'Enter') {
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/send', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        let message = document.querySelector("#message").value;
        xhr.send(JSON.stringify({"message":message}))
        xhr.onload = function() {
            let jsonchik = JSON.parse(this.responseText);
            console.log(jsonchik)
            if (this.status != 200 || jsonchik.error) {
                alert(this.responseText)
                return
            }
            botiq_message = jsonchik.result;
            let user_message_li = document.createElement("li");
            user_message_li.innerText = message;
            let ul = document.querySelector("ul");
            ul.append(user_message_li);
            let botiq_message_li = document.createElement("li");
            botiq_message_li.innerText = botiq_message;
            ul.append(botiq_message_li);
            scrollbot();

            document.querySelector("#message").value = "";
        }
    }
});
