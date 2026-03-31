function addMember() {
    const container = document.getElementById("teamContainer");

    const div = document.createElement("div");
    div.classList.add("team-member");

    div.innerHTML = `
    <div class="team-input-group">
        <input type="text" required>
        <label>Ism</label>
    </div>

    <div class="team-input-group">
        <input type="text" required>
        <label>Familya</label>
    </div>

    <div class="team-input-group">
        <input type="text" required>
        <label>Vazifasi</label>
    </div>

    <button type="button" class="remove-btn" onclick="this.parentElement.remove()">
        <i class="fa-solid fa-xmark"></i>
    </button>
`;

    container.appendChild(div);
}

document.getElementById("applicationForm").addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Ariza yuborildi!");
});