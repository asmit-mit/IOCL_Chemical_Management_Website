const unit_dropdown = document.getElementById("unit");
const chemical_dropdown = document.getElementById("chemical");
const forms = document.querySelectorAll("form");

const entry_form = document.getElementById("entryform");
const table_container = document.querySelector(".table-container");

window.onload = function () {
  forms.forEach((form) => form.reset());

  history.replaceState(null, null, window.location.href);

  for (const [unit_code, unit_data] of Object.entries(data_json)) {
    const option = document.createElement("option");
    option.value = unit_code;
    option.textContent = unit_data.unit_name;
    unit_dropdown.appendChild(option);
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const openingBalance = document.getElementById("opening_balance");
  const receiveQty = document.getElementById("receive_qty");
  const consumptionQty = document.getElementById("consumption_qty");

  function calculateClosingBalance() {
    const opening = parseFloat(openingBalance.value) || 0;
    const received = parseFloat(receiveQty.value) || 0;
    const consumed = parseFloat(consumptionQty.value) || 0;

    const calculatedBalance = (opening + received - consumed).toFixed(2);
    document.getElementById("closing_balance_input").value = calculatedBalance;
  }

  openingBalance.addEventListener("input", calculateClosingBalance);
  receiveQty.addEventListener("input", calculateClosingBalance);
  consumptionQty.addEventListener("input", calculateClosingBalance);
});

document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  const todayStr = `${year}-${month}-${day}`;

  document.getElementById("date").setAttribute("max", todayStr);
});

const detailsButton = document.querySelector("#details");
const detailsDialog = document.querySelector("#details_dialog");
const closeButton = document.querySelector("#close_details");

detailsButton.addEventListener("click", () => {
  const openingBalance = document.getElementById("opening_balance");
  const receiveQty = document.getElementById("receive_qty");
  const consumptionQty = document.getElementById("consumption_qty");
  const closingBalance = document.getElementById("closing_balance_input");

  const opening = parseFloat(openingBalance.value) || 0;
  const received = parseFloat(receiveQty.value) || 0;
  const consumed = parseFloat(consumptionQty.value) || 0;
  const closing = parseFloat(closingBalance.value) || 0;

  document.getElementById("details_opening_bal").value = opening;
  document.getElementById("details_rcv_qty").value = received;
  document.getElementById("details_consumption_qty").value = consumed;
  document.getElementById("details_closing_bal").value = closing;

  detailsDialog.showModal();
});

closeButton.addEventListener("click", () => detailsDialog.close());

unit_dropdown.addEventListener("change", function () {
  chemical_dropdown.innerHTML = '<option disabled selected value="">Select Chemical</option>';

  if (data_json[unit_dropdown.value]["chemicals"]) {
    for (const chemical of data_json[unit_dropdown.value]["chemicals"]) {
      const [chemical_code, chemical_name] = Object.entries(chemical)[0];
      const option = document.createElement("option");
      option.value = chemical_code;
      option.textContent = chemical_name;
      chemical_dropdown.appendChild(option);
    }
  }
});

chemical_dropdown.addEventListener("click", function () {
  const date = document.getElementById("date");
  const alertlog = document.getElementById("alert-log");
  const alertMessage = document.getElementById("alert-message");

  if (date.value === "") {
    alertMessage.textContent = "Please select a date first.";
    alertlog.showModal();
    return;
  }

  if (unit_dropdown.value === "") {
    alertMessage.textContent = "Please select a unit first.";
    alertlog.showModal();
    return;
  }
});

chemical_dropdown.addEventListener("change", function () {
  const uom = document.getElementById("uom");
  const smc = document.getElementById("smc");
  const avg_consume = document.getElementById("avg-consume");
  const sap_stock = document.getElementById("sap-stock");

  const selected_unit = unit_dropdown.value;
  const selected_chemical = chemical_dropdown.value;

  const chemical_data = data_json[selected_unit]["chemicals"];

  for (const chemical of chemical_data) {
    if (chemical.hasOwnProperty(selected_chemical)) {
      uom.value = chemical.uom || 0;
      smc.value = chemical.smc || 0;
      avg_consume.value = chemical.avg_consume || 0;
      sap_stock.value = chemical.sap_stock || 0;

      if (avg_consume.value !== "0") {
        entry_form.style.width = "40%";
        entry_form.style.left = "270px";
        table_container.removeAttribute("hidden");

        document.querySelectorAll(".recent-data-table tr:not(#header-row)").forEach((row) => {
          row.remove();
        });

        const chemical_data = data_json[selected_unit]["chemicals"];
        for (const chemical of chemical_data) {
          const [chemical_code, chemical_name] = Object.entries(chemical)[0];
          if (chemical_code === selected_chemical) {
            const consumption_data = chemical["consumption_data"];
            consumption_data.forEach((record) => {
              const recordDate = record[0];
              const recordConsumption = record[1];

              const row = document.createElement("tr");

              const date_td = document.createElement("td");
              date_td.textContent = recordDate;

              const consumption_td = document.createElement("td");
              consumption_td.textContent = recordConsumption;

              const table_body = document.querySelector(".recent-data-table tbody");

              row.appendChild(date_td);
              row.appendChild(consumption_td);

              table_body.appendChild(row);
            });
            break;
          }
        }
      } else {
        entry_form.style.width = "calc(100% - 340px)";
        entry_form.style.left = "270px";
        table_container.setAttribute("hidden", "");
      }

      return;
    }
  }

  uom.value = 0;
  smc.value = 0;
  avg_consume.value = 0;
  sap_stock.value = 0;
});

document.getElementById("clear").addEventListener("click", function () {
  entry_form.style.width = "calc(100% - 340px)";
  entry_form.style.left = "270px";
  table_container.setAttribute("hidden", "");
  return;
});

// const all_inputs = document.querySelectorAll("input");
//
// all_inputs.forEach((input) => {
//   input.addEventListener("change", function () {
//     if (input.value !== "") {
//       input.style.borderLeftColor = "green";
//     } else {
//       input.style.borderLeftColor = "red";
//     }
//   });
// });
