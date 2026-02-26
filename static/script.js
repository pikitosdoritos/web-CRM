let selectedRow = null;

function selectRow(row) {
    if (selectedRow) {
        selectedRow.classList.remove("selected-row");
    }

    selectedRow = row;
    selectedRow.classList.add("selected-row");

    document.getElementById("selected_id").value = row.dataset.id;

    // Enable/Disable Buttons
    document.querySelector(".del").disabled = false;
    document.querySelector(".edit-btn").disabled = false;

    populateForm(row);
}

function populateForm(row) {
    const cells = Array.from(row.querySelectorAll("td"));
    const form = document.getElementById("crm-form");

    const [, fullname, dob, phone, email, position, date, status] = cells.map(cell => cell.innerText);

    form.fullname.value = fullname || "";
    form.dob.value = dob || "";
    form.phone.value = phone || "";
    form.email.value = email || "";
    form.position.value = position || "";
    form.date.value = date || "";
    form.status.value = status || "";
}

function enableEdit() {
    if (!selectedRow) return;

    // Switch to Edit Mode
    document.querySelector(".save").classList.remove("hidden-el");
    document.querySelector(".submit").classList.add("hidden-el");
    document.querySelector(".edit-btn").classList.add("hidden-el");

    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

function clearForm() {
    const form = document.getElementById("crm-form");
    form.reset();

    if (selectedRow) {
        selectedRow.classList.remove("selected-row");
    }
    selectedRow = null;
    document.getElementById("selected_id").value = "";

    // Reset Buttons Mode
    document.querySelector(".save").classList.add("hidden-el");
    document.querySelector(".submit").classList.remove("hidden-el");

    const editBtn = document.querySelector(".edit-btn");
    editBtn.classList.remove("hidden-el");
    editBtn.disabled = true;

    document.querySelector(".del").disabled = true;
}

function filterTable() {
    const input = document.getElementById("search");
    const filter = input.value.toUpperCase();
    const table = document.querySelector("table");
    const tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length - 1; i++) {
        let textContent = tr[i].innerText.toUpperCase();
        if (textContent.indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}