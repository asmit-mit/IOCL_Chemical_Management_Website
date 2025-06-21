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

document.getElementById("unit").addEventListener("change", function () {
  const unitCode = this.value;
  const chemicalSelect = document.getElementById("chemical");

  chemicalSelect.innerHTML = '<option disabled selected value="">Select Chemical</option>';

  if (!unitCode) return;

  const chemicals = allData.filter((item) => item.unit_code === unitCode);
  chemicals.forEach((chem) => {
    const option = document.createElement("option");
    option.value = chem.chemical_code;
    option.textContent = chem.chemical_name;
    chemicalSelect.appendChild(option);
  });
});
