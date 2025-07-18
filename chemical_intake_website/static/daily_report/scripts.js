const unit_dropdown = document.getElementById("unit");
const chemical_dropdown = document.getElementById("chemical");
const submit_button = document.getElementById("submit");
const clear_button = document.getElementById("clear");
const form = document.getElementById("daily-form");
const tooltip = document.getElementById("tooltip");
const selection_line = document.getElementById("selection-details");

window.onload = function () {
  form.reset();

  history.replaceState(null, null, window.location.href);

  for (const [unit_code, unit_data] of Object.entries(data_json)) {
    const option = document.createElement("option");
    option.value = unit_code;
    option.textContent = unit_data.unit_name;
    unit_dropdown.appendChild(option);
  }
};

document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  const todayStr = `${year}-${month}-${day}`;

  const startDateInput = document.getElementById("start_date");
  const endDateInput = document.getElementById("end_date");

  startDateInput.setAttribute("max", todayStr);
  endDateInput.setAttribute("max", todayStr);

  startDateInput.addEventListener("change", function () {
    const startDate = startDateInput.value;

    if (startDate) {
      endDateInput.setAttribute("min", startDate);
    } else {
      endDateInput.removeAttribute("min");
    }
  });

  endDateInput.addEventListener("change", function () {
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    if (startDate && endDate < startDate) {
      endDateInput.value = "";
    }
  });
});

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
  const datasheetTable = document.querySelector(".datasheet");
  datasheetTable.setAttribute("hidden", "");
  selection_line.setAttribute("hidden", "");
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

chemical_dropdown.addEventListener("mouseenter", () => {
  const key = unit_dropdown.value + chemical_dropdown.value;

  if (chemical_dropdown.value !== "" && chemical_dropdown.value !== "all") {
    const unitList = tooltip_data[key];
    tooltip.style.display = "block";

    tooltip.innerHTML = "";

    const heading = document.createElement("div");
    heading.textContent = "This chemical belongs to the following units:";
    tooltip.appendChild(heading);

    const ul = document.createElement("ul");

    for (const unitName of unitList || []) {
      const li = document.createElement("li");
      li.textContent = unitName;
      ul.appendChild(li);
    }

    tooltip.appendChild(ul);
  } else {
    tooltip.style.display = "none";
  }
});

chemical_dropdown.addEventListener("mouseleave", () => {
  tooltip.style.display = "none";
});

chemical_dropdown.addEventListener("mousemove", (e) => {
  tooltip.style.left = e.pageX - 10 + "px";
  tooltip.style.top = e.pageY - 50 + "px";
});
