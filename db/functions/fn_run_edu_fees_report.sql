CREATE OR REPLACE FUNCTION public.fn_run_edu_fees_report (
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
   rec_account_list         RECORD;
   rec_date_list            RECORD;
   w_current_business_day   DATE;
   w_opening_date           DATE;
   w_ason_date              DATE;
   w_from_date              DATE;
   w_upto_date              DATE;
   w_sql_stat               TEXT := '';
   w_account_type           VARCHAR;
   w_zero_balance           VARCHAR;
   w_delar_id               INTEGER;
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
   w_closing_balance        NUMERIC (22, 2);
   w_opening_balance        NUMERIC (22, 2);
   w_branch_code            INTEGER;
   w_gl_name                VARCHAR;
   w_cash_gl_code           VARCHAR;
   w_account_number         VARCHAR;
   w_employee_id            VARCHAR;
   w_class_id               VARCHAR;
   w_section_id             VARCHAR;
   w_class_group_id         VARCHAR;
   w_fees_head_code         VARCHAR;
   rec_branch_list          RECORD;
   w_teller_id              NUMERIC (22, 2);
BEGIN
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

   IF p_report_name = 'edu_report_studentfeescollection'
   THEN
      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_class_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_class_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_section_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_section_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_class_group_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_class_group_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_fees_head_code
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_fees_head_code'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      w_sql_stat :=
         'INSERT INTO appauth_report_table_tabular (report_column1,
                                          report_column2,
                                          report_column3,
                                          report_column4,
                                          report_column5,
                                          report_column6,
                                          report_column7,
                                          report_column8,
                                          report_column9,
                                          report_column10,
                                          report_column11,
                                          report_column12,
                                          report_column13,
                                          report_column14,
                                          report_column15,
                                          report_column16,
                                          report_column17,
                                          report_column18,
                                          app_user_id)
     SELECT r.student_roll,
            s.student_name,
            h.head_name,
            r.receive_date,
            r.total_due,
            r.total_paid,
            r.total_waive,
            r.total_overdue,
            r.fine_paid,
            r.fees_due,
            r.fees_overdue,
            r.fees_paid,
            r.fees_waive,
            r.fine_due,
            r.fine_overdue,
            r.fine_waive,
            s.class_id,
             r.receive_month,
       ''' || p_app_user_id || ''' 
       FROM edu_fees_receive_student r,
            edu_fees_head_settings h,
            edu_students_info s
      WHERE h.head_code = r.head_code 
      AND r.student_roll = s.student_roll 
      and r.cancel_by is null ';

      IF w_branch_code IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and s.branch_code = ' || w_branch_code || '';
      END IF;

      IF w_from_date IS NOT NULL AND w_upto_date IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and r.receive_date between '''
            || w_from_date
            || ''' and '''
            || w_upto_date
            || '''';
      END IF;

      IF w_ason_date IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and r.receive_date = ''' || w_ason_date || '''';
      END IF;

      IF w_class_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and s.class_id = ''' || w_class_id || '''';
      END IF;

      IF w_section_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and s.section_id = ''' || w_section_id || '''';
      END IF;

      IF w_class_group_id IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and s.class_group_id = '''
            || w_class_group_id
            || '''';
      END IF;

      IF w_fees_head_code IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and r.head_code = ''' || w_fees_head_code || '''';
      END IF;

      w_sql_stat :=
         w_sql_stat || 'ORDER BY s.class_id, s.section_id, s.student_name ';

      --RAISE EXCEPTION USING MESSAGE = w_sql_stat;

      EXECUTE w_sql_stat;
   END IF;

   IF p_report_name = 'edu_report_studentfeesunpaid'
   THEN
      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_class_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_class_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_section_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_section_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_class_group_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_class_group_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_fees_head_code
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_fees_head_code'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      w_sql_stat :=
         ' INSERT INTO appauth_report_table_tabular (report_column1,
                                          report_column2,
                                          report_column3,
                                          report_column4,
                                          report_column5,
                                          report_column6,
                                          report_column7,
                                          report_column8,
                                          report_column9,
                                          report_column10,
                                          report_column11,
                                          report_column12,
                                          report_column13,
                                          report_column14,
                                          report_column15,
                                          report_column16,
                                          report_column17,
                                          report_column18,
                                          app_user_id)
     SELECT s.class_id,
       cc.class_name,
       student_roll_due,
       s.student_name,
       head_code_due,
       h.head_name,
       due_month,
       due_year,
       total_fees,
       fee_amount,
       fine_amount,
       student_roll_receive,
       head_code_receive,
       receive_month,
       receive_year,
       total_paid,
       fees_paid,
       fees_overdue,
	   ''' || p_app_user_id || ''' 
  FROM (SELECT *
          FROM (  SELECT a.student_roll AS student_roll_due,
                         a.head_code head_code_due,
                         a.due_month,
                         a.due_year,
                         SUM (a.fee_amount + a.fine_amount) TOTAL_FEES,
                         SUM (a.fee_amount) fee_amount,
                         SUM (a.fine_amount) fine_amount
                    FROM edu_fees_due_student a';


      IF w_from_date IS NOT NULL AND w_upto_date IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' WHERE a.due_date between '''
            || w_from_date
            || ''' and '''
            || w_upto_date
            || '''';
      END IF;

      IF w_branch_code IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and a.branch_code = ' || w_branch_code || '';
      END IF;


      IF w_fees_head_code IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and a.head_code = ''' || w_fees_head_code || '''';
      END IF;

      w_sql_stat := w_sql_stat || ' GROUP BY a.student_roll,
                         a.head_code,
                         a.due_month,
                         a.due_year) AA
               LEFT OUTER JOIN
               (  SELECT r.student_roll AS student_roll_receive,
                         r.head_code AS head_code_receive,
                         r.receive_month,
                         r.receive_year,
                         SUM (r.total_paid) total_paid,
                         SUM (r.fees_paid) fees_paid,
                         SUM (r.fees_overdue) fees_overdue
                    FROM edu_fees_receive_student r
                   WHERE r.cancel_by IS NULL
                GROUP BY r.student_roll,
                         r.head_code,
                         r.receive_month,
                         r.receive_year) rr
                  ON     aa.student_roll_due = rr.student_roll_receive
                     AND aa.head_code_due = rr.head_code_receive
                     AND aa.due_month = rr.receive_month
                     AND aa.due_year = rr.receive_year) pp,
       edu_fees_head_settings h,
       edu_students_info s,
       edu_academic_class cc
 WHERE     h.head_code = pp.head_code_due
       AND s.student_roll = pp.student_roll_due
       AND cc.class_id = s.class_id';


      IF w_class_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and cc.class_id = ''' || w_class_id || '''';
      END IF;

      IF w_section_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and s.section_id = ''' || w_section_id || '''';
      END IF;

      IF w_class_group_id IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and s.class_group_id = '''
            || w_class_group_id
            || '''';
      END IF;

      w_sql_stat :=
         w_sql_stat || ' ORDER BY s.class_id, s.section_id, s.student_name ';

      -- RAISE EXCEPTION USING MESSAGE = w_sql_stat;

      EXECUTE w_sql_stat;
   END IF;



   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      IF w_status = 'E'
      THEN
         o_status := w_status;
         o_errm := w_errm;
      ELSE
         o_status := 'E';
         o_errm := SQLERRM;
      END IF;
END;
$$