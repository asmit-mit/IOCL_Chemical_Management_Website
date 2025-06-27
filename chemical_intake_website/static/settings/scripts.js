const forms = document.querySelectorAll("form");

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
