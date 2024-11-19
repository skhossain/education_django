"use strict";

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _defineProperties(target, props) {
  for (var i = 0; i < props.length; i++) {
    var descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ("value" in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  return Constructor;
}

// Class Template
// =============================================================
var stepsDemo =
  /*#__PURE__*/
  (function () {
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) == name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    function stepsDemo() {
      _classCallCheck(this, stepsDemo);

      this.init();
    }

    _createClass(stepsDemo, [
      {
        key: "init",
        value: function init() {
          // event handlers
          this.handleValidations();
          this.handleSteps();
        },
      },
      {
        key: "validateBy",
        value: function validateBy(trigger) {
          var $trigger = $(trigger);
          var group = $trigger.data().validate;
          var groupId = $trigger.parents(".content").attr("id");
          var $groupStep = $('[data-target="#'.concat(groupId, '"]'));
          $("#stepper-form")
            .parsley()
            .on("form:validate", function (formInstance) {
              var isValid = formInstance.isValid({
                group: group,
              }); // normalize states

              $groupStep.removeClass("success error"); // give step item a validate state

              if (isValid) {
                $groupStep.addClass("success"); // go to next step or submit

                if ($trigger.hasClass("submit")) {
                  var csrftoken = getCookie("csrftoken");
                  let data_string = $("#stepper-form").serializeArray();
                  console.log(data_string);
                  const data_url = $("#stepper-form").attr("data-url");
                  $("#page_loading").modal("show");
                  $.ajax({
                    url: data_url,
                    data: data_string,
                    type: "POST",
                    dataType: "json",
                    headers: {
                      "X-CSRF-Token": csrftoken,
                    },
                    success: function (data) {
                      if (data.form_is_valid) {
                        $("#page_loading").modal("hide");
                        $("#submitfeedback").toast("show");
                        // alert(data.success_message);
                        location.reload();
                      } else {
                        $("#page_loading").modal("hide");
                        alert(data.error_message);
                      }
                    },
                  });
                } else {
                  stepperDemo.next();
                }
              } else {
                $groupStep.addClass("error");
              }
            })
            .validate({
              group: group,
            }); // kill listener

          $("#stepper-form").parsley().off("form:validate");
        },
      },
      {
        key: "handleValidations",
        value: function handleValidations() {
          var self = this; // validate on next buttons

          $(".next").on("click", function () {
            self.validateBy(this);
          }); // prev buttons

          $(".prev").on("click", function () {
            var $trigger = $(this);
            var groupId = $trigger.parents(".content").attr("id");
            var $groupStep = $('[data-target="#'.concat(groupId, '"]')); // normalize states

            $groupStep.removeClass("success error");
            $groupStep.prev().removeClass("success error");
            stepperDemo.previous();
          }); // save creadit card

          $("#savecc").on("click", function () {
            $("#stepper-form").parsley().whenValidate({
              group: "creditcard",
            });
          }); // submit button

          $(".submit").on("click", function () {
            self.validateBy(this);
            return false;
          });
        },
      },
      {
        key: "handleSteps",
        value: function handleSteps() {
          var selector = document.querySelector("#stepper");
          window.stepperDemo = new Stepper(selector, {
            linear: false,
          });
        },
      },
    ]);

    return stepsDemo;
  })();
/**
 * Keep in mind that your scripts may not always be executed after the theme is completely ready,
 * you might need to observe the `theme:load` event to make sure your scripts are executed after the theme is ready.
 */

$(document).on("theme:init", function () {
  new stepsDemo();
});
