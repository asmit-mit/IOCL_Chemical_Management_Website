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

    analytics_table_rows.forEach((row) => {
      row.setAttribute("hidden", "");
    });

    prediction_images.forEach((image) => {
      image.removeAttribute("hidden");
    });

    precdiction_table_rows.forEach((row) => {
      row.removeAttribute("hidden");
    });
  } else {
    analytics_table.removeAttribute("hidden");
    prediction_table.setAttribute("hidden", "");

    analytics_images.forEach((image) => {
      image.removeAttribute("hidden");
    });

    analytics_table_rows.forEach((row) => {
      row.removeAttribute("hidden");
    });

    prediction_images.forEach((image) => {
      image.setAttribute("hidden", "");
    });

    precdiction_table_rows.forEach((row) => {
      row.setAttribute("hidden", "");
    });
  }
});

unit_dropdown.addEventListener("change", function () {
  const unit_value = unit_dropdown.value;

  if (view_dropdown.value === "analytics") {
    if (unit_value === "all") {
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

window.addEventListener("DOMContentLoaded", () => {
  const lowCoverage = 0;
  const optimalCoverage = 3;
  const highCoverage = 6;

  function hexToRgb(hex) {
    const bigint = parseInt(hex.replace("#", ""), 16);
    return {
      r: (bigint >> 16) & 255,
      g: (bigint >> 8) & 255,
      b: bigint & 255,
    };
  }

  function interpolateColor(color1, color2, factor) {
    const result = {
      r: Math.round(color1.r + (color2.r - color1.r) * factor),
      g: Math.round(color1.g + (color2.g - color1.g) * factor),
      b: Math.round(color1.b + (color2.b - color1.b) * factor),
    };
    return `rgb(${result.r}, ${result.g}, ${result.b})`;
  }

  const red = hexToRgb("#f44336");
  const green = hexToRgb("#4caf50");
  const blue = hexToRgb("#2196f3");

  document.querySelectorAll("td.coverage").forEach((cell) => {
    const value = parseFloat(cell.textContent);
    if (isNaN(value)) return;

    let bgColor;

    if (value <= optimalCoverage) {
      const factor = Math.max((value - lowCoverage) / (optimalCoverage - lowCoverage), 0);
      bgColor = interpolateColor(red, green, factor);
    } else {
      const factor = Math.min((value - optimalCoverage) / (highCoverage - optimalCoverage), 1);
      bgColor = interpolateColor(green, blue, factor);
    }

    cell.style.backgroundColor = bgColor;
    cell.style.color = "white";
  });
});
