const chartsUsuarios = document.querySelectorAll(".totalusuarios");

chartsUsuarios.forEach(function (chart) {
  var ctx = chart.getContext("2d");
  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Empresas", "Talentos"],
      datasets: [
        {
          label: "# of Votes",
          data: [12, 19],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
  });
});

$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable();
  });
});

const chartsTalentos = document.querySelectorAll(".niveltalento");

chartsTalentos.forEach(function (chart) {
  var ctx = chart.getContext("2d");
  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Estudante", "Junior", "Pleno", "Senior"],
      datasets: [
        {
          label: "#",
          data: [12, 19, 20, 3],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(150, 162, 235, 0.2)",
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 205, 86, 0.2)',
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgb(153, 102, 255)",
            'rgb(255, 205, 86)'
          ],
          borderWidth: 1,
        },
      ],
    },
  });
});

$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable();
  });
});
