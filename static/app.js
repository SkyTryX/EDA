const zm = document.getElementById('zone_map')
const socket = io()

socket.on('connect', () => {
})

socket.on('maj',(msg) => {
    zm.textContent = msg.data
})