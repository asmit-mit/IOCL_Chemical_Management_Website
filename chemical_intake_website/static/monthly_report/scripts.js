const unit_dropdown = document.getElementById("unit");
const chemical_dropdown = document.getElementById("chemical");
const submit_button = document.getElementById("submit");
const clear_button = document.getElementById("clear");
const form = document.getElementById("montly-form");

window.onload = function () {
  if (form) {
    form.reset();
  }

  history.replaceState(null, null, window.location.href);

  for (const [unit_code, unit_data] of Object.entries(data_json)) {
    const option = document.createElement("option");
    option.value = unit_code;
    option.textContent = unit_data.unit_name;
    unit_dropdown.appendChild(option);
  }
};

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

  const option = document.createElement("option");
  option.value = "all";
  option.textContent = "All";
  chemical_dropdown.appendChild(option);
});

clear_button.addEventListener("click", function () {
  const table = document.querySelector(".scrollable-table-container");
  table.setAttribute("hidden", "");
  history.replaceState(null, null, window.location.href);
});

chemical_dropdown.addEventListener("click", function () {
  const alertlog = document.getElementById("alert-log");
  const alertMessage = document.getElementById("alert-message");

  if (unit_dropdown.value === "") {
    alertMessage.textContent = "Please select a unit first.";
    alertlog.showModal();
    return;
  }
});
