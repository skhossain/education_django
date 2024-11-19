CREATE OR REPLACE FUNCTION public.fn_run_report (
   IN      p_app_user_id   CHARACTER,
   IN      p_report_name   CHARACTER,
       OUT o_status        CHARACTER,
       OUT o_errm          CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
   w_sql_stat               TEXT := '';
   w_from_date              DATE;
   w_upto_date              DATE;
   w_ason_date              DATE;
   w_current_business_day   DATE;
   w_ledger_code            VARCHAR;
   w_invoice_number         VARCHAR;
   w_user_id                VARCHAR;
   w_acc_type_code          VARCHAR;
   w_employee_id            VARCHAR;
   w_client_id              VARCHAR;
   w_supplier_id            VARCHAR;
   w_account_number         VARCHAR;
   w_account_title          VARCHAR;
   w_product_id             VARCHAR;
   w_branch_code            INTEGER;
   w_zero_balance           VARCHAR := 'N';
   w_transfer_tran          VARCHAR := 'N';
   w_delar_id               INTEGER;
   w_closing_balance        NUMERIC (22, 2);
   w_opening_balance        NUMERIC (22, 2);
   w_cash_gl_code           VARCHAR;
   rec_delar_list           RECORD;
   rec_branch_list          RECORD;
   rec_product_list         RECORD;
   w_branch_name            VARCHAR;
   w_branch_address         VARCHAR;
   w_empty_sheet            VARCHAR;
   w_center_name            VARCHAR;
   w_center_address         VARCHAR;
BEGIN
   DELETE FROM appauth_report_table_tabular
         WHERE app_user_id = p_app_user_id;

   SELECT CASE WHEN parameter_values != '' THEN parameter_values END w_user_id
     INTO w_user_id
     FROM appauth_report_parameter
    WHERE     parameter_name = 'p_user_id'
          AND report_name = p_report_name
          AND app_user_id = p_app_user_id;

   SELECT CASE
             WHEN parameter_values != ''
             THEN
                cast (parameter_values AS INTEGER)
          END w_branch_code
     INTO w_branch_code
     FROM appauth_report_parameter
    WHERE     parameter_name = 'p_branch_code'
          AND report_name = p_report_name
          AND app_user_id = p_app_user_id;

   IF w_branch_code IS NOT NULL
   THEN
      SELECT branch_name, branch_address
        INTO w_branch_name, w_branch_address
        FROM appauth_branch
       WHERE branch_code = w_branch_code;

      BEGIN
         INSERT INTO appauth_report_parameter (app_user_id,
                                               report_name,
                                               parameter_name,
                                               parameter_values)
              VALUES (p_app_user_id,
                      p_report_name,
                      'p_branch_name',
                      w_branch_name);

         INSERT INTO appauth_report_parameter (app_user_id,
                                               report_name,
                                               parameter_name,
                                               parameter_values)
              VALUES (p_app_user_id,
                      p_report_name,
                      'p_branch_address',
                      w_branch_address);
      END;
   END IF;

   SELECT CASE
             WHEN parameter_values != '' THEN cast (parameter_values AS DATE)
          END p_from_date
     INTO w_from_date
     FROM appauth_report_parameter
    WHERE     parameter_name = 'p_from_date'
          AND report_name = p_report_name
          AND app_user_id = p_app_user_id;

   SELECT CASE
             WHEN parameter_values != '' THEN cast (parameter_values AS DATE)
          END p_upto_date
     INTO w_upto_date
     FROM appauth_report_parameter
    WHERE     parameter_name = 'p_upto_date'
          AND report_name = p_report_name
          AND app_user_id = p_app_user_id;

   SELECT CASE
             WHEN parameter_values != '' THEN cast (parameter_values AS DATE)
          END p_ason_date
     INTO w_ason_date
     FROM appauth_report_parameter
    WHERE     parameter_name = 'p_ason_date'
          AND report_name = p_report_name
          AND app_user_id = p_app_user_id;

   IF w_from_date = w_upto_date AND w_ason_date IS NULL
   THEN
      w_ason_date := w_upto_date;
   END IF;

   IF p_report_name = 'finance_cashnbank_report'
   THEN
      BEGIN
         SELECT cash_gl_code
           INTO w_cash_gl_code
           FROM finance_application_settings;

         SELECT CASE
                   WHEN parameter_values != ''
                   THEN
                      cast (parameter_values AS DATE)
                END p_ason_date
           INTO w_ason_date
           FROM appauth_report_parameter
          WHERE     parameter_name = 'p_ason_date'
                AND report_name = p_report_name
                AND app_user_id = p_app_user_id;

         FOR rec_branch_list
            IN (SELECT DISTINCT branch_code
                  FROM finance_ledger_balance
                 WHERE     last_balance_update <= w_ason_date
                       AND gl_code = w_cash_gl_code)
         LOOP
            SELECT *
            INTO w_status, w_status
            FROM fn_finance_glbal_hist (w_cash_gl_code,
                                        rec_delar_list.delar_id,
                                        w_ason_date);
         END LOOP;

         BEGIN
            SELECT o_gl_balance
            INTO w_opening_balance
            FROM fn_finance_get_ason_glbal (0,
                                            w_cash_gl_code,
                                            w_ason_date - 1);
         END;

         BEGIN
            SELECT o_gl_balance
              INTO w_closing_balance
              FROM fn_finance_get_ason_glbal (0, w_cash_gl_code, w_ason_date);
         END;

         INSERT INTO appauth_report_parameter (parameter_name,
                                               report_name,
                                               app_user_id,
                                               parameter_values)
              VALUES ('p_closing_balance',
                      p_report_name,
                      p_app_user_id,
                      w_closing_balance);

         INSERT INTO appauth_report_parameter (parameter_name,
                                               report_name,
                                               app_user_id,
                                               parameter_values)
              VALUES ('p_opening_balance',
                      p_report_name,
                      p_app_user_id,
                      w_opening_balance);
      END;

      SELECT
      INTO w_status, w_errm
      FROM fn_run_finance_cash_report (COALESCE (w_branch_code, 0),
                                       w_from_date,
                                       w_upto_date,
                                       p_app_user_id);

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING MESSAGE = w_errm;
      END IF;
   ELSIF p_report_name IN ('finance_trial_balance',
                           'finance_receipt_payment',
                           'finance_asset_liabilities',
                           'finance_income_expenses')
   THEN
      IF COALESCE (w_branch_code, 0) > 0
      THEN
         SELECT *
         INTO w_status, w_errm
         FROM fn_run_finance_ledger_balance_branch (
                 COALESCE (w_branch_code, 0),
                 p_report_name,
                 w_ason_date,
                 w_from_date,
                 w_upto_date,
                 p_app_user_id);
      ELSE
         SELECT *
         INTO w_status, w_errm
         FROM fn_run_finance_ledger_balance_headoffice (
                 COALESCE (w_branch_code, 0),
                 p_report_name,
                 w_ason_date,
                 w_from_date,
                 w_upto_date,
                 p_app_user_id);
      END IF;

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING MESSAGE = w_errm;
      END IF;
   ELSIF p_report_name IN ('finance_account_balance_report',
                           'finance_cash_transaction_details',
                           'finance_ledger_statements',
                           'finance_teller_balance_report',
                           'finance_teller_transaction_report')
   THEN
      SELECT *
        INTO w_status, w_errm
        FROM fn_run_finance_all_report (p_app_user_id, p_report_name);

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING MESSAGE = w_errm;
      END IF;
   ELSIF p_report_name IN
            ('edu_report_studentfeescollection',
             'edu_report_studentfeesunpaid')
   THEN
      SELECT *
        INTO w_status, w_errm
        FROM fn_run_edu_fees_report (p_app_user_id, p_report_name);

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING MESSAGE = w_errm;
      END IF;
   END IF;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;
      o_status := 'E';
END;
$$