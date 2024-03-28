compteur_function = () => {
    if (compteur !== 0) {
        compteur--
        compteur_html.textContent = compteur
    }

}

fin_manche = () => {
    if (fin_du_jeu !== 1) {
        boutonLancer.disabled = true
        codeInput.disabled = true
        fin_du_jeu = 1
        text = codeInput.value
        envoyer_texte(text)
    }
}

envoyer_texte = (text) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/combat/next-turn", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ text: text }));
}

verifyAfterDelay = () => {
    let code = codeInput.value
    // Envoi de ma requête AJAX au serveur Flask
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "/verify", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText)
            if (response.result === true) {
                alert.style.display = 'none' // Cacher le message d'erreur ( quand il n'y a pas d'erreur )
                boutonLancer.disabled = false // Réactiver le bouton pour pouvoir commit le code
                error_message.style.display = 'none'
            } else {
                alert.style.display = 'block' // Afficher le message d'erreur avec la bonne erreur
                boutonLancer.disabled = true // Désactiver le bouton pour commit le code
                    error_message.innerText = response.error // Afficher l'erreur
                    error_message.style.display = 'block' // Afficher le message d'erreur
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

window.addEventListener("beforeunload", function (event) {
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "/refresh", true)
})

let fin_du_jeu = 0
let compteur_html = document.getElementById("compteur")
let compteur = 180
const codeInput = document.getElementById('story')
const boutonLancer = document.getElementById('bouton_lancer')
let timer
let timer_jeu
const duree_manche = 180000
const intervalleEcriture = 1500
const alert = document.getElementById("alert")
const error_message = document.getElementById("error-message")


codeInput.addEventListener('input', desactive_pdt_ecrire)
timer_jeu = setTimeout(fin_manche, duree_manche)
setInterval(compteur_function, 1000)
