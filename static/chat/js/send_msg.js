function send_msg() {
    console.log('yee')
    let socket = new WebSocket('ws://127.0.0.1:9090');
    socket.onopen = (event) => {
        let msg_field = document.getElementById("message-field");
        msg_field.get

        socket.send('Heeey');
    }
    socket.onmessage = (event) => {
        console.log(event.data)
    }

    socket.onopen = function(e) {
        console.log("[open] Соединение установлено");
        console.log("Отправляем данные на сервер");
        let info = {hello: "world"};
        let json = JSON.stringify(info);
        console.log(json);
        socket.send(json);
      };
      
    socket.onmessage = function(event) {
    console.log(`[message] Данные получены с сервера: ${event.data}`);
    };
    
    socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`);
    } else {
        // например, сервер убил процесс или сеть недоступна
        // обычно в этом случае event.code 1006
        console.log('[close] Соединение прервано');
    }
    };
    
    socket.onerror = function(error) {
    console.log(`[error] ${error.message}`);
    };
};

// send_msg()