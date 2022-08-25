function send_msg() {
    console.log('yee')
    let socket = new WebSocket('ws://127.0.0.1:8000/ws/chat/');

    socket.onopen = function(e) {
        // let info = {hello: "world", request_id: 2, action: 'create_message'};
        let info = {action: 'create_message', message: 'heya', user: 1, request_id: 299, 'hren': 299};
        let json = JSON.stringify(info);
        console.log("DATA: ", json);
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