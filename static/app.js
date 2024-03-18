const zm = document.getElementById('zone_map')
const socket = io()

socket.on('connect', () => {
    socket.emit("send_maj", {data: "Hi!"})
})

socket.on('maj',(msg) => {
    zm.textContent = msg.data
})