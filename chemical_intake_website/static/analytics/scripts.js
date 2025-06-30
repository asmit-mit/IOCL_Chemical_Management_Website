const view_dropdown = document.getElementById("view-dropdown");
const analytics_table = document.getElementById("analytics-table");
const prediction_table = document.getElementById("predictions-table");
const analytics_images = document.querySelectorAll(".statistics-img");
const prediction_images = document.querySelectorAll(".predictions-img");
const analytics_table_rows = document.querySelectorAll(".analytics-table-row");
const precdiction_table_rows = document.querySelectorAll(".predictions-table-row");

const unit_dropdown = document.getElementById("unit-dropdown");

window.onload = function () {
  history.replaceState(null, null, window.location.href);
  view_dropdown.value = "analytics";
  unit_dropdown.value = "";
};

view_dropdown.addEventListener("change", function () {
  unit_dropdown.value = "all";

  if (view_dropdown.value === "predictions") {
    analytics_table.setAttribute("hidden", "");
    prediction_table.removeAttribute("hidden");
    analytics_images.forEach((image) => {
      image.setAttribute("hidden", "");
    });
    prediction_images.forEach((image) => {
      image.removeAttribute("hidden");
    });
  } else {
    analytics_table.removeAttribute("hidden");
    prediction_table.setAttribute("hidden", "");
    analytics_images.forEach((image) => {
      image.removeAttribute("hidden");
    });
    prediction_images.forEach((image) => {
      image.setAttribute("hidden", "");
    });
  }
});

unit_dropdown.addEventListener("change", function () {
  const unit_value = unit_dropdown.value;

  if (view_dropdown.value === "analytics") {
    if (unit === "all") {
      analytics_images.forEach((img) => {
        img.removeAttribute("hidden");
      });

      analytics_table_rows.forEach((row) => {
        row.removeAttribute("hidden");
      });
    } else {
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
    }
  }

  if (view_dropdown.value === "predictions") {
    if (unit_value === "all") {
      prediction_images.forEach((img) => {
        img.removeAttribute("hidden");
      });

      precdiction_table_rows.forEach((row) => {
        row.removeAttribute("hidden");
      });
    } else {
      prediction_images.forEach((img) => {
        if (img.id !== unit_value) {
          img.setAttribute("hidden", "");
        } else {
          img.removeAttribute("hidden");
        }
      });

      precdiction_table_rows.forEach((row) => {
        if (row.id !== unit_value) {
          row.setAttribute("hidden", "");
        } else {
          row.removeAttribute("hidden");
        }
      });
    }
  }
});
