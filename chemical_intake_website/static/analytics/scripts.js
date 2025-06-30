const view_dropdown = document.getElementById("view-dropdown");
const analytics_table = document.getElementById("analytics-table");
const prediction_table = document.getElementById("predictions-table");
const analytics_images = document.querySelectorAll(".statistics-img");
const analytics_table_rows = document.querySelectorAll(".analytics-table-row");

const unit_dropdown = document.getElementById("unit-dropdown");

window.onload = function () {
  history.replaceState(null, null, window.location.href);
  view_dropdown.value = "analytics";
  unit_dropdown.value = "";
};

view_dropdown.addEventListener("change", function () {
  if (view_dropdown.value === "predictions") {
    analytics_table.setAttribute("hidden", "");
    prediction_table.removeAttribute("hidden");
    analytics_images.forEach((image) => {
      image.setAttribute("hidden", "");
    });
  } else if (view_dropdown.value === "analytics") {
    analytics_table.removeAttribute("hidden");
    prediction_table.setAttribute("hidden", "");
    analytics_images.forEach((image) => {
      image.removeAttribute("hidden");
    });
  }
});

unit_dropdown.addEventListener("change", function () {
  const unit_value = unit_dropdown.value;

  analytics_images.forEach((img) => {
    if (img.id !== unit_value) {
      img.setAttribute("hidden", "");
    } else {
      img.removeAttribute("hidden");
    }
  });

  analytics_table_rows.forEach((row) => {
    if (row.id !== unit_value) {
      row.setAttribute("hidden", "");
    } else {
      row.removeAttribute("hidden");
    }
  });
});
