async function getDentists() {
    const response = await fetch("/api/dentists", {
        method: "GET",
        headers: { "Accept": "application/json" }
    });

    if (response.ok === true) {
        const dentists = await response.json();
        const rows = document.querySelector("tbody");
        dentists.forEach(dentist => rows.append(row(dentist)));
    }
}

async function getDentist(id) {
    const response = await fetch(`/api/dentists/${id}`, {
        method: "GET",
        headers: { "Accept": "application/json" }
    });
    if (response.ok === true) {
        const user = await response.json();
        document.getElementById("userId").value = dentist.id;
        document.getElementById("userName").value = dentist.name;
        document.getElementById("userAge").value = dentist.age;
        document.getElementById("userExp").value = dentist.exp;
        document.getElementById("userPhone").value = dentist.phone;

    }
    else {
        // якщо сталася помилка, отримуємо повідомлення про помилку
        const error = await response.json();
        console.log(error.message); // і виводимо його на консоль
    }
}
// Додавання користувача
async function createDentist(dentistName, dentistAge, dentistExp, dentistPhone) {
    const response = await fetch("/api/dentists", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: dentistName,
            age: parseInt(dentistAge, 10),
            experience: parseInt(dentistExp, 10),
            phoneNumber: dentistPhone
        })
    });
    if (response.ok === true) {
        const dentist = await response.json();
        document.querySelector("tbody").append(row(dentist));
    }
    else {
        const error = await response.json();
        console.log(error.message);
    }
}

// Зміна користувача
async function editDentist(dentistId, dentistName, dentistAge) {
    const response = await fetch("api/dentists", {
        method: "PUT",
        headers: {
            "Accept": "application/json", "Content-Type":

                "application/json"
        },

        body: JSON.stringify({
            id: dentistId,
            name: dentistName,
            age: parseInt(dentistAge, 10)
        })
    });
    if (response.ok === true) {
        const dentist = await response.json();

        document.querySelector(`tr[data-rowid='${dentist.id}']`).replaceWith(row(dentist));

    }
    else {
        const error = await response.json();
        console.log(error.message);
    }
}
// Видалення користувача
async function deleteDentist(id) {
    const response = await fetch(`/api/dentists/${id}`, {
        method: "DELETE",
        headers: { "Accept": "application/json" }
    });
    if (response.ok === true) {
        const dentist = await response.json();
        document.querySelector(`tr[data-rowid='${dentist.id}']`).remove();
    }
    else {
        const error = await response.json();
        console.log(error.message);
    }
}
// скидання даних форми після відправлення
function reset() {
    document.getElementById("dentistId").value =
        document.getElementById("dentistName").value =
        document.getElementById("dentistAge").value = "";
}
// створення рядка для таблиці
function row(dentist) {
    const tr = document.createElement("tr");
    tr.setAttribute("data-rowid", dentist.id);

    const nameTd = document.createElement("td");
    nameTd.append(dentist.name);
    tr.append(nameTd);

    const ageTd = document.createElement("td");
    ageTd.append(dentist.age);
    tr.append(ageTd);

    const expTd = document.createElement("td");
    expTd.append(dentist.experience);
    tr.append(expTd);

    const phoneTd = document.createElement("td");
    phoneTd.append(dentist.phoneNumber);
    tr.append(phoneTd);

    const linksTd = document.createElement("td");
    const editLink = document.createElement("button");
    editLink.append("Змінити");
    editLink.addEventListener("click", async () => await getDentist(dentist.id));
    linksTd.append(editLink);

    const removeLink = document.createElement("button");
    removeLink.append("Видалити");
    removeLink.addEventListener("click", async () => await deleteDentist(dentist.id));
    linksTd.append(removeLink);

    tr.appendChild(linksTd);
    return tr;
}


// скидання значень форми
document.getElementById("resetBtn").addEventListener("click", () => reset());
// надсилання форми
document.getElementById("saveBtn").addEventListener("click", async () => {
    const id = document.getElementById("dentistId").value;
    const name = document.getElementById("dentistName").value;
    const age = document.getElementById("dentistAge").value;
    const exp = document.getElementById("dentistExp").value;
    const phone = document.getElementById("dentistPhone").value;

    if (id === "")
        await createDentist(name, age, exp, phone);
    else
        await editDentist(id, name, age);

    reset();
});

// завантаження користувачів
getDentists();