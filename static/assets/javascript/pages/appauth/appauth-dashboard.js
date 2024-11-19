"use strict";

$(function () {
  $(document).ready(function () {
    // set_dashboard_data();
    $("#id_branch_code").select2();
    // set_dashboard_data2();
    fn_set_dashboard_data();
    

    refresh_myChart3_data();

  });

  var backgroundColor_charts = [
    "rgb(246, 54, 54,0.5)",
    "#4BC0C0",
    "rgba(75, 192, 192, 0.2)",
    "rgba(153, 102, 255, 0.2)",
    "rgba(69, 185, 104, 1)",
    "rgba(255, 99, 132, 1)",
    "rgba(54, 162, 235, 1)",
    "rgba(255, 206, 86, 1)",
    "rgba(75, 192, 192, 1)",
    "rgba	(0,0,128,1)",
    "#C0C0C0",
    "#808080",
    "#800000",
    "#808000",
    "#008000",
    "#800080",
    "#32CD32",
  ];

  var borderColor_charts = [
    "rgba(255, 99, 132, 1)",
    "rgba(54, 162, 235, 1)",
    "rgba(255, 206, 86, 1)",
    "rgba(75, 192, 192, 1)",
    "rgba(79, 174, 168, 1)",
    "#808080",
    "#800000",
    "#808000",
    "#008000",
    "#800080",
  ];

  // function set_dashboard_data() {
  //   var url = "/appauth-dashboard-chart-data";
  //   $.ajax({
  //     url: url,
  //     data: {},
  //     success: function (data) {
  //       refresh_myChart2_data(data);
  //       refresh_myChart_data(data);
  //     },
  //   });
  //   return false;
  // }

  // function set_dashboard_data2() {
  //   var url = "/appauth-dashboard-top-data";
  //   $.ajax({
  //     url: url,
  //     data: {},
  //     success: function (data) {
  //       console.log(data);
  //       refresh_low_profit_product_amount(data);
  //       refresh_top_profit_product_amount(data);
  //       refresh_low_profit_product_quantity(data);
  //       refresh_top_profit_product_quantity(data);
  //       refresh_top_due_supplier(data);
  //       refresh_top_due_customer(data);
  //     },
  //   });
  //   return false;
  // }

  function refresh_low_profit_product_amount(datas) {
    let chart_data = datas.low_profit_product;
    var product = [];
    $.each(chart_data, function (_key, value) {
      product.push({
        product_name: value.product_name,
        nested: {
          available_quantity_value: value.available_quantity_value,
          total_purchase_amount: value.total_purchase_amount,
        },
      });
    });

    const data = {
      labels: product.map((x) => x.product_name),
      datasets: [
        {
          label: "Total Purchase Amount",
          data: product.map((x) => x.nested.total_purchase_amount),
          borderColor: borderColor_charts,
          backgroundColor: backgroundColor_charts,
          fill: true,
        },
      ],
    };

    var ctx = document.getElementById("lowProfitProductAmount");
    var myChart = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: "index",
        },
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: (ctx) =>
              "Low profit Data: " + ctx.chart.options.plugins.tooltip.position,
          },
        },
      },
    });

    return false;
  }

  function refresh_top_profit_product_amount(datas) {
    let chart_data = datas.top_profit_product;
    var product = [];
    $.each(chart_data, function (_key, value) {
      product.push({
        product_name: value.product_name,
        nested: {
          available_quantity_value: value.available_quantity_value,
          total_purchase_amount: value.total_purchase_amount,
        },
      });
    });

    const data = {
      labels: product.map((x) => x.product_name),
      datasets: [
        {
          label: "Total Purchase Amount",
          data: product.map((x) => x.nested.total_purchase_amount),
          borderColor: backgroundColor_charts,
          backgroundColor: borderColor_charts,
          fill: true,
        },
      ],
    };

    var ctx = document.getElementById("TopProfitProductAmount");
    var myChart = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: "index",
        },
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: (ctx) =>
              "Top profit Data: " + ctx.chart.options.plugins.tooltip.position,
          },
        },
      },
    });

    return false;
  }

  function refresh_low_profit_product_quantity(datas) {
    let chart_data = datas.low_profit_product;
    var product = [];
    $.each(chart_data, function (_key, value) {
      product.push({
        product_name: value.product_name,
        nested: {
          available_quantity_value: value.available_quantity_value,
          total_purchase_amount: value.total_purchase_amount,
        },
      });
    });

    const data = {
      labels: product.map((x) => x.product_name),
      datasets: [
        {
          label: "Available Quantity Value ",
          data: product.map((x) => x.nested.available_quantity_value),
          borderColor: backgroundColor_charts,
          backgroundColor: borderColor_charts,
          fill: true,
        },
      ],
    };

    var ctx = document.getElementById("lowProfitProductQuantity");
    var myChart = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: "index",
        },
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: (ctx) =>
              "Low  profit Product Quantity: " +
              ctx.chart.options.plugins.tooltip.position,
          },
        },
      },
    });

    return false;
  }

  function refresh_top_profit_product_quantity(datas) {
    let chart_data = datas.top_profit_product;
    var product = [];
    $.each(chart_data, function (_key, value) {
      product.push({
        product_name: value.product_name,
        nested: {
          available_quantity_value: value.available_quantity_value,
          total_purchase_amount: value.total_purchase_amount,
        },
      });
    });

    const data = {
      labels: product.map((x) => x.product_name),
      datasets: [
        {
          label: "Available Quantity Value ",
          data: product.map((x) => x.nested.available_quantity_value),
          borderColor: borderColor_charts,
          backgroundColor: backgroundColor_charts,
          fill: true,
        },
      ],
    };

    var ctx = document.getElementById("TopProfitProductQuantity");
    var myChart = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: "index",
        },
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: (ctx) =>
              "Top profit Product Quantity: " +
              ctx.chart.options.plugins.tooltip.position,
          },
        },
      },
    });

    return false;
  }

  function refresh_top_due_supplier(datas) {
    console.log(datas);
    let chart_data = datas.top_due_supplier;
    var product = [];
    $.each(chart_data, function (_key, value) {
      product.push({
        account_title: value.account_title,
        account_balance: value.account_balance,
      });
    });

    const data = {
      labels: product.map((x) => x.account_title),
      datasets: [
        {
          label: "Top Due Supplier ",
          data: product.map((x) => x.account_balance),
          borderColor: "#4BC0C0",
          backgroundColor: backgroundColor_charts,
          fill: true,
        },
      ],
    };

    var ctx = document.getElementById("TopDueSupplier");
    var myChart = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: "index",
        },
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: (ctx) =>
              "Top Due Supplier: " + ctx.chart.options.plugins.tooltip.position,
          },
        },
      },
    });

    return false;
  }
  function refresh_top_due_customer(datas) {
    console.log(datas);
    let chart_data = datas.top_due_customer;
    var product = [];
    $.each(chart_data, function (_key, value) {
      product.push({
        account_title: value.account_title,
        account_balance: value.account_balance,
      });
    });

    const data = {
      labels: product.map((x) => x.account_title),
      datasets: [
        {
          label: "Top Due Customer ",
          data: product.map((x) => x.account_balance),
          borderColor: "#4BC0C0",
          backgroundColor: backgroundColor_charts,
          fill: true,
        },
      ],
    };

    var ctx = document.getElementById("TopDueCustomer");
    var myChart = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: "index",
        },
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: (ctx) =>
              "Top Due customer: " + ctx.chart.options.plugins.tooltip.position,
          },
        },
      },
    });

    return false;
  }

  function refresh_myChart_data(data) {
    var chart_data = data.general_info[0];
    var keys_data = [
      "Male",
      "Female",
      "Other"
    ];
    const keys_data2 = [];

    const value_of_chart = [chart_data.total_st_male,chart_data.total_st_female,chart_data.total_st_other];
    // $.each(chart_data, function (key, value) {
    //   var key1 = key;
    //   var value1 = value;
    //   keys_data.forEach(function (item) {
    //     if (key1 === item) {
    //       value_of_chart.push(parseFloat(value1));
    //       const keys = key1.toUpperCase().replace(/_/g, " ");
    //       keys_data2.push(keys);
    //     }
    //   });
    // });

    var ctx = document.getElementById("TotalAmountChart");
    var myChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: keys_data,
        datasets: [
          {
            label: value_of_chart,
            data: value_of_chart,
            backgroundColor: backgroundColor_charts,
            borderColor: borderColor_charts,
            borderWidth: 1,
          },
        ],
      },
      options: {
        layout: {
          padding: {
            // left: 50
          },
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",

            labels: {
              // This more specific font property overrides the global property
              font: {
                size: 9,
              },
              padding: 5,
            },
          },
          title: {
            display: true,
            text: "Student Summary",
          },
        },
      },
    });
  }

  function refresh_myChart2_data(data=[]) {
    var chart_data = data.emp_info[0];
    var keys_data = [
      "Male",
      "FEMALE",
      "OTHERS"
    ];
    const keys_data2 = [];

    const value_of_chart = [chart_data.total_male_emp,chart_data.total_female_emp,chart_data.total_other_emp];
    // $.each(chart_data, function (key, value) {
    //   var key1 = key;
    //   var value1 = value;
    //   keys_data.forEach(function (item) {
    //     if (key1 === item) {
    //       value_of_chart.push(parseFloat(value1));

    //       const keys = key1.toUpperCase().replace(/_/g, " ");
    //       keys_data2.push(keys);
    //     }
    //   });
    // });
    var ctx = document.getElementById("TotalQuantityChart");
    var myChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: keys_data,
        datasets: [
          {
            label: "# of Votes",
            data: value_of_chart,
            backgroundColor: backgroundColor_charts,
            borderColor: borderColor_charts,
            borderWidth: 1,
          },
        ],
      },
      options: {
        layout: {
          padding: {
            // left: 50
          },
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",

            labels: {
              // This more specific font property overrides the global property
              font: {
                size: 9,
              },
              padding: 5,
            },
          },
          title: {
            display: true,
            text: "Employee Summary",
          },
          subtitle: {
            display: true,
            text: "Custom Chart Subtitle",
          },
        },
      },
    });
  }
  function refresh_myChart3_data (data = []) {
    // var chart_data = data.dashboard[0];
    var keys_data = [
      "total_purchase_quantity",
      "total_sales_quantity",
      "purchase_return_quantity",
      "total_order_quantity",
      "total_available_quantity",
      "sales_return_quantity",
      "total_damage_quantity",
    ];
    const keys_data2 = [];

    const value_of_chart = [10,20,30,40,20,30,40];
    // $.each(chart_data, function (key, value) {
    //   var key1 = key;
    //   var value1 = value;
    //   keys_data.forEach(function (item) {
    //     if (key1 === item) {
    //       value_of_chart.push(parseFloat(value1));

    //       const keys = key1.toUpperCase().replace(/_/g, " ");
    //       keys_data2.push(keys);
    //     }
    //   });
    // });
    var ctx = document.getElementById("StackedChart");
    var myChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: keys_data,
        datasets: [
          {
            label: "# of Votes",
            data: value_of_chart,
            backgroundColor: backgroundColor_charts,
            borderColor: borderColor_charts,
            borderWidth: 1,
          },
        ],
      },
      options: {
        layout: {
          padding: {
            // left: 50
          },
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",

            labels: {
              // This more specific font property overrides the global property
              font: {
                size: 9,
              },
              padding: 5,
            },
          },
          title: {
            display: true,
            text: "Product Quantity Summary",
          },
          subtitle: {
            display: true,
            text: "Custom Chart Subtitle",
          },
        },
      },
    });
  }



    function fn_set_dashboard_data() {
      $.ajax({
        url: "/appauth-dashboard-data",
        type: "get",
        dataType: "json",
        beforeSend: function () {},
        success: function (data) {
          refresh_myChart_data(data);
          refresh_myChart2_data(data);
          console.log(data.emp_info[0]);
          $("#id_total_section").text(data.general_info[0].total_section);
          $("#id_total_class").text(data.general_info[0].total_class);
          $("#id_total_shift").text(data.general_info[0].total_shift??0);
          $("#id_total_branch").text(data.general_info[0].total_branch??0);
          $("#id_total_student").text(data.general_info[0].total_student);
          $("#id_total_St_male").text(data.general_info[0].total_st_male);
          $("#id_total_st_female").text(data.general_info[0].total_st_female);
          $("#id_total_st_o").text(data.general_info[0].total_st_other);
          $("#id_total_Hr").text(data.emp_info[0].total_employee);
          $("#id_total_female_emp").text(data.emp_info[0].total_female_emp);
          $("#id_total_male_emp").text(data.emp_info[0].total_male_emp);
          $("#id_total_loan_ac").text(data.emp_info[0].total_other_emp);
        },
      });
    }



});
