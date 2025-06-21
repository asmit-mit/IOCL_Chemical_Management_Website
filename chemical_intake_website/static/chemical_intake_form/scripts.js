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

document.getElementById("unit").addEventListener("change", function () {
  const unitCode = this.value;
  const chemicalSelect = document.getElementById("chemical");
  const uomInput = document.getElementById("uom");

  chemicalSelect.innerHTML = '<option disabled selected value="">Select Chemical</option>';
  uomInput.value = "";

  if (!unitCode) {
    return;
  }

  const chemicals = allData.filter((item) => item.unit_code === unitCode);
  chemicals.forEach((chem) => {
    const option = document.createElement("option");
    option.value = chem.chemical_code;
    option.textContent = chem.chemical_name;
    chemicalSelect.appendChild(option);
  });
});

document.getElementById("chemical").addEventListener("click", function () {
  const unitCode = document.getElementById("unit");
  const message_modal = document.querySelector("#message_modal");
  const messagesList = message_modal.querySelector(".messages");

  if (!unitCode.value) {
    messagesList.innerHTML = "";
    const newMessage = document.createElement("li");
    newMessage.textContent = "Please select a unit first.";
    messagesList.appendChild(newMessage);
    message_modal.showModal();
    return;
  }
});

document.getElementById("chemical").addEventListener("change", function () {
  const unitCode = document.getElementById("unit").value;
  const chemicalCode = this.value;
  const uomInput = document.getElementById("uom");
  const smcInput = document.getElementById("smc");

  if (!unitCode || !chemicalCode) return;

  function getRandomString() {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
    let result = "";
    for (let i = 0; i < 4; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      result += characters[randomIndex];
    }
    return result;
  }

  const chemical = allData.find(
    (item) => item.unit_code === unitCode && item.chemical_code === chemicalCode,
  );
  if (chemical) {
    uomInput.value = chemical.unit;
    smcInput.value = getRandomString();
  }
});
