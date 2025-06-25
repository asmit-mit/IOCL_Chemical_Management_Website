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
