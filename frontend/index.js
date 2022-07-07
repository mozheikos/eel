window.addEventListener('load', () => {
    const send = document.querySelector('#msg-send');
    send.addEventListener('click', () => {
        const input = document.querySelector('#msg-input');
        const data = input.value;
        console.log('in listener');
        eel.send_msg(data);
        input.value = '';
    })
});

eel.expose(receive_msg);
function receive_msg(data) {
    const messages = document.querySelector('.messages');
    const newMsg = document.createElement('li');
    newMsg.innerHTML = data;
    messages.append(newMsg);
}
