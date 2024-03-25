verifyAfterDelay = () => {
    let code = codeInput.value
    // Envoi de ma requête AJAX au serveur Flask
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "/verify", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText)
            if (response.result === true) {
                alert.style.display = 'none' // Cacher le message d'erreur ( quand il n'y a pas d'erreur )
                boutonLancer.disabled = false // Réactiver le bouton pour pouvoir commit le code
                error_message.style.display = 'none'
            } else {
                alert.style.display = 'block' // Afficher le message d'erreur avec la bonne erreur
                boutonLancer.disabled = true // Désactiver le bouton pour commit le code
                if (response.error !== null) {
                    error_message.innerText = response.error // Afficher l'erreur
                    error_message.style.display = 'block' // Afficher le message d'erreur
                } 
            }
        }
    }
    xhr.send(JSON.stringify({ code: code }))
}

desactive_pdt_ecrire = () => {
    clearTimeout(timer)
    alert.style.display = 'none' // Cacher le message d'erreur pendant l'écriture jusqu'à prochaine vérification 
    boutonLancer.disabled = true // Désactive le bouton pour lancer pendant l'écriture
    error_message.textContent = ""
    timer = setTimeout(verifyAfterDelay, intervalleEcriture)
}


const codeInput = document.getElementById('story')
const boutonLancer = document.getElementById('bouton_lancer')
let timer
const intervalleEcriture = 1500
const alert = document.getElementById("alert")
const error_message = document.getElementById("error-message")
codeInput.addEventListener('input', desactive_pdt_ecrire)

