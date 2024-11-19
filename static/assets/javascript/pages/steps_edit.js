"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// Class Template
// =============================================================
var stepsEdit =
/*#__PURE__*/
function () {
  function stepsEdit() {
    _classCallCheck(this, stepsEdit);

    this.init();
  }

  _createClass(stepsEdit, [{
    key: "init",
    value: function init() {
      // event handlers
      this.handleValidations();
      this.handleSteps();
    }
  }, {
    key: "validateByEdit",
    value: function validateByEdit(trigger) {
      var $trigger = $(trigger);
      var group = $trigger.data().validate;
      var groupId = $trigger.parents('.content').attr('id');
      var $groupStep = $("[data-target=\"#".concat(groupId, "\"]"));
      $('#edit_form').parsley().on('form:validate', function (formInstance) {
        var isValid = formInstance.isValid({
          group: group
        }); // normalize states

        $groupStep.removeClass('success error'); // give step item a validate state

        if (isValid) {
          $groupStep.addClass('success'); // go to next step or submit

          if ($trigger.hasClass('submit')) {
            const data_string = $("#edit_form").serialize();
            const data_url = $("#edit_form").attr('data-url');
            $('#page_loading').modal('show');
            $.ajax({
                url: data_url,
                data: data_string,
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    if (data.form_is_valid) {
                        $('#page_loading').modal('hide');
                        $('#submitfeedback').toast('show');
                        // alert(data.success_message);
                    } else {
                        $('#page_loading').modal('hide');
                        alert(data.error_message);
                    }
                }
            })
          } else {
            stepperDemo.next();
          }
        } else {
          $groupStep.addClass('error');
        }
      }).validate({
        group: group
      }); // kill listener

      $('#edit_form').parsley().off('form:validate');
    }
  }, {
    key: "handleValidations",
    value: function handleValidations() {
      var self = this; // validate on next buttons

      $('.next').on('click', function () {
        self.validateByEdit(this);
      }); // prev buttons

      $('.prev').on('click', function () {
        var $trigger = $(this);
        var groupId = $trigger.parents('.content').attr('id');
        var $groupStep = $("[data-target=\"#".concat(groupId, "\"]")); // normalize states

        $groupStep.removeClass('success error');
        $groupStep.prev().removeClass('success error');
        stepperDemo.previous();
      }); // save creadit card

      $('#savecc').on('click', function () {
        $('#edit_form').parsley().whenValidate({
          group: 'creditcard'
        });
      }); // submit button

      $('.submit').on('click', function () {
        self.validateByEdit(this);
        return false;
      });
    }
  }, {
    key: "handleSteps",
    value: function handleSteps() {
      var selector = document.querySelector('#stepper2');
      window.stepperDemo = new Stepper(selector, {
        linear: false
      });
    }
  }]);

  return stepsEdit;
}();
/**
 * Keep in mind that your scripts may not always be executed after the theme is completely ready,
 * you might need to observe the `theme:load` event to make sure your scripts are executed after the theme is ready.
 */


 new stepsEdit();