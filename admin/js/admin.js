/* DEMO ARIZALAR */

let applications = [

    {
        id: 1,
        name: "Sattorov Alixon",
        startup: "AI Startup",
        phone: "+998901234567",
        desc: "AI asosidagi platforma",
        accepted: false
    },

    {
        id: 2,
        name: "Jasur Karimov",
        startup: "Fintech System",
        phone: "+998991234567",
        desc: "Online payment system",
        accepted: false
    }

]

const container = document.getElementById("apps")

if (container) {

    renderApps()

}

function renderApps() {

    container.innerHTML = ""

    applications.forEach(app => {

        let card = document.createElement("div")

        card.className = "app-card"

        if (app.accepted) card.classList.add("accepted")

        card.innerHTML = `
<h3>${app.name}</h3>
<p>${app.startup}</p>
<button onclick="accept(${app.id})">Qabul qilindi</button>
`

        card.onclick = () => showDetails(app)

        container.appendChild(card)

    })

}

function accept(id) {

    applications = applications.map(a => {
        if (a.id === id) a.accepted = true
        return a
    })

    renderApps()

}

/* MODAL */

function showDetails(app) {

    const modal = document.getElementById("modal")

    const content = document.getElementById("modalContent")

    content.innerHTML = `

<h3>${app.name}</h3>

<p><b>Startup:</b> ${app.startup}</p>

<p><b>Telefon:</b> ${app.phone}</p>

<p>${app.desc}</p>

<button onclick="closeModal()">Yopish</button>

`

    modal.style.display = "flex"

}

function closeModal() {

    document.getElementById("modal").style.display = "none"

}


/* HACKATHON */

let hacks = []

function addHack() {

    const name = document.getElementById("hackName").value
    const date = document.getElementById("hackDate").value

    hacks.push({ name, date })

    renderHacks()

}

function renderHacks() {

    const grid = document.getElementById("hackGrid")

    if (!grid) return

    grid.innerHTML = ""

    hacks.forEach((h, i) => {

        let card = document.createElement("div")

        card.className = "hack-card"

        card.innerHTML = `

<h3>${h.name}</h3>

<p>${h.date}</p>

<button onclick="deleteHack(${i})">O'chirish</button>

`

        grid.appendChild(card)

    })

}

function deleteHack(i) {

    hacks.splice(i, 1)

    renderHacks()

}