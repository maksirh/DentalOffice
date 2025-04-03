async function getPatients() {
    const response = await fetch("/api/patients", {
        method: "GET",
        headers: { "Accept": "application/json" }
    });

    if (response.ok) {
        const patients = await response.json();
        const rows = document.querySelector("tbody");
        patients.forEach(patient => rows.append(row(patient)));
    }
}

async function getPatient(id) {
    const response = await fetch(`/api/patients/${id}`, {
        method: "GET",
        headers: { "Accept": "application/json" }
    });

    if (response.ok) {
        const user = await response.json();
        document.getElementById("patientId").value = user.id;
        document.getElementById("patientName").value = user.name;
        document.getElementById("patientAge").value = user.age;
        document.getElementById("patientPhone").value = user.phoneNumber;
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function createPatient(patientName, patientAge, patientPhone) {
    const response = await fetch("/api/patients", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: patientName,
            age: parseInt(patientAge, 10),
            phoneNumber: patientPhone
        })
    });

    if (response.ok) {
        const user = await response.json();
        document.querySelector("tbody").append(row(user));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function editPatient(patientId, patientName, patientAge, patientPhone) {
    const response = await fetch("/api/patients", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: patientId,
            name: patientName,
            age: parseInt(patientAge, 10),
            phoneNumber: patientPhone
        })
    });

    if (response.ok) {
        const user = await response.json();
        document.querySelector(`tr[data-rowid='${user.id}']`).replaceWith(row(user));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function deletePatient(id) {
    const response = await fetch(`/api/patients/${id}`, {
        method: "DELETE",
        headers: { "Accept": "application/json" }
    });

    if (response.ok) {
        document.querySelector(`tr[data-rowid='${id}']`).remove();
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

function reset() {
    document.getElementById("patientId").value = "";
    document.getElementById("patientName").value = "";
    document.getElementById("patientAge").value = "";
    document.getElementById("patientPhone").value = "";
}

function row(user) {
    const tr = document.createElement("tr");
    tr.setAttribute("data-rowid", user.id);

    const nameTd = document.createElement("td");
    nameTd.append(user.name);
    tr.append(nameTd);

    const ageTd = document.createElement("td");
    ageTd.append(user.age);
    tr.append(ageTd);

    const phoneTd = document.createElement("td");
    phoneTd.append(user.phoneNumber);
    tr.append(phoneTd);

    const linksTd = document.createElement("td");

    const editLink = document.createElement("button");
    editLink.append("Змінити");
    editLink.addEventListener("click", async () => await getPatient(user.id));
    linksTd.append(editLink);

    const removeLink = document.createElement("button");
    removeLink.append("Видалити");
    removeLink.addEventListener("click", async () => await deletePatient(user.id));
    linksTd.append(removeLink);

    tr.appendChild(linksTd);
    return tr;
}

document.getElementById("savePat").addEventListener("click", async () => {
    const id = document.getElementById("patientId").value;
    const name = document.getElementById("patientName").value;
    const age = document.getElementById("patientAge").value;
    const phoneNumber = document.getElementById("patientPhone").value;

    if (id === "")
        await createPatient(name, age, phoneNumber);
    else
        await editPatient(id, name, age, phoneNumber);

    reset();
});

getPatients();
