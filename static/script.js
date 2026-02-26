let selectedRow = null;

function selectRow(row) {
    // Basic Selection logic
    if (selectedRow) {
        selectedRow.classList.remove("selected-row");
    }

    selectedRow = row;
    selectedRow.classList.add("selected-row");
    
    // Update Hidden Field
    document.getElementById("selected_id").value = row.dataset.id;
    
    // Enable/Disable Buttons
    document.querySelector(".del").disabled = false;
    document.querySelector(".edit-btn").disabled = false;
    
    // Auto-populate form when selecting (for convenience)
    populateForm(row);
}

function populateForm(row) {
    const cells = Array.from(row.querySelectorAll("td"));
    const form = document.getElementById("crm-form");
    
    // Cell extraction: first cell is # (id), then name, dob, phone, email, pos, date, status
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
    
    // Visual UI Switch
    document.querySelector(".save").hidden = false;
    document.querySelector(".submit").hidden = true;
    document.querySelector(".edit-btn").hidden = true;
    
    // Scroll to the edit inputs (which double as add inputs) at the bottom
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

function clearForm() {
    const form = document.getElementById("crm-form");
    form.reset();
    
    // Reset selection
    if (selectedRow) {
        selectedRow.classList.remove("selected-row");
    }
    selectedRow = null;
    document.getElementById("selected_id").value = "";
    
    // Reset Buttons Visibility
    document.querySelector(".save").hidden = true;
    document.querySelector(".submit").hidden = false;
    document.querySelector(".edit-btn").hidden = false;
    document.querySelector(".edit-btn").disabled = true;
    document.querySelector(".del").disabled = true;
}

function filterTable() {
    const input = document.getElementById("search");
    const filter = input.value.toUpperCase();
    const table = document.querySelector("table");
    const tr = table.getElementsByTagName("tr");
    
    // Loop through all table rows, except the first (header) and last (add form)
    for (let i = 1; i < tr.length - 1; i++) {
        let textContent = tr[i].innerText.toUpperCase();
        if (textContent.indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}