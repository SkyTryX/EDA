const zm = document.getElementById('zone_map')
const socket = io()

socket.on('connect', () => {
})

socket.on('maj',(msg) => {
    console.log('Received map data:', msg.data);
    zm.textContent = msg.data;
})

socket.on('send_maj', (msg) => {
    zm.textContent = msg.data;
});