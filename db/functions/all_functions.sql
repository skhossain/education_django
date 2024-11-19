-- ----------------------------------------------------------------
--  FUNCTION fn_appauth_check_day_month_year
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_appauth_check_day_month_year (
   p_frequenct   CHARACTER,
   p_date        DATE)
   RETURNS BOOLEAN
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_month_end         DATE;
   w_quarter_end       DATE;
   w_half_year_end     DATE;
   w_year_end          DATE;
   w_month_start       DATE;
   w_quarter_start     DATE;
   w_half_year_start   DATE;
   w_year_start        DATE;
BEGIN
   SELECT CAST (
               date_trunc ('month', p_date)
             + INTERVAL '1 months'
             - INTERVAL '1 day'
                AS DATE)
             month_end,
          CAST (
               date_trunc ('quarter', p_date)
             + INTERVAL '3 months'
             - INTERVAL '1 day'
                AS DATE)
             quarter_end,
          CAST (
               date_trunc ('year', p_date)
             + INTERVAL '6 months'
             - INTERVAL '1 day'
                AS DATE)
             half_year_end,
          CAST (
               date_trunc ('year', p_date)
             + INTERVAL '12 months'
             - INTERVAL '1 day'
                AS DATE)
             year_end,
          CAST (date_trunc ('month', p_date) AS DATE)
             month_start,
          CAST (date_trunc ('quarter', p_date) AS DATE)
             quarter_start,
          CAST (
             CAST (EXTRACT (YEAR FROM p_date) AS INTEGER) || '-07-01' AS DATE)
             half_year_start,
          CAST (date_trunc ('year', p_date) AS DATE)
             year_start
     INTO w_month_end,
          w_quarter_end,
          w_half_year_end,
          w_year_end,
          w_month_start,
          w_quarter_start,
          w_half_year_start,
          w_year_start;

   IF p_frequenct = 'D'
   THEN
      RETURN TRUE;
   END IF;

   IF p_frequenct = 'M'
   THEN
      IF w_month_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   IF p_frequenct = 'Q'
   THEN
      IF w_quarter_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   IF p_frequenct = 'H'
   THEN
      IF w_half_year_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   IF p_frequenct = 'Y'
   THEN
      IF w_year_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   RETURN FALSE;
EXCEPTION
   WHEN OTHERS
   THEN
      RETURN FALSE;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_fees_generate
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_fees_generate (
   IN      p_branch_code      INTEGER,
   IN      p_academic_year    INTEGER,
   IN      p_class_id         CHARACTER,
   IN      p_class_group_id   CHARACTER,
   IN      p_section_id       CHARACTER,
   IN      p_process_date     DATE,
   IN      p_student_roll     CHARACTER,
   IN      p_app_user_id      CHARACTER,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
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
   rec_fees_list            RECORD;
   rec_students_list        RECORD;
   w_fine_effective_date    DATE;
   w_effective_date         DATE;
   w_start_date             DATE;
   w_end_date               DATE;
   w_waive_effective_date   DATE;
   w_waive_parsentag        NUMERIC (22, 2) := 0;
   w_waive_amount           NUMERIC (22, 2) := 0;
   w_no_of_month            INTEGER := 1;
   w_fees_sql               VARCHAR;
   w_students_sql           VARCHAR;
   w_waive_sql              VARCHAR;
BEGIN
   w_fees_sql :=
         'SELECT d.effective_date,
             d.fee_amount,
             d.fine_amount,
             d.class_group_id,
             d.class_id,
             d.head_code,
             d.section_id,
             d.pay_freq,
             d.fine_effective_days
        FROM edu_fees_mapping_history d,
             (  SELECT h.head_code,h.class_id,h.class_group_id,h.section_id,
                       h.effective_date,
                       max (h.day_serial) day_serial
                  FROM edu_fees_mapping_history h,
                       (  SELECT head_code,class_id,class_group_id,section_id, max (effective_date) effective_date
                            FROM edu_fees_mapping_history
                           WHERE effective_date <= '''
      || p_process_date
      || '''';

   IF p_class_id IS NOT NULL
   THEN
      w_fees_sql := w_fees_sql || ' and class_id=''' || p_class_id || '''';
   END IF;

   IF p_class_group_id IS NOT NULL
   THEN
      w_fees_sql :=
         w_fees_sql || ' and class_group_id=''' || p_class_group_id || '''';
   END IF;

   IF p_section_id IS NOT NULL
   THEN
      w_fees_sql :=
         w_fees_sql || ' and section_id=''' || p_section_id || '''';
   END IF;

   w_fees_sql :=
         w_fees_sql
      || ' AND is_active
            AND NOT is_deleted
                        GROUP BY head_code,class_id,class_group_id,section_id) m
                 WHERE     h.head_code = m.head_code
                      AND  COALESCE (h.class_id,''#'') = COALESCE (m.class_id,''#'')
                      AND  COALESCE (h.class_group_id,''#'') = COALESCE (m.class_group_id,''#'')
                      AND  COALESCE (h.section_id,''#'') = COALESCE (m.section_id,''#'')
                       AND h.effective_date = m.effective_date ';

   IF p_class_id IS NOT NULL
   THEN
      w_fees_sql := w_fees_sql || ' and h.class_id=''' || p_class_id || '''';
   END IF;

   IF p_class_group_id IS NOT NULL
   THEN
      w_fees_sql :=
         w_fees_sql || ' and h.class_group_id=''' || p_class_group_id || '''';
   END IF;

   IF p_section_id IS NOT NULL
   THEN
      w_fees_sql :=
         w_fees_sql || ' and h.section_id=''' || p_section_id || '''';
   END IF;

   w_fees_sql :=
         w_fees_sql
      || '  
              GROUP BY h.head_code,h.class_id,h.class_group_id,h.section_id, h.effective_date) h
       WHERE     h.head_code = d.head_code
             AND COALESCE (h.class_id,''#'') = COALESCE (d.class_id,''#'')
             AND COALESCE (h.class_group_id,''#'') = COALESCE (d.class_group_id,''#'')
             AND COALESCE (h.section_id,''#'') = COALESCE (d.section_id,''#'')
             AND h.effective_date = d.effective_date
             AND h.day_serial = d.day_serial
             AND d.is_active
             AND NOT d.is_deleted ';

   IF p_class_id IS NOT NULL
   THEN
      w_fees_sql := w_fees_sql || ' and d.class_id=''' || p_class_id || '''';
   END IF;

   IF p_class_group_id IS NOT NULL
   THEN
      w_fees_sql :=
         w_fees_sql || ' and d.class_group_id=''' || p_class_group_id || '''';
   END IF;

   IF p_section_id IS NOT NULL
   THEN
      w_fees_sql :=
         w_fees_sql || ' and d.section_id=''' || p_section_id || '''';
   END IF;

   --RAISE EXCEPTION USING message = w_fees_sql;

   FOR rec_fees_list IN EXECUTE w_fees_sql
   LOOP
      w_students_sql := 'SELECT student_roll,
             academic_year,
             catagory_id,
             class_id,
             class_group_id,
             section_id,
             shift_id,
             student_status,
             branch_code
        FROM edu_students_info 
        where 1=1 ';

      IF p_student_roll IS NOT NULL
      THEN
         w_students_sql :=
               w_students_sql
            || ' and student_roll='''
            || p_student_roll
            || '''';
      END IF;

      IF p_branch_code IS NOT NULL
      THEN
         w_students_sql :=
            w_students_sql || ' and branch_code= ' || p_branch_code;
      END IF;

      IF rec_fees_list.class_id IS NOT NULL
      THEN
         w_students_sql :=
               w_students_sql
            || ' and class_id='''
            || rec_fees_list.class_id
            || '''';
      END IF;

      IF rec_fees_list.class_group_id IS NOT NULL
      THEN
         w_students_sql :=
               w_students_sql
            || ' and class_group_id='''
            || rec_fees_list.class_group_id
            || '''';
      END IF;

      IF rec_fees_list.section_id IS NOT NULL
      THEN
         w_students_sql :=
               w_students_sql
            || ' and section_id='''
            || rec_fees_list.section_id
            || '''';
      END IF;

      --RAISE EXCEPTION USING message = w_students_sql;
      --- do processing
      SELECT CAST (
                FLOOR (
                     DATE_PART ('year', AGE (end_date, start_date)) * 12
                   + DATE_PART ('month', AGE (end_date, start_date))
                   + 1)
                   AS INTEGER) no_of_month,
             start_date,
             end_date
        INTO w_no_of_month, w_start_date, w_end_date
        FROM edu_academic_year
       WHERE academic_year = p_academic_year;

      FOR rec_students_list IN EXECUTE w_students_sql
      LOOP
         IF rec_fees_list.pay_freq = 'M'
         THEN
            w_effective_date := w_start_date;
         ELSE
            w_no_of_month := 1;
            w_effective_date := rec_fees_list.effective_date;
         END IF;

         w_waive_sql :=
               'SELECT d.effective_date,
             d.waiver_parsentag,
             d.waiver_amount
        FROM edu_fees_waiver_mapping_hist d,
             (  SELECT h.head_code,h.class_id,h.class_group_id,h.section_id,
                       h.effective_date,
                       max (h.day_serial) day_serial
                  FROM edu_fees_waiver_mapping_hist h,
                       (  SELECT head_code,class_id,class_group_id,section_id, max (effective_date) effective_date
                            FROM edu_fees_waiver_mapping_hist
                           WHERE     effective_date <= '''
            || w_end_date
            || '''';

         IF rec_fees_list.class_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and class_id='''
               || rec_fees_list.class_id
               || '''';
         END IF;

         IF rec_fees_list.head_code IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and head_code='''
               || rec_fees_list.head_code
               || '''';
         END IF;

         IF rec_fees_list.class_group_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and class_group_id='''
               || rec_fees_list.class_group_id
               || '''';
         END IF;

         IF rec_fees_list.section_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and section_id='''
               || rec_fees_list.section_id
               || '''';
         END IF;

         w_waive_sql :=
               w_waive_sql
            || ' AND is_active
                                 AND NOT is_deleted
                        GROUP BY head_code,class_id,class_group_id,section_id) m
                 WHERE     h.head_code = m.head_code
                      AND  COALESCE (h.class_id,''#'') = COALESCE (m.class_id,''#'')
                      AND  COALESCE (h.class_group_id,''#'') = COALESCE (m.class_group_id,''#'')
                      AND  COALESCE (h.section_id,''#'') = COALESCE (m.section_id,''#'')
                       AND h.effective_date = m.effective_date ';

         IF rec_fees_list.class_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and h.class_id='''
               || rec_fees_list.class_id
               || '''';
         END IF;

         IF rec_fees_list.head_code IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and h.head_code='''
               || rec_fees_list.head_code
               || '''';
         END IF;

         IF rec_fees_list.class_group_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and h.class_group_id='''
               || rec_fees_list.class_group_id
               || '''';
         END IF;

         IF rec_fees_list.section_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and h.section_id='''
               || rec_fees_list.section_id
               || '''';
         END IF;

         w_waive_sql :=
               w_waive_sql
            || '  
              GROUP BY h.head_code,h.class_id,h.class_group_id,h.section_id, h.effective_date) h
       WHERE     h.head_code = d.head_code
             AND COALESCE (h.class_id,''#'') = COALESCE (d.class_id,''#'')
             AND COALESCE (h.class_group_id,''#'') = COALESCE (d.class_group_id,''#'')
             AND COALESCE (h.section_id,''#'') = COALESCE (d.section_id,''#'')
             AND h.effective_date = d.effective_date
             AND h.day_serial = d.day_serial
             AND d.is_active
             AND NOT d.is_deleted ';

         IF rec_fees_list.class_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and d.class_id='''
               || rec_fees_list.class_id
               || '''';
         END IF;

         IF rec_fees_list.head_code IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and d.head_code='''
               || rec_fees_list.head_code
               || '''';
         END IF;

         IF rec_fees_list.class_group_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and d.class_group_id='''
               || rec_fees_list.class_group_id
               || '''';
         END IF;

         IF rec_fees_list.section_id IS NOT NULL
         THEN
            w_waive_sql :=
                  w_waive_sql
               || ' and d.section_id='''
               || rec_fees_list.section_id
               || '''';
         END IF;

         EXECUTE w_waive_sql
            INTO w_waive_effective_date, w_waive_parsentag, w_waive_amount;

         FOR noi IN 1 .. w_no_of_month
         LOOP
            DELETE FROM
               edu_fees_due_student
                  WHERE     student_roll = rec_students_list.student_roll
                        AND academic_year = p_academic_year
                        AND due_date = w_effective_date
                        AND head_code = rec_fees_list.head_code;

            IF rec_fees_list.fine_effective_days > 0
            THEN
               w_fine_effective_date :=
                  w_effective_date + rec_fees_list.fine_effective_days;
            ELSE
               w_fine_effective_date := NULL;
            END IF;

            w_waive_amount :=
               GREATEST (
                  ROUND (
                       rec_fees_list.fee_amount
                     * (COALESCE (w_waive_parsentag, 0.00) / 100)),
                  COALESCE (w_waive_amount, 0.00));

            INSERT INTO edu_fees_due_student (branch_code,
                                              student_roll,
                                              class_id,
                                              class_group_id,
                                              section_id,
                                              academic_year,
                                              head_code,
                                              due_date,
                                              due_month,
                                              due_year,
                                              process_date,
                                              fine_due_date,
                                              fee_amount,
                                              waive_percentage,
                                              waive_amount,
                                              fine_waive,
                                              fine_amount,
                                              app_user_id,
                                              app_data_time)
                    VALUES (
                              rec_students_list.branch_code,
                              rec_students_list.student_roll,
                              rec_students_list.class_id,
                              rec_students_list.class_group_id,
                              rec_students_list.section_id,
                              p_academic_year,
                              rec_fees_list.head_code,
                              w_effective_date,
                              cast (
                                 to_char (w_effective_date, 'MM') AS INTEGER),
                              cast (
                                 to_char (w_effective_date, 'YYYY')
                                    AS INTEGER),
                              p_process_date,
                              w_fine_effective_date,
                              rec_fees_list.fee_amount,
                              COALESCE (w_waive_parsentag, 0.00),
                              COALESCE (w_waive_amount, 0.00),
                              0.00,
                              rec_fees_list.fine_amount,
                              p_app_user_id,
                              current_timestamp);

            w_effective_date :=
               fn_get_next_installment_date (rec_fees_list.pay_freq,
                                             w_start_date,
                                             w_effective_date);
         END LOOP;
      END LOOP;
   END LOOP;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_fees_others_receive
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_fees_others_receive (
   IN      p_student_roll      CHARACTER,
   IN      p_collection_date   DATE,
   IN      p_head_code         CHARACTER,
   IN      p_receive_amount    NUMERIC,
   IN      p_app_user_id       CHARACTER,
       OUT o_status            CHARACTER,
       OUT o_errm              CHARACTER,
       OUT o_transaction_id    CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_ledger_code      VARCHAR := '0';
   w_head_name        VARCHAR := '';
   w_branch_code      INTEGER := 0;
   w_status           VARCHAR;
   w_errm             VARCHAR;
   w_class_id         VARCHAR;
   w_class_group_id   VARCHAR;
   w_section_id       VARCHAR;
BEGIN
   SELECT head_ledger, head_name
     INTO w_ledger_code, w_head_name
     FROM edu_fees_head_settings
    WHERE head_code = p_head_code;

   BEGIN
      SELECT branch_code,
             class_id,
             class_group_id,
             section_id
        INTO w_branch_code,
             w_class_id,
             w_class_group_id,
             w_section_id
        FROM edu_students_info
       WHERE student_roll = p_student_roll;
   END;

   INSERT INTO edu_fees_receive_temp (student_roll,
                                      class_id,
                                      class_group_id,
                                      section_id,
                                      branch_code,
                                      head_code,
                                      head_name,
                                      ledger_code,
                                      total_due,
                                      total_paid,
                                      due_date,
                                      app_user_id,
                                      app_data_time)
        VALUES (p_student_roll,
                w_class_id,
                w_class_group_id,
                w_section_id,
                w_branch_code,
                p_head_code,
                w_head_name,
                w_ledger_code,
                p_receive_amount,
                p_receive_amount,
                p_collection_date,
                p_app_user_id,
                current_timestamp);

   SELECT *
   INTO w_status, w_errm, o_transaction_id
   FROM fn_edu_fees_submit (p_student_roll, p_collection_date, p_app_user_id);

   IF w_status != 'S'
   THEN
      RAISE EXCEPTION USING message = w_errm;
   END IF;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_fees_students
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_fees_students (
   p_student_roll      CHARACTER,
   p_collection_date   DATE)
   RETURNS SETOF edu_fees_month_students
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
   ROWS 1000
AS
$$
DECLARE
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
   w_current_business_day   DATE;
   result_record            edu_fees_month_students;
   rec_student_list         RECORD;
   rec_fees_list            RECORD;
   w_fine_due               NUMERIC (22, 2) := 0;
   w_payment_balance        NUMERIC (22, 2) := 0;
   w_total_paid             NUMERIC (22, 2) := 0;
   w_due_balance            NUMERIC (22, 2) := 0;
   w_waive_amount           NUMERIC (22, 2) := 0;
   w_payment_date           DATE;
BEGIN
   FOR rec_fees_list
      IN (SELECT *
              FROM (  SELECT d.due_serial
                                serial_number,
                             d.branch_code,
                             d.head_code,
                             d.class_id,
                             d.class_group_id,
                             d.section_id,
                             LAG (d.head_code, 1)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                prev_head_code,
                             d.due_date,
                             d.due_month,
                             d.due_year,
                             receive_month,
                             receive_year,
                             d.fine_due_date,
                             d.fee_amount
                                fees_due,
                             d.fine_amount,
                             d.fine_waive,
                             d.waive_amount
                                fees_waive,
                             p.receipt_serial,
                             p.head_code
                                payment_head_code,
                             p.receive_date
                                payment_date,
                             p.total_paid,
                             sum (d.fee_amount)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                due_balance,
                             sum (d.waive_amount)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                waive_balance,
                             sum (d.fine_waive)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                fine_waive_balance,
                             sum (p.total_paid)
                             OVER (
                                PARTITION BY COALESCE (p.head_code, d.head_code),
                                             COALESCE (receive_month, due_month),
                                             COALESCE (receive_year, due_year)
                                ORDER BY p.head_code)
                                payment_balance
                        FROM (  SELECT row_number ()
                                       OVER (
                                          PARTITION BY head_code, due_month, due_year
                                          ORDER BY
                                             head_code,
                                             due_month,
                                             due_year,
                                             due_date) due_serial,
                                       head_code,
                                       due_date,
                                       due_month,
                                       due_year,
                                       fine_due_date,
                                       class_id,
                                       class_group_id,
                                       section_id,
                                       branch_code,
                                       sum (fee_amount) fee_amount,
                                       sum (fine_amount) fine_amount,
                                       sum (waive_amount) waive_amount,
                                       sum (fine_waive) fine_waive
                                  FROM edu_fees_due_student
                                 WHERE     student_roll = p_student_roll
                                       AND cancel_by IS NULL
                              GROUP BY head_code,
                                       due_date,
                                       due_month,
                                       due_year,
                                       fine_due_date,
                                       class_id,
                                       class_group_id,
                                       section_id,
                                       branch_code
                              ORDER BY due_date) d
                             FULL OUTER JOIN
                             (  SELECT row_number ()
                                       OVER (
                                          PARTITION BY head_code,
                                                       receive_month,
                                                       receive_year
                                          ORDER BY
                                             head_code,
                                             receive_date,
                                             receive_month,
                                             receive_year) receipt_serial,
                                       head_code,
                                       class_id,
                                       class_group_id,
                                       section_id,
                                       receive_date,
                                       receive_month,
                                       receive_year,
                                       sum (total_paid) total_paid
                                  FROM edu_fees_receive_student
                                 WHERE     student_roll = p_student_roll
                                       AND cancel_by IS NULL
                              GROUP BY head_code,
                                       receive_date,
                                       receive_month,
                                       receive_year,
                                       class_id,
                                       class_group_id,
                                       section_id
                              ORDER BY receive_date) p
                                ON (    d.head_code = p.head_code
                                    AND d.class_id = p.class_id
                                    AND d.class_group_id = p.class_group_id
                                    AND d.section_id = p.section_id
                                    AND d.due_serial = p.receipt_serial
                                    AND d.due_month = p.receive_month
                                    AND d.due_year = p.receive_year)
                    ORDER BY d.head_code, d.due_date) t
          ORDER BY COALESCE (head_code, payment_head_code),
                   class_id,
                   COALESCE (serial_number, receipt_serial),
                   due_month,
                   due_year)
   LOOP
      IF rec_fees_list.payment_date < rec_fees_list.fine_due_date
      THEN
         w_payment_balance := COALESCE (rec_fees_list.payment_balance, 0.00);
      ELSE
         w_payment_balance := 0.00;
      END IF;

      IF rec_fees_list.payment_date IS NOT NULL
      THEN
         w_total_paid := COALESCE (rec_fees_list.payment_balance, 0.00);
         w_payment_date := rec_fees_list.payment_date;
      END IF;

      IF w_payment_date < rec_fees_list.due_date
      THEN
         w_payment_date := NULL;
         w_total_paid := 0.00;
      END IF;

      IF     (rec_fees_list.due_balance - w_payment_balance) > 0
         AND rec_fees_list.fine_due_date < p_collection_date
      THEN
         w_fine_due := rec_fees_list.fine_amount;
      ELSE
         w_fine_due := 0.00;
      END IF;

      SELECT sum (waive_amount) waive_amount
        INTO w_waive_amount
        FROM edu_fees_waive_student
       WHERE     student_roll = p_student_roll
             AND head_code = rec_fees_list.head_code
             AND fees_month = rec_fees_list.due_month
             AND fees_year = rec_fees_list.due_year
             AND cancel_by IS NULL;

      w_waive_amount := COALESCE (w_waive_amount, 0.00);

      result_record.serial_number := rec_fees_list.serial_number;
      result_record.branch_code := rec_fees_list.branch_code;
      result_record.head_code := rec_fees_list.head_code;
      result_record.class_id := rec_fees_list.class_id;
      result_record.class_group_id := rec_fees_list.class_group_id;
      result_record.section_id := rec_fees_list.section_id;
      result_record.due_date := rec_fees_list.due_date;
      result_record.due_month := rec_fees_list.due_month;
      result_record.due_year := rec_fees_list.due_year;
      result_record.fine_due := w_fine_due;
      result_record.fees_due := rec_fees_list.fees_due;
      result_record.fine_waive := COALESCE (rec_fees_list.fine_waive, 0.00);
      result_record.fees_waive := COALESCE (rec_fees_list.fees_waive, 0.00);
      result_record.total_waive :=
         result_record.fees_waive + result_record.fine_waive + w_waive_amount;
      result_record.total_due :=
         (  result_record.fine_due
          + result_record.fees_due
          - result_record.total_waive);

      IF rec_fees_list.serial_number <> 1
      THEN
         w_due_balance := w_due_balance + result_record.total_due;
      ELSE
         w_due_balance := result_record.total_due;
      END IF;

      result_record.payment_date := w_payment_date;
      result_record.total_paid := w_total_paid;
      result_record.due_balance := w_due_balance;
      result_record.payment_balance :=
         COALESCE (rec_fees_list.payment_balance, 0.00);
      result_record.actual_due :=
         greatest (
            least (
                 result_record.due_balance
               + w_fine_due
               - result_record.payment_balance,
               (rec_fees_list.fees_due + w_fine_due)),
            0.00);

      RETURN NEXT
         result_record;
   END LOOP;

   RETURN;
EXCEPTION
   WHEN OTHERS
   THEN
      NULL;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_fees_students_old
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_fees_students_old (
   p_student_roll      CHARACTER,
   p_collection_date   DATE)
   RETURNS SETOF edu_fees_students
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
   ROWS 1000
AS
$$
DECLARE
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
   w_current_business_day   DATE;
   result_record            edu_fees_students;
   rec_student_list         RECORD;
   rec_fees_list            RECORD;
   w_fine_due               NUMERIC (22, 2) := 0;
   w_payment_balance        NUMERIC (22, 2) := 0;
   w_total_paid             NUMERIC (22, 2) := 0;
   w_due_balance            NUMERIC (22, 2) := 0;
   w_payment_date           DATE;
BEGIN
   FOR rec_fees_list
      IN (SELECT *
              FROM (  SELECT d.due_serial
                                serial_number,
                             d.branch_code,
                             d.head_code,
                             d.class_id,
                             d.class_group_id,
                             d.section_id,
                             LAG (d.head_code, 1)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                prev_head_code,
                             d.due_date,
                             d.fine_due_date,
                             d.fee_amount
                                fees_due,
                             d.fine_amount,
                             d.fine_waive,
                             d.waive_amount
                                fees_waive,
                             p.receipt_serial,
                             p.head_code
                                payment_head_code,
                             p.receive_date
                                payment_date,
                             p.total_paid,
                             sum (d.fee_amount)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                due_balance,
                             sum (d.waive_amount)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                waive_balance,
                             sum (d.fine_waive)
                             OVER (PARTITION BY d.head_code
                                   ORDER BY d.head_code, d.due_date)
                                fine_waive_balance,
                             sum (p.total_paid)
                             OVER (PARTITION BY COALESCE (p.head_code, d.head_code)
                                   ORDER BY p.head_code)
                                payment_balance
                        FROM (  SELECT row_number ()
                                       OVER (PARTITION BY head_code
                                             ORDER BY head_code, due_date)
                                          due_serial,
                                       head_code,
                                       due_date,
                                       due_month,
                                       due_year,
                                       fine_due_date,
                                       class_id,
                                       class_group_id,
                                       section_id,
                                       branch_code,
                                       sum (fee_amount)
                                          fee_amount,
                                       sum (fine_amount)
                                          fine_amount,
                                       sum (waive_amount)
                                          waive_amount,
                                       sum (fine_waive)
                                          fine_waive
                                  FROM edu_fees_due_student
                                 WHERE     student_roll = p_student_roll
                                       AND cancel_by IS NULL
                              GROUP BY head_code,
                                       due_date,
                                       due_month,
                                       due_year,
                                       fine_due_date,
                                       class_id,
                                       class_group_id,
                                       section_id,
                                       branch_code
                              ORDER BY due_date) d
                             FULL OUTER JOIN
                             (  SELECT row_number ()
                                       OVER (PARTITION BY head_code
                                             ORDER BY head_code, receive_date)
                                          receipt_serial,
                                       head_code,
                                       class_id,
                                       class_group_id,
                                       section_id,
                                       receive_date,
                                       receive_month,
                                       receive_year,
                                       sum (total_paid)
                                          total_paid
                                  FROM edu_fees_receive_student
                                 WHERE     student_roll = p_student_roll
                                       AND cancel_by IS NULL
                              GROUP BY head_code,
                                       receive_date,
                                       receive_month,
                                       receive_year,
                                       class_id,
                                       class_group_id,
                                       section_id
                              ORDER BY receive_date) p
                                ON (    d.head_code = p.head_code
                                    AND d.class_id = p.class_id
                                    AND d.class_group_id = p.class_group_id
                                    AND d.section_id = p.section_id
                                    AND d.due_serial = p.receipt_serial)
                    ORDER BY d.head_code, d.due_date) t
          ORDER BY COALESCE (head_code, payment_head_code),
                   class_id,
                   COALESCE (serial_number, receipt_serial))
   LOOP
      IF rec_fees_list.payment_date < rec_fees_list.fine_due_date
      THEN
         w_payment_balance := COALESCE (rec_fees_list.payment_balance, 0.00);
      ELSE
         w_payment_balance := 0.00;
      END IF;

      IF rec_fees_list.payment_date IS NOT NULL
      THEN
         w_total_paid := COALESCE (rec_fees_list.payment_balance, 0.00);
         w_payment_date := rec_fees_list.payment_date;
      END IF;

      IF w_payment_date < rec_fees_list.due_date
      THEN
         w_payment_date := NULL;
         w_total_paid := 0.00;
      END IF;

      IF     (rec_fees_list.due_balance - w_payment_balance) > 0
         AND rec_fees_list.fine_due_date < p_collection_date
      THEN
         w_fine_due := rec_fees_list.fine_amount;
      ELSE
         w_fine_due := 0.00;
      END IF;

      result_record.serial_number := rec_fees_list.serial_number;
      result_record.branch_code := rec_fees_list.branch_code;
      result_record.head_code := rec_fees_list.head_code;
      result_record.class_id := rec_fees_list.class_id;
      result_record.class_group_id := rec_fees_list.class_group_id;
      result_record.section_id := rec_fees_list.section_id;
      result_record.due_date := rec_fees_list.due_date;
      result_record.fine_due := w_fine_due;
      result_record.fees_due := rec_fees_list.fees_due;
      result_record.fine_waive := COALESCE (rec_fees_list.fine_waive, 0.00);
      result_record.fees_waive := COALESCE (rec_fees_list.fees_waive, 0.00);
      result_record.total_waive :=
         result_record.fees_waive + result_record.fine_waive;
      result_record.total_due :=
         (  result_record.fine_due
          + result_record.fees_due
          - result_record.total_waive);

      IF rec_fees_list.serial_number <> 1
      THEN
         w_due_balance := w_due_balance + result_record.total_due;
      ELSE
         w_due_balance := result_record.total_due;
      END IF;

      result_record.payment_date := w_payment_date;
      result_record.total_paid := w_total_paid;
      result_record.due_balance := w_due_balance;
      result_record.payment_balance :=
         COALESCE (rec_fees_list.payment_balance, 0.00);
      result_record.actual_due :=
         greatest (
            least (
                 result_record.due_balance
               + w_fine_due
               - result_record.payment_balance
               - result_record.total_waive,
               (  rec_fees_list.fees_due
                + w_fine_due
                - result_record.total_waive)),
            0.00);

      RETURN NEXT
         result_record;
   END LOOP;

   RETURN;
EXCEPTION
   WHEN OTHERS
   THEN
      NULL;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_fees_submit
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_fees_submit (
   IN      p_student_roll      CHARACTER,
   IN      p_collection_date   DATE,
   IN      p_app_user_id       CHARACTER,
       OUT o_status            CHARACTER,
       OUT o_errm              CHARACTER,
       OUT o_transaction_id    CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_tran_gl_code           VARCHAR := '0';
   w_contra_gl_code         VARCHAR := '0';
   w_cash_gl_code           VARCHAR := '0';
   w_account_number         VARCHAR := '0';
   w_debit_credit           VARCHAR;
   w_tran_type              VARCHAR;
   w_serial_no              INTEGER := 0;
   w_batch_number           INTEGER := 0;
   w_tran_amount            NUMERIC (22, 2) := 0;
   w_total_receive_amount   NUMERIC (22, 2) := 0;
   w_tran_naration          VARCHAR;
   w_branch_code            INTEGER := 0;
   rec_fees_list            RECORD;
   w_transaction_id         VARCHAR;
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
BEGIN
   w_transaction_id :=
      fn_get_inventory_number (30001,
                               100,
                               'FE',
                               'Student Fee Receive',
                               8);

   BEGIN
      SELECT cash_gl_code
        INTO STRICT w_cash_gl_code
        FROM finance_application_settings;
   EXCEPTION
      WHEN NO_DATA_FOUND
      THEN
         RAISE EXCEPTION
         USING message = 'Cash in Hand Ledger is Not Confired!';
   END;

   BEGIN
      SELECT branch_code
        INTO w_branch_code
        FROM edu_students_info
       WHERE student_roll = p_student_roll;
   END;

   ---RAISE EXCEPTION USING message = 'A';

   FOR rec_fees_list
      IN (SELECT *
           FROM edu_fees_receive_temp
          WHERE     app_user_id = p_app_user_id
                AND student_roll = p_student_roll
                AND total_paid > 0)
   LOOP
      IF rec_fees_list.total_paid > 0
      THEN
         w_total_receive_amount :=
            w_total_receive_amount + rec_fees_list.total_paid;

         w_tran_gl_code := rec_fees_list.ledger_code;
         w_contra_gl_code := w_cash_gl_code;
         w_account_number := '0';
         w_tran_amount := rec_fees_list.total_paid;
         w_tran_naration :=
            rec_fees_list.head_name || ' - ' || p_student_roll;
         w_serial_no := w_serial_no + 1;
         w_debit_credit := 'C';
         w_tran_type := 'FEES';

         INSERT INTO finance_transaction_table (branch_code,
                                                transaction_date,
                                                batch_serial,
                                                account_number,
                                                tran_gl_code,
                                                contra_gl_code,
                                                tran_debit_credit,
                                                tran_type,
                                                tran_amount,
                                                available_balance,
                                                tran_person_phone,
                                                tran_person_name,
                                                tran_document_prefix,
                                                tran_document_number,
                                                tran_sign_verified,
                                                system_posted_tran,
                                                transaction_narration,
                                                app_user_id,
                                                app_data_time)
              VALUES (rec_fees_list.branch_code,
                      p_collection_date,
                      w_serial_no,
                      '0',
                      w_tran_gl_code,
                      w_contra_gl_code,
                      w_debit_credit,
                      w_tran_type,
                      w_tran_amount,
                      0,
                      '',
                      NULL,
                      NULL,
                      p_student_roll,
                      FALSE,
                      TRUE,
                      w_tran_naration,
                      p_app_user_id,
                      current_timestamp);

         w_tran_gl_code := w_cash_gl_code;
         w_contra_gl_code := rec_fees_list.ledger_code;
         w_account_number := '0';
         w_tran_amount := rec_fees_list.total_paid;
         w_tran_naration :=
            rec_fees_list.head_name || ' - ' || p_student_roll;
         w_serial_no := w_serial_no + 1;
         w_debit_credit := 'D';
         w_tran_type := 'FEES';

         INSERT INTO finance_transaction_table (branch_code,
                                                transaction_date,
                                                batch_serial,
                                                account_number,
                                                tran_gl_code,
                                                contra_gl_code,
                                                tran_debit_credit,
                                                tran_type,
                                                tran_amount,
                                                available_balance,
                                                tran_person_phone,
                                                tran_person_name,
                                                tran_document_prefix,
                                                tran_document_number,
                                                tran_sign_verified,
                                                system_posted_tran,
                                                transaction_narration,
                                                app_user_id,
                                                app_data_time)
              VALUES (rec_fees_list.branch_code,
                      p_collection_date,
                      w_serial_no,
                      '0',
                      w_tran_gl_code,
                      w_contra_gl_code,
                      w_debit_credit,
                      w_tran_type,
                      w_tran_amount,
                      0,
                      '',
                      NULL,
                      NULL,
                      p_student_roll,
                      FALSE,
                      TRUE,
                      w_tran_naration,
                      p_app_user_id,
                      current_timestamp);

         IF rec_fees_list.total_paid > rec_fees_list.total_due
         THEN
            RAISE EXCEPTION
            USING message = 'Receive amount more then due amount!';
         END IF;

         INSERT INTO edu_fees_receive_student (branch_code,
                                               transaction_id,
                                               student_roll,
                                               class_id,
                                               class_group_id,
                                               section_id,
                                               head_code,
                                               ledger_code,
                                               receive_date,
                                               receive_year,
                                               receive_month,
                                               due_date,
                                               fees_due,
                                               fees_waive,
                                               fine_due,
                                               fine_waive,
                                               total_due,
                                               total_waive,
                                               fees_paid,
                                               fine_paid,
                                               total_paid,
                                               fees_overdue,
                                               fine_overdue,
                                               total_overdue,
                                               auth_by,
                                               auth_on,
                                               cancel_by,
                                               cancel_on,
                                               app_user_id,
                                               app_data_time)
                 VALUES (
                           rec_fees_list.branch_code,
                           w_transaction_id,
                           p_student_roll,
                           rec_fees_list.class_id,
                           rec_fees_list.class_group_id,
                           rec_fees_list.section_id,
                           rec_fees_list.head_code,
                           rec_fees_list.ledger_code,
                           p_collection_date,
                           rec_fees_list.due_year,
                           rec_fees_list.due_month,
                           rec_fees_list.due_date,
                           rec_fees_list.fees_due,
                           rec_fees_list.fees_waive,
                           rec_fees_list.fine_due,
                           rec_fees_list.fine_waive,
                           rec_fees_list.total_due,
                           rec_fees_list.total_waive,
                             rec_fees_list.total_paid
                           - rec_fees_list.fine_waive
                           - rec_fees_list.fine_due,              ---fees_paid
                           rec_fees_list.fine_due - rec_fees_list.fine_waive, ---fine_paid
                           rec_fees_list.total_paid,
                             rec_fees_list.fees_due
                           - rec_fees_list.total_paid
                           + rec_fees_list.fine_due
                           - rec_fees_list.fine_waive,         ---fees_overdue
                           rec_fees_list.fine_overdue,
                           rec_fees_list.total_overdue,
                           p_app_user_id,
                           current_timestamp,
                           NULL,
                           NULL,
                           p_app_user_id,
                           current_timestamp);
      END IF;
   END LOOP;

   BEGIN
      SELECT *
        INTO w_status, w_errm, w_batch_number
        FROM fn_finance_post_tran (w_branch_code,
                                   p_app_user_id,
                                   'FEES',
                                   p_collection_date,
                                   'Fee Receive ' || p_student_roll,
                                   'FEES');

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING message = w_errm;
      ELSE
         INSERT INTO edu_fees_receive_summary (branch_code,
                                               transaction_id,
                                               student_roll,
                                               receive_date,
                                               receive_amount,
                                               tran_batch_number,
                                               auth_by,
                                               auth_on,
                                               app_user_id,
                                               app_data_time)
              VALUES (w_branch_code,
                      w_transaction_id,
                      p_student_roll,
                      p_collection_date,
                      w_total_receive_amount,
                      w_batch_number,
                      p_app_user_id,
                      current_timestamp,
                      p_app_user_id,
                      current_timestamp);

         o_transaction_id := w_transaction_id;

         DELETE FROM
            edu_fees_receive_temp
               WHERE     app_user_id = p_app_user_id
                     AND student_roll = p_student_roll;
      END IF;
   END;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_fees_tempdata
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_fees_tempdata (
   IN      p_student_roll      CHARACTER,
   IN      p_collection_date   DATE,
   IN      p_app_user_id       CHARACTER,
       OUT o_status            CHARACTER,
       OUT o_errm              CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_status            VARCHAR;
   w_errm              VARCHAR;
   rec_fees_due_list   RECORD;
BEGIN
   DELETE FROM edu_fees_receive_temp
         WHERE app_user_id = p_app_user_id;

   INSERT INTO edu_fees_receive_temp (branch_code,
                                      student_roll,
                                      class_id,
                                      class_group_id,
                                      section_id,
                                      head_code,
                                      head_name,
                                      ledger_code,
                                      due_date,
                                      due_month,
                                      due_year,
                                      total_due,
                                      total_paid,
                                      total_waive,
                                      fees_due,
                                      fine_due,
                                      fees_waive,
                                      fine_waive,
                                      total_overdue,
                                      app_user_id,
                                      app_data_time)
        SELECT d.branch_code,
               p_student_roll student_roll,
               d.class_id,
               d.class_group_id,
               d.section_id,
               h.head_code,
               h.head_name,
               h.head_ledger,
               d.due_date,
               d.due_month,
               d.due_year,
               d.actual_due,
               NULL,
               d.total_waive,
               d.fees_due,
               d.fine_due,
               d.fees_waive,
               d.fine_waive,
               0.00,
               p_app_user_id,
               current_timestamp
          FROM fn_edu_fees_students (p_student_roll, p_collection_date) d,
               edu_fees_head_settings h
         WHERE     d.head_code = h.head_code
               AND d.actual_due > 0
               AND d.due_date <= p_collection_date
      ORDER BY h.head_code, d.serial_number;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_fees_waive_tempdata
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_fees_waive_tempdata (
   IN      p_student_roll   CHARACTER,
   IN      p_waive_date     DATE,
   IN      p_app_user_id    CHARACTER,
       OUT o_status         CHARACTER,
       OUT o_errm           CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_status            VARCHAR;
   w_errm              VARCHAR;
   rec_fees_due_list   RECORD;
BEGIN
   DELETE FROM edu_fees_receive_temp
         WHERE app_user_id = p_app_user_id;

   INSERT INTO edu_fees_receive_temp (student_roll,
                                      head_code,
                                      head_name,
                                      ledger_code,
                                      due_date,
                                      total_due,
                                      total_paid,
                                      total_overdue,
                                      total_waiver,
                                      fine_payable,
                                      fees_payable,
                                      app_user_id,
                                      app_data_time)
        SELECT p_student_roll student_roll,
               h.head_code,
               h.head_name,
               h.head_ledger,
               d.due_date,
               d.actual_due,
               NULL,
               0.00,
               d.total_waiver,
               d.fine_due,
               d.fees_due,
               p_app_user_id,
               current_timestamp
          FROM fn_edu_fees_students (p_student_roll, current_date) d,
               edu_fees_head_settings h
         WHERE     d.head_code = h.head_code
               AND (d.due_balance - d.payment_balance) > 0
               AND d.due_date <= p_collection_date
      ORDER BY h.head_code, d.serial_number;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_result_grade_update
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_result_grade_update (
   IN      p_academic_year   INTEGER,
   IN      p_term_id         INTEGER,
   IN      p_class_id        CHARACTER,
       OUT o_status          CHARACTER,
       OUT o_errm            CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_status             VARCHAR;
   w_errm               VARCHAR;
   rec_students_list    RECORD;
   w_final_result_gpa   NUMERIC;
   w_final_grade_name   VARCHAR;
BEGIN
   FOR rec_students_list IN (SELECT *
                               FROM edu_students_info
                              WHERE class_id = p_class_id)
   LOOP
      SELECT result_gpa, grade_name
        INTO w_final_result_gpa, w_final_grade_name
        FROM fn_get_final_result_gpa (p_academic_year,
                                      p_term_id,
                                      p_class_id,
                                      rec_students_list.student_roll,
                                      'Admin');

      UPDATE edu_students_info
         SET final_result_gpa = w_final_result_gpa,
             final_grade_name = w_final_grade_name
       WHERE student_roll = rec_students_list.student_roll;
   END LOOP;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_edu_result_processing
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_edu_result_processing (
   IN      p_academic_year    INTEGER,
   IN      p_term_id          INTEGER,
   IN      p_class_id         CHARACTER,
   IN      p_class_group_id   CHARACTER,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_status            VARCHAR;
   w_errm              VARCHAR;
   rec_students_list   RECORD;
BEGIN
   DELETE FROM edu_result_processing
         WHERE class_id = p_class_id AND term_id = p_term_id;

   SELECT *
     INTO w_status, w_errm
     FROM fn_view_class_subject_mark (p_academic_year,
                                      p_term_id,
                                      p_class_id,
                                      p_class_group_id,
                                      'Admin');


   INSERT INTO edu_result_processing
      SELECT total_subject item_count,
             (CASE WHEN subject_serial = 1 THEN 'Y' ELSE NULL END) row_span,
             subject_serial,
             student_roll,
             class_roll,
             student_name,
             subject_name,
             total_obtain_marks,
             total_marks,
             final_result_gpa,
             final_grade_name,
             result_gpa,
             grade_name,
             academic_year,
             class_id,
             subject_id,
             p_term_id term_id
        FROM (SELECT count (student_roll)
                     OVER (PARTITION BY student_roll
                           ORDER BY cast (student_roll AS BIGINT))
                        total_subject,
                     ROW_NUMBER ()
                     OVER (
                        PARTITION BY student_roll
                        ORDER BY cast (student_roll AS BIGINT), subject_name)
                        subject_serial,
                     student_roll,
                     class_roll,
                     student_name,
                     final_result_gpa,
                     final_grade_name,
                     subject_name,
                     total_obtain_marks,
                     sum (total_obtain_marks)
                     OVER (PARTITION BY student_roll
                           ORDER BY cast (student_roll AS BIGINT))
                        total_obtain_marks_subject,
                     sum (total_marks)
                     OVER (PARTITION BY student_roll
                           ORDER BY cast (student_roll AS BIGINT))
                        total_marks_subject,
                     total_marks,
                     result_gpa,
                     grade_name,
                     academic_year,
                     class_id,
                     subject_id
                FROM (  SELECT s.student_roll,
                               s.class_roll,
                               s.student_name,
                               s.final_result_gpa,
                               s.final_grade_name,
                               sub.subject_name,
                               t.total_obtain_marks,
                               t.total_marks,
                               t.result_gpa,
                               t.grade_name,
                               t.academic_year,
                               t.class_id,
                               t.subject_id
                          FROM edu_subjectmarktemp t,
                               (SELECT s.student_roll,
                                       s.class_roll,
                                       s.student_name,
                                       (SELECT result_gpa
                                        FROM fn_get_final_result_gpa (
                                                p_academic_year,
                                                p_term_id,
                                                p_class_id,
                                                student_roll,
                                                'Admin')) final_result_gpa,
                                       (SELECT grade_name
                                        FROM fn_get_final_result_gpa (
                                                p_academic_year,
                                                p_term_id,
                                                p_class_id,
                                                student_roll,
                                                'Admin')) final_grade_name
                                  FROM edu_students_info s
                                 WHERE     s.academic_year = p_academic_year
                                       AND s.class_id = p_class_id) s,
                               edu_subject_list sub
                         WHERE     t.student_roll = s.student_roll
                               AND sub.subject_id = t.subject_id
                               AND t.academic_year = p_academic_year
                               AND t.class_id = p_class_id
                               AND t.app_user_id = 'Admin'
                      ORDER BY cast (s.class_roll AS BIGINT)) data)
             final_data;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_exam_mark_publish
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_exam_mark_publish (
   IN      p_academic_year_id   INTEGER,
   IN      p_term_id            INTEGER,
   IN      p_class_id           CHARACTER,
   IN      p_class_group_id     CHARACTER,
   IN      p_app_user_id        CHARACTER,
       OUT o_status             CHARACTER,
       OUT o_errm               CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_students         RECORD;
   w_subjects         RECORD;
   w_subject_result   RECORD;
   w_final_result     RECORD;
   w_details_result   RECORD;
   w_check_result     RECORD;
   w_single_result    RECORD;
   w_class_group_id   VARCHAR;
BEGIN
   FOR w_students
      IN (  SELECT student_roll, class_group_id
              FROM edu_students_info s
             WHERE     s.academic_year = p_academic_year_id
                   AND s.class_id = p_class_id
                   AND CASE
                          WHEN p_class_group_id IS NULL
                          THEN
                             s.class_group_id IS NULL
                          ELSE
                             s.class_group_id = p_class_group_id
                       END
          ORDER BY s.student_roll)
   LOOP
      w_class_group_id := w_students.class_group_id;

      --RAISE EXCEPTION USING MESSAGE = w_students.student_roll;

      FOR w_subjects
         IN (SELECT subject_id
              FROM edu_subject_choice sub
             WHERE     sub.class_id = p_class_id
                   AND sub.student_roll = w_students.student_roll)
      LOOP
         --RAISE EXCEPTION USING MESSAGE = w_students.student_roll;

         --'Error in single result calculation for student '
         -- || w_students.student_roll || 'Subject' || w_subjects.subject_id;

         SELECT *
           INTO w_subject_result
           FROM fn_set_subject_mark_by_student (p_academic_year_id,
                                                p_term_id,
                                                p_class_id,
                                                w_class_group_id,
                                                w_students.student_roll,
                                                w_subjects.subject_id,
                                                p_app_user_id);
      END LOOP;


      SELECT *
        INTO w_final_result
        FROM fn_set_final_exam_mark (p_academic_year_id,
                                     p_term_id,
                                     p_class_id,
                                     w_students.student_roll,
                                     p_app_user_id);
   END LOOP;

   SELECT *
     INTO w_details_result
     FROM fn_storing_dtails_exam_marks (p_academic_year_id,
                                        p_term_id,
                                        p_class_id,
                                        w_class_group_id,
                                        p_app_user_id);

   SELECT *
     INTO w_single_result
     FROM fn_store_single_exam_mark (p_academic_year_id,
                                     p_term_id,
                                     p_class_id,
                                     w_class_group_id,
                                     p_app_user_id);

   --RAISE EXCEPTION USING MESSAGE = 'No Enter';
   o_status := 'S';
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;
      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_fin_check_day_month_year
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_fin_check_day_month_year (
   p_frequenct   CHARACTER,
   p_date        DATE)
   RETURNS BOOLEAN
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_month_end         DATE;
   w_quarter_end       DATE;
   w_half_year_end     DATE;
   w_year_end          DATE;
   w_month_start       DATE;
   w_quarter_start     DATE;
   w_half_year_start   DATE;
   w_year_start        DATE;
BEGIN
   SELECT CAST (
               date_trunc ('month', p_date)
             + INTERVAL '1 months'
             - INTERVAL '1 day'
                AS DATE)
             month_end,
          CAST (
               date_trunc ('quarter', p_date)
             + INTERVAL '3 months'
             - INTERVAL '1 day'
                AS DATE)
             quarter_end,
          CAST (
               date_trunc ('year', p_date)
             + INTERVAL '6 months'
             - INTERVAL '1 day'
                AS DATE)
             half_year_end,
          CAST (
               date_trunc ('year', p_date)
             + INTERVAL '12 months'
             - INTERVAL '1 day'
                AS DATE)
             year_end,
          CAST (date_trunc ('month', p_date) AS DATE)
             month_start,
          CAST (date_trunc ('quarter', p_date) AS DATE)
             quarter_start,
          CAST (
             CAST (EXTRACT (YEAR FROM p_date) AS INTEGER) || '-07-01' AS DATE)
             half_year_start,
          CAST (date_trunc ('year', p_date) AS DATE)
             year_start
     INTO w_month_end,
          w_quarter_end,
          w_half_year_end,
          w_year_end,
          w_month_start,
          w_quarter_start,
          w_half_year_start,
          w_year_start;

   IF p_frequenct = 'D'
   THEN
      RETURN TRUE;
   END IF;

   IF p_frequenct = 'M'
   THEN
      IF w_month_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   IF p_frequenct = 'Q'
   THEN
      IF w_quarter_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   IF p_frequenct = 'H'
   THEN
      IF w_half_year_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   IF p_frequenct = 'Y'
   THEN
      IF w_year_end = p_date
      THEN
         RETURN TRUE;
      END IF;
   END IF;

   RETURN FALSE;
EXCEPTION
   WHEN OTHERS
   THEN
      RETURN FALSE;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_acbal_hist
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_acbal_hist (
   IN      p_account_number   CHARACTER,
   IN      p_ason_date        DATE,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   rec_account_list             RECORD;
   rec_date_list                RECORD;
   w_calculate_date             DATE;
   w_current_business_day       DATE;
   w_total_debit_sum            NUMERIC (22, 2) := 0;
   w_total_credit_sum           NUMERIC (22, 2) := 0;
   w_account_balance            NUMERIC (22, 2) := 0;
   w_account_balance_prev       NUMERIC (22, 2) := 0;
   w_cum_debit_sum              NUMERIC (22, 2) := 0;
   w_cum_credit_sum             NUMERIC (22, 2) := 0;
   w_principal_credit_sum       NUMERIC (22, 2);
   w_principal_debit_sum        NUMERIC (22, 2);
   w_principal_balance          NUMERIC (22, 2);
   w_profit_credit_sum          NUMERIC (22, 2);
   w_profit_debit_sum           NUMERIC (22, 2);
   w_profit_balance             NUMERIC (22, 2);
   w_charge_credit_sum          NUMERIC (22, 2);
   w_charge_debit_sum           NUMERIC (22, 2);
   w_charge_balance             NUMERIC (22, 2);
   w_cum_charge_credit_sum      NUMERIC (22, 2);
   w_cum_charge_debit_sum       NUMERIC (22, 2);
   w_cum_principal_credit_sum   NUMERIC (22, 2);
   w_cum_principal_debit_sum    NUMERIC (22, 2);
   w_cum_profit_credit_sum      NUMERIC (22, 2);
   w_cum_profit_debit_sum       NUMERIC (22, 2);
   w_status                     VARCHAR;
   w_errm                       VARCHAR;
BEGIN
   FOR rec_account_list
      IN (SELECT branch_code,
                 account_number,
                 account_balance,
                 last_transaction_date,
                 last_balance_update
            FROM finance_accounts_balance
           WHERE account_number = p_account_number AND NOT is_balance_updated)
   LOOP
      w_calculate_date := rec_account_list.last_balance_update;

      BEGIN
         SELECT COALESCE (account_balance, 0.00),
                COALESCE (cum_credit_sum, 0.00),
                COALESCE (cum_debit_sum, 0.00),
                COALESCE (principal_credit_sum, 0.00),
                COALESCE (principal_debit_sum, 0.00),
                COALESCE (principal_balance, 0.00),
                COALESCE (profit_credit_sum, 0.00),
                COALESCE (profit_debit_sum, 0.00),
                COALESCE (profit_balance, 0.00),
                COALESCE (charge_credit_sum, 0.00),
                COALESCE (charge_debit_sum, 0.00),
                COALESCE (charge_balance, 0.00),
                COALESCE (cum_charge_credit_sum, 0.00),
                COALESCE (cum_charge_debit_sum, 0.00),
                COALESCE (cum_principal_credit_sum, 0.00),
                COALESCE (cum_principal_debit_sum, 0.00),
                COALESCE (cum_profit_credit_sum, 0.00),
                COALESCE (cum_profit_debit_sum, 0.00)
           INTO w_account_balance,
                w_cum_credit_sum,
                w_cum_debit_sum,
                w_principal_credit_sum,
                w_principal_debit_sum,
                w_principal_balance,
                w_profit_credit_sum,
                w_profit_debit_sum,
                w_profit_balance,
                w_charge_credit_sum,
                w_charge_debit_sum,
                w_charge_balance,
                w_cum_charge_credit_sum,
                w_cum_charge_debit_sum,
                w_cum_principal_credit_sum,
                w_cum_principal_debit_sum,
                w_cum_profit_credit_sum,
                w_cum_profit_debit_sum
           FROM finance_accounts_balance_hist h
          WHERE     h.account_number = rec_account_list.account_number
                AND h.transaction_date =
                    (SELECT max (transaction_date)
                      FROM finance_accounts_balance_hist
                     WHERE     account_number =
                               rec_account_list.account_number
                           AND transaction_date <= w_calculate_date - 1);
      END;

      w_account_balance := COALESCE (w_account_balance, 0.00);
      w_cum_credit_sum := COALESCE (w_cum_credit_sum, 0.00);
      w_cum_debit_sum := COALESCE (w_cum_debit_sum, 0.00);
      w_principal_credit_sum := COALESCE (w_principal_credit_sum, 0.00);
      w_principal_debit_sum := COALESCE (w_principal_debit_sum, 0.00);
      w_principal_balance := COALESCE (w_principal_balance, 0.00);
      w_profit_credit_sum := COALESCE (w_profit_credit_sum, 0.00);
      w_profit_debit_sum := COALESCE (w_profit_debit_sum, 0.00);
      w_profit_balance := COALESCE (w_profit_balance, 0.00);
      w_charge_credit_sum := COALESCE (w_charge_credit_sum, 0.00);
      w_charge_debit_sum := COALESCE (w_charge_debit_sum, 0.00);
      w_charge_balance := COALESCE (w_charge_balance, 0.00);
      w_cum_charge_credit_sum := COALESCE (w_cum_charge_credit_sum, 0.00);
      w_cum_charge_debit_sum := COALESCE (w_cum_charge_debit_sum, 0.00);
      w_cum_principal_credit_sum :=
         COALESCE (w_cum_principal_credit_sum, 0.00);
      w_cum_principal_debit_sum := COALESCE (w_cum_principal_debit_sum, 0.00);
      w_cum_profit_credit_sum := COALESCE (w_cum_profit_credit_sum, 0.00);
      w_cum_profit_debit_sum := COALESCE (w_cum_profit_debit_sum, 0.00);

      FOR rec_date_list
         IN (  SELECT transaction_date,
                      COALESCE (SUM (debit_amount), 0.00)
                         total_debit_amount,
                      COALESCE (sum (credit_amount), 0.00)
                         total_credit_amount,
                      COALESCE (sum (principal_debit_amount), 0.00)
                         principal_debit_amount,
                      COALESCE (sum (principal_credit_amount), 0.00)
                         principal_credit_amount,
                      COALESCE (sum (profit_debit_amount), 0.00)
                         profit_debit_amount,
                      COALESCE (sum (profit_credit_amount), 0.00)
                         profit_credit_amount,
                      COALESCE (sum (charge_debit_amount), 0.00)
                         charge_debit_amount,
                      COALESCE (sum (charge_credit_amount), 0.00)
                         charge_credit_amount
                 FROM (SELECT transaction_date,
                              (CASE
                                  WHEN tran_debit_credit = 'D' THEN tran_amount
                                  ELSE 0
                               END) debit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'C' THEN tran_amount
                                  ELSE 0
                               END) credit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'D'
                                  THEN
                                     COALESCE (principal_amount, 0.00)
                                  ELSE
                                     0
                               END) principal_debit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'C'
                                  THEN
                                     COALESCE (principal_amount, 0.00)
                                  ELSE
                                     0
                               END) principal_credit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'D'
                                  THEN
                                     COALESCE (profit_amount, 0.00)
                                  ELSE
                                     0
                               END) profit_debit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'C'
                                  THEN
                                     COALESCE (profit_amount, 0.00)
                                  ELSE
                                     0
                               END) profit_credit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'D'
                                  THEN
                                     COALESCE (charge_amount, 0.00)
                                  ELSE
                                     0
                               END) charge_debit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'C'
                                  THEN
                                     COALESCE (charge_amount, 0.00)
                                  ELSE
                                     0
                               END) charge_credit_amount
                         FROM finance_transaction_details S
                        WHERE     account_number = p_account_number
                              AND s.cancel_by IS NULL
                              AND transaction_date >
                                  rec_account_list.last_balance_update - 1) T
             GROUP BY transaction_date
             ORDER BY transaction_date)
      LOOP
         w_calculate_date := rec_date_list.transaction_date;
         w_total_credit_sum := rec_date_list.total_credit_amount;
         w_total_debit_sum := rec_date_list.total_debit_amount;
         w_cum_credit_sum :=
            w_cum_credit_sum + rec_date_list.total_credit_amount;
         w_cum_debit_sum :=
            w_cum_debit_sum + rec_date_list.total_debit_amount;
         w_account_balance :=
            w_account_balance + (w_total_credit_sum - w_total_debit_sum);

         w_principal_credit_sum := rec_date_list.principal_credit_amount;
         w_principal_debit_sum := rec_date_list.principal_debit_amount;
         w_principal_balance :=
              w_principal_balance
            + (w_principal_credit_sum - w_principal_debit_sum);
         w_cum_principal_credit_sum :=
              w_cum_principal_credit_sum
            + rec_date_list.principal_credit_amount;
         w_cum_principal_debit_sum :=
            w_cum_principal_debit_sum + rec_date_list.principal_debit_amount;

         w_profit_credit_sum := rec_date_list.profit_credit_amount;
         w_profit_debit_sum := rec_date_list.profit_debit_amount;
         w_profit_balance :=
            w_profit_balance + (w_profit_credit_sum - w_profit_debit_sum);
         w_cum_profit_credit_sum :=
            w_cum_profit_credit_sum + rec_date_list.profit_credit_amount;
         w_cum_profit_debit_sum :=
            w_cum_profit_debit_sum + rec_date_list.profit_debit_amount;

         w_charge_credit_sum := rec_date_list.charge_credit_amount;
         w_charge_debit_sum := rec_date_list.charge_debit_amount;
         w_charge_balance :=
            w_charge_balance + (w_charge_credit_sum - w_charge_debit_sum);
         w_cum_charge_credit_sum :=
            w_cum_charge_credit_sum + rec_date_list.charge_credit_amount;
         w_cum_charge_debit_sum :=
            w_cum_charge_debit_sum + rec_date_list.charge_debit_amount;

         DELETE FROM
            finance_accounts_balance_hist
               WHERE     account_number = rec_account_list.account_number
                     AND transaction_date = w_calculate_date;

         INSERT INTO finance_accounts_balance_hist (branch_code,
                                                    account_number,
                                                    transaction_date,
                                                    total_debit_sum,
                                                    total_credit_sum,
                                                    account_balance,
                                                    cum_debit_sum,
                                                    cum_credit_sum,
                                                    principal_credit_sum,
                                                    principal_debit_sum,
                                                    principal_balance,
                                                    profit_credit_sum,
                                                    profit_debit_sum,
                                                    profit_balance,
                                                    charge_credit_sum,
                                                    charge_debit_sum,
                                                    charge_balance,
                                                    cum_charge_credit_sum,
                                                    cum_charge_debit_sum,
                                                    cum_principal_credit_sum,
                                                    cum_principal_debit_sum,
                                                    cum_profit_credit_sum,
                                                    cum_profit_debit_sum,
                                                    app_user_id,
                                                    app_data_time)
              VALUES (rec_account_list.branch_code,
                      rec_account_list.account_number,
                      w_calculate_date,
                      w_total_debit_sum,
                      w_total_credit_sum,
                      w_account_balance,
                      w_cum_debit_sum,
                      w_cum_credit_sum,
                      w_principal_credit_sum,
                      w_principal_debit_sum,
                      w_principal_balance,
                      w_profit_credit_sum,
                      w_profit_debit_sum,
                      w_profit_balance,
                      w_charge_credit_sum,
                      w_charge_debit_sum,
                      w_charge_balance,
                      w_cum_charge_credit_sum,
                      w_cum_charge_debit_sum,
                      w_cum_principal_credit_sum,
                      w_cum_principal_debit_sum,
                      w_cum_profit_credit_sum,
                      w_cum_profit_debit_sum,
                      'SYSTEM',
                      current_timestamp);
      END LOOP;

      UPDATE finance_accounts_balance
         SET last_balance_update = w_calculate_date,
             is_balance_updated = TRUE
       WHERE account_number = p_account_number;
   END LOOP;

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_balance_histac
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_balance_histac (
   IN      p_branch_code      INTEGER,
   IN      p_account_number   CHARACTER,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
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
   w_current_business_day   DATE;
   rec_gl_list              RECORD;
   rec_account_list         RECORD;
   w_account_number         VARCHAR;
BEGIN
   FOR rec_account_list
      IN (SELECT branch_code,
                 account_number,
                 account_balance,
                 last_transaction_date,
                 last_balance_update
            FROM finance_accounts_balance
           WHERE branch_code = p_branch_code AND NOT is_balance_updated)
   LOOP
      w_account_number := rec_account_list.account_number;

      BEGIN
         SELECT *
         INTO w_status, w_errm
         FROM fn_finance_acbal_hist (rec_account_list.account_number,
                                     rec_account_list.last_transaction_date);

         IF w_status = 'E'
         THEN
            RAISE EXCEPTION
            USING MESSAGE =
                        'Error From Account Balance History for Account'
                     || rec_account_list.account_number
                     || ' '
                     || w_errm;
         END IF;
      END;
   END LOOP;

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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_balance_history
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_balance_history (
   IN      p_branch_code   INTEGER,
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
   w_current_business_day   DATE;
   rec_gl_list              RECORD;
   rec_account_list         RECORD;
   w_account_number         VARCHAR;
BEGIN
   FOR rec_gl_list
      IN (SELECT branch_code,
                 gl_code,
                 total_debit_sum,
                 total_credit_sum,
                 gl_balance,
                 last_transaction_date,
                 last_balance_update
            FROM finance_ledger_balance
           WHERE branch_code = p_branch_code AND NOT is_balance_updated)
   LOOP
      BEGIN
         SELECT *
         INTO w_status, w_errm
         FROM fn_finance_glbal_hist (rec_gl_list.gl_code,
                                     rec_gl_list.branch_code,
                                     rec_gl_list.last_transaction_date);

         IF w_status = 'E'
         THEN
            w_errm :=
                  'Error From Ledger Balance History for Ledger'
               || rec_gl_list.gl_code
               || ' '
               || w_errm;
            RAISE EXCEPTION USING MESSAGE = w_errm;
         END IF;

         SELECT w_status, w_errm
           INTO w_status, w_errm
           FROM fn_finance_glmonbal_hist (rec_gl_list.gl_code,
                                          rec_gl_list.branch_code,
                                          rec_gl_list.last_transaction_date);

         IF w_status = 'E'
         THEN
            RAISE EXCEPTION USING MESSAGE = w_errm;
         END IF;

         SELECT w_status, w_errm
           INTO w_status, w_errm
           FROM fn_finance_glmonbal_recpay_hist (
                   rec_gl_list.gl_code,
                   rec_gl_list.branch_code,
                   rec_gl_list.last_transaction_date);

         IF w_status = 'E'
         THEN
            RAISE EXCEPTION USING MESSAGE = w_errm;
         END IF;
      END;
   END LOOP;

   FOR rec_gl_list
      IN (SELECT branch_code, gl_code, last_transaction_date
            FROM finance_cash_and_bank_ledger
           WHERE branch_code = p_branch_code AND NOT is_balance_updated)
   LOOP
      SELECT *
      INTO w_status, w_errm
      FROM fn_finance_glbal_recpay_hist (rec_gl_list.gl_code,
                                         rec_gl_list.branch_code,
                                         rec_gl_list.last_transaction_date);

      IF w_status = 'E'
      THEN
         w_errm :=
               'Error From Receipt Payment History for Ledger'
            || rec_gl_list.gl_code
            || ' '
            || w_errm;
         RAISE EXCEPTION USING MESSAGE = w_errm;
      END IF;
   END LOOP;

   FOR rec_account_list
      IN (SELECT branch_code,
                 account_number,
                 account_balance,
                 last_transaction_date,
                 last_balance_update
            FROM finance_accounts_balance
           WHERE branch_code = p_branch_code AND NOT is_balance_updated)
   LOOP
      w_account_number := rec_account_list.account_number;

      BEGIN
         SELECT *
         INTO w_status, w_errm
         FROM fn_finance_acbal_hist (rec_account_list.account_number,
                                     rec_account_list.last_transaction_date);

         IF w_status = 'E'
         THEN
            RAISE EXCEPTION
            USING MESSAGE =
                        'Error From Account Balance History for Account'
                     || rec_account_list.account_number
                     || ' '
                     || w_errm;
         END IF;
      END;
   END LOOP;



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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_get_ason_acbal
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_get_ason_acbal (
   IN      p_account_number    CHARACTER,
   IN      p_ason_date         DATE,
       OUT o_account_balance   NUMERIC,
       OUT o_block_amount      NUMERIC,
       OUT o_total_credit      NUMERIC,
       OUT o_total_debit       NUMERIC)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_current_business_day       DATE;
   w_account_balance            NUMERIC (22, 2) := 0;
   W_minimum_balance_required   NUMERIC (22, 2) := 0;
   w_total_credit               NUMERIC (22, 2) := 0;
   w_total_debit                NUMERIC (22, 2) := 0;
   w_products_type              CHARACTER (10);
   w_phone_number               CHARACTER (20);
   w_total_block_amount         NUMERIC (22, 2) := 0;
   w_status                     VARCHAR;
   w_errm                       VARCHAR;
   w_last_balance_update        DATE;
   w_last_transaction_date      DATE;
BEGIN
   SELECT account_balance,
          total_debit_amount,
          total_credit_amount,
          account_type,
          phone_number,
          last_balance_update,
          last_transaction_date
     INTO w_account_balance,
          w_total_debit,
          w_total_credit,
          w_products_type,
          w_phone_number,
          w_last_balance_update,
          w_last_transaction_date
     FROM finance_accounts_balance
    WHERE account_number = p_account_number;

   IF     w_last_balance_update = w_last_transaction_date
      AND p_ason_date = w_last_transaction_date
   THEN
      w_account_balance := w_account_balance;
   ELSE
      SELECT account_balance, cum_debit_sum, cum_credit_sum
        INTO w_account_balance, w_total_debit, w_total_credit
        FROM finance_accounts_balance_hist h
       WHERE     h.account_number = p_account_number
             AND h.transaction_date =
                 (SELECT max (transaction_date)
                   FROM finance_accounts_balance_hist
                  WHERE     account_number = p_account_number
                        AND transaction_date <= p_ason_date);
   END IF;

   o_account_balance := COALESCE (w_account_balance, 0.00);
   o_block_amount := COALESCE (w_total_block_amount, 0.00);
   o_total_credit := COALESCE (w_total_credit, 0.00);
   o_total_debit := COALESCE (w_total_debit, 0.00);
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_get_ason_glbal
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_get_ason_glbal (
   IN      p_branch_code    INTEGER,
   IN      p_gl_code        CHARACTER,
   IN      p_ason_date      DATE,
       OUT o_gl_balance     NUMERIC,
       OUT o_gl_credit      NUMERIC,
       OUT o_gl_debit       NUMERIC,
       OUT o_block_amount   NUMERIC,
       OUT o_status         CHARACTER,
       OUT o_errm           CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_ledger_banalce          NUMERIC (22, 2) := 0;
   w_credit_banalce          NUMERIC (22, 2) := 0;
   w_debit_banalce           NUMERIC (22, 2) := 0;
   w_last_balance_update     DATE;
   w_last_transaction_date   DATE;
   w_status                  VARCHAR;
   w_errm                    VARCHAR;
BEGIN
   o_gl_balance := w_ledger_banalce;
   o_gl_credit := COALESCE (w_credit_banalce, 0.00);
   o_gl_debit := COALESCE (w_debit_banalce, 0.00);
   o_block_amount := 0.00;

   IF p_branch_code = 0
   THEN
      SELECT sum (gl_balance),
             sum (total_credit_sum),
             sum (total_debit_sum),
             min (last_balance_update),
             max (last_transaction_date)
        INTO w_ledger_banalce,
             w_credit_banalce,
             w_debit_banalce,
             w_last_balance_update,
             w_last_transaction_date
        FROM finance_ledger_balance
       WHERE gl_code = p_gl_code;

      IF     w_last_balance_update = w_last_transaction_date
         AND p_ason_date = w_last_transaction_date
      THEN
         w_ledger_banalce := w_ledger_banalce;
      ELSE
         SELECT sum (gl_balance) gl_balance,
                sum (cum_credit_sum),
                sum (cum_debit_sum)
           INTO w_ledger_banalce, w_credit_banalce, w_debit_banalce
           FROM finance_ledger_balance_hist h,
                (  SELECT branch_code,
                          max (transaction_date) last_transaction_date
                     FROM finance_ledger_balance_hist g
                    WHERE     g.gl_code = p_gl_code
                          AND transaction_date <= p_ason_date
                 GROUP BY branch_code) b
          WHERE     h.gl_code = p_gl_code
                AND h.transaction_date = b.last_transaction_date
                AND h.branch_code = b.branch_code;
      END IF;
   ELSIF p_branch_code > 0
   THEN
      SELECT sum (gl_balance),
             sum (total_credit_sum),
             sum (total_debit_sum),
             min (last_balance_update),
             max (last_transaction_date)
        INTO w_ledger_banalce,
             w_credit_banalce,
             w_debit_banalce,
             w_last_balance_update,
             w_last_transaction_date
        FROM finance_ledger_balance
       WHERE gl_code = p_gl_code AND branch_code = p_branch_code;


      IF     w_last_balance_update = w_last_transaction_date
         AND p_ason_date = w_last_transaction_date
      THEN
         w_ledger_banalce := w_ledger_banalce;
      ELSE
         SELECT sum (gl_balance) gl_balance,
                sum (cum_credit_sum),
                sum (cum_debit_sum)
           INTO w_ledger_banalce, w_credit_banalce, w_debit_banalce
           FROM finance_ledger_balance_hist h,
                (  SELECT branch_code,
                          max (transaction_date) last_transaction_date
                     FROM finance_ledger_balance_hist g
                    WHERE     g.gl_code = p_gl_code
                          AND g.branch_code = p_branch_code
                          AND g.transaction_date <= p_ason_date
                 GROUP BY branch_code) b
          WHERE     h.gl_code = p_gl_code
                AND h.branch_code = p_branch_code
                AND h.transaction_date = b.last_transaction_date
                AND h.branch_code = b.branch_code;
      END IF;
   END IF;

   w_ledger_banalce := COALESCE (w_ledger_banalce, 0.00);

   o_gl_balance := w_ledger_banalce;
   o_gl_credit := COALESCE (w_credit_banalce, 0.00);
   o_gl_debit := COALESCE (w_debit_banalce, 0.00);
   o_block_amount := 0.00;
EXCEPTION
   WHEN OTHERS
   THEN
      IF w_status = 'E'
      THEN
         o_status := w_status;
         o_errm := w_errm;
      ELSE
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_get_charges
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_get_charges (
   p_amount            NUMERIC DEFAULT 0,
   p_actype_code       CHARACTER DEFAULT ''::bpchar,
   p_charge_code       CHARACTER DEFAULT ''::bpchar,
   p_account_opening   BOOLEAN DEFAULT FALSE,
   p_account_closing   BOOLEAN DEFAULT FALSE)
   RETURNS SETOF charge_type
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
   ROWS 1000
AS
$$
DECLARE
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
   w_current_business_day   DATE;
   result_record            charge_type;
   rec_open_list            RECORD;
BEGIN
   /*
   CREATE TYPE charge_type AS (charges_code varchar(20), charge_amount NUMERIC (22, 2));

   result_record.charges_code := '1';
   result_record.charge_amount := '1';
   RETURN NEXT
      result_record;

   result_record.charges_code := '2';
   result_record.charge_amount := '2';
   RETURN NEXT
      result_record;
   */

   IF CHAR_LENGTH (p_charge_code) > 1
   THEN
      FOR rec_open_list
         IN (SELECT charges_id,
                    charges_code,
                    charges_name,
                    charge_amount,
                    charge_type,
                    charge_percentage
               FROM finance_charges
              WHERE     charges_code = p_charge_code
                    AND p_amount BETWEEN charge_from_amount
                                     AND charge_upto_amount)
      LOOP
         IF rec_open_list.charge_type = 'F'
         THEN
            result_record.charges_id := rec_open_list.charges_id;
            result_record.charges_code := rec_open_list.charges_code;
            result_record.charges_name := rec_open_list.charges_name;
            result_record.charge_amount := rec_open_list.charge_amount;
            RETURN NEXT
               result_record;
         ELSE
            result_record.charges_id := rec_open_list.charges_id;
            result_record.charges_code := rec_open_list.charges_code;
            result_record.charges_name := rec_open_list.charges_name;
            result_record.charge_amount :=
               (p_amount * (rec_open_list.charge_percentage / 100));
            RETURN NEXT
               result_record;
         END IF;
      END LOOP;
   ELSE
      IF p_account_opening
      THEN
         FOR rec_open_list
            IN (SELECT charges_id,
                       charges_code,
                       charges_name,
                       charge_amount,
                       charge_type,
                       charge_percentage
                  FROM finance_charges
                 WHERE     actype_code = p_actype_code
                       AND account_opening_charge = p_account_opening
                       AND p_amount BETWEEN charge_from_amount
                                        AND charge_upto_amount)
         LOOP
            IF rec_open_list.charge_type = 'F'
            THEN
               result_record.charges_id := rec_open_list.charges_id;
               result_record.charges_code := rec_open_list.charges_code;
               result_record.charges_name := rec_open_list.charges_name;
               result_record.charge_amount := rec_open_list.charge_amount;
               RETURN NEXT
                  result_record;
            ELSE
               result_record.charges_id := rec_open_list.charges_id;
               result_record.charges_code := rec_open_list.charges_code;
               result_record.charges_name := rec_open_list.charges_name;
               result_record.charge_amount :=
                  (p_amount * (rec_open_list.charge_percentage / 100));
               RETURN NEXT
                  result_record;
            END IF;
         END LOOP;
      END IF;

      IF p_account_closing
      THEN
         FOR rec_open_list
            IN (SELECT charges_id,
                       charges_code,
                       charges_name,
                       charge_amount,
                       charge_type,
                       charge_percentage
                  FROM finance_charges
                 WHERE     actype_code = p_actype_code
                       AND account_closing_charge = p_account_closing
                       AND p_amount BETWEEN charge_from_amount
                                        AND charge_upto_amount)
         LOOP
            IF rec_open_list.charge_type = 'F'
            THEN
               result_record.charges_id := rec_open_list.charges_id;
               result_record.charges_code := rec_open_list.charges_code;
               result_record.charges_name := rec_open_list.charges_name;
               result_record.charge_amount := rec_open_list.charge_amount;
               RETURN NEXT
                  result_record;
            ELSE
               result_record.charges_id := rec_open_list.charges_id;
               result_record.charges_code := rec_open_list.charges_code;
               result_record.charges_name := rec_open_list.charges_name;
               result_record.charge_amount :=
                  (p_amount * (rec_open_list.charge_percentage / 100));
               RETURN NEXT
                  result_record;
            END IF;
         END LOOP;
      END IF;
   END IF;

   RETURN;
EXCEPTION
   WHEN OTHERS
   THEN
      NULL;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_glbal_hist
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_glbal_hist (
   IN      p_gl_code       CHARACTER,
   IN      p_branch_code   INTEGER,
   IN      p_ason_date     DATE,
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
   rec_gl_list              RECORD;
   rec_date_list            RECORD;
   w_current_business_day   DATE;
   w_calculate_date         DATE;
   w_total_debit_sum        NUMERIC (22, 2) := 0;
   w_total_credit_sum       NUMERIC (22, 2) := 0;
   w_ledger_banalce         NUMERIC (22, 2) := 0;
   w_ledger_banalce_prev    NUMERIC (22, 2) := 0;
   w_principal_banalce      NUMERIC (22, 2) := 0;
   w_interest_banalce       NUMERIC (22, 2) := 0;
   w_charge_banalce         NUMERIC (22, 2) := 0;
   w_cum_credit_sum         NUMERIC (22, 2) := 0;
   w_cum_debit_sum          NUMERIC (22, 2) := 0;
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
BEGIN
   FOR rec_gl_list
      IN (SELECT branch_code,
                 gl_code,
                 total_debit_sum,
                 total_credit_sum,
                 gl_balance,
                 last_transaction_date,
                 last_balance_update
            FROM finance_ledger_balance
           WHERE     branch_code = p_branch_code
                 AND gl_code = p_gl_code
                 AND NOT is_balance_updated)
   LOOP
      w_calculate_date := rec_gl_list.last_balance_update;

      BEGIN
         SELECT o_gl_balance, o_gl_credit, o_gl_debit
           INTO w_ledger_banalce, w_cum_credit_sum, w_cum_debit_sum
           FROM fn_finance_get_ason_glbal (rec_gl_list.branch_code,
                                           p_gl_code,
                                           w_calculate_date - 1);
      END;

      FOR rec_date_list
         IN (  SELECT transaction_date,
                      COALESCE (SUM (debit_amount), 0.00) total_debit_amount,
                      COALESCE (sum (credit_amount), 0.00) total_credit_amount
                 FROM (SELECT transaction_date,
                              (CASE
                                  WHEN tran_debit_credit = 'D' THEN tran_amount
                                  ELSE 0
                               END) debit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'C' THEN tran_amount
                                  ELSE 0
                               END) credit_amount
                         FROM finance_transaction_details S
                        WHERE     tran_gl_code = p_gl_code
                              AND s.cancel_by IS NULL
                              AND s.auth_by IS NOT NULL
                              AND acbrn_code = p_branch_code
                              AND transaction_date >
                                  rec_gl_list.last_balance_update - 1) T
             GROUP BY transaction_date
             ORDER BY transaction_date)
      LOOP
         w_calculate_date := rec_date_list.transaction_date;
         w_total_credit_sum := rec_date_list.total_credit_amount;
         w_total_debit_sum := rec_date_list.total_debit_amount;
         w_cum_credit_sum :=
            w_cum_credit_sum + rec_date_list.total_credit_amount;
         w_cum_debit_sum :=
            w_cum_debit_sum + rec_date_list.total_debit_amount;
         w_ledger_banalce :=
            w_ledger_banalce + (w_total_credit_sum - w_total_debit_sum);

         DELETE FROM
            finance_ledger_balance_hist
               WHERE     branch_code = rec_gl_list.branch_code
                     AND gl_code = p_gl_code
                     AND transaction_date = w_calculate_date;

         INSERT INTO finance_ledger_balance_hist (branch_code,
                                                  transaction_date,
                                                  gl_code,
                                                  total_debit_sum,
                                                  total_credit_sum,
                                                  cum_credit_sum,
                                                  cum_debit_sum,
                                                  gl_balance,
                                                  app_user_id,
                                                  app_data_time)
              VALUES (rec_gl_list.branch_code,
                      w_calculate_date,
                      p_gl_code,
                      COALESCE (w_total_debit_sum, 0.00),
                      COALESCE (w_total_credit_sum, 0.00),
                      COALESCE (w_cum_credit_sum, 0.00),
                      COALESCE (w_cum_debit_sum, 0.00),
                      COALESCE (w_ledger_banalce, 0.00),
                      'SYSTEM',
                      current_timestamp);
      END LOOP;

      UPDATE finance_ledger_balance
         SET last_balance_update = w_calculate_date,
             is_balance_updated = TRUE
       WHERE branch_code = rec_gl_list.branch_code AND gl_code = p_gl_code;
   END LOOP;

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_glbal_recpay_hist
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_glbal_recpay_hist (
   IN      p_gl_code       CHARACTER,
   IN      p_branch_code   INTEGER,
   IN      p_ason_date     DATE,
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
   rec_gl_list              RECORD;
   rec_date_list            RECORD;
   w_current_business_day   DATE;
   w_calculate_date         DATE;
   w_total_debit_sum        NUMERIC (22, 2) := 0;
   w_total_credit_sum       NUMERIC (22, 2) := 0;
   w_ledger_banalce         NUMERIC (22, 2) := 0;
   w_ledger_banalce_prev    NUMERIC (22, 2) := 0;
   w_principal_banalce      NUMERIC (22, 2) := 0;
   w_interest_banalce       NUMERIC (22, 2) := 0;
   w_charge_banalce         NUMERIC (22, 2) := 0;
   w_cum_credit_sum         NUMERIC (22, 2) := 0;
   w_cum_debit_sum          NUMERIC (22, 2) := 0;
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
BEGIN
   FOR rec_gl_list
      IN (SELECT last_transaction_date, last_balance_update
            FROM finance_cash_and_bank_ledger
           WHERE     branch_code = p_branch_code
                 AND gl_code = p_gl_code
                 AND NOT is_balance_updated)
   LOOP
      w_calculate_date := rec_gl_list.last_balance_update;

      /*
      As we are calculating contra ledger balance, hence here debit and credit reversal working
      */

      FOR rec_date_list
         IN (  SELECT transaction_date,
                      contra_gl_code,
                      COALESCE (SUM (debit_amount), 0.00) total_debit_amount,
                      COALESCE (sum (credit_amount), 0.00) total_credit_amount
                 FROM (SELECT transaction_date,
                              contra_gl_code,
                              (CASE
                                  WHEN tran_debit_credit = 'C' THEN tran_amount
                                  ELSE 0
                               END) debit_amount,
                              (CASE
                                  WHEN tran_debit_credit = 'D' THEN tran_amount
                                  ELSE 0
                               END) credit_amount
                         FROM finance_transaction_details S
                        WHERE     tran_gl_code = p_gl_code
                              AND s.cancel_by IS NULL
                              AND s.auth_by IS NOT NULL
                              AND acbrn_code = p_branch_code
                              AND transaction_date >
                                  rec_gl_list.last_balance_update - 1) T
             GROUP BY transaction_date, contra_gl_code
             ORDER BY transaction_date, contra_gl_code)
      LOOP
         w_calculate_date := rec_date_list.transaction_date;
         w_total_credit_sum := rec_date_list.total_credit_amount;
         w_total_debit_sum := rec_date_list.total_debit_amount;

         BEGIN
            SELECT COALESCE (sum (cum_credit_sum), 0),
                   COALESCE (sum (cum_debit_sum), 0)
              INTO w_cum_credit_sum, w_cum_debit_sum
              FROM finance_led_rec_pay_bal_hist h,
                   (  SELECT branch_code,
                             max (transaction_date) last_transaction_date
                        FROM finance_led_rec_pay_bal_hist g
                       WHERE     g.gl_code = rec_date_list.contra_gl_code
                             AND g.branch_code = p_branch_code
                             AND g.transaction_date < w_calculate_date
                    GROUP BY branch_code) b
             WHERE     h.gl_code = rec_date_list.contra_gl_code
                   AND h.branch_code = p_branch_code
                   AND h.transaction_date = b.last_transaction_date
                   AND h.branch_code = b.branch_code;
         END;

         w_cum_credit_sum :=
              COALESCE (w_cum_credit_sum, 0.00)
            + rec_date_list.total_credit_amount;
         w_cum_debit_sum :=
              COALESCE (w_cum_debit_sum, 0.00)
            + rec_date_list.total_debit_amount;

         w_ledger_banalce := w_cum_credit_sum - w_cum_debit_sum;

         DELETE FROM
            finance_led_rec_pay_bal_hist
               WHERE     branch_code = p_branch_code
                     AND gl_code = rec_date_list.contra_gl_code
                     AND transaction_date = w_calculate_date;

         INSERT INTO finance_led_rec_pay_bal_hist (branch_code,
                                                   transaction_date,
                                                   gl_code,
                                                   total_debit_sum,
                                                   total_credit_sum,
                                                   cum_credit_sum,
                                                   cum_debit_sum,
                                                   gl_balance,
                                                   app_user_id,
                                                   app_data_time)
              VALUES (p_branch_code,
                      w_calculate_date,
                      rec_date_list.contra_gl_code,
                      COALESCE (w_total_debit_sum, 0.00),
                      COALESCE (w_total_credit_sum, 0.00),
                      COALESCE (w_cum_credit_sum, 0.00),
                      COALESCE (w_cum_debit_sum, 0.00),
                      COALESCE (w_ledger_banalce, 0.00),
                      'SYSTEM',
                      current_timestamp);
      END LOOP;

      UPDATE finance_cash_and_bank_ledger
         SET last_balance_update = w_calculate_date,
             is_balance_updated = TRUE
       WHERE branch_code = p_branch_code AND gl_code = p_gl_code;
   END LOOP;

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_glmonbal_hist
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_glmonbal_hist (
   IN      p_gl_code       CHARACTER,
   IN      p_branch_code   INTEGER,
   IN      p_ason_date     DATE,
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
   rec_gl_list                RECORD;
   rec_date_list              RECORD;
   w_current_business_day     DATE;
   w_calculate_date           DATE;
   w_total_debit_sum          NUMERIC (22, 2) := 0;
   w_total_credit_sum         NUMERIC (22, 2) := 0;
   w_ledger_banalce           NUMERIC (22, 2) := 0;
   w_ledger_banalce_prev      NUMERIC (22, 2) := 0;
   w_principal_banalce        NUMERIC (22, 2) := 0;
   w_interest_banalce         NUMERIC (22, 2) := 0;
   w_charge_banalce           NUMERIC (22, 2) := 0;
   w_cum_credit_sum           NUMERIC (22, 2) := 0;
   w_cum_debit_sum            NUMERIC (22, 2) := 0;
   w_status                   VARCHAR;
   w_errm                     VARCHAR;
   w_calculate_month          INTEGER;
   w_calculate_year           INTEGER;
   w_transaction_year_month   INTEGER;
   w_month_start_date         DATE;
   w_month_end_date           DATE;
BEGIN
   FOR rec_gl_list
      IN (SELECT branch_code,
                 gl_code,
                 total_debit_sum,
                 total_credit_sum,
                 gl_balance,
                 last_transaction_date,
                 last_balance_update,
                 last_monbal_update
            FROM finance_ledger_balance
           WHERE     branch_code = p_branch_code
                 AND gl_code = p_gl_code
                 AND NOT is_monbal_updated)
   LOOP
      IF TO_CHAR (rec_gl_list.last_monbal_update, 'MMYYYY') <>
         TO_CHAR (rec_gl_list.last_transaction_date, 'MMYYYY')
      THEN
         w_calculate_date :=
            CAST (
               date_trunc ('month', rec_gl_list.last_monbal_update) AS DATE);
      END IF;

      WHILE (w_calculate_date < rec_gl_list.last_transaction_date)
      LOOP
         w_month_end_date :=
            CAST (
                 date_trunc ('month', w_calculate_date)
               + INTERVAL '1 months'
               - INTERVAL '1 day'
                  AS DATE);

         w_month_start_date :=
            CAST (date_trunc ('month', w_calculate_date) AS DATE);

         w_calculate_month :=
            cast (TO_CHAR (w_month_end_date, 'MM') AS INTEGER);
         w_calculate_year :=
            cast (TO_CHAR (w_month_end_date, 'YYYY') AS INTEGER);
         w_transaction_year_month :=
            cast (TO_CHAR (w_month_end_date, 'YYYYMM') AS INTEGER);

         DELETE FROM
            finance_ledger_balmon_hist
               WHERE     branch_code = rec_gl_list.branch_code
                     AND gl_code = p_gl_code
                     AND transaction_month = w_calculate_month
                     AND transaction_year = w_calculate_year;

         INSERT INTO finance_ledger_balmon_hist (branch_code,
                                                 gl_code,
                                                 transaction_date,
                                                 transaction_month,
                                                 transaction_year,
                                                 transaction_year_month,
                                                 total_debit_sum,
                                                 total_credit_sum,
                                                 cum_credit_sum,
                                                 cum_debit_sum,
                                                 gl_balance,
                                                 app_user_id,
                                                 app_data_time)
            WITH
               gl_sum_bal
               AS
                  (  SELECT gl_code,
                            branch_code,
                            sum (total_debit_sum) total_debit_sum,
                            sum (total_credit_sum) total_credit_sum
                       FROM finance_ledger_balance_hist S
                      WHERE     gl_code = p_gl_code
                            AND branch_code = p_branch_code
                            AND transaction_date BETWEEN w_month_start_date
                                                     AND w_month_end_date
                   GROUP BY gl_code, branch_code),
               gl_balance
               AS
                  (  SELECT h.gl_code,
                            h.branch_code,
                            sum (gl_balance) gl_balance,
                            sum (cum_credit_sum) cum_credit_sum,
                            sum (cum_debit_sum) cum_debit_sum
                       FROM finance_ledger_balance_hist h,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) last_transaction_date
                                 FROM finance_ledger_balance_hist g
                                WHERE     g.gl_code = p_gl_code
                                      AND g.branch_code = p_branch_code
                                      AND g.transaction_date <= w_month_end_date
                             GROUP BY branch_code, gl_code) b
                      WHERE     h.gl_code = p_gl_code
                            AND h.branch_code = p_branch_code
                            AND h.transaction_date = b.last_transaction_date
                            AND h.branch_code = b.branch_code
                   GROUP BY h.gl_code, h.branch_code)
            SELECT s.branch_code,
                   s.gl_code,
                   w_month_end_date,
                   w_calculate_month,
                   w_calculate_year,
                   w_transaction_year_month,
                   total_debit_sum,
                   total_credit_sum,
                   cum_credit_sum,
                   cum_debit_sum,
                   gl_balance,
                   'SYSTEM',
                   current_timestamp
              FROM gl_sum_bal s, gl_balance b
             WHERE s.gl_code = b.gl_code AND s.branch_code = b.branch_code;

         w_calculate_date :=
            CAST (w_calculate_date + INTERVAL '1 month' AS DATE);
      END LOOP;

      UPDATE finance_ledger_balance
         SET last_monbal_update = rec_gl_list.last_transaction_date,
             is_monbal_updated = TRUE
       WHERE branch_code = rec_gl_list.branch_code AND gl_code = p_gl_code;
   END LOOP;

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_glmonbal_recpay_hist
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_glmonbal_recpay_hist (
   IN      p_gl_code       CHARACTER,
   IN      p_branch_code   INTEGER,
   IN      p_ason_date     DATE,
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
   rec_gl_list                RECORD;
   rec_date_list              RECORD;
   w_current_business_day     DATE;
   w_calculate_date           DATE;
   w_total_debit_sum          NUMERIC (22, 2) := 0;
   w_total_credit_sum         NUMERIC (22, 2) := 0;
   w_ledger_banalce           NUMERIC (22, 2) := 0;
   w_ledger_banalce_prev      NUMERIC (22, 2) := 0;
   w_principal_banalce        NUMERIC (22, 2) := 0;
   w_interest_banalce         NUMERIC (22, 2) := 0;
   w_charge_banalce           NUMERIC (22, 2) := 0;
   w_cum_credit_sum           NUMERIC (22, 2) := 0;
   w_cum_debit_sum            NUMERIC (22, 2) := 0;
   w_status                   VARCHAR;
   w_errm                     VARCHAR;
   w_calculate_month          INTEGER;
   w_calculate_year           INTEGER;
   w_transaction_year_month   INTEGER;
   w_month_start_date         DATE;
   w_month_end_date           DATE;
BEGIN
   FOR rec_gl_list
      IN (SELECT branch_code,
                 gl_code,
                 total_debit_sum,
                 total_credit_sum,
                 gl_balance,
                 last_transaction_date,
                 last_balance_update,
                 last_monbal_recpay_update
            FROM finance_ledger_balance
           WHERE     branch_code = p_branch_code
                 AND gl_code = p_gl_code
                 AND NOT is_monbal_recpay_updated)
   LOOP
      IF TO_CHAR (rec_gl_list.last_monbal_recpay_update, 'MMYYYY') <>
         TO_CHAR (rec_gl_list.last_transaction_date, 'MMYYYY')
      THEN
         w_calculate_date :=
            CAST (
               date_trunc ('month', rec_gl_list.last_monbal_recpay_update)
                  AS DATE);
      END IF;

      WHILE (w_calculate_date < rec_gl_list.last_transaction_date)
      LOOP
         w_month_end_date :=
            CAST (
                 date_trunc ('month', w_calculate_date)
               + INTERVAL '1 months'
               - INTERVAL '1 day'
                  AS DATE);

         w_month_start_date :=
            CAST (date_trunc ('month', w_calculate_date) AS DATE);

         w_calculate_month :=
            cast (TO_CHAR (w_month_end_date, 'MM') AS INTEGER);
         w_calculate_year :=
            cast (TO_CHAR (w_month_end_date, 'YYYY') AS INTEGER);
         w_transaction_year_month :=
            cast (TO_CHAR (w_month_end_date, 'YYYYMM') AS INTEGER);

         DELETE FROM
            finance_led_rec_pay_balmon_hist
               WHERE     branch_code = rec_gl_list.branch_code
                     AND gl_code = p_gl_code
                     AND transaction_month = w_calculate_month
                     AND transaction_year = w_calculate_year;

         INSERT INTO finance_led_rec_pay_balmon_hist (branch_code,
                                                      gl_code,
                                                      transaction_date,
                                                      transaction_month,
                                                      transaction_year,
                                                      transaction_year_month,
                                                      total_debit_sum,
                                                      total_credit_sum,
                                                      cum_credit_sum,
                                                      cum_debit_sum,
                                                      gl_balance,
                                                      app_user_id,
                                                      app_data_time)
            WITH
               gl_sum_bal
               AS
                  (  SELECT gl_code,
                            branch_code,
                            sum (total_debit_sum) total_debit_sum,
                            sum (total_credit_sum) total_credit_sum
                       FROM finance_led_rec_pay_bal_hist S
                      WHERE     gl_code = p_gl_code
                            AND branch_code = p_branch_code
                            AND transaction_date BETWEEN w_month_start_date
                                                     AND w_month_end_date
                   GROUP BY gl_code, branch_code),
               gl_balance
               AS
                  (  SELECT h.gl_code,
                            h.branch_code,
                            sum (gl_balance) gl_balance,
                            sum (cum_credit_sum) cum_credit_sum,
                            sum (cum_debit_sum) cum_debit_sum
                       FROM finance_led_rec_pay_bal_hist h,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) last_transaction_date
                                 FROM finance_led_rec_pay_bal_hist g
                                WHERE     g.gl_code = p_gl_code
                                      AND g.branch_code = p_branch_code
                                      AND g.transaction_date <= w_month_end_date
                             GROUP BY branch_code, gl_code) b
                      WHERE     h.gl_code = p_gl_code
                            AND h.branch_code = p_branch_code
                            AND h.transaction_date = b.last_transaction_date
                            AND h.branch_code = b.branch_code
                   GROUP BY h.gl_code, h.branch_code)
            SELECT s.branch_code,
                   s.gl_code,
                   w_month_end_date,
                   w_calculate_month,
                   w_calculate_year,
                   w_transaction_year_month,
                   total_debit_sum,
                   total_credit_sum,
                   cum_credit_sum,
                   cum_debit_sum,
                   gl_balance,
                   'SYSTEM',
                   current_timestamp
              FROM gl_sum_bal s, gl_balance b
             WHERE s.gl_code = b.gl_code AND s.branch_code = b.branch_code;

         w_calculate_date :=
            CAST (w_calculate_date + INTERVAL '1 month' AS DATE);
      END LOOP;

      UPDATE finance_ledger_balance
         SET last_monbal_recpay_update = rec_gl_list.last_transaction_date,
             is_monbal_recpay_updated = TRUE
       WHERE branch_code = rec_gl_list.branch_code AND gl_code = p_gl_code;
   END LOOP;

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_ibrtran_post
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_ibrtran_post (
   IN      p_transaction_id   CHARACTER,
   IN      p_app_user_id      CHARACTER,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
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
   w_current_business_day   DATE;
   rec_tran_list            RECORD;
   w_tran_type              VARCHAR := '0';
   w_tran_ac_number         VARCHAR := '0';
   w_tran_gl_code           VARCHAR := '0';
   w_contra_gl_code         VARCHAR := '0';
   w_cash_transaction       BOOLEAN;
   w_total_leg              INTEGER;
   w_tran_amount            NUMERIC (22, 2) := 0;
   w_principal_amount       NUMERIC (22, 2) := 0;
   w_charge_amount          NUMERIC (22, 2) := 0;
   w_interest_amount        NUMERIC (22, 2) := 0;
   w_serial_no              INTEGER := 0;
   w_day_serial_no          INTEGER := 0;
   w_debit_credit           VARCHAR;
   w_tran_reference         VARCHAR;
   w_batch_number           INTEGER;
   w_ibr_gl_code            VARCHAR := '0';
   w_branch_code            INTEGER := 0;
   w_acbrn_code             INTEGER := 0;
   w_tran_narration         VARCHAR := 0;
   w_transaction_date       DATE;
BEGIN
   SELECT inter_branch_ledger
     INTO w_ibr_gl_code
     FROM finance_application_settings;

   IF w_ibr_gl_code IS NULL
   THEN
      RAISE EXCEPTION USING MESSAGE = 'Invalid IBR GL Configuration';
   END IF;

   FOR rec_tran_list IN (SELECT org_branch_code,
                                res_branch_code,
                                transaction_date,
                                org_gl_code,
                                res_gl_code,
                                tran_amount,
                                cancel_amount,
                                transaction_narration,
                                app_user_id,
                                transaction_id,
                                tran_status,
                                cancel_by,
                                auth_by
                           FROM finance_transaction_ibr
                          WHERE transaction_id = p_transaction_id)
   LOOP
      w_tran_amount := rec_tran_list.tran_amount;
      w_branch_code := rec_tran_list.res_branch_code;
      w_transaction_date := rec_tran_list.transaction_date;

      IF w_tran_amount <= 0
      THEN
         RAISE EXCEPTION
         USING MESSAGE = 'Transaction amount can not be Zero or Negative!';
      END IF;

      IF rec_tran_list.org_gl_code IS NULL
      THEN
         RAISE EXCEPTION USING MESSAGE = 'Orginating Ledger is Null!';
      END IF;

      IF rec_tran_list.res_gl_code IS NULL
      THEN
         RAISE EXCEPTION USING MESSAGE = 'Responding Ledger is Null!';
      END IF;

      IF rec_tran_list.cancel_by IS NOT NULL
      THEN
         RAISE EXCEPTION USING MESSAGE = 'Transaction already Canceled!';
      END IF;

      IF rec_tran_list.auth_by IS NOT NULL
      THEN
         RAISE EXCEPTION USING MESSAGE = 'Transaction already Authorized!';
      END IF;

      --- Credit Orginating Branch Ledger
      w_serial_no := w_serial_no + 1;
      w_tran_ac_number := '0';
      w_tran_gl_code := rec_tran_list.org_gl_code;
      w_contra_gl_code := w_ibr_gl_code;
      w_tran_type := 'IBR_POST';
      w_tran_amount := rec_tran_list.tran_amount;
      w_debit_credit := 'C';
      w_tran_narration :=
         'IBR Transaction ' || rec_tran_list.transaction_narration;
      w_tran_reference := rec_tran_list.transaction_id;
      w_acbrn_code := rec_tran_list.org_branch_code;

      INSERT INTO finance_transaction_table (branch_code,
                                             acbrn_code,
                                             transaction_date,
                                             batch_serial,
                                             account_number,
                                             tran_gl_code,
                                             contra_gl_code,
                                             tran_debit_credit,
                                             tran_type,
                                             tran_amount,
                                             available_balance,
                                             tran_person_phone,
                                             tran_person_name,
                                             tran_document_prefix,
                                             tran_document_number,
                                             tran_sign_verified,
                                             system_posted_tran,
                                             transaction_narration,
                                             app_user_id,
                                             app_data_time)
           VALUES (w_branch_code,
                   w_acbrn_code,
                   w_transaction_date,
                   w_serial_no,
                   w_tran_ac_number,
                   w_tran_gl_code,
                   w_contra_gl_code,
                   w_debit_credit,
                   w_tran_type,
                   w_tran_amount,
                   0,
                   '',
                   '',
                   NULL,
                   w_tran_reference,
                   FALSE,
                   TRUE,
                   w_tran_narration,
                   p_app_user_id,
                   current_timestamp);


      --- Debit Orginating Branch IBR Ledger
      w_serial_no := w_serial_no + 1;
      w_tran_ac_number := '0';
      w_tran_gl_code := w_ibr_gl_code;
      w_contra_gl_code := rec_tran_list.org_gl_code;
      w_tran_type := 'IBR_POST';
      w_tran_amount := rec_tran_list.tran_amount;
      w_debit_credit := 'D';
      w_tran_narration :=
         'IBR Transaction ' || rec_tran_list.transaction_narration;
      w_tran_reference := rec_tran_list.transaction_id;
      w_acbrn_code := rec_tran_list.org_branch_code;

      INSERT INTO finance_transaction_table (branch_code,
                                             acbrn_code,
                                             transaction_date,
                                             batch_serial,
                                             account_number,
                                             tran_gl_code,
                                             contra_gl_code,
                                             tran_debit_credit,
                                             tran_type,
                                             tran_amount,
                                             available_balance,
                                             tran_person_phone,
                                             tran_person_name,
                                             tran_document_prefix,
                                             tran_document_number,
                                             tran_sign_verified,
                                             system_posted_tran,
                                             transaction_narration,
                                             app_user_id,
                                             app_data_time)
           VALUES (w_branch_code,
                   w_acbrn_code,
                   w_transaction_date,
                   w_serial_no,
                   w_tran_ac_number,
                   w_tran_gl_code,
                   w_contra_gl_code,
                   w_debit_credit,
                   w_tran_type,
                   w_tran_amount,
                   0,
                   '',
                   '',
                   NULL,
                   w_tran_reference,
                   FALSE,
                   TRUE,
                   w_tran_narration,
                   p_app_user_id,
                   current_timestamp);


      --- Credit Respinding Branch IBR Ledger
      w_serial_no := w_serial_no + 1;
      w_tran_ac_number := '0';
      w_tran_gl_code := w_ibr_gl_code;
      w_contra_gl_code := rec_tran_list.res_gl_code;
      w_tran_type := 'IBR_POST';
      w_tran_amount := rec_tran_list.tran_amount;
      w_debit_credit := 'C';
      w_tran_narration :=
         'IBR Transaction ' || rec_tran_list.transaction_narration;
      w_tran_reference := rec_tran_list.transaction_id;
      w_acbrn_code := rec_tran_list.res_branch_code;

      INSERT INTO finance_transaction_table (branch_code,
                                             acbrn_code,
                                             transaction_date,
                                             batch_serial,
                                             account_number,
                                             tran_gl_code,
                                             contra_gl_code,
                                             tran_debit_credit,
                                             tran_type,
                                             tran_amount,
                                             available_balance,
                                             tran_person_phone,
                                             tran_person_name,
                                             tran_document_prefix,
                                             tran_document_number,
                                             tran_sign_verified,
                                             system_posted_tran,
                                             transaction_narration,
                                             app_user_id,
                                             app_data_time)
           VALUES (w_branch_code,
                   w_acbrn_code,
                   w_transaction_date,
                   w_serial_no,
                   w_tran_ac_number,
                   w_tran_gl_code,
                   w_contra_gl_code,
                   w_debit_credit,
                   w_tran_type,
                   w_tran_amount,
                   0,
                   '',
                   '',
                   NULL,
                   w_tran_reference,
                   FALSE,
                   TRUE,
                   w_tran_narration,
                   p_app_user_id,
                   current_timestamp);

      --- Debit Respinding Branch Ledger
      w_serial_no := w_serial_no + 1;
      w_tran_ac_number := '0';
      w_tran_gl_code := rec_tran_list.res_gl_code;
      w_contra_gl_code := w_ibr_gl_code;
      w_tran_type := 'IBR_POST';
      w_tran_amount := rec_tran_list.tran_amount;
      w_debit_credit := 'D';
      w_tran_narration :=
         'IBR Transaction ' || rec_tran_list.transaction_narration;
      w_tran_reference := rec_tran_list.transaction_id;
      w_acbrn_code := rec_tran_list.res_branch_code;

      INSERT INTO finance_transaction_table (branch_code,
                                             acbrn_code,
                                             transaction_date,
                                             batch_serial,
                                             account_number,
                                             tran_gl_code,
                                             contra_gl_code,
                                             tran_debit_credit,
                                             tran_type,
                                             tran_amount,
                                             available_balance,
                                             tran_person_phone,
                                             tran_person_name,
                                             tran_document_prefix,
                                             tran_document_number,
                                             tran_sign_verified,
                                             system_posted_tran,
                                             transaction_narration,
                                             app_user_id,
                                             app_data_time)
           VALUES (w_branch_code,
                   w_acbrn_code,
                   w_transaction_date,
                   w_serial_no,
                   w_tran_ac_number,
                   w_tran_gl_code,
                   w_contra_gl_code,
                   w_debit_credit,
                   w_tran_type,
                   w_tran_amount,
                   0,
                   '',
                   '',
                   NULL,
                   w_tran_reference,
                   FALSE,
                   TRUE,
                   w_tran_narration,
                   p_app_user_id,
                   current_timestamp);
   END LOOP;

   BEGIN
      SELECT *
        INTO w_status, w_errm, w_batch_number
        FROM fn_finance_post_tran (w_branch_code,
                                   p_app_user_id,
                                   'IBR_POST',
                                   w_transaction_date,
                                   'Inter Branch Fund Transfer',
                                   'IBR_POST');

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING MESSAGE = w_errm;
      ELSE
         BEGIN
            UPDATE finance_transaction_ibr
               SET tran_status = 'A',
                   batch_number = w_batch_number,
                   auth_by = p_app_user_id,
                   auth_on = current_timestamp
             WHERE transaction_id = p_transaction_id;
         END;
      END IF;
   END;

   o_status := 'S';
   o_errm := w_batch_number;
EXCEPTION
   WHEN OTHERS
   THEN
      IF w_status = 'E'
      THEN
         o_status := w_status;
         o_errm := w_errm;
      ELSE
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_post_cash_tran
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_post_cash_tran (
   IN      p_branch_code          INTEGER,
   IN      p_app_user_id          CHARACTER,
   IN      p_transaction_type     CHARACTER,
   IN      p_transaction_ledger   CHARACTER,
   IN      p_tran_date            DATE,
   IN      p_tran_narration       CHARACTER,
   IN      p_receive_payment      CHARACTER,
   IN      p_tran_source          CHARACTER,
       OUT o_status               CHARACTER,
       OUT o_errm                 CHARACTER,
       OUT o_batch_number         CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_error_message         VARCHAR;
   w_batch_number          INTEGER;
   w_check                 BOOLEAN;
   w_account_number        VARCHAR := '0';
   w_transaction_date      DATE;
   TRAN_DATA               RECORD;
   w_tran_gl_code          VARCHAR := '0';
   w_contra_gl_code        VARCHAR := '0';
   w_cash_transaction      BOOLEAN;
   w_total_leg             INTEGER;
   w_total_debit_amount    NUMERIC (22, 2) := 0;
   w_total_credit_amount   NUMERIC (22, 2) := 0;
   w_available_balance     NUMERIC (22, 2) := 0;
   w_tran_amount           NUMERIC (22, 2) := 0;
   w_batch_serial          INTEGER := 0;
   w_day_serial_no         INTEGER := 0;
   w_tran_debit_credit     VARCHAR;
   w_status                VARCHAR;
   w_errm                  VARCHAR;
BEGIN
     SELECT count (batch_serial) + 1
               batch_serial,
            SUM (
               (CASE WHEN tran_debit_credit = 'D' THEN tran_amount ELSE 0 END))
               debit_amount,
            SUM (
               (CASE WHEN tran_debit_credit = 'C' THEN tran_amount ELSE 0 END))
               credit_amount
       INTO w_batch_serial, w_total_debit_amount, w_total_credit_amount
       FROM finance_transaction_table S
      WHERE S.branch_code = p_branch_code AND S.app_user_id = p_app_user_id
   ORDER BY batch_serial;

   BEGIN
      SELECT cash_gl_code
        INTO w_tran_gl_code
        FROM finance_application_settings;
   END;

   IF w_batch_serial > 0
   THEN
      FOR TRAN_DATA
         IN (  SELECT tran_gl_code,
                      account_number,
                      count (batch_serial) batch_serial,
                      SUM (
                         (CASE
                             WHEN tran_debit_credit = 'D' THEN tran_amount
                             ELSE 0
                          END)) debit_amount,
                      SUM (
                         (CASE
                             WHEN tran_debit_credit = 'C' THEN tran_amount
                             ELSE 0
                          END)) credit_amount
                 FROM finance_transaction_table S
                WHERE S.app_user_id = p_app_user_id
             GROUP BY S.tran_gl_code, s.account_number
             ORDER BY batch_serial)
      LOOP
         w_batch_serial := TRAN_DATA.batch_serial + 1;
         w_account_number := TRAN_DATA.account_number;

         IF TRAN_DATA.debit_amount > 0.00
         THEN
            w_tran_debit_credit := 'C';
            w_tran_amount := TRAN_DATA.debit_amount;
         ELSE
            w_tran_debit_credit := 'D';
            w_tran_amount := TRAN_DATA.credit_amount;
         END IF;

         IF w_account_number != '0'
         THEN
            BEGIN
               SELECT account_ledger_code
                 INTO STRICT w_contra_gl_code
                 FROM finance_accounts_balance
                WHERE account_number = w_account_number;
            EXCEPTION
               WHEN NO_DATA_FOUND
               THEN
                  RAISE EXCEPTION USING MESSAGE = 'Invalid Account Number!';
            END;

            w_account_number := '0';
         ---RAISE EXCEPTION USING MESSAGE = w_contra_gl_code;
         ELSE
            w_contra_gl_code := TRAN_DATA.tran_gl_code;
         END IF;

         IF w_tran_amount > 0
         THEN
            INSERT INTO finance_transaction_table (branch_code,
                                                   transaction_date,
                                                   batch_serial,
                                                   account_number,
                                                   tran_gl_code,
                                                   contra_gl_code,
                                                   tran_debit_credit,
                                                   tran_type,
                                                   tran_amount,
                                                   available_balance,
                                                   tran_person_phone,
                                                   tran_person_name,
                                                   tran_document_prefix,
                                                   tran_document_number,
                                                   tran_sign_verified,
                                                   system_posted_tran,
                                                   transaction_narration,
                                                   app_user_id,
                                                   app_data_time)
                 VALUES (p_branch_code,
                         p_tran_date,
                         w_batch_serial,
                         w_account_number,
                         p_transaction_ledger,
                         w_contra_gl_code,
                         w_tran_debit_credit,
                         p_transaction_type,
                         w_tran_amount,
                         0.00,
                         NULL,
                         NULL,
                         NULL,
                         NULL,
                         FALSE,
                         FALSE,
                         p_tran_narration,
                         p_app_user_id,
                         current_timestamp);
         END IF;
      END LOOP;

      SELECT *
        INTO w_status, w_errm, w_batch_number
        FROM fn_finance_post_tran (p_branch_code,
                                   p_app_user_id,
                                   p_transaction_type,
                                   p_tran_date,
                                   p_tran_narration,
                                   p_tran_source);

      IF w_tran_gl_code = p_transaction_ledger
      THEN
         BEGIN
            SELECT COALESCE (max (batch_number) + 1, 1)
             INTO w_day_serial_no
             FROM finance_cash_transaction
            WHERE     branch_code = p_branch_code
                  AND app_user_id = p_app_user_id
                  AND transaction_date = p_tran_date;

            INSERT INTO finance_cash_transaction (branch_code,
                                                  transaction_date,
                                                  batch_number,
                                                  day_serial_no,
                                                  receive_payment,
                                                  transaction_amount,
                                                  transaction_narration,
                                                  auth_by,
                                                  auth_on,
                                                  cancel_by,
                                                  cancel_on,
                                                  app_user_id,
                                                  app_data_time)
                 VALUES (p_branch_code,
                         p_tran_date,
                         w_batch_number,
                         w_day_serial_no,
                         p_receive_payment,
                         w_tran_amount,
                         p_tran_narration,
                         p_app_user_id,
                         current_timestamp,
                         NULL,
                         NULL,
                         p_app_user_id,
                         current_timestamp);
         END;
      END IF;

      o_batch_number := w_batch_number;
      o_status := w_status;
      o_errm := w_errm;
   END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_post_tran
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_post_tran (
   IN      p_branch_code        INTEGER,
   IN      p_app_user_id        CHARACTER,
   IN      p_transaction_type   CHARACTER,
   IN      p_tran_date          DATE,
   IN      p_tran_narration     CHARACTER,
   IN      p_tran_source        CHARACTER,
       OUT o_status             CHARACTER,
       OUT o_errm               CHARACTER,
       OUT o_batch_number       CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_error_message             VARCHAR;
   w_batch_number              INTEGER;
   w_check                     BOOLEAN;
   w_account_number            VARCHAR := '0';
   w_transaction_date          DATE;
   w_last_balance_update       DATE;
   w_last_transaction_date     DATE;
   w_last_monbal_update        DATE;
   TRAN_DATA                   RECORD;
   w_tran_gl_code              VARCHAR := '0';
   w_cash_transaction          BOOLEAN;
   w_total_leg                 INTEGER;
   w_total_debit_amount        NUMERIC (22, 2) := 0;
   w_total_credit_amount       NUMERIC (22, 2) := 0;
   w_available_balance         NUMERIC (22, 2) := 0;
   w_new_credit_balance        NUMERIC (22, 2) := 0;
   w_new_debit_balance         NUMERIC (22, 2) := 0;
   w_new_available_balance     NUMERIC (22, 2) := 0;
   w_daily_credit_limit        NUMERIC (22, 2) := 0;
   w_daily_debit_limit         NUMERIC (22, 2) := 0;
   w_batch_serial              INTEGER := 0;
   w_status                    VARCHAR;
   w_errm                      VARCHAR;
   w_credit_limit              NUMERIC (22, 2) := 0;
   w_system_posted_tran        BOOL := FALSE;
   w_counter                   INTEGER := 0;
   w_branch_code               INTEGER := 0;
   w_cash_gl_code              VARCHAR;
   w_cash_user_id              VARCHAR;
   w_last_transaction_credit   DATE;
   w_last_transaction_debit    DATE;
BEGIN
   BEGIN
      SELECT COUNT (*)
        INTO w_total_leg
        FROM finance_transaction_table S
       WHERE S.app_user_id = p_app_user_id;
   END;

   IF w_total_leg = 0
   THEN
      w_status := 'E';
      w_errm := 'Nothing to Post.';
      RAISE EXCEPTION USING MESSAGE = w_errm;
   END IF;

   BEGIN
      SELECT COALESCE (max (batch_number) + 1, 1)
        INTO w_batch_number
        FROM finance_transaction_master
       WHERE branch_code = p_branch_code AND transaction_date = p_tran_date;
   END;

   BEGIN
      SELECT daily_credit_limit,
             daily_debit_limit,
             branch_code,
             cash_gl_code
        INTO w_daily_credit_limit,
             w_daily_debit_limit,
             w_branch_code,
             w_cash_gl_code
        FROM appauth_user_settings
       WHERE app_user_id = p_app_user_id;
   END;

   BEGIN
      SELECT cash_gl_code
        INTO STRICT w_cash_gl_code
        FROM finance_application_settings;
   EXCEPTION
      WHEN NO_DATA_FOUND
      THEN
         RAISE EXCEPTION USING MESSAGE = 'Invalid Cash Ledger Settings!';
   END;


   FOR TRAN_DATA
      IN (  SELECT branch_code,
                   COALESCE (acbrn_code, branch_code) acbrn_code,
                   transaction_date,
                   batch_serial,
                   account_number,
                   tran_gl_code,
                   contra_gl_code,
                   tran_debit_credit,
                   tran_type,
                   tran_amount,
                   COALESCE (principal_amount, 0.00) principal_amount,
                   COALESCE (profit_amount, 0.00) profit_amount,
                   COALESCE (charge_amount, 0.00) charge_amount,
                   (CASE
                       WHEN tran_debit_credit = 'D' THEN -tran_amount
                       ELSE tran_amount
                    END) balance_amount,
                   (CASE
                       WHEN tran_debit_credit = 'D' THEN tran_amount
                       ELSE 0
                    END) debit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'C' THEN tran_amount
                       ELSE 0
                    END) credit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'D'
                       THEN
                          COALESCE (principal_amount, 0.00)
                       ELSE
                          0
                    END) principal_debit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'C'
                       THEN
                          COALESCE (principal_amount, 0.00)
                       ELSE
                          0
                    END) principal_credit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'D'
                       THEN
                          COALESCE (profit_amount, 0.00)
                       ELSE
                          0
                    END) profit_debit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'C'
                       THEN
                          COALESCE (profit_amount, 0.00)
                       ELSE
                          0
                    END) profit_credit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'D'
                       THEN
                          COALESCE (charge_amount, 0.00)
                       ELSE
                          0
                    END) charge_debit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'C'
                       THEN
                          COALESCE (charge_amount, 0.00)
                       ELSE
                          0
                    END) charge_credit_amount,
                   charge_code,
                   available_balance,
                   tran_document_prefix,
                   tran_document_number,
                   tran_person_phone,
                   tran_person_name,
                   tran_sign_verified,
                   system_posted_tran,
                   transaction_narration,
                   app_user_id,
                   app_data_time
              FROM finance_transaction_table S
             WHERE S.app_user_id = p_app_user_id
          ORDER BY batch_serial)
   LOOP
      w_account_number := TRAN_DATA.account_number;
      w_transaction_date := TRAN_DATA.transaction_date;
      w_tran_gl_code := TRAN_DATA.tran_gl_code;
      w_total_debit_amount := w_total_debit_amount + TRAN_DATA.debit_amount;
      w_total_credit_amount :=
         w_total_credit_amount + TRAN_DATA.credit_amount;
      w_batch_serial := w_batch_serial + 1;

      w_last_balance_update := NULL;
      w_last_transaction_date := NULL;

      IF w_account_number != '0'
      THEN
         BEGIN
            SELECT account_ledger_code
              INTO STRICT w_tran_gl_code
              FROM finance_accounts_balance
             WHERE account_number = w_account_number;
         EXCEPTION
            WHEN NO_DATA_FOUND
            THEN
               RAISE EXCEPTION USING MESSAGE = 'Invalid Account Number!';
         END;
      END IF;

      IF     COALESCE (TRAN_DATA.account_number, '0') = '0'
         AND COALESCE (TRAN_DATA.tran_gl_code, '0') = '0'
      THEN
         RAISE EXCEPTION
         USING MESSAGE =
                  'Posting Error Both ledger code and phone number can not be Zero!';
      END IF;

      IF     TRAN_DATA.tran_debit_credit = 'D'
         AND TRAN_DATA.debit_amount > w_daily_debit_limit
      THEN
         RAISE EXCEPTION
         USING MESSAGE =
                     'Your Transaction Limit '
                  || w_daily_debit_limit
                  || ' Will be Exceeded for This Transaction!';
      END IF;

      IF     TRAN_DATA.tran_debit_credit = 'C'
         AND TRAN_DATA.credit_amount > w_daily_credit_limit
      THEN
         RAISE EXCEPTION
         USING MESSAGE =
                     'Your Transaction Limit '
                  || w_daily_credit_limit
                  || ' Will be Exceeded for This Transaction!';
      END IF;

      IF w_tran_gl_code != '0'
      THEN
         BEGIN
            SELECT gl_code
              INTO STRICT w_tran_gl_code
              FROM finance_general_ledger
             WHERE gl_code = w_tran_gl_code;
         EXCEPTION
            WHEN NO_DATA_FOUND
            THEN
               RAISE EXCEPTION
               USING MESSAGE =
                           'Posting Error Invalid Ledger Code! '
                        || w_tran_gl_code;
         END;

         BEGIN
            SELECT gl_balance,
                   COALESCE (last_balance_update, w_transaction_date)
                      last_balance_update,
                   COALESCE (last_transaction_date, w_transaction_date)
                      last_transaction_date,
                   COALESCE (last_monbal_update, w_transaction_date)
                      last_monbal_update
              INTO STRICT w_available_balance,
                          w_last_balance_update,
                          w_last_transaction_date,
                          w_last_monbal_update
              FROM finance_ledger_balance
             WHERE     branch_code = TRAN_DATA.acbrn_code
                   AND gl_code = w_tran_gl_code;

            w_last_balance_update :=
               LEAST (w_last_balance_update, w_transaction_date);
            w_last_transaction_date :=
               GREATEST (w_last_transaction_date, w_transaction_date);
            w_last_monbal_update :=
               LEAST (w_last_monbal_update, w_transaction_date);

            UPDATE finance_ledger_balance
               SET gl_balance = gl_balance + TRAN_DATA.balance_amount,
                   total_debit_sum = total_debit_sum + TRAN_DATA.debit_amount,
                   total_credit_sum =
                      total_credit_sum + TRAN_DATA.credit_amount,
                   last_balance_update = w_last_balance_update,
                   last_transaction_date = w_last_transaction_date,
                   last_monbal_update = w_last_monbal_update,
                   is_balance_updated = FALSE,
                   is_monbal_updated = FALSE,
                   is_monbal_recpay_updated = FALSE
             WHERE     branch_code = TRAN_DATA.acbrn_code
                   AND gl_code = w_tran_gl_code;

            UPDATE finance_cash_and_bank_ledger
               SET last_balance_update = w_last_balance_update,
                   last_transaction_date = w_last_transaction_date,
                   is_balance_updated = FALSE
             WHERE     branch_code = TRAN_DATA.acbrn_code
                   AND gl_code = w_tran_gl_code;

            w_available_balance :=
               w_available_balance + TRAN_DATA.balance_amount;
         EXCEPTION
            WHEN NO_DATA_FOUND
            THEN
               INSERT INTO finance_ledger_balance (branch_code,
                                                   gl_code,
                                                   last_transaction_date,
                                                   last_balance_update,
                                                   is_balance_updated,
                                                   is_monbal_updated,
                                                   is_monbal_recpay_updated,
                                                   total_debit_sum,
                                                   total_credit_sum,
                                                   gl_balance,
                                                   unauth_debit_sum,
                                                   unauth_credit_sum,
                                                   transfer_debit_sum,
                                                   transfer_credit_sum,
                                                   auth_by,
                                                   auth_on,
                                                   cancel_by,
                                                   cancel_on,
                                                   app_user_id,
                                                   app_data_time)
                    VALUES (TRAN_DATA.acbrn_code,
                            w_tran_gl_code,
                            w_transaction_date,
                            w_transaction_date,
                            FALSE,
                            FALSE,
                            FALSE,
                            TRAN_DATA.debit_amount,
                            TRAN_DATA.credit_amount,
                            TRAN_DATA.balance_amount,
                            0.00,
                            0.00,
                            0.00,
                            0.00,
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            p_app_user_id,
                            current_timestamp);

               w_available_balance := TRAN_DATA.balance_amount;
         END;
      END IF;

      IF TRAN_DATA.system_posted_tran
      THEN
         w_system_posted_tran := TRUE;
      END IF;

      IF w_account_number != '0'
      THEN
         BEGIN
            SELECT COALESCE (account_balance, 0),
                   COALESCE (credit_limit, 0),
                   COALESCE (last_balance_update, w_transaction_date)
                      last_balance_update,
                   COALESCE (last_transaction_date, w_transaction_date)
                      last_transaction_date,
                   COALESCE (last_monbal_update, w_transaction_date)
                      last_monbal_update,
                   last_transaction_credit,
                   last_transaction_debit
              INTO STRICT w_available_balance,
                          w_credit_limit,
                          w_last_balance_update,
                          w_last_transaction_date,
                          w_last_monbal_update,
                          w_last_transaction_credit,
                          w_last_transaction_debit
              FROM finance_accounts_balance
             WHERE account_number = w_account_number;
         EXCEPTION
            WHEN NO_DATA_FOUND
            THEN
               RAISE EXCEPTION
               USING MESSAGE = 'Invalid Account Number !' || w_account_number;
         END;


         IF TRAN_DATA.tran_debit_credit = 'C'
         THEN
            w_last_transaction_credit :=
               GREATEST (w_last_transaction_credit, w_transaction_date);
         END IF;

         IF TRAN_DATA.tran_debit_credit = 'D'
         THEN
            w_last_transaction_debit :=
               GREATEST (w_last_transaction_debit, w_transaction_date);
         END IF;

         w_last_transaction_date :=
            GREATEST (w_last_transaction_date, w_transaction_date);
         w_last_balance_update :=
            least (w_last_balance_update, w_transaction_date);
         w_last_monbal_update :=
            LEAST (w_last_monbal_update, w_transaction_date);

         UPDATE finance_accounts_balance
            SET account_balance = account_balance + TRAN_DATA.balance_amount,
                total_debit_amount =
                   total_debit_amount + TRAN_DATA.debit_amount,
                total_credit_amount =
                   total_credit_amount + TRAN_DATA.credit_amount,
                principal_debit =
                   principal_debit + TRAN_DATA.principal_debit_amount,
                principal_credit =
                   principal_credit + TRAN_DATA.principal_credit_amount,
                profit_debit = profit_debit + TRAN_DATA.profit_debit_amount,
                profit_credit =
                   profit_credit + TRAN_DATA.profit_credit_amount,
                charge_debit = charge_debit + TRAN_DATA.charge_debit_amount,
                charge_credit =
                   charge_credit + TRAN_DATA.charge_credit_amount,
                last_balance_update = w_last_balance_update,
                last_transaction_date = w_last_transaction_date,
                last_monbal_update = w_last_monbal_update,
                is_balance_updated = FALSE,
                last_transaction_debit = w_last_transaction_debit,
                last_transaction_credit = w_last_transaction_credit
          WHERE account_number = w_account_number;

         BEGIN
            SELECT sum (tran_amount)
             INTO w_new_credit_balance
             FROM finance_transaction_table S
            WHERE     S.branch_code = p_branch_code
                  AND S.app_user_id = p_app_user_id
                  AND s.account_number = w_account_number
                  AND s.tran_debit_credit = 'C';
         END;

         BEGIN
            SELECT sum (tran_amount)
             INTO w_new_debit_balance
             FROM finance_transaction_table S
            WHERE     S.branch_code = p_branch_code
                  AND S.app_user_id = p_app_user_id
                  AND s.account_number = w_account_number
                  AND s.tran_debit_credit = 'D';
         END;

         w_new_available_balance :=
            w_new_credit_balance - w_new_debit_balance;

         -- w_errm:= w_available_balance||' . '||TRAN_DATA.tran_amount||TRAN_DATA.tran_debit_credit||' . '||w_credit_limit;
         -- w_status := 'E';
         -- RAISE EXCEPTION USING MESSAGE = w_errm;

         IF     TRAN_DATA.tran_debit_credit = 'D'
            AND (w_available_balance) < TRAN_DATA.tran_amount
         THEN
            IF    w_credit_limit < abs (w_available_balance)
               OR w_credit_limit = 0
            THEN
               w_status := 'E';
               w_errm :=
                     'Credit Limit ('
                  || w_available_balance
                  || ') Exceed For This Transaction!';
               RAISE EXCEPTION USING MESSAGE = w_errm;
            END IF;
         END IF;
      END IF;


      IF w_cash_gl_code = w_tran_gl_code
      THEN
         BEGIN
            SELECT teller_id
              INTO STRICT w_cash_user_id
              FROM finance_transaction_telbal
             WHERE teller_id = p_app_user_id;

            UPDATE finance_transaction_telbal
               SET total_credit_amount =
                      total_credit_amount + TRAN_DATA.credit_amount,
                   total_debit_amount =
                      total_debit_amount + TRAN_DATA.debit_amount,
                   cash_balance = cash_balance - TRAN_DATA.balance_amount,
                   last_balance_update = w_last_balance_update,
                   last_transaction_date = w_last_transaction_date,
                   is_balance_updated = FALSE
             WHERE teller_id = p_app_user_id;
         EXCEPTION
            WHEN NO_DATA_FOUND
            THEN
               INSERT INTO finance_transaction_telbal (branch_code,
                                                       teller_id,
                                                       cash_od_allowed,
                                                       is_balance_updated,
                                                       credit_limit_amount,
                                                       debit_limit_amount,
                                                       total_credit_amount,
                                                       total_debit_amount,
                                                       cash_balance,
                                                       last_balance_update,
                                                       last_transaction_date,
                                                       app_user_id,
                                                       app_data_time)
                    VALUES (p_branch_code,
                            p_app_user_id,
                            FALSE,
                            FALSE,
                            999999999999999.00,
                            999999999999999.00,
                            TRAN_DATA.credit_amount,
                            TRAN_DATA.debit_amount,
                            TRAN_DATA.balance_amount,
                            w_last_balance_update,
                            w_last_transaction_date,
                            p_app_user_id,
                            current_timestamp);
         END;
      END IF;

      INSERT INTO finance_transaction_details (branch_code,
                                               acbrn_code,
                                               transaction_date,
                                               batch_number,
                                               batch_serial,
                                               account_number,
                                               tran_gl_code,
                                               contra_gl_code,
                                               tran_debit_credit,
                                               tran_type,
                                               tran_amount,
                                               principal_amount,
                                               profit_amount,
                                               charge_amount,
                                               charge_code,
                                               cancel_amount,
                                               available_balance,
                                               tran_document_prefix,
                                               tran_document_number,
                                               tran_person_phone,
                                               tran_person_name,
                                               tran_sign_verified,
                                               system_posted_tran,
                                               transaction_narration,
                                               auth_by,
                                               auth_on,
                                               cancel_by,
                                               cancel_on,
                                               app_user_id,
                                               app_data_time)
           VALUES (p_branch_code,
                   TRAN_DATA.acbrn_code,
                   p_tran_date,
                   w_batch_number,
                   w_batch_serial,
                   w_account_number,
                   w_tran_gl_code,
                   TRAN_DATA.contra_gl_code,
                   TRAN_DATA.tran_debit_credit,
                   TRAN_DATA.tran_type,
                   TRAN_DATA.tran_amount,
                   TRAN_DATA.principal_amount,
                   TRAN_DATA.profit_amount,
                   TRAN_DATA.charge_amount,
                   TRAN_DATA.charge_code,
                   0,
                   w_available_balance,
                   TRAN_DATA.tran_document_prefix,
                   TRAN_DATA.tran_document_number,
                   TRAN_DATA.tran_person_phone,
                   TRAN_DATA.tran_person_name,
                   TRAN_DATA.tran_sign_verified,
                   TRAN_DATA.system_posted_tran,
                   TRAN_DATA.transaction_narration,
                   p_app_user_id,
                   current_timestamp,
                   NULL,
                   NULL,
                   p_app_user_id,
                   current_timestamp);
   /*
         IF w_account_number != '0'
         THEN
            SELECT w_status, w_errm
              INTO w_status, w_errm
              FROM fn_finance_acbal_hist (w_account_number,
                                          w_last_transaction_date);

            IF w_status = 'E'
            THEN
               RAISE EXCEPTION USING MESSAGE = w_errm;
            END IF;
         END IF;

         IF w_tran_gl_code != '0'
         THEN
            SELECT w_status, w_errm
              INTO w_status, w_errm
              FROM fn_finance_glbal_hist (w_tran_gl_code,
                                          p_branch_code,
                                          w_last_transaction_date);

            IF w_status = 'E'
            THEN
               RAISE EXCEPTION USING MESSAGE = w_errm;
            END IF;

            SELECT w_status, w_errm
              INTO w_status, w_errm
              FROM fn_finance_glmonbal_hist (w_tran_gl_code,
                                             p_branch_code,
                                             w_last_transaction_date);

            IF w_status = 'E'
            THEN
               RAISE EXCEPTION USING MESSAGE = w_errm;
            END IF;
         END IF;
         */
   END LOOP;

   IF w_total_debit_amount != w_total_credit_amount
   THEN
      w_status := 'E';
      w_errm :=
            'Total Debit ('
         || w_total_debit_amount
         || ') and Credit Amount ('
         || w_total_credit_amount
         || ') Must Be Same';
      RAISE EXCEPTION USING MESSAGE = w_errm;
   END IF;

   BEGIN
      INSERT INTO finance_transaction_master (branch_code,
                                              transaction_date,
                                              batch_number,
                                              tran_type,
                                              total_debit_amount,
                                              total_credit_amount,
                                              tran_source_table,
                                              tran_source_key,
                                              transaction_narration,
                                              system_posted_tran,
                                              auth_by,
                                              auth_on,
                                              cancel_by,
                                              cancel_on,
                                              app_user_id,
                                              app_data_time)
           VALUES (p_branch_code,
                   p_tran_date,
                   w_batch_number,
                   p_transaction_type,
                   w_total_debit_amount,
                   w_total_credit_amount,
                   p_tran_source,
                   'NA',
                   p_tran_narration,
                   w_system_posted_tran,
                   p_app_user_id,
                   current_timestamp,
                   NULL,
                   NULL,
                   p_app_user_id,
                   current_timestamp);
   END;

   BEGIN
      DELETE FROM finance_transaction_table S
            WHERE S.app_user_id = p_app_user_id;
   END;

   o_batch_number := w_batch_number;
   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      IF w_status = 'E'
      THEN
         o_status := w_status;
         o_errm := w_errm;
         o_batch_number := 0;
      ELSE
         o_errm := SQLERRM;
         o_status := 'E';
         o_batch_number := 0;
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_post_tran_cancel
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_post_tran_cancel (
   IN      p_branch_code     INTEGER,
   IN      p_app_user_id     CHARACTER,
   IN      p_tran_date       DATE,
   IN      p_batch_number    INTEGER,
   IN      p_cancel_reason   CHARACTER,
       OUT o_status          CHARACTER,
       OUT o_errm            CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_error_message           VARCHAR;
   w_status                  VARCHAR;
   w_batch_number            INTEGER;
   w_check                   BOOLEAN;
   w_account_number          VARCHAR := '0';
   w_transaction_date        DATE;
   w_last_balance_update     DATE;
   w_last_transaction_date   DATE;
   w_last_monbal_update      DATE;
   TRAN_DATA                 RECORD;
   w_tran_gl_code            VARCHAR := '0';
   w_cash_gl_code            VARCHAR := '0';
   w_cash_transaction        BOOLEAN;
   w_total_leg               INTEGER;
   w_total_debit_amount      NUMERIC (22, 2) := 0;
   w_total_credit_amount     NUMERIC (22, 2) := 0;
   w_available_balance       NUMERIC (22, 2) := 0;
   w_batch_serial            INTEGER := 0;
   w_counter                 INTEGER := 0;
BEGIN
   BEGIN
      SELECT count (1)
       INTO w_counter
       FROM finance_transaction_details S
      WHERE     S.branch_code = p_branch_code
            AND s.transaction_date = p_tran_date
            AND s.batch_number = p_batch_number;
   END;

   IF w_counter = 0
   THEN
      RAISE EXCEPTION USING MESSAGE = 'Invalid Batch Information';
   END IF;

   w_counter := 0;

   BEGIN
      SELECT cash_gl_code
        INTO STRICT w_cash_gl_code
        FROM finance_application_settings;
   EXCEPTION
      WHEN NO_DATA_FOUND
      THEN
         RAISE EXCEPTION USING MESSAGE = 'Invalid Cash Ledger Code!';
   END;


   FOR TRAN_DATA
      IN (  SELECT branch_code,
                   transaction_date,
                   batch_serial,
                   account_number,
                   tran_gl_code,
                   contra_gl_code,
                   tran_debit_credit,
                   tran_type,
                   tran_amount,
                   (CASE
                       WHEN tran_debit_credit = 'C' THEN -tran_amount
                       ELSE tran_amount
                    END) balance_amount,
                   (CASE
                       WHEN tran_debit_credit = 'D' THEN -tran_amount
                       ELSE 0
                    END) debit_amount,
                   (CASE
                       WHEN tran_debit_credit = 'C' THEN -tran_amount
                       ELSE 0
                    END) credit_amount,
                   available_balance,
                   tran_document_prefix,
                   tran_document_number,
                   tran_person_phone,
                   tran_person_name,
                   tran_sign_verified,
                   system_posted_tran,
                   transaction_narration,
                   app_user_id,
                   app_data_time
              FROM finance_transaction_details S
             WHERE     S.branch_code = p_branch_code
                   AND s.transaction_date = p_tran_date
                   AND s.batch_number = p_batch_number
                   AND s.cancel_by IS NULL
          ORDER BY batch_serial)
   LOOP
      w_account_number := TRAN_DATA.account_number;
      w_transaction_date := TRAN_DATA.transaction_date;
      w_tran_gl_code := TRAN_DATA.tran_gl_code;
      w_total_debit_amount := w_total_debit_amount + TRAN_DATA.debit_amount;
      w_total_credit_amount :=
         w_total_credit_amount + TRAN_DATA.credit_amount;
      w_batch_serial := w_batch_serial + 1;
      w_counter := w_counter + 1;

      IF w_tran_gl_code != '0'
      THEN
         BEGIN
            SELECT gl_balance,
                   COALESCE (last_balance_update, w_transaction_date)
                      last_balance_update,
                   COALESCE (last_transaction_date, w_transaction_date)
                      last_transaction_date,
                   COALESCE (last_monbal_update, w_transaction_date)
                      last_monbal_update
              INTO STRICT w_available_balance,
                          w_last_balance_update,
                          w_last_transaction_date,
                          w_last_monbal_update
              FROM finance_ledger_balance
             WHERE     branch_code = TRAN_DATA.branch_code
                   AND gl_code = w_tran_gl_code;

            w_last_balance_update :=
               LEAST (w_last_balance_update, w_transaction_date);
            w_last_transaction_date :=
               GREATEST (w_last_transaction_date, w_transaction_date);
            w_last_monbal_update :=
               LEAST (w_last_monbal_update, w_transaction_date);

            UPDATE finance_ledger_balance
               SET gl_balance = gl_balance + TRAN_DATA.balance_amount,
                   total_debit_sum = total_debit_sum + TRAN_DATA.debit_amount,
                   total_credit_sum =
                      total_credit_sum + TRAN_DATA.credit_amount,
                   last_balance_update = w_last_balance_update,
                   last_transaction_date = w_last_transaction_date,
                   last_monbal_update = w_last_monbal_update,
                   is_balance_updated = FALSE,
                   is_monbal_updated = FALSE,
                   is_monbal_recpay_updated = FALSE
             WHERE     branch_code = TRAN_DATA.branch_code
                   AND gl_code = w_tran_gl_code;

            UPDATE finance_cash_and_bank_ledger
               SET last_balance_update = w_last_balance_update,
                   last_transaction_date = w_last_transaction_date,
                   is_balance_updated = FALSE
             WHERE     branch_code = TRAN_DATA.branch_code
                   AND gl_code = w_tran_gl_code;

            DELETE FROM
               finance_ledger_balance_hist
                  WHERE     gl_code = w_tran_gl_code
                        AND transaction_date = w_transaction_date
                        AND branch_code = TRAN_DATA.branch_code;

            DELETE FROM
               finance_led_rec_pay_bal_hist
                  WHERE     gl_code = TRAN_DATA.contra_gl_code
                        AND transaction_date = w_transaction_date
                        AND branch_code = TRAN_DATA.branch_code;

            IF w_cash_gl_code = w_tran_gl_code
            THEN
               BEGIN
                  UPDATE finance_transaction_telbal
                     SET total_credit_amount =
                            total_credit_amount + TRAN_DATA.credit_amount,
                         total_debit_amount =
                            total_debit_amount + TRAN_DATA.debit_amount,
                         cash_balance =
                            cash_balance - TRAN_DATA.balance_amount
                   WHERE teller_id = TRAN_DATA.app_user_id;
               END;
            END IF;
         END;
      END IF;

      IF w_account_number != '0'
      THEN
         BEGIN
            SELECT COALESCE (account_balance, 0),
                   COALESCE (last_balance_update, w_transaction_date)
                      last_balance_update,
                   COALESCE (last_transaction_date, w_transaction_date)
                      last_transaction_date,
                   COALESCE (last_monbal_update, w_transaction_date)
                      last_monbal_update
              INTO STRICT w_available_balance,
                          w_last_balance_update,
                          w_last_transaction_date,
                          w_last_monbal_update
              FROM finance_accounts_balance
             WHERE account_number = w_account_number;
         EXCEPTION
            WHEN NO_DATA_FOUND
            THEN
               RAISE EXCEPTION
               USING MESSAGE = 'Invalid Account Number !' || w_account_number;
         END;

         w_last_transaction_date :=
            GREATEST (w_last_transaction_date, w_transaction_date);
         w_last_balance_update :=
            least (w_last_balance_update, w_transaction_date);
         w_last_monbal_update :=
            LEAST (w_last_monbal_update, w_transaction_date);

         UPDATE finance_accounts_balance
            SET account_balance = account_balance + TRAN_DATA.balance_amount,
                total_debit_amount =
                   total_debit_amount + TRAN_DATA.debit_amount,
                total_credit_amount =
                   total_credit_amount + TRAN_DATA.credit_amount,
                last_balance_update = w_last_balance_update,
                last_transaction_date = w_last_transaction_date,
                last_monbal_update = w_last_monbal_update,
                is_balance_updated = FALSE
          WHERE account_number = w_account_number;

         DELETE FROM
            finance_accounts_balance_hist
               WHERE     account_number = w_account_number
                     AND transaction_date = w_transaction_date;
      END IF;

      BEGIN
         UPDATE finance_transaction_details S
            SET cancel_amount = tran_amount,
                cancel_by = p_app_user_id,
                cancel_on = current_timestamp,
                cancel_remarks = p_cancel_reason
          WHERE     S.branch_code = p_branch_code
                AND s.transaction_date = p_tran_date
                AND s.batch_number = p_batch_number;

         UPDATE finance_transaction_master M
            SET cancel_by = p_app_user_id,
                cancel_on = current_timestamp,
                cancel_remarks = p_cancel_reason
          WHERE     M.branch_code = p_branch_code
                AND M.transaction_date = p_tran_date
                AND M.batch_number = p_batch_number;

         UPDATE finance_cash_transaction c
            SET cancel_by = p_app_user_id,
                cancel_on = current_timestamp,
                cancel_remarks = p_cancel_reason
          WHERE     c.branch_code = p_branch_code
                AND c.transaction_date = p_tran_date
                AND c.batch_number = p_batch_number;
      END;
   END LOOP;

   IF w_counter = 0
   THEN
      RAISE EXCEPTION USING MESSAGE = 'Batch Already Canceled!';
   END IF;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      IF w_status = 'E'
      THEN
         o_status := w_status;
         o_errm := w_error_message || ' ' || w_tran_gl_code;
      ELSE
         o_errm := SQLERRM || ' ' || w_tran_gl_code;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_query_account_statement
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_query_account_statement (
   IN      p_account_number   CHARACTER,
   IN      p_from_date        DATE,
   IN      p_upto_date        DATE,
   IN      p_app_user_id      CHARACTER,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_status                  VARCHAR;
   w_counter                 INTEGER;
   w_errm                    VARCHAR;
   w_last_transaction_date   DATE;
   w_account_number          VARCHAR;
   w_account_title           VARCHAR;
   w_account_balance         NUMERIC (22, 2) := 0;
BEGIN
   SELECT count (account_number)
     INTO w_counter
     FROM finance_accounts_balance
    WHERE account_number = p_account_number;

   IF w_counter = 0
   THEN
      RAISE EXCEPTION USING MESSAGE = 'Invalid Account Number!';
   END IF;

   SELECT account_number,
          account_title,
          account_balance,
          last_transaction_date
     INTO w_account_number,
          w_account_title,
          w_account_balance,
          w_last_transaction_date
     FROM finance_accounts_balance
    WHERE account_number = p_account_number;

   SELECT w_status, w_errm
     INTO w_status, w_errm
     FROM fn_finance_acbal_hist (p_account_number, w_last_transaction_date);

   DELETE FROM appauth_query_table
         WHERE app_user_id = p_app_user_id;

   INSERT INTO appauth_query_table (chr_column1,
                                    chr_column3,
                                    chr_column4,
                                    dec_column4,
                                    dat_column1,
                                    chr_column2,
                                    dec_column1,
                                    dec_column2,
                                    dec_column3,
                                    app_user_id)
      SELECT serial_number,
             w_account_number,
             w_account_title,
             w_account_balance,
             transaction_date,
             transaction_narration,
             credit_balance,
             debit_balance,
             SUM (credit_balance - debit_balance)
                OVER (ORDER BY serial_number) account_balance,
             p_app_user_id
        FROM (SELECT 1  serial_number,
                     p_from_date - 1 transaction_date,
                     'Opening Balance' transaction_narration,
                     (CASE
                         WHEN o_account_balance > 0 THEN o_account_balance
                         ELSE 0
                      END) credit_balance,
                     (CASE
                         WHEN o_account_balance < 0
                         THEN
                            abs (o_account_balance)
                         ELSE
                            0
                      END) debit_balance
                FROM fn_finance_get_ason_acbal (p_account_number,
                                                p_from_date - 1)
              UNION ALL
              SELECT   (ROW_NUMBER ()
                        OVER (
                           ORDER BY
                              transaction_date, batch_number, batch_serial))
                     + 1 serial_number,
                     transaction_date,
                     transaction_narration,
                     (CASE
                         WHEN tran_debit_credit = 'C' THEN tran_amount
                         ELSE 0
                      END) credit_balance,
                     (CASE
                         WHEN tran_debit_credit = 'D' THEN tran_amount
                         ELSE 0
                      END) debit_balance
                FROM finance_transaction_details
               WHERE     account_number = p_account_number
                     AND cancel_by IS NULL
                     AND transaction_date BETWEEN p_from_date AND p_upto_date)
             a;

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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_query_daily_transaction
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_query_daily_transaction (
   IN      p_branch_code      INTEGER,
   IN      p_from_date        DATE,
   IN      p_upto_date        DATE,
   IN      p_account_number   CHARACTER,
   IN      p_tran_gl_code     CHARACTER,
   IN      p_app_user_id      CHARACTER,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_errm        VARCHAR;
   w_status      VARCHAR;
   w_sql_stat    TEXT := '';
   w_ason_date   DATE;
   w_from_date   DATE;
   w_upto_date   DATE;
BEGIN
   IF p_from_date = p_upto_date
   THEN
      w_ason_date := p_from_date;
   ELSE
      w_from_date := p_from_date;
      w_upto_date := p_upto_date;
   END IF;

   DELETE FROM appauth_query_table
         WHERE app_user_id = p_app_user_id;

   IF p_account_number <> '0'
   THEN
      w_sql_stat :=
            'INSERT INTO appauth_query_table (int_column1,
                                  dat_column1,
                                  int_column2,
                                  chr_column1,
                                  chr_column2,
                                  chr_column3,
                                  chr_column4,
                                  chr_column5,
                                  dec_column1,
                                  dec_column2,
                                  chr_column6,
                                  chr_column7,
                                  chr_column8,
                                  dat_column2,
                                  chr_column9,
                                  dat_column3,
                                  app_user_id)
      SELECT t.branch_code,
             t.transaction_date,
             t.batch_number,
             t.tran_gl_code,
             l.gl_name,
             t.account_number,
             a.account_title account_name,
             (case when t.tran_debit_credit=''C'' then ''Payment'' else ''Receipt'' end) tran_debit_credit,
             t.tran_amount,
             t.cancel_amount,
             t.tran_document_number,
             t.transaction_narration,
             t.cancel_by,
             t.cancel_on,
             t.app_user_id,
             t.app_data_time,
             '''
         || p_app_user_id
         || '''
        FROM finance_transaction_details t, finance_general_ledger l, finance_accounts_balance a
       WHERE t.tran_gl_code = l.gl_code 
       and a.account_number=t.account_number
       and a.account_number= '''
         || p_account_number
         || '''';
   ELSIF p_tran_gl_code <> '0'
   THEN
      w_sql_stat :=
            'INSERT INTO appauth_query_table (int_column1,
                                  dat_column1,
                                  int_column2,
                                  chr_column1,
                                  chr_column2,
                                  chr_column3,
                                  chr_column4,
                                  chr_column5,
                                  dec_column1,
                                  dec_column2,
                                  chr_column6,
                                  chr_column7,
                                  chr_column8,
                                  dat_column2,
                                  chr_column9,
                                  dat_column3,
                                  app_user_id)
      SELECT t.branch_code,
             t.transaction_date,
             t.batch_number,
             t.tran_gl_code,
             l.gl_name,
             t.account_number,
             '' '' account_name,
             (case when t.tran_debit_credit=''C'' then ''Payment'' else ''Receipt'' end) tran_debit_credit,
             t.tran_amount,
             t.cancel_amount,
             t.tran_document_number,
             t.transaction_narration,
             t.cancel_by,
             t.cancel_on,
             t.app_user_id,
             t.app_data_time,
             '''
         || p_app_user_id
         || '''
        FROM finance_transaction_details t, finance_general_ledger l
       WHERE t.tran_gl_code = l.gl_code ';
   END IF;

   IF p_account_number <> '0' OR p_tran_gl_code <> '0'
   THEN
      IF p_tran_gl_code <> '0'
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and t.tran_gl_code = '''
            || p_tran_gl_code
            || '''';
      END IF;

      IF w_from_date IS NOT NULL AND w_upto_date IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and t.transaction_date between '''
            || w_from_date
            || ''' and '''
            || w_upto_date
            || '''';
      END IF;

      IF w_ason_date IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and t.transaction_date = '''
            || w_ason_date
            || '''';
      END IF;

      IF p_branch_code IS NOT NULL
      THEN
         w_sql_stat := w_sql_stat || ' and t.branch_code = ' || p_branch_code;
      END IF;


      --RAISE EXCEPTION USING MESSAGE = w_sql_stat;

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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_query_ledger_statement
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_query_ledger_statement (
   IN      p_gl_code       CHARACTER,
   IN      p_branch_code   INTEGER,
   IN      p_from_date     DATE,
   IN      p_upto_date     DATE,
   IN      p_app_user_id   CHARACTER,
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
   w_counter                INTEGER;
   w_errm                   VARCHAR;
   w_gl_name                VARCHAR;
   w_current_business_day   DATE;
   w_gl_balance             NUMERIC (20, 2);
BEGIN
   SELECT count (gl_code)
     INTO w_counter
     FROM finance_general_ledger
    WHERE gl_code = p_gl_code;

   DELETE FROM appauth_query_table
         WHERE app_user_id = p_app_user_id;

   IF w_counter = 0
   THEN
      RAISE EXCEPTION USING MESSAGE = 'Invalid Ledger Code!';
   END IF;

   --    RAISE EXCEPTION USING MESSAGE = p_branch_code;

   SELECT gl_name
     INTO w_gl_name
     FROM finance_general_ledger
    WHERE gl_code = p_gl_code;

   IF p_branch_code = 0
   THEN
      INSERT INTO appauth_query_table (chr_column1,
                                       dat_column1,
                                       chr_column2,
                                       dec_column1,
                                       dec_column2,
                                       dec_column3,
                                       app_user_id)
           SELECT serial_number,
                  transaction_date,
                  transaction_narration,
                  credit_balance,
                  debit_balance,
                  SUM (credit_balance - debit_balance)
                     OVER (ORDER BY serial_number) ledger_balance,
                  p_app_user_id
             FROM (SELECT 1  serial_number,
                          p_from_date - 1 transaction_date,
                          'Opening Balance' transaction_narration,
                          (CASE
                              WHEN o_gl_balance > 0 THEN o_gl_balance
                              ELSE 0
                           END) credit_balance,
                          (CASE
                              WHEN o_gl_balance < 0 THEN abs (o_gl_balance)
                              ELSE 0
                           END) debit_balance
                     FROM fn_finance_get_ason_glbal (p_branch_code,
                                                     p_gl_code,
                                                     p_from_date - 1)
                   UNION ALL
                   SELECT   (ROW_NUMBER ()
                             OVER (
                                ORDER BY
                                   transaction_date, batch_number, batch_serial))
                          + 1 serial_number,
                          transaction_date,
                          transaction_narration,
                          (CASE
                              WHEN tran_debit_credit = 'C' THEN tran_amount
                              ELSE 0
                           END) credit_balance,
                          (CASE
                              WHEN tran_debit_credit = 'D' THEN tran_amount
                              ELSE 0
                           END) debit_balance
                     FROM finance_transaction_details
                    WHERE     tran_gl_code = p_gl_code
                          AND transaction_date BETWEEN p_from_date
                                                   AND p_upto_date
                          AND cancel_by IS NULL) a
         ORDER BY serial_number;

      SELECT sum (gl_balance)
        INTO w_gl_balance
        FROM finance_ledger_balance
       WHERE gl_code = p_gl_code;

      UPDATE appauth_query_table
         SET chr_column3 = w_gl_name, dec_column4 = w_gl_balance
       WHERE app_user_id = p_app_user_id;
   ELSIF p_branch_code > 0
   THEN
      INSERT INTO appauth_query_table (chr_column1,
                                       dat_column1,
                                       chr_column2,
                                       dec_column1,
                                       dec_column2,
                                       dec_column3,
                                       app_user_id)
           SELECT serial_number,
                  transaction_date,
                  transaction_narration,
                  credit_balance,
                  debit_balance,
                  SUM (credit_balance - debit_balance)
                     OVER (ORDER BY serial_number) ledger_balance,
                  p_app_user_id
             FROM (SELECT 1  serial_number,
                          p_from_date - 1 transaction_date,
                          'Opening Balance' transaction_narration,
                          (CASE
                              WHEN o_gl_balance > 0 THEN o_gl_balance
                              ELSE 0
                           END) credit_balance,
                          (CASE
                              WHEN o_gl_balance < 0 THEN abs (o_gl_balance)
                              ELSE 0
                           END) debit_balance
                     FROM fn_finance_get_ason_glbal (p_branch_code,
                                                     p_gl_code,
                                                     p_from_date - 1)
                   UNION ALL
                   SELECT   (ROW_NUMBER ()
                             OVER (
                                ORDER BY
                                   transaction_date, batch_number, batch_serial))
                          + 1 serial_number,
                          transaction_date,
                          transaction_narration,
                          (CASE
                              WHEN tran_debit_credit = 'C' THEN tran_amount
                              ELSE 0
                           END) credit_balance,
                          (CASE
                              WHEN tran_debit_credit = 'D' THEN tran_amount
                              ELSE 0
                           END) debit_balance
                     FROM finance_transaction_details
                    WHERE     tran_gl_code = p_gl_code
                          AND acbrn_code = p_branch_code
                          AND cancel_by IS NULL
                          AND transaction_date BETWEEN p_from_date
                                                   AND p_upto_date) a
         ORDER BY serial_number;

      SELECT sum (gl_balance)
        INTO w_gl_balance
        FROM finance_ledger_balance
       WHERE branch_code = p_branch_code AND gl_code = p_gl_code;

      UPDATE appauth_query_table
         SET chr_column3 = w_gl_name, dec_column4 = w_gl_balance
       WHERE app_user_id = p_app_user_id;
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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_run_cash_report
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_run_cash_report (
   IN      p_branch_code   INTEGER,
   IN      p_from_date     DATE,
   IN      p_upto_date     DATE,
   IN      p_app_user_id   CHARACTER,
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
   w_cash_gl_code           VARCHAR;
   w_delar_id               INTEGER;
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
   w_closing_balance        NUMERIC (22, 2);
   w_opening_balance        NUMERIC (22, 2);
BEGIN
   SELECT cash_gl_code
     INTO w_cash_gl_code
     FROM appauth_user_settings
    WHERE app_user_id = p_app_user_id;

   IF p_from_date = p_upto_date
   THEN
      w_opening_date := p_from_date - 1;
      w_ason_date := p_from_date;
   ELSE
      w_from_date := p_from_date;
      w_upto_date := p_upto_date;
      w_opening_date := p_from_date - 1;
   END IF;

   w_sql_stat =
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
                                        app_user_id)
   SELECT ROW_NUMBER () OVER (ORDER BY t.transaction_date, t.contra_gl_code)
             ROW_NUMBER,
       t.transaction_date,
       t.contra_gl_code,
       COALESCE (l.gl_name || '' ['' || l.gl_code || '']'', ''Opening Balance'')
          gl_name,
       t.cash_credit_amount,
       t.cash_debit_amount,
       t.cash_balance,
       t.bank_credit_amount,
       t.bank_debit_amount,
       t.bank_balance,
         '''
      || p_app_user_id
      || '''
  FROM (  SELECT transaction_date,
                 contra_gl_code,
                 sum (cash_credit_amount)
                    cash_credit_amount,
                 sum (cash_debit_amount)
                    cash_debit_amount,
                 sum (sum (cash_credit_amount) - sum (cash_debit_amount))
                    OVER (ORDER BY transaction_date, contra_gl_code)
                    cash_balance,
                 sum (bank_credit_amount)
                    bank_credit_amount,
                 sum (bank_debit_amount)
                    bank_debit_amount,
                 sum (sum (bank_credit_amount) - sum (bank_debit_amount))
                    OVER (ORDER BY transaction_date, contra_gl_code)
                    bank_balance
            FROM (SELECT '''
      || w_opening_date
      || ''' transaction_date,
                         ''00000000'' contra_gl_code,
                         cum_credit_sum cash_credit_amount,
                         cum_debit_sum cash_debit_amount,
                         0.00 bank_credit_amount,
                         0.00 bank_debit_amount
                    FROM (  SELECT b.gl_code,
                                   sum (b.cum_credit_sum) cum_credit_sum,
                                   sum (b.cum_debit_sum) cum_debit_sum
                              FROM finance_ledger_balance_hist b,
                                   (  SELECT branch_code, gl_code,
                                             max (transaction_date) transaction_date
                                        FROM finance_ledger_balance_hist t
                                       WHERE  t.transaction_date <= '''
      || w_opening_date
      || ''' and t.gl_code = '''
      || w_cash_gl_code
      || '''';

   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and branch_code = ' || p_branch_code;
   END IF;

   w_sql_stat :=
         w_sql_stat
      || ' GROUP BY branch_code, gl_code) h,
                                   finance_general_ledger l
                             WHERE     h.gl_code = b.gl_code
                                   AND h.transaction_date = b.transaction_date
                                   and h.branch_code=b.branch_code
                                   AND l.gl_code = b.gl_code
                          GROUP BY b.gl_code) og
                  UNION ALL
                  SELECT transaction_date,
                         contra_gl_code,
                         (CASE
                             WHEN tran_debit_credit = ''C'' THEN tran_amount
                             ELSE 0
                          END) cash_credit_amount,
                         (CASE
                             WHEN tran_debit_credit = ''D'' THEN tran_amount
                             ELSE 0
                          END) cash_debit_amount,
                         0.00 bank_credit_amount,
                         0.00 bank_debit_amount
                    FROM finance_transaction_details t
                   WHERE tran_gl_code = '''
      || w_cash_gl_code
      || ''' AND cancel_by IS NULL ';

   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and t.acbrn_code = ' || p_branch_code;
   END IF;


   IF w_from_date IS NOT NULL AND w_upto_date IS NOT NULL
   THEN
      w_sql_stat :=
            w_sql_stat
         || ' and t.transaction_date between '''
         || w_from_date
         || ''' and '''
         || w_upto_date
         || '''';
   END IF;

   IF w_ason_date IS NOT NULL
   THEN
      w_sql_stat :=
         w_sql_stat || ' and t.transaction_date = ''' || w_ason_date || '''';
   END IF;

   w_sql_stat :=
         w_sql_stat
      || '  UNION ALL
                  SELECT '''
      || w_opening_date
      || ''' transaction_date,
                         ''00000000'' contra_gl_code,
                         0.00 cash_credit_amount,
                         0.00 cash_debit_amount,
                         cum_credit_sum bank_credit_amount,
                         cum_debit_sum bank_debit_amount
                    FROM (  SELECT b.gl_code,
                                   sum (b.cum_credit_sum) cum_credit_sum,
                                   sum (b.cum_debit_sum) cum_debit_sum
                              FROM finance_ledger_balance_hist b,
                                   (  SELECT t.branch_code, gl_code,
                                             max (transaction_date) transaction_date
                                        FROM finance_ledger_balance_hist t,
                                             finance_bank_ledger b
                                       WHERE    t.transaction_date <= '''
      || w_opening_date
      || ''' and t.gl_code = b.ledger_code  AND t.branch_code = b.branch_code ';

   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and t.branch_code = ' || p_branch_code;
   END IF;

   w_sql_stat :=
         w_sql_stat
      || '  GROUP BY t.branch_code, gl_code) h,
                                   finance_general_ledger l
                             WHERE     h.gl_code = b.gl_code
                                   AND h.transaction_date = b.transaction_date
                                   AND l.gl_code = b.gl_code
                                   and h.branch_code=b.branch_code
                          GROUP BY b.gl_code) og
                  UNION ALL
                  SELECT t.transaction_date,
                         t.contra_gl_code,
                         0.00 cash_credit_amount,
                         0.00 cash_debit_amount,
                         (CASE
                             WHEN t.tran_debit_credit = ''C'' THEN t.tran_amount
                             ELSE 0
                          END) bank_credit_amount,
                         (CASE
                             WHEN t.tran_debit_credit = ''D'' THEN t.tran_amount
                             ELSE 0
                          END) bank_debit_amount
                    FROM finance_transaction_details t, finance_bank_ledger b
                   WHERE     t.tran_gl_code = b.ledger_code
                         AND t.acbrn_code = b.branch_code ';

   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and t.acbrn_code = ' || p_branch_code;
   END IF;

   IF w_from_date IS NOT NULL AND w_upto_date IS NOT NULL
   THEN
      w_sql_stat :=
            w_sql_stat
         || ' and t.transaction_date between '''
         || w_from_date
         || ''' and '''
         || w_upto_date
         || '''';
   END IF;

   IF w_ason_date IS NOT NULL
   THEN
      w_sql_stat :=
         w_sql_stat || ' and t.transaction_date = ''' || w_ason_date || '''';
   END IF;

   w_sql_stat := w_sql_stat || '  AND cancel_by IS NULL) d
        GROUP BY transaction_date, contra_gl_code
        ORDER BY transaction_date, contra_gl_code) t
       LEFT OUTER JOIN finance_general_ledger l
          ON (l.gl_code = t.contra_gl_code)';

   --RAISE EXCEPTION USING MESSAGE = w_sql_stat;
   EXECUTE w_sql_stat;

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_finance_telbal_hist
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_finance_telbal_hist (
   IN      p_teller_id     CHARACTER,
   IN      p_branch_code   INTEGER,
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
   rec_teller_list      RECORD;
   rec_date_list        RECORD;
   w_calculate_date     DATE;
   w_teller_banalce     NUMERIC (22, 2) := 0;
   w_cum_credit_sum     NUMERIC (22, 2) := 0;
   w_cum_debit_sum      NUMERIC (22, 2) := 0;
   w_total_debit_sum    NUMERIC (22, 2) := 0;
   w_total_credit_sum   NUMERIC (22, 2) := 0;
   w_status             VARCHAR;
   w_errm               VARCHAR;
   w_tran_gl_code       VARCHAR;
BEGIN
   BEGIN
      SELECT cash_gl_code
        INTO w_tran_gl_code
        FROM finance_application_settings;
   END;

   FOR rec_teller_list
      IN (SELECT branch_code,
                 teller_id,
                 last_transaction_date,
                 last_balance_update
            FROM finance_transaction_telbal
           WHERE     branch_code = p_branch_code
                 AND teller_id = p_teller_id
                 AND NOT is_balance_updated)
   LOOP
      w_calculate_date := rec_teller_list.last_balance_update;

      SELECT COALESCE (teller_balance, 0.00),
             COALESCE (cum_credit_sum, 0.00),
             COALESCE (cum_debit_sum, 0.00)
        INTO w_teller_banalce, w_cum_credit_sum, w_cum_debit_sum
        FROM finance_tran_telbal_hist h
       WHERE     h.teller_id = rec_teller_list.teller_id
             AND branch_code = rec_teller_list.branch_code
             AND h.transaction_date =
                 (SELECT max (transaction_date)
                   FROM finance_tran_telbal_hist
                  WHERE     teller_id = rec_teller_list.teller_id
                        AND transaction_date <= w_calculate_date - 1);

      w_teller_banalce := COALESCE (w_teller_banalce, 0.00);
      w_cum_credit_sum := COALESCE (w_cum_credit_sum, 0.00);
      w_cum_debit_sum := COALESCE (w_cum_debit_sum, 0.00);

      FOR rec_date_list
         IN (  SELECT transaction_date,
                      COALESCE (SUM (debit_amount), 0.00) total_debit_amount,
                      COALESCE (sum (credit_amount), 0.00) total_credit_amount
                 FROM (  SELECT transaction_date,
                                sum (cash_credit_amount) credit_amount,
                                sum (cash_debit_amount) debit_amount
                           FROM (SELECT transaction_date,
                                        (CASE
                                            WHEN tran_debit_credit = 'D'
                                            THEN
                                               tran_amount - cancel_amount
                                            ELSE
                                               0
                                         END) cash_credit_amount,
                                        (CASE
                                            WHEN tran_debit_credit = 'C'
                                            THEN
                                               tran_amount - cancel_amount
                                            ELSE
                                               0
                                         END) cash_debit_amount
                                   FROM finance_transaction_details t
                                  WHERE     tran_gl_code = w_tran_gl_code
                                        AND app_user_id = p_teller_id
                                        AND transaction_date >
                                              rec_teller_list.last_balance_update
                                            - 1
                                        AND cancel_by IS NULL) t
                       GROUP BY transaction_date
                       UNION ALL
                         SELECT transaction_date,
                                sum (cash_credit_amount) cash_payment_amount,
                                sum (cash_debit_amount) cash_receive_amount
                           FROM (SELECT org_teller_id,
                                        transaction_date,
                                        (CASE
                                            WHEN tran_debit_credit = 'D'
                                            THEN
                                               tran_amount - cancel_amount
                                            ELSE
                                               0
                                         END) cash_credit_amount,
                                        (CASE
                                            WHEN tran_debit_credit = 'C'
                                            THEN
                                               tran_amount - cancel_amount
                                            ELSE
                                               0
                                         END) cash_debit_amount
                                   FROM finance_tran_telbal_details t
                                  WHERE     org_teller_id = p_teller_id
                                        AND transaction_date >
                                              rec_teller_list.last_balance_update
                                            - 1
                                        AND auth_by IS NOT NULL) t
                       GROUP BY transaction_date) T
             GROUP BY transaction_date
             ORDER BY transaction_date)
      LOOP
         w_calculate_date := rec_date_list.transaction_date;
         w_total_credit_sum := rec_date_list.total_credit_amount;
         w_total_debit_sum := rec_date_list.total_debit_amount;
         w_cum_credit_sum :=
            w_cum_credit_sum + rec_date_list.total_credit_amount;
         w_cum_debit_sum :=
            w_cum_debit_sum + rec_date_list.total_debit_amount;
         w_teller_banalce :=
            w_teller_banalce + (w_total_credit_sum - w_total_debit_sum);

         DELETE FROM
            finance_tran_telbal_hist
               WHERE     branch_code = rec_teller_list.branch_code
                     AND teller_id = p_teller_id
                     AND transaction_date = w_calculate_date;

         INSERT INTO finance_tran_telbal_hist (branch_code,
                                               transaction_date,
                                               teller_id,
                                               total_debit_sum,
                                               total_credit_sum,
                                               cum_debit_sum,
                                               cum_credit_sum,
                                               teller_balance,
                                               app_user_id,
                                               app_data_time)
              VALUES (rec_teller_list.branch_code,
                      w_calculate_date,
                      p_teller_id,
                      COALESCE (w_total_debit_sum, 0.00),
                      COALESCE (w_total_credit_sum, 0.00),
                      COALESCE (w_cum_credit_sum, 0.00),
                      COALESCE (w_cum_debit_sum, 0.00),
                      COALESCE (w_teller_banalce, 0.00),
                      'SYSTEM',
                      current_timestamp);
      END LOOP;

      UPDATE finance_transaction_telbal
         SET last_balance_update = w_calculate_date,
             is_balance_updated = TRUE
       WHERE     branch_code = rec_teller_list.branch_code
             AND teller_id = p_teller_id;
   END LOOP;

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_final_result_gpa
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_get_final_result_gpa (
   IN      p_academic_year_id    INTEGER,
   IN      p_term_id             INTEGER,
   IN      p_class_id            CHARACTER,
   IN      p_student_roll        CHARACTER,
   IN      p_app_user_id         CHARACTER,
       OUT o_total_mark          NUMERIC,
       OUT o_total_obtain_mark   NUMERIC,
       OUT result_gpa            NUMERIC,
       OUT grade_name            CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
   w_total_mark           NUMERIC := 0.00;

   w_total_grade_point    NUMERIC := 0.00;

   w_total_earned_point   NUMERIC := 0.00;

   w_obtain_mark          NUMERIC := 0.00;

   w_out_of               NUMERIC := 0.00;

   w_credit               NUMERIC := 0.00;

   w_total_subjects       NUMERIC := 0;

   w_final_grade_name     CHARACTER VARYING (200);
   w_subject_cat_name     RECORD;

   w_grade_point_s        NUMERIC := 0;

   w_subjects             RECORD;

   w_subject_mark_info    RECORD;

   w_grades               RECORD;
BEGIN
   --WITH subjects as (SELECT * FROM edu_subject_list sub where class_id=p_class_id)

   SELECT out_of
     INTO w_out_of
     FROM edu_academic_class
    WHERE class_id = p_class_id;

   FOR w_subjects
      IN (SELECT DISTINCT sub.subject_id, sub.out_of, sub.credit
            FROM edu_subject_list sub
                 JOIN edu_exam_single_mark e
                    ON     sub.class_id = p_class_id
                       AND sub.class_id = e.class_id
                       AND sub.subject_id = e.subject_id
                       AND e.term_id = p_term_id
                       AND e.student_roll = p_student_roll)
   LOOP
      SELECT *
        INTO w_subject_mark_info
        FROM fn_get_student_subject_mark (p_academic_year_id,
                                          p_term_id,
                                          p_class_id,
                                          p_student_roll,
                                          w_subjects.subject_id,
                                          w_subjects.out_of,
                                          p_app_user_id);



      IF w_subject_mark_info.o_grade_name = 'F'
      THEN
         WITH
            subject_choice
            AS
               (SELECT *
                 FROM edu_subject_choice
                WHERE     academic_year = p_academic_year_id
                      AND class_id = p_class_id
                      AND subject_id = w_subjects.subject_id
                      AND student_roll = p_student_roll)
         SELECT *
         INTO w_subject_cat_name
         FROM subject_choice sc
              JOIN edu_subject_category subcat
                 ON sc.category_id = subcat.category_id;

         IF w_subject_cat_name.category_name = 'Optional'
         THEN
         ELSE
            w_total_grade_point := 0;
            w_total_earned_point := 0;
            result_gpa := 0.0;
            EXIT;
         END IF;
      END IF;

      IF w_subject_mark_info.o_grade_name IS NOT NULL
      THEN
         w_credit := w_credit + w_subjects.credit;

         w_total_earned_point :=
              w_total_earned_point
            + (w_subjects.credit * w_subject_mark_info.o_grade_point);

         w_total_mark := w_total_mark + w_subject_mark_info.o_total_mark;

         w_total_grade_point :=
            w_total_grade_point + w_subject_mark_info.o_grade_point;

         w_obtain_mark :=
            w_obtain_mark + w_subject_mark_info.o_total_obtain_mark;

         w_total_subjects := w_total_subjects + 1;
      END IF;
   END LOOP;

   IF w_out_of = 5 AND w_total_subjects > 0
   THEN
      result_gpa :=
         CAST ((w_total_grade_point / w_total_subjects) AS decimal (10, 2));
   ELSEIF w_out_of = 4 AND w_credit > 0
   THEN
      result_gpa :=
         CAST ((w_total_earned_point / w_credit) AS decimal (10, 2));
   END IF;

   SELECT g.grade_name
     INTO w_final_grade_name
     FROM fn_get_grade_nameBy_point (result_gpa, w_out_of) g;



   --RAISE 'value of a : %', w_grade_name;

   grade_name := w_final_grade_name;

   o_total_mark := w_total_mark;

   o_total_obtain_mark := w_obtain_mark;
END
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_grade_nameby_point
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_get_grade_nameby_point (
   IN      p_gpa        NUMERIC,
   IN      p_out_of     NUMERIC,
       OUT grade_name   CHARACTER)
   RETURNS CHARACTER
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_grades   RECORD;
BEGIN
   SELECT t.grade_name
    INTO w_grades
    FROM (  SELECT t.grade_name,
                   ROW_NUMBER () OVER (ORDER BY result_gpa DESC) row_number
              FROM (  SELECT result_gpa,
                             CASE
                                WHEN LEAD (result_gpa) OVER (ORDER BY result_gpa)
                                        IS NULL
                                THEN
                                   result_gpa
                                ELSE
                                   LEAD (result_gpa) OVER (ORDER BY result_gpa)
                             END AS next_point,
                             g.grade_name
                        FROM edu_result_grade g
                       WHERE out_of = p_out_of
                    ORDER BY result_gpa) t
             WHERE p_gpa BETWEEN result_gpa AND next_point
          ORDER BY result_gpa DESC) t
   WHERE row_number = 1;

   grade_name := w_grades.grade_name;
END
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_inventory_number
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_get_inventory_number (
   p_inv_code       INTEGER,
   p_branch_code    INTEGER,
   p_inv_prefix     CHARACTER,
   p_inv_naration   CHARACTER,
   p_length         INTEGER DEFAULT 1)
   RETURNS CHARACTER VARYING
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_message              VARCHAR;
   w_last_used_number     INTEGER;
   w_return               VARCHAR;
   w_inv_prefix           VARCHAR;
   w_number_with_prefix   VARCHAR;
   w_inv_length           INTEGER;
BEGIN
   BEGIN
      SELECT last_used_number, inv_prefix, inv_length
        INTO w_last_used_number, w_inv_prefix, w_inv_length
        FROM appauth_inventory_number s
       WHERE     s.inv_code = p_inv_code
             AND s.branch_code = p_branch_code
             AND s.inv_prefix = p_inv_prefix;

      IF NOT FOUND
      THEN
         INSERT INTO appauth_inventory_number (inv_code,
                                               branch_code,
                                               app_user_id,
                                               inv_prefix,
                                               last_used_number,
                                               inv_naration,
                                               inv_length)
              VALUES (p_inv_code,
                      p_branch_code,
                      NULL,
                      P_inv_prefix,
                      1,
                      p_inv_naration,
                      p_length);

         w_last_used_number := 1;
         w_inv_prefix := P_inv_prefix;
         w_inv_length := p_length;
      END IF;
   EXCEPTION
      WHEN NO_DATA_FOUND
      THEN
         INSERT INTO appauth_inventory_number (inv_code,
                                               branch_code,
                                               app_user_id,
                                               inv_prefix,
                                               last_used_number,
                                               inv_naration,
                                               inv_length)
              VALUES (p_inv_code,
                      p_branch_code,
                      NULL,
                      P_inv_prefix,
                      0,
                      p_inv_naration,
                      p_length);

         w_last_used_number := 0;
         w_inv_prefix := p_inv_prefix;
         w_inv_length := p_length;
   END;

   -- limit 100 for update;

   UPDATE appauth_inventory_number s
      SET last_used_number = last_used_number + 1
    WHERE s.inv_code = p_inv_code AND s.branch_code = p_branch_code;

   IF w_inv_length > 1
   THEN
      w_number_with_prefix :=
            w_inv_prefix
         || lpad (cast (w_last_used_number AS VARCHAR), w_inv_length, '0');
      w_return := w_number_with_prefix;
   ELSE
      w_return := w_inv_prefix || w_last_used_number;
   END IF;

   RETURN w_return;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_next_installment_date
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_get_next_installment_date (
   p_inst_freq        CHARACTER,
   p_inst_from_date   DATE,
   p_ason_date        DATE)
   RETURNS DATE
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   W_MESSAGE          CHARACTER (20);
   w_next_inst_date   DATE;
   O_ERRM             CHARACTER (100);
   W_STATUS           CHARACTER (20);
   W_NOI              INTEGER;
   W_NOD              INTEGER;
BEGIN
   IF p_inst_freq = 'W'
   THEN
      W_NOD := FLOOR ((p_ason_date - p_inst_from_date) / 7) * 7 + 7;
      w_next_inst_date := p_inst_from_date + W_NOD;
      W_NOI := W_NOD / 7;
   ELSIF p_inst_freq = 'M'
   THEN
      W_NOI :=
           DATE_PART ('year', AGE (p_ason_date, p_inst_from_date)) * 12
         + DATE_PART ('month', AGE (p_ason_date, p_inst_from_date))
         + 1;
      w_next_inst_date :=
         (p_inst_from_date + (W_NOI || ' months')::INTERVAL)::DATE;
   ELSIF p_inst_freq = 'Q'
   THEN
      W_NOI :=
           DATE_PART ('year', AGE (p_ason_date, p_inst_from_date)) * 4
         + FLOOR (
              DATE_PART ('month', AGE (p_ason_date, p_inst_from_date)) / 3)
         + 1;
      w_next_inst_date :=
         (p_inst_from_date + (3 * W_NOI || ' months')::INTERVAL)::DATE;
   ELSIF p_inst_freq = 'H'
   THEN
      W_NOI :=
           DATE_PART ('year', AGE (p_ason_date, p_inst_from_date)) * 2
         + FLOOR (
              DATE_PART ('month', AGE (p_ason_date, p_inst_from_date)) / 6)
         + 1;
      w_next_inst_date :=
         (p_inst_from_date + (6 * W_NOI || ' months')::INTERVAL)::DATE;
   ELSIF p_inst_freq = 'Y'
   THEN
      W_NOI :=
           DATE_PART ('year', AGE (p_ason_date, p_inst_from_date)) * 1
         + FLOOR (
              DATE_PART ('month', AGE (p_ason_date, p_inst_from_date)) / 12)
         + 1;
      w_next_inst_date :=
         (p_inst_from_date + (12 * W_NOI || ' months')::INTERVAL)::DATE;
   ELSIF p_inst_freq = 'D'
   THEN
      w_next_inst_date := p_ason_date + 1;
      W_NOI := p_inst_from_date - p_ason_date;
   END IF;

   RETURN w_next_inst_date;
EXCEPTION
   WHEN OTHERS
   THEN
      NULL;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_result_gpa
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_get_result_gpa (
   IN      p_obtain_mark   NUMERIC,
   IN      p_total_mark    NUMERIC,
   IN      p_out_of        NUMERIC,
       OUT result_gpa      NUMERIC,
       OUT grade_name      CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   w_obtain_mark_prsent   NUMERIC;
   w_grade_name           CHARACTER VARYING (200);
   w_result_gpa           NUMERIC;
BEGIN
   IF p_obtain_mark <= 0
   THEN
      w_obtain_mark_prsent = 0;
   ELSE
      w_obtain_mark_prsent := round ((p_obtain_mark / p_total_mark) * 100);
   END IF;

   SELECT g.grade_name, g.result_gpa
     INTO w_grade_name, w_result_gpa
     FROM edu_result_grade g
    WHERE     p_out_of = g.out_of
          AND w_obtain_mark_prsent BETWEEN g.lowest_mark AND g.highest_mark;

   grade_name := w_grade_name;
   result_gpa := w_result_gpa;
END
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_student_subject_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_get_student_subject_mark (
   IN      p_academic_year_id    INTEGER,
   IN      p_term_id             INTEGER,
   IN      p_class_id            CHARACTER,
   IN      p_student_roll        CHARACTER,
   IN      p_subject_id          CHARACTER,
   IN      p_out_of              NUMERIC,
   IN      p_app_user_id         CHARACTER,
       OUT o_grade_name          CHARACTER,
       OUT o_grade_point         NUMERIC,
       OUT o_total_mark          NUMERIC,
       OUT o_total_obtain_mark   NUMERIC,
       OUT o_status              CHARACTER,
       OUT o_errm                CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
   w_student_mark   RECORD;
BEGIN
   WITH
      exams
      AS
         (SELECT *
           FROM edu_exam_single_mark
          WHERE     academic_year = p_academic_year_id
                AND term_id = p_term_id
                AND class_id = p_class_id
                AND subject_id = p_subject_id
                AND student_roll = p_student_roll),
      student_marks
      AS
         (  SELECT student_roll,
                   sum (total_exam_marks) AS total_marks,
                   sum (obtain_marks) AS total_obtain_marks
              FROM exams
          GROUP BY student_roll)
   SELECT DISTINCT
          (e.student_roll),
          e.academic_year,
          e.class_id,
          e.subject_id,
          m.total_marks,
          m.total_obtain_marks,
          (SELECT result_gpa
           FROM fn_get_result_gpa (m.total_obtain_marks,
                                   m.total_marks,
                                   p_out_of)) result_gpa,
          (SELECT grade_name
           FROM fn_get_result_gpa (m.total_obtain_marks,
                                   m.total_marks,
                                   p_out_of)) grade_name
     INTO w_student_mark
     FROM student_marks m
          LEFT JOIN exams e ON e.student_roll = m.student_roll;



   o_grade_name := w_student_mark.grade_name;

   o_grade_point := w_student_mark.result_gpa;

   o_total_mark := w_student_mark.total_marks;

   o_total_obtain_mark := w_student_mark.total_obtain_marks;
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;

      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_hostel_fees_generate
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_hostel_fees_generate (
   IN      p_branch_code     INTEGER,
   IN      p_academic_year   INTEGER,
   IN      p_process_date    DATE,
   IN      p_student_roll    CHARACTER,
   IN      p_app_user_id     CHARACTER,
       OUT o_status          CHARACTER,
       OUT o_errm            CHARACTER)
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
   rec_fees_list            RECORD;
   rec_students_list        RECORD;
   w_fine_effective_date    DATE;
   w_effective_date         DATE;
   w_start_date             DATE;
   w_end_date               DATE;
   w_waive_effective_date   DATE;
   w_waive_parsentag        NUMERIC (22, 2) := 0;
   w_waive_amount           NUMERIC (22, 2) := 0;
   w_no_of_month            INTEGER := 1;
   w_fees_sql               VARCHAR;
   w_students_sql           VARCHAR;
   w_waive_sql              VARCHAR;
BEGIN
   w_fees_sql :=
         'SELECT d.effective_date,
		   d.head_code,
		   d.hall_code,
		   d.pay_freq,
		   d.fine_effective_days,
		   d.fee_amount,
		   d.fine_amount
	  FROM hostel_hostel_fees_mapping_hist d,
		   (  SELECT h.head_code,
					 h.hall_code,
					 h.effective_date,
					 max (h.day_serial) day_serial
				FROM hostel_hostel_fees_mapping_hist h,
					 (  SELECT head_code,
							   hall_code,
							   max (effective_date) effective_date
						  FROM hostel_hostel_fees_mapping_hist
						 WHERE effective_date <= '''
      || p_process_date
      || '''  GROUP BY head_code, hall_code) m
			   WHERE     COALESCE (h.hall_code, ''#'') = COALESCE (m.hall_code, ''#'')
					 AND h.effective_date = m.effective_date
					 AND COALESCE (h.head_code, ''#'') = COALESCE (m.head_code, ''#'')
			GROUP BY h.head_code, h.hall_code, h.effective_date) t
	 WHERE     COALESCE (d.hall_code, ''#'') = COALESCE (t.hall_code, ''#'')
		   AND d.effective_date = t.effective_date
		   AND COALESCE (d.head_code, ''#'') = COALESCE (t.head_code, ''#'')
		   AND d.day_serial = t.day_serial';

   FOR rec_fees_list IN EXECUTE w_fees_sql
   LOOP
      w_students_sql :=
         'select h.student_roll, h.branch_code, s.class_id, s.class_group_id,s.section_id
            from hostel_hostel_admit h, edu_students_info s 
          where h.student_roll=s.student_roll ';

      IF p_student_roll IS NOT NULL
      THEN
         w_students_sql :=
               w_students_sql
            || ' and h.student_roll='''
            || p_student_roll
            || '''';
      END IF;

      IF p_branch_code IS NOT NULL
      THEN
         w_students_sql :=
            w_students_sql || ' and h.branch_code= ' || p_branch_code;
      END IF;

      IF rec_fees_list.hall_code IS NOT NULL
      THEN
         w_students_sql :=
               w_students_sql
            || ' and h.hall_code='''
            || rec_fees_list.hall_code
            || '''';
      END IF;

      ---RAISE EXCEPTION USING message = w_students_sql;
      --- do processing
      SELECT CAST (
                FLOOR (
                     DATE_PART ('year', AGE (end_date, start_date)) * 12
                   + DATE_PART ('month', AGE (end_date, start_date))
                   + 1)
                   AS INTEGER) no_of_month,
             start_date,
             end_date
        INTO w_no_of_month, w_start_date, w_end_date
        FROM edu_academic_year
       WHERE academic_year = p_academic_year;

      FOR rec_students_list IN EXECUTE w_students_sql
      LOOP
         IF rec_fees_list.pay_freq = 'M'
         THEN
            w_effective_date := w_start_date;
         ELSE
            w_no_of_month := 1;
            w_effective_date := rec_fees_list.effective_date;
         END IF;

         FOR noi IN 1 .. w_no_of_month
         LOOP
            DELETE FROM
               edu_fees_due_student
                  WHERE     student_roll = rec_students_list.student_roll
                        AND academic_year = p_academic_year
                        AND due_date = w_effective_date
                        AND head_code = rec_fees_list.head_code;

            w_fine_effective_date := NULL;

            w_waive_amount := 0.00;

            INSERT INTO edu_fees_due_student (branch_code,
                                              student_roll,
                                              class_id,
                                              class_group_id,
                                              section_id,
                                              academic_year,
                                              head_code,
                                              due_date,
                                              due_month,
                                              due_year,
                                              process_date,
                                              fine_due_date,
                                              fee_amount,
                                              waive_percentage,
                                              waive_amount,
                                              fine_waive,
                                              fine_amount,
                                              app_user_id,
                                              app_data_time)
                    VALUES (
                              rec_students_list.branch_code,
                              rec_students_list.student_roll,
                              rec_students_list.class_id,
                              rec_students_list.class_group_id,
                              rec_students_list.section_id,
                              p_academic_year,
                              rec_fees_list.head_code,
                              w_effective_date,
                              cast (
                                 to_char (w_effective_date, 'MM') AS INTEGER),
                              cast (
                                 to_char (w_effective_date, 'YYYY')
                                    AS INTEGER),
                              p_process_date,
                              w_fine_effective_date,
                              rec_fees_list.fee_amount,
                              COALESCE (w_waive_parsentag, 0.00),
                              COALESCE (w_waive_amount, 0.00),
                              0.00,
                              rec_fees_list.fine_amount,
                              p_app_user_id,
                              current_timestamp);

            w_effective_date :=
               fn_get_next_installment_date (rec_fees_list.pay_freq,
                                             w_start_date,
                                             w_effective_date);
         END LOOP;
      END LOOP;
   END LOOP;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_onlineexam_live
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_onlineexam_live (
   IN      p_branch_code      INTEGER,
   IN      p_student_roll     CHARACTER,
   IN      p_online_exam_id   CHARACTER,
   IN      p_app_user_id      CHARACTER,
       OUT o_status           CHARACTER,
       OUT o_errm             CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$
DECLARE
   r_online_exam           RECORD;
   w_ans_info_id           CHARACTER VARYING (20);
   w_answer_id             CHARACTER VARYING (20);
   w_online_exam_ques      RECORD;
   w_online_exam_que_dtl   RECORD;
   w_obtain_mark           NUMERIC;
   w_total_mark            NUMERIC;
   w_exam                  RECORD;
BEGIN
   BEGIN
      SELECT *
        INTO w_ans_info_id
        FROM fn_get_inventory_number (20000,
                                      p_branch_code,
                                      'ANS',
                                      'Answer ID Generate',
                                      6);

      SELECT *
        INTO r_online_exam
        FROM edu_online_exam_information i
       WHERE i.online_exam_id = p_online_exam_id;

      INSERT INTO edu_onlineexam_ans_info (ans_info_id,
                                           exam_date,
                                           exam_start_time,
                                           exam_end_time,
                                           publish_status,
                                           total_obtain_marks,
                                           total_marks,
                                           app_user_id,
                                           app_data_time,
                                           online_exam_id,
                                           student_roll)
           VALUES (w_ans_info_id,
                   r_online_exam.exam_date,
                   r_online_exam.exam_start_time,
                   r_online_exam.exam_end_time,
                   'Live',
                   0,
                   r_online_exam.total_marks,
                   p_app_user_id,
                   current_timestamp,
                   r_online_exam.online_exam_id,
                   p_student_roll);

      FOR w_online_exam_ques IN (SELECT *
                                   FROM edu_online_exam_questions q
                                  WHERE q.online_exam_id = p_online_exam_id)
      LOOP
         SELECT *
           INTO w_answer_id
           FROM fn_get_inventory_number (30000,
                                         p_branch_code,
                                         'QS',
                                         'Question Answer ID Generate',
                                         6);

         INSERT INTO edu_onlineexam_question_ans (answer_id,
                                                  ans_info_id,
                                                  student_roll,
                                                  question_id,
                                                  obtain_marks,
                                                  question_marks,
                                                  app_user_id,
                                                  app_data_time)
              VALUES (w_answer_id,
                      w_ans_info_id,
                      p_student_roll,
                      w_online_exam_ques.question_id,
                      0,
                      w_online_exam_ques.question_marks,
                      p_app_user_id,
                      current_timestamp);

         FOR w_online_exam_que_dtl
            IN (SELECT *
                  FROM edu_online_exam_qstn_dtl d
                 WHERE d.question_id = w_online_exam_ques.question_id)
         LOOP
            INSERT INTO edu_onlineexam_qstn_ansdtl (question_details_id,
                                                    answer_id,
                                                    answer_option,
                                                    is_correct_answer,
                                                    app_user_id,
                                                    app_data_time)
                 VALUES (w_online_exam_que_dtl.question_details_id,
                         w_answer_id,
                         w_online_exam_que_dtl.question_option,
                         0,
                         p_app_user_id,
                         current_timestamp);
         END LOOP;
      END LOOP;
   END;
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;
      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_run_edu_fees_report
-- ----------------------------------------------------------------

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_run_finance_all_report
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_run_finance_all_report (
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
   rec_branch_list          RECORD;
   w_teller_id              VARCHAR;
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


   IF p_report_name = 'finance_account_balance_report'
   THEN
      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_account_type
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_account_type'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_zero_balance
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_zero_balance'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_account_number
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_account_number'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_employee_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_employee_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;

      BEGIN
         SELECT *
           INTO w_status, w_errm
           FROM fn_finance_balance_histac (w_branch_code, w_account_number);
      END;


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
                                          app_user_id)
SELECT h.account_number,
       b.branch_code,
       '''' center_code,
       b.client_id,
       b.account_type,
       b.account_title,
       h.cum_debit_sum,
       h.cum_credit_sum,
       h.account_balance,
       ''' || p_app_user_id || ''' 
  FROM finance_accounts_balance_hist h,
       (  SELECT b.account_number,
                 a.branch_code,
                 a.client_id,
                 a.account_type,
                 a.account_title,
                 max (transaction_date) transaction_date
            FROM finance_accounts_balance_hist b, finance_accounts_balance a
           WHERE b.account_number = a.account_number 
           and transaction_date<=''' || w_ason_date || ''' ';

      IF w_account_type IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and a.account_type = '''
            || w_account_type
            || '''';
      END IF;

      IF w_branch_code IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and a.branch_code = ' || w_branch_code || '';
      END IF;

      IF w_account_number IS NOT NULL
      THEN
         w_sql_stat :=
               w_sql_stat
            || ' and a.account_number = '''
            || w_account_number
            || '''';
      END IF;

      w_sql_stat := w_sql_stat || '     
        GROUP BY b.account_number,
                 a.branch_code,
                 a.client_id,
                 a.account_type,
                 a.account_title) b
 WHERE     h.account_number = b.account_number
       AND h.transaction_date = b.transaction_date ';

      IF w_zero_balance = 'N'
      THEN
         w_sql_stat := w_sql_stat || ' and h.account_balance <>0 ';
      END IF;

      w_sql_stat := w_sql_stat || ' order by cast(b.client_id as bigint) ';

      --RAISE EXCEPTION USING MESSAGE = w_sql_stat;
      EXECUTE w_sql_stat;
   ELSIF p_report_name = 'finance_teller_balance_report'
   THEN
      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_teller_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_teller_id'
            AND report_name = p_report_name
            AND app_user_id = p_app_user_id;


      FOR rec_branch_list
         IN (SELECT branch_code, teller_id FROM finance_transaction_telbal)
      LOOP
         SELECT *
         INTO w_status, w_errm
         FROM fn_finance_telbal_hist (rec_branch_list.teller_id,
                                      rec_branch_list.branch_code);
      END LOOP;

      w_sql_stat :=
         'INSERT INTO appauth_report_table_tabular (report_column1,
                                          report_column2,
                                          report_column3,
                                          report_column4,
                                          report_column5,
                                          report_column6,
                                          app_user_id)
   WITH
      opening_balance
      AS
         (SELECT h.teller_id,
                 COALESCE (teller_balance, 0.00) teller_balance,
                 COALESCE (cum_credit_sum, 0.00) cum_credit_sum,
                 COALESCE (cum_debit_sum, 0.00) cum_debit_sum
            FROM finance_tran_telbal_hist h
           WHERE     branch_code = ' || w_branch_code || ' ';

      IF w_teller_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' AND h.teller_id =  ''' || w_teller_id || '''';
      END IF;

      w_sql_stat := w_sql_stat || ' AND h.transaction_date =
                     (SELECT max (transaction_date)
                       FROM finance_tran_telbal_hist
                      WHERE     branch_code = ' || w_branch_code || ' ';

      IF w_teller_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' AND h.teller_id =  ''' || w_teller_id || '''';
      END IF;

      w_sql_stat :=
            w_sql_stat
         || ' AND transaction_date < '''
         || w_from_date
         || ''')),
      periodic_balance
      AS
         (  SELECT b.teller_id,
                   sum (b.total_debit_sum) this_period_debit_sum,
                   sum (b.total_credit_sum) this_period_credit_sum
              FROM finance_tran_telbal_hist b
             WHERE     b.branch_code = '
         || w_branch_code
         || '';

      IF w_teller_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' AND h.teller_id =  ''' || w_teller_id || '''';
      END IF;

      w_sql_stat :=
            w_sql_stat
         || ' 
                   AND b.transaction_date BETWEEN '''
         || w_from_date
         || ''' 
                                              AND '''
         || w_upto_date
         || ''' 
          GROUP BY b.teller_id),
      teller_balance
      AS
         (SELECT COALESCE (o.teller_id, p.teller_id) teller_id,
                 teller_balance opening_balance,
                 COALESCE (this_period_debit_sum, 0.00) this_period_debit_sum,
                 COALESCE (this_period_credit_sum, 0.00) this_period_credit_sum,
                   teller_balance
                 - (COALESCE (this_period_credit_sum, 0.00) - COALESCE (this_period_debit_sum, 0.00)) closing_balance
            FROM opening_balance o
                 FULL OUTER JOIN periodic_balance p
                    ON (o.teller_id = p.teller_id))
   SELECT teller_id,
          employee_name,
          opening_balance,
          this_period_debit_sum,
          this_period_credit_sum,
          closing_balance,
          '''
         || p_app_user_id
         || ''' 
     FROM teller_balance b, appauth_user_settings a
    WHERE b.teller_id = a.app_user_id';

      --RAISE EXCEPTION USING MESSAGE = w_sql_stat;
      EXECUTE w_sql_stat;
   ELSIF p_report_name = 'finance_teller_transaction_report'
   THEN
      SELECT CASE WHEN parameter_values != '' THEN parameter_values END
       INTO w_teller_id
       FROM appauth_report_parameter
      WHERE     parameter_name = 'p_teller_id'
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
                                          app_user_id)
SELECT   ROW_NUMBER ()
             OVER (ORDER BY transaction_date, batch_number, batch_serial)
          serial_number,
       transaction_date,
       transaction_narration,
       (CASE WHEN tran_debit_credit = ''C'' THEN tran_amount ELSE 0 END)
          credit_balance,
       (CASE WHEN tran_debit_credit = ''D'' THEN tran_amount ELSE 0 END)
          debit_balance,
       t.app_user_id,
       t.app_data_time,
          ''' || p_app_user_id || ''' 
  FROM finance_transaction_details t, finance_cash_and_bank_ledger l
 WHERE     tran_gl_code = gl_code
       and t.acbrn_code=l.branch_code
       AND cancel_by IS NULL ';

      IF w_teller_id IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' AND t.app_user_id =  ''' || w_teller_id || '''';
      END IF;

      IF w_branch_code IS NOT NULL
      THEN
         w_sql_stat :=
            w_sql_stat || ' and t.acbrn_code = ' || w_branch_code || '';
      END IF;

      w_sql_stat :=
            w_sql_stat
         || '  AND t.transaction_date BETWEEN '''
         || w_from_date
         || '''  AND '''
         || w_upto_date
         || '''';
      w_sql_stat := w_sql_stat || ' order by t.app_data_time ';

      -- RAISE EXCEPTION USING MESSAGE = w_sql_stat;
      EXECUTE w_sql_stat;
   ELSIF p_report_name IN
            ('finance_cash_transaction_details', 'finance_ledger_statements')
   THEN
      BEGIN
         -- RAISE EXCEPTION USING MESSAGE = p_report_name;

         IF p_report_name = 'finance_cash_transaction_details'
         THEN
            SELECT cash_gl_code
              INTO w_cash_gl_code
              FROM appauth_user_settings
             WHERE app_user_id = p_app_user_id;
         ELSE
            SELECT CASE WHEN parameter_values != '' THEN parameter_values END p_gl_code
              INTO w_cash_gl_code
              FROM appauth_report_parameter
             WHERE     parameter_name = 'p_gl_code'
                   AND report_name = p_report_name
                   AND app_user_id = p_app_user_id;

            SELECT gl_name
              INTO w_gl_name
              FROM finance_general_ledger
             WHERE gl_code = w_cash_gl_code;

            INSERT INTO appauth_report_parameter (parameter_name,
                                                  report_name,
                                                  app_user_id,
                                                  parameter_values)
                 VALUES ('p_gl_name',
                         p_report_name,
                         p_app_user_id,
                         w_gl_name);
         END IF;

         FOR rec_branch_list
            IN (SELECT DISTINCT branch_code
                  FROM finance_ledger_balance
                 WHERE     last_transaction_date <> last_balance_update
                       AND gl_code = w_cash_gl_code
                       AND branch_code = w_branch_code)
         LOOP
            SELECT *
            INTO w_status, w_status
            FROM fn_finance_glbal_hist (w_cash_gl_code,
                                        rec_branch_list.branch_code,
                                        w_ason_date);
         END LOOP;

         BEGIN
            SELECT o_gl_balance
            INTO w_opening_balance
            FROM fn_finance_get_ason_glbal (COALESCE (w_branch_code, 0),
                                            w_cash_gl_code,
                                            w_ason_date - 1);
         END;

         BEGIN
            SELECT o_gl_balance
            INTO w_closing_balance
            FROM fn_finance_get_ason_glbal (COALESCE (w_branch_code, 0),
                                            w_cash_gl_code,
                                            w_ason_date);
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

      SELECT *
        INTO w_status, w_errm
        FROM fn_finance_query_ledger_statement (w_cash_gl_code,
                                                COALESCE (w_branch_code, 0),
                                                w_from_date,
                                                w_upto_date,
                                                p_app_user_id);

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
      IF w_status = 'E'
      THEN
         o_status := w_status;
         o_errm := w_errm;
      ELSE
         o_status := 'E';
         o_errm := SQLERRM;
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_run_finance_cash_report
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_run_finance_cash_report (
   IN      p_branch_code   INTEGER,
   IN      p_from_date     DATE,
   IN      p_upto_date     DATE,
   IN      p_app_user_id   CHARACTER,
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
   w_cash_gl_code           VARCHAR;
   w_delar_id               INTEGER;
   w_status                 VARCHAR;
   w_errm                   VARCHAR;
   w_closing_balance        NUMERIC (22, 2);
   w_opening_balance        NUMERIC (22, 2);
BEGIN
   BEGIN
      SELECT cash_gl_code
        INTO STRICT w_cash_gl_code
        FROM finance_application_settings;
   EXCEPTION
      WHEN NO_DATA_FOUND
      THEN
         RAISE EXCEPTION
         USING MESSAGE =
                  'Cash Ledger Is not Configured In Allication Settings!';
   END;

   IF p_from_date = p_upto_date
   THEN
      w_opening_date := p_from_date - 1;
      w_ason_date := p_from_date;
   ELSE
      w_from_date := p_from_date;
      w_upto_date := p_upto_date;
      w_opening_date := p_from_date - 1;
   END IF;

   DELETE FROM appauth_report_table_tabular
         WHERE app_user_id = p_app_user_id;

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
                                        app_user_id)
   SELECT ROW_NUMBER () OVER (ORDER BY t.transaction_date, t.contra_gl_code)
             ROW_NUMBER,
       t.transaction_date,
       t.contra_gl_code,
       COALESCE (l.gl_name || COALESCE ('' ['' || l.reporting_gl_code || '']'',''''), ''Opening Balance'')
          gl_name,
       t.cash_credit_amount,
       t.cash_debit_amount,
       t.cash_balance,
       t.bank_credit_amount,
       t.bank_debit_amount,
       t.bank_balance,
         '''
      || p_app_user_id
      || '''
  FROM (  SELECT transaction_date,
                 contra_gl_code,
                 sum (cash_credit_amount)
                    cash_credit_amount,
                 sum (cash_debit_amount)
                    cash_debit_amount,
                 sum (sum (cash_debit_amount) - sum (cash_credit_amount) )
                    OVER (ORDER BY transaction_date, contra_gl_code)
                    cash_balance,
                 sum (bank_credit_amount)
                    bank_credit_amount,
                 sum (bank_debit_amount)
                    bank_debit_amount,
                 sum (sum (bank_debit_amount) - sum (bank_credit_amount) )
                    OVER (ORDER BY transaction_date, contra_gl_code)
                    bank_balance
            FROM (SELECT '''
      || w_opening_date
      || ''' transaction_date,
                         ''00000000'' contra_gl_code,
                         cum_credit_sum cash_credit_amount,
                         cum_debit_sum cash_debit_amount,
                         0.00 bank_credit_amount,
                         0.00 bank_debit_amount
                    FROM (  SELECT b.gl_code,
                                   sum (b.cum_credit_sum) cum_credit_sum,
                                   sum (b.cum_debit_sum) cum_debit_sum
                              FROM finance_ledger_balance_hist b,
                                   (  SELECT branch_code, gl_code,
                                             max (transaction_date) transaction_date
                                        FROM finance_ledger_balance_hist t
                                       WHERE  t.transaction_date <= '''
      || w_opening_date
      || ''' and t.gl_code = '''
      || w_cash_gl_code
      || '''';


   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and branch_code = ' || p_branch_code;
   END IF;

   w_sql_stat :=
         w_sql_stat
      || ' GROUP BY branch_code, gl_code) h,
                                   finance_general_ledger l
                             WHERE     h.gl_code = b.gl_code
                                   AND h.transaction_date = b.transaction_date
                                   and h.branch_code=b.branch_code
                                   AND l.gl_code = b.gl_code
                          GROUP BY b.gl_code) og
                  UNION ALL
                  SELECT transaction_date,
                         contra_gl_code,
                         (CASE
                             WHEN tran_debit_credit = ''C'' THEN t.tran_amount-COALESCE(t.cancel_amount,0.00)
                             ELSE 0
                          END) cash_credit_amount,
                         (CASE
                             WHEN tran_debit_credit = ''D'' THEN t.tran_amount-COALESCE(t.cancel_amount,0.00)
                             ELSE 0
                          END) cash_debit_amount,
                         0.00 bank_credit_amount,
                         0.00 bank_debit_amount
                    FROM finance_transaction_details t
                   WHERE tran_gl_code = '''
      || w_cash_gl_code
      || ''' AND cancel_by IS NULL 
      and t.tran_amount-COALESCE(t.cancel_amount,0.00)>0';

   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and t.acbrn_code = ' || p_branch_code;
   END IF;


   IF w_from_date IS NOT NULL AND w_upto_date IS NOT NULL
   THEN
      w_sql_stat :=
            w_sql_stat
         || ' and t.transaction_date between '''
         || w_from_date
         || ''' and '''
         || w_upto_date
         || '''';
   END IF;

   IF w_ason_date IS NOT NULL
   THEN
      w_sql_stat :=
         w_sql_stat || ' and t.transaction_date = ''' || w_ason_date || '''';
   END IF;

   w_sql_stat :=
         w_sql_stat
      || '  UNION ALL
                  SELECT '''
      || w_opening_date
      || ''' transaction_date,
                         ''00000000'' contra_gl_code,
                         0.00 cash_credit_amount,
                         0.00 cash_debit_amount,
                         cum_credit_sum bank_credit_amount,
                         cum_debit_sum bank_debit_amount
                    FROM (  SELECT b.gl_code,
                                   sum (b.cum_credit_sum) cum_credit_sum,
                                   sum (b.cum_debit_sum) cum_debit_sum
                              FROM finance_ledger_balance_hist b,
                                   (  SELECT t.branch_code, t.gl_code,
                                             max (transaction_date) transaction_date
                                        FROM finance_ledger_balance_hist t,
                                             finance_cash_and_bank_ledger b
                                       WHERE  b.gl_code <> '''
      || w_cash_gl_code
      || '''AND  t.transaction_date <= '''
      || w_opening_date
      || ''' and t.gl_code = b.gl_code  AND t.branch_code = b.branch_code ';

   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and t.branch_code = ' || p_branch_code;
   END IF;

   w_sql_stat :=
         w_sql_stat
      || '  GROUP BY t.branch_code, t.gl_code) h,
                                   finance_general_ledger l
                             WHERE     h.gl_code = b.gl_code
                                   AND h.transaction_date = b.transaction_date
                                   AND l.gl_code = b.gl_code
                                   and h.branch_code=b.branch_code
                          GROUP BY b.gl_code) og
                  UNION ALL
                  SELECT t.transaction_date,
                         t.contra_gl_code,
                         0.00 cash_credit_amount,
                         0.00 cash_debit_amount,
                         (CASE
                             WHEN t.tran_debit_credit = ''C'' THEN t.tran_amount-COALESCE(t.cancel_amount,0.00)
                             ELSE 0
                          END) bank_credit_amount,
                         (CASE
                             WHEN t.tran_debit_credit = ''D'' THEN t.tran_amount-COALESCE(t.cancel_amount,0.00)
                             ELSE 0
                          END) bank_debit_amount
                    FROM finance_transaction_details t, finance_cash_and_bank_ledger b
                   WHERE     t.tran_gl_code = b.gl_code
                         AND t.acbrn_code = b.branch_code 
                        and t.tran_amount-COALESCE(t.cancel_amount,0.00)>0
                         and b.gl_code <> '''
      || w_cash_gl_code
      || '''';

   IF p_branch_code <> 0
   THEN
      w_sql_stat := w_sql_stat || ' and t.acbrn_code = ' || p_branch_code;
   END IF;

   IF w_from_date IS NOT NULL AND w_upto_date IS NOT NULL
   THEN
      w_sql_stat :=
            w_sql_stat
         || ' and t.transaction_date between '''
         || w_from_date
         || ''' and '''
         || w_upto_date
         || '''';
   END IF;

   IF w_ason_date IS NOT NULL
   THEN
      w_sql_stat :=
         w_sql_stat || ' and t.transaction_date = ''' || w_ason_date || '''';
   END IF;

   w_sql_stat := w_sql_stat || '  AND cancel_by IS NULL) d
        GROUP BY transaction_date, contra_gl_code
        ORDER BY transaction_date, contra_gl_code) t
       LEFT OUTER JOIN finance_general_ledger l
          ON (l.gl_code = t.contra_gl_code)';

   --RAISE EXCEPTION USING MESSAGE = w_sql_stat;

   EXECUTE w_sql_stat;

   o_status := 'S';
   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_status := 'E';
      o_errm := SQLERRM;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_run_finance_ledger_balance_branch
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_run_finance_ledger_balance_branch (
   IN      p_branch_code   INTEGER,
   IN      p_report_name   CHARACTER,
   IN      p_ason_date     DATE,
   IN      p_from_date     DATE,
   IN      p_upto_date     DATE,
   IN      p_app_user_id   CHARACTER,
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
   w_status                    VARCHAR;
   w_errm                      VARCHAR;
   rec_ledger_balance          RECORD;
   rec_parent_ledger           RECORD;
   rec_parent_ledger_balance   RECORD;
   rec_ledger_list             RECORD;
   rec_cashnbank_list          RECORD;
   w_parent_ledger_balance     NUMERIC (22, 2) := 0;
   w_total_debit_sum           NUMERIC (22, 2) := 0;
   w_total_credit_sum          NUMERIC (22, 2) := 0;
   w_total_income              NUMERIC (22, 2) := 0;
   w_total_expense             NUMERIC (22, 2) := 0;
   w_total_profit_and_loss     NUMERIC (22, 2) := 0;
   w_asonday_opening_bal       NUMERIC (22, 2) := 0;
   w_month_opening_bal         NUMERIC (22, 2) := 0;
   w_quarter_opening_bal       NUMERIC (22, 2) := 0;
   w_halfyear_opening_bal      NUMERIC (22, 2) := 0;
   w_year_opening_bal          NUMERIC (22, 2) := 0;
   w_asonday_closing_bal       NUMERIC (22, 2) := 0;
   w_month_closing_bal         NUMERIC (22, 2) := 0;
   w_quarter_closing_bal       NUMERIC (22, 2) := 0;
   w_halfyear_closing_bal      NUMERIC (22, 2) := 0;
   w_year_closing_bal          NUMERIC (22, 2) := 0;
   w_ason_date                 DATE;
   w_month_start_date          DATE;
   w_month_end_date            DATE;
   w_year_start                DATE;
   w_year_end                  DATE;
   rec_branch_list             RECORD;
   w_this_year_month           INTEGER;
   w_past_year_month           INTEGER;
   w_current_month             INTEGER;
   w_past_month                INTEGER;
   w_current_year              INTEGER;
   w_past_year                 INTEGER;
   w_branch_name               VARCHAR;
   w_branch_address            VARCHAR;
   w_asset_main_gl             VARCHAR;
   w_liabilities_main_gl       VARCHAR;
   w_income_main_gl            VARCHAR;
   w_expenses_main_gl          VARCHAR;
   w_profit_and_loss_ledger    VARCHAR;
BEGIN
   w_ason_date := p_ason_date;

   IF p_ason_date IS NULL
   THEN
      w_ason_date := p_upto_date;
   END IF;

   SELECT asset_main_gl,
          liabilities_main_gl,
          income_main_gl,
          expenses_main_gl,
          profit_and_loss_ledger
     INTO w_asset_main_gl,
          w_liabilities_main_gl,
          w_income_main_gl,
          w_expenses_main_gl,
          w_profit_and_loss_ledger
     FROM finance_application_settings;

   w_month_start_date := CAST (date_trunc ('month', w_ason_date) AS DATE);
   w_month_end_date :=
      CAST (
           date_trunc ('month', w_ason_date)
         + INTERVAL '1 months'
         - INTERVAL '1 day'
            AS DATE);

   w_year_end :=
      CAST (
           date_trunc ('year', w_ason_date)
         + INTERVAL '12 months'
         - INTERVAL '1 day'
            AS DATE);

   w_year_start := CAST (date_trunc ('year', w_ason_date) AS DATE);

   IF w_year_end > w_ason_date
   THEN
      w_year_end := w_ason_date;
   END IF;

   IF w_month_end_date > w_ason_date
   THEN
      w_month_end_date := w_ason_date;
   END IF;

   IF p_report_name = 'finance_receipt_payment2'
   THEN
      w_month_end_date := p_upto_date;
      w_month_start_date := p_from_date;
      w_ason_date := p_from_date;
   END IF;

   --RAISE EXCEPTION USING message = w_month_start_date;

   w_past_year_month :=
      CAST (
            TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE) - 1,
                     'YYYY')
         || TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE) - 1,
                     'MM')
            AS INTEGER);
   w_this_year_month :=
      CAST (
            TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE),
                     'YYYY')
         || TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE), 'MM')
            AS INTEGER);

   DELETE FROM finance_ledger_report_param
         WHERE app_user_id = p_app_user_id;

   DELETE FROM finance_ledger_report_balance
         WHERE app_user_id = p_app_user_id;

   FOR rec_branch_list IN (SELECT *
                             FROM appauth_branch
                            WHERE branch_code = p_branch_code)
   LOOP
      SELECT w_status, w_errm
        INTO w_status, w_errm
        FROM fn_finance_balance_history (rec_branch_list.branch_code);

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING MESSAGE = w_errm;
      END IF;
   END LOOP;


   INSERT INTO finance_ledger_report_param (branch_code,
                                            gl_code,
                                            gl_level,
                                            gl_name,
                                            reporting_gl_code,
                                            reporting_gl_serial,
                                            parent_code,
                                            gl_level_class,
                                            income_gl,
                                            expense_gl,
                                            assets_gl,
                                            liabilities_gl,
                                            is_leaf_node,
                                            maintain_by_system,
                                            sundry_flag,
                                            app_user_id)
      WITH
         RECURSIVE root_data
         AS
            (SELECT gl_code,
                    gl_name,
                    reporting_gl_code,
                    reporting_gl_serial,
                    parent_code,
                    is_leaf_node,
                    income_gl,
                    expense_gl,
                    assets_gl,
                    liabilities_gl,
                    sundry_flag,
                    maintain_by_system,
                    1  AS level
               FROM finance_general_ledger
              WHERE parent_code IS NULL
             UNION ALL
             SELECT e.gl_code,
                    e.gl_name,
                    e.reporting_gl_code,
                    e.reporting_gl_serial,
                    e.parent_code,
                    e.is_leaf_node,
                    e.income_gl,
                    e.expense_gl,
                    e.assets_gl,
                    e.liabilities_gl,
                    e.sundry_flag,
                    e.maintain_by_system,
                    c.level + 1
               FROM root_data c
                    JOIN finance_general_ledger e
                       ON e.parent_code = c.gl_code)
        SELECT p_branch_code branch_code,
               gl_code,
               level gl_level,
               gl_name || COALESCE (' [' || reporting_gl_code || ']', ''),
               reporting_gl_code,
               reporting_gl_serial,
               parent_code,
                  'padding-left: '
               || 10 * level
               || 'px; '
               || (CASE
                      WHEN is_leaf_node THEN 'font-weight: normal'
                      ELSE 'font-weight: bold;'
                   END)
               || '; ' gl_level_class,
               income_gl,
               expense_gl,
               assets_gl,
               liabilities_gl,
               is_leaf_node,
               maintain_by_system,
               sundry_flag,
               p_app_user_id app_user_id
          FROM root_data
      ORDER BY reporting_gl_serial, reporting_gl_code, parent_code;

   IF p_report_name = 'finance_trial_balance'
   THEN
      INSERT INTO finance_ledger_report_balance (branch_code,
                                                 gl_code,
                                                 ason_credit_sum,
                                                 ason_debit_sum,
                                                 this_period_credit_sum,
                                                 this_period_debit_sum,
                                                 asof_credit_sum,
                                                 asof_debit_sum,
                                                 app_user_id)
         WITH
            opening_balance
            AS
               (  SELECT b.gl_code,
                         sum (b.cum_debit_sum) opening_debit_sum,
                         sum (b.cum_credit_sum) opening_credit_sum,
                         SUM (b.cum_credit_sum - b.cum_debit_sum) asof_gl_balance
                    FROM finance_ledger_balance_hist b,
                         (  SELECT branch_code,
                                   gl_code,
                                   max (transaction_date) transaction_date
                              FROM finance_ledger_balance_hist
                             WHERE     transaction_date < p_from_date
                                   AND branch_code = p_branch_code
                          GROUP BY gl_code, branch_code) h
                   WHERE     h.gl_code = b.gl_code
                         AND h.branch_code = b.branch_code
                         AND b.branch_code = p_branch_code
                         AND h.transaction_date = b.transaction_date
                GROUP BY b.gl_code),
            periodic_balance
            AS
               (  SELECT b.gl_code,
                         sum (b.total_debit_sum) this_period_debit_sum,
                         sum (b.total_credit_sum) this_period_credit_sum
                    FROM finance_ledger_balance_hist b
                   WHERE     b.branch_code = p_branch_code
                         AND b.transaction_date BETWEEN p_from_date
                                                    AND p_upto_date
                GROUP BY b.gl_code),
            gl_balance
            AS
               (SELECT COALESCE (b.gl_code, m.gl_code)
                          gl_code,
                       COALESCE (b.opening_debit_sum, 0)
                          opening_debit_sum,
                       COALESCE (b.opening_credit_sum, 0)
                          opening_credit_sum,
                       COALESCE (m.this_period_debit_sum, 0)
                          this_period_debit_sum,
                       COALESCE (m.this_period_credit_sum, 0)
                          this_period_credit_sum
                  FROM opening_balance b
                       FULL OUTER JOIN periodic_balance m
                          ON (b.gl_code = m.gl_code))
         SELECT p_branch_code
                   branch_code,
                COALESCE (p.gl_code, b.gl_code)
                   gl_code,
                COALESCE (opening_credit_sum, 0.00)
                   opening_credit_sum,
                COALESCE (opening_debit_sum, 0.00)
                   opening_debit_sum,
                COALESCE (this_period_credit_sum, 0.00)
                   this_period_credit_sum,
                COALESCE (this_period_debit_sum, 0.00)
                   this_period_debit_sum,
                  COALESCE (opening_credit_sum, 0.00)
                + COALESCE (this_period_credit_sum, 0.00)
                   closing_credit_sum,
                  COALESCE (opening_debit_sum, 0.00)
                + COALESCE (this_period_debit_sum, 0.00)
                   closing_debit_sum,
                p_app_user_id
                   app_user_id
           FROM gl_balance b
                FULL OUTER JOIN (SELECT *
                                   FROM finance_ledger_report_param
                                  WHERE app_user_id = p_app_user_id) p
                   ON (b.gl_code = p.gl_code);
   END IF;

   IF p_report_name IN
         ('finance_receipt_payment', 'finance_receipt_payment2')
   THEN
      DELETE FROM finance_ledger_report_param
            WHERE sundry_flag AND app_user_id = p_app_user_id;

      BEGIN
         INSERT INTO finance_ledger_report_balance (branch_code,
                                                    gl_code,
                                                    ason_credit_sum,
                                                    ason_debit_sum,
                                                    ason_gl_balance,
                                                    asof_credit_sum,
                                                    asof_debit_sum,
                                                    asof_gl_balance,
                                                    this_month_credit_sum,
                                                    this_month_debit_sum,
                                                    this_month_gl_balance,
                                                    past_month_credit_sum,
                                                    past_month_debit_sum,
                                                    past_month_gl_balance,
                                                    this_quarter_credit_sum,
                                                    this_quarter_debit_sum,
                                                    this_quarter_gl_balance,
                                                    past_quarter_credit_sum,
                                                    past_quarter_debit_sum,
                                                    past_quarter_gl_balance,
                                                    this_halfyear_credit_sum,
                                                    this_halfyear_debit_sum,
                                                    this_halfyear_gl_balance,
                                                    past_halfyear_credit_sum,
                                                    past_halfyear_debit_sum,
                                                    past_halfyear_gl_balance,
                                                    this_year_credit_sum,
                                                    this_year_debit_sum,
                                                    this_year_gl_balance,
                                                    past_year_credit_sum,
                                                    past_year_debit_sum,
                                                    past_year_gl_balance,
                                                    this_period_credit_sum,
                                                    this_period_debit_sum,
                                                    this_period_gl_balance,
                                                    app_user_id)
            WITH
               ason_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.gl_balance) ason_gl_balance,
                            sum (b.total_debit_sum) ason_debit_sum,
                            sum (b.total_credit_sum) ason_credit_sum
                       FROM finance_led_rec_pay_bal_hist b
                      WHERE     b.branch_code = p_branch_code
                            AND b.transaction_date = w_ason_date
                   GROUP BY b.gl_code),
               asof_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.cum_debit_sum) asof_debit_sum,
                            sum (b.cum_credit_sum) asof_credit_sum,
                            SUM (b.cum_credit_sum - b.cum_debit_sum) asof_gl_balance
                       FROM finance_led_rec_pay_bal_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_led_rec_pay_bal_hist
                                WHERE     branch_code = p_branch_code
                                      AND transaction_date <= w_ason_date
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               this_month_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) this_month_debit_sum,
                            sum (b.total_credit_sum) this_month_credit_sum,
                            SUM (b.gl_balance) this_month_gl_balance
                       FROM finance_led_rec_pay_bal_hist b
                      WHERE     branch_code = p_branch_code
                            AND transaction_date BETWEEN w_month_start_date
                                                     AND w_month_end_date
                   GROUP BY b.gl_code),
               this_year_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) this_year_debit_sum,
                            sum (b.total_credit_sum) this_year_credit_sum,
                            SUM (b.gl_balance) this_month_gl_balance
                       FROM finance_led_rec_pay_bal_hist b
                      WHERE     branch_code = p_branch_code
                            AND transaction_date BETWEEN w_year_start
                                                     AND w_year_end
                   GROUP BY b.gl_code)
            SELECT p_branch_code,
                   COALESCE (p.gl_code,
                             b.gl_code,
                             m.gl_code,
                             y.gl_code)
                      gl_code,
                   COALESCE (ason_credit_sum, 0.00)
                      ason_credit_sum,
                   COALESCE (ason_debit_sum, 0.00)
                      ason_debit_sum,
                   0.00
                      ason_gl_balance,
                   COALESCE (asof_credit_sum, 0.00)
                      asof_credit_sum,
                   COALESCE (asof_debit_sum, 0.00)
                      asof_debit_sum,
                   COALESCE (asof_gl_balance, 0.00)
                      asof_gl_balance,
                   COALESCE (this_month_credit_sum, 0.00)
                      this_month_credit_sum,
                   COALESCE (this_month_debit_sum, 0.00)
                      this_month_debit_sum,
                   0.00
                      this_month_gl_balance,
                   0.00
                      past_month_credit_sum,
                   0.00
                      past_month_debit_sum,
                   0.00
                      past_month_gl_balance,
                   0.00
                      this_quarter_credit_sum,
                   0.00
                      this_quarter_debit_sum,
                   0.00
                      this_quarter_gl_balance,
                   0.00
                      past_quarter_credit_sum,
                   0.00
                      past_quarter_debit_sum,
                   0.00
                      past_quarter_gl_balance,
                   0.00
                      this_halfyear_credit_sum,
                   0.00
                      this_halfyear_debit_sum,
                   0.00
                      this_halfyear_gl_balance,
                   0.00
                      past_halfyear_credit_sum,
                   0.00
                      past_halfyear_debit_sum,
                   0.00
                      past_halfyear_gl_balance,
                   COALESCE (this_year_credit_sum, 0.00)
                      this_year_credit_sum,
                   COALESCE (this_year_debit_sum, 0.00)
                      this_year_debit_sum,
                   0.00
                      this_year_gl_balance,
                   0.00
                      past_year_credit_sum,
                   0.00
                      past_year_debit_sum,
                   0.00
                      past_year_gl_balance,
                   0.00
                      this_period_credit_sum,
                   0.00
                      this_period_debit_sum,
                   0.00
                      this_period_gl_balance,
                   p_app_user_id
                      app_user_id
              FROM (SELECT *
                      FROM finance_ledger_report_param
                     WHERE app_user_id = p_app_user_id) p
                   FULL OUTER JOIN asof_day_bal o ON (p.gl_code = o.gl_code)
                   FULL OUTER JOIN this_month_bal m
                      ON (p.gl_code = m.gl_code)
                   FULL OUTER JOIN this_year_bal y ON (p.gl_code = y.gl_code)
                   FULL OUTER JOIN ason_day_bal b ON (p.gl_code = b.gl_code);
      ----RAISE EXCEPTION USING message = w_month_start_date;
      END;
   END IF;

   IF p_report_name IN
         ('finance_asset_liabilities', 'finance_income_expenses')
   THEN
      DELETE FROM finance_ledger_report_param
            WHERE sundry_flag AND app_user_id = p_app_user_id;

      BEGIN
         INSERT INTO finance_ledger_report_balance (branch_code,
                                                    gl_code,
                                                    ason_credit_sum,
                                                    ason_debit_sum,
                                                    ason_gl_balance,
                                                    asof_credit_sum,
                                                    asof_debit_sum,
                                                    asof_gl_balance,
                                                    this_month_credit_sum,
                                                    this_month_debit_sum,
                                                    this_month_gl_balance,
                                                    past_month_credit_sum,
                                                    past_month_debit_sum,
                                                    past_month_gl_balance,
                                                    this_quarter_credit_sum,
                                                    this_quarter_debit_sum,
                                                    this_quarter_gl_balance,
                                                    past_quarter_credit_sum,
                                                    past_quarter_debit_sum,
                                                    past_quarter_gl_balance,
                                                    this_halfyear_credit_sum,
                                                    this_halfyear_debit_sum,
                                                    this_halfyear_gl_balance,
                                                    past_halfyear_credit_sum,
                                                    past_halfyear_debit_sum,
                                                    past_halfyear_gl_balance,
                                                    this_year_credit_sum,
                                                    this_year_debit_sum,
                                                    this_year_gl_balance,
                                                    past_year_credit_sum,
                                                    past_year_debit_sum,
                                                    past_year_gl_balance,
                                                    this_period_credit_sum,
                                                    this_period_debit_sum,
                                                    this_period_gl_balance,
                                                    app_user_id)
            WITH
               ason_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.gl_balance) ason_gl_balance,
                            sum (b.total_debit_sum) ason_debit_sum,
                            sum (b.total_credit_sum) ason_credit_sum
                       FROM finance_ledger_balance_hist b
                      WHERE     b.transaction_date = w_ason_date
                            AND branch_code = p_branch_code
                   GROUP BY b.gl_code),
               asof_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.cum_debit_sum) asof_debit_sum,
                            sum (b.cum_credit_sum) asof_credit_sum,
                            SUM (b.cum_credit_sum - b.cum_debit_sum) asof_gl_balance
                       FROM finance_ledger_balance_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balance_hist
                                WHERE     transaction_date <= w_ason_date
                                      AND branch_code = p_branch_code
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               past_month_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) past_month_debit_sum,
                            sum (b.total_credit_sum) past_month_credit_sum,
                            SUM (b.gl_balance) past_month_gl_balance
                       FROM finance_ledger_balmon_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balmon_hist
                                WHERE     transaction_date <=
                                          w_month_start_date - 1
                                      AND branch_code = p_branch_code
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               this_month_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) this_month_debit_sum,
                            sum (b.total_credit_sum) this_month_credit_sum,
                            SUM (b.gl_balance) this_month_gl_balance
                       FROM finance_ledger_balance_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balance_hist
                                WHERE     transaction_date <= w_month_end_date
                                      AND branch_code = p_branch_code
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               past_year_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) past_year_debit_sum,
                            sum (b.total_credit_sum) past_year_credit_sum,
                            SUM (b.gl_balance) past_year_gl_balance
                       FROM finance_ledger_balmon_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balmon_hist
                                WHERE     transaction_date <= w_year_start - 1
                                      AND branch_code = p_branch_code
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code)
            SELECT p_branch_code,
                   COALESCE (p.gl_code,
                             b.gl_code,
                             m.gl_code,
                             y.gl_code)
                      gl_code,
                   COALESCE (ason_credit_sum, 0.00)
                      ason_credit_sum,
                   COALESCE (ason_debit_sum, 0.00)
                      ason_debit_sum,
                   COALESCE (ason_gl_balance, 0.00)
                      ason_gl_balance,
                   COALESCE (asof_credit_sum, 0.00)
                      asof_credit_sum,
                   COALESCE (asof_debit_sum, 0.00)
                      asof_debit_sum,
                   COALESCE (asof_gl_balance, 0.00)
                      asof_gl_balance,
                   COALESCE (this_month_credit_sum, 0.00)
                      this_month_credit_sum,
                   COALESCE (this_month_debit_sum, 0.00)
                      this_month_debit_sum,
                   COALESCE (this_month_gl_balance, 0.00)
                      this_month_gl_balance,
                   COALESCE (past_month_credit_sum, 0.00)
                      past_month_credit_sum,
                   COALESCE (past_month_debit_sum, 0.00)
                      past_month_debit_sum,
                   COALESCE (past_month_gl_balance, 0.00)
                      past_month_gl_balance,
                   0.00
                      this_quarter_credit_sum,
                   0.00
                      this_quarter_debit_sum,
                   0.00
                      this_quarter_gl_balance,
                   0.00
                      past_quarter_credit_sum,
                   0.00
                      past_quarter_debit_sum,
                   0.00
                      past_quarter_gl_balance,
                   0.00
                      this_halfyear_credit_sum,
                   0.00
                      this_halfyear_debit_sum,
                   0.00
                      this_halfyear_gl_balance,
                   0.00
                      past_halfyear_credit_sum,
                   0.00
                      past_halfyear_debit_sum,
                   0.00
                      past_halfyear_gl_balance,
                   0.00
                      this_year_credit_sum,
                   0.00
                      this_year_debit_sum,
                   0.00
                      this_year_gl_balance,
                   COALESCE (past_year_credit_sum, 0.00)
                      past_year_credit_sum,
                   COALESCE (past_year_debit_sum, 0.00)
                      past_year_debit_sum,
                   COALESCE (past_year_gl_balance, 0.00)
                      past_year_gl_balance,
                   0.00
                      this_period_credit_sum,
                   0.00
                      this_period_debit_sum,
                   0.00
                      this_period_gl_balance,
                   p_app_user_id
                      app_user_id
              FROM (SELECT *
                      FROM finance_ledger_report_param
                     WHERE app_user_id = p_app_user_id) p
                   FULL OUTER JOIN asof_day_bal o ON (p.gl_code = o.gl_code)
                   FULL OUTER JOIN past_month_bal m
                      ON (p.gl_code = m.gl_code)
                   FULL OUTER JOIN past_year_bal y ON (p.gl_code = y.gl_code)
                   FULL OUTER JOIN this_month_bal t
                      ON (p.gl_code = t.gl_code)
                   FULL OUTER JOIN ason_day_bal b ON (p.gl_code = b.gl_code);
      END;
   END IF;

   --- Updating Parent Ledger Balance

   BEGIN
      FOR rec_parent_ledger IN (  SELECT DISTINCT gl_level, parent_code
                                    FROM finance_ledger_report_param
                                   WHERE app_user_id = p_app_user_id
                                ORDER BY gl_level DESC)
      LOOP
         FOR rec_parent_ledger_balance
            IN (SELECT sum (ason_credit_sum)
                          ason_credit_sum,
                       sum (ason_debit_sum)
                          ason_debit_sum,
                       sum (ason_gl_balance)
                          ason_gl_balance,
                       sum (asof_credit_sum)
                          asof_credit_sum,
                       sum (asof_debit_sum)
                          asof_debit_sum,
                       sum (asof_gl_balance)
                          asof_gl_balance,
                       sum (this_month_credit_sum)
                          this_month_credit_sum,
                       sum (this_month_debit_sum)
                          this_month_debit_sum,
                       sum (this_month_gl_balance)
                          this_month_gl_balance,
                       sum (past_month_credit_sum)
                          past_month_credit_sum,
                       sum (past_month_debit_sum)
                          past_month_debit_sum,
                       sum (past_month_gl_balance)
                          past_month_gl_balance,
                       sum (this_quarter_credit_sum)
                          this_quarter_credit_sum,
                       sum (this_quarter_debit_sum)
                          this_quarter_debit_sum,
                       sum (this_quarter_gl_balance)
                          this_quarter_gl_balance,
                       sum (past_quarter_credit_sum)
                          past_quarter_credit_sum,
                       sum (past_quarter_debit_sum)
                          past_quarter_debit_sum,
                       sum (past_quarter_gl_balance)
                          past_quarter_gl_balance,
                       sum (this_halfyear_credit_sum)
                          this_halfyear_credit_sum,
                       sum (this_halfyear_debit_sum)
                          this_halfyear_debit_sum,
                       sum (this_halfyear_gl_balance)
                          this_halfyear_gl_balance,
                       sum (past_halfyear_credit_sum)
                          past_halfyear_credit_sum,
                       sum (past_halfyear_debit_sum)
                          past_halfyear_debit_sum,
                       sum (past_halfyear_gl_balance)
                          past_halfyear_gl_balance,
                       sum (this_year_credit_sum)
                          this_year_credit_sum,
                       sum (this_year_debit_sum)
                          this_year_debit_sum,
                       sum (this_year_gl_balance)
                          this_year_gl_balance,
                       sum (past_year_credit_sum)
                          past_year_credit_sum,
                       sum (past_year_debit_sum)
                          past_year_debit_sum,
                       sum (past_year_gl_balance)
                          past_year_gl_balance,
                       sum (this_period_credit_sum)
                          this_period_credit_sum,
                       sum (this_period_debit_sum)
                          this_period_debit_sum,
                       sum (this_period_gl_balance)
                          this_period_gl_balance
                  FROM finance_ledger_report_balance b,
                       (SELECT *
                          FROM finance_ledger_report_param
                         WHERE app_user_id = p_app_user_id) p
                 WHERE     b.gl_code = p.gl_code
                       AND p.parent_code = rec_parent_ledger.parent_code
                       AND p.app_user_id = b.app_user_id
                       AND p.app_user_id = p_app_user_id)
         LOOP
            UPDATE finance_ledger_report_balance
               SET ason_gl_balance =
                      rec_parent_ledger_balance.ason_gl_balance,
                   ason_debit_sum = rec_parent_ledger_balance.ason_debit_sum,
                   ason_credit_sum =
                      rec_parent_ledger_balance.ason_credit_sum,
                   asof_debit_sum = rec_parent_ledger_balance.asof_debit_sum,
                   asof_credit_sum =
                      rec_parent_ledger_balance.asof_credit_sum,
                   asof_gl_balance =
                      rec_parent_ledger_balance.asof_gl_balance,
                   this_month_debit_sum =
                      rec_parent_ledger_balance.this_month_debit_sum,
                   this_month_credit_sum =
                      rec_parent_ledger_balance.this_month_credit_sum,
                   this_month_gl_balance =
                      rec_parent_ledger_balance.this_month_gl_balance,
                   past_month_debit_sum =
                      rec_parent_ledger_balance.past_month_debit_sum,
                   past_month_credit_sum =
                      rec_parent_ledger_balance.past_month_credit_sum,
                   past_month_gl_balance =
                      rec_parent_ledger_balance.past_month_gl_balance,
                   this_quarter_credit_sum =
                      rec_parent_ledger_balance.this_quarter_credit_sum,
                   this_quarter_debit_sum =
                      rec_parent_ledger_balance.this_quarter_debit_sum,
                   this_quarter_gl_balance =
                      rec_parent_ledger_balance.this_quarter_gl_balance,
                   past_quarter_credit_sum =
                      rec_parent_ledger_balance.past_quarter_credit_sum,
                   past_quarter_debit_sum =
                      rec_parent_ledger_balance.past_quarter_debit_sum,
                   past_quarter_gl_balance =
                      rec_parent_ledger_balance.past_quarter_gl_balance,
                   this_halfyear_credit_sum =
                      rec_parent_ledger_balance.this_halfyear_credit_sum,
                   this_halfyear_debit_sum =
                      rec_parent_ledger_balance.this_halfyear_debit_sum,
                   this_halfyear_gl_balance =
                      rec_parent_ledger_balance.this_halfyear_gl_balance,
                   past_halfyear_credit_sum =
                      rec_parent_ledger_balance.past_halfyear_credit_sum,
                   past_halfyear_debit_sum =
                      rec_parent_ledger_balance.past_halfyear_debit_sum,
                   past_halfyear_gl_balance =
                      rec_parent_ledger_balance.past_halfyear_gl_balance,
                   this_year_credit_sum =
                      rec_parent_ledger_balance.this_year_credit_sum,
                   this_year_debit_sum =
                      rec_parent_ledger_balance.this_year_debit_sum,
                   this_year_gl_balance =
                      rec_parent_ledger_balance.this_year_gl_balance,
                   past_year_credit_sum =
                      rec_parent_ledger_balance.past_year_credit_sum,
                   past_year_debit_sum =
                      rec_parent_ledger_balance.past_year_debit_sum,
                   past_year_gl_balance =
                      rec_parent_ledger_balance.past_year_gl_balance,
                   this_period_credit_sum =
                      rec_parent_ledger_balance.this_period_credit_sum,
                   this_period_debit_sum =
                      rec_parent_ledger_balance.this_period_debit_sum,
                   this_period_gl_balance =
                      rec_parent_ledger_balance.this_period_gl_balance
             WHERE     gl_code = rec_parent_ledger.parent_code
                   AND app_user_id = p_app_user_id;
         END LOOP;
      END LOOP;

      -- RAISE EXCEPTION USING MESSAGE = w_income_main_gl||w_expenses_main_gl;
      IF p_report_name = 'finance_asset_liabilities'
      THEN
         BEGIN
            FOR rec_parent_ledger_balance
               IN (WITH
                      income_balance
                      AS
                         (SELECT *
                           FROM finance_ledger_report_balance
                          WHERE     app_user_id = p_app_user_id
                                AND gl_code = w_income_main_gl),
                      expences_balance
                      AS
                         (SELECT *
                           FROM finance_ledger_report_balance
                          WHERE     app_user_id = p_app_user_id
                                AND gl_code = w_expenses_main_gl)
                   SELECT (i.ason_credit_sum + e.ason_credit_sum)
                             ason_credit_sum,
                          (i.ason_debit_sum + e.ason_debit_sum)
                             ason_debit_sum,
                          (i.ason_gl_balance + e.ason_gl_balance)
                             ason_gl_balance,
                          (i.asof_credit_sum + e.asof_credit_sum)
                             asof_credit_sum,
                          (i.asof_debit_sum + e.asof_debit_sum)
                             asof_debit_sum,
                          (i.asof_gl_balance + e.asof_gl_balance)
                             asof_gl_balance,
                          (i.this_month_credit_sum + e.this_month_credit_sum)
                             this_month_credit_sum,
                          (i.this_month_debit_sum + e.this_month_debit_sum)
                             this_month_debit_sum,
                          (i.this_month_gl_balance + e.this_month_gl_balance)
                             this_month_gl_balance,
                          (i.past_month_credit_sum + e.past_month_credit_sum)
                             past_month_credit_sum,
                          (i.past_month_debit_sum + e.past_month_debit_sum)
                             past_month_debit_sum,
                          (i.past_month_gl_balance + e.past_month_gl_balance)
                             past_month_gl_balance,
                          (  i.this_quarter_credit_sum
                           + e.this_quarter_credit_sum)
                             this_quarter_credit_sum,
                          (  i.this_quarter_debit_sum
                           + e.this_quarter_debit_sum)
                             this_quarter_debit_sum,
                          (  i.this_quarter_gl_balance
                           + e.this_quarter_gl_balance)
                             this_quarter_gl_balance,
                          (  i.past_quarter_credit_sum
                           + e.past_quarter_credit_sum)
                             past_quarter_credit_sum,
                          (  i.past_quarter_debit_sum
                           + e.past_quarter_debit_sum)
                             past_quarter_debit_sum,
                          (  i.past_quarter_gl_balance
                           + e.past_quarter_gl_balance)
                             past_quarter_gl_balance,
                          (  i.this_halfyear_credit_sum
                           + e.this_halfyear_credit_sum)
                             this_halfyear_credit_sum,
                          (  i.this_halfyear_debit_sum
                           + e.this_halfyear_debit_sum)
                             this_halfyear_debit_sum,
                          (  i.this_halfyear_gl_balance
                           + e.this_halfyear_gl_balance)
                             this_halfyear_gl_balance,
                          (  i.past_halfyear_credit_sum
                           + e.past_halfyear_credit_sum)
                             past_halfyear_credit_sum,
                          (  i.past_halfyear_debit_sum
                           + e.past_halfyear_debit_sum)
                             past_halfyear_debit_sum,
                          (  i.past_halfyear_gl_balance
                           + e.past_halfyear_gl_balance)
                             past_halfyear_gl_balance,
                          (i.this_year_credit_sum + e.this_year_credit_sum)
                             this_year_credit_sum,
                          (i.this_year_debit_sum + e.this_year_debit_sum)
                             this_year_debit_sum,
                          (i.this_year_gl_balance + e.this_year_gl_balance)
                             this_year_gl_balance,
                          (i.past_year_credit_sum + e.past_year_credit_sum)
                             past_year_credit_sum,
                          (i.past_year_debit_sum + e.past_year_debit_sum)
                             past_year_debit_sum,
                          (i.past_year_gl_balance + e.past_year_gl_balance)
                             past_year_gl_balance,
                          (  i.this_period_credit_sum
                           + e.this_period_credit_sum)
                             this_period_credit_sum,
                          (i.this_period_debit_sum + e.this_period_debit_sum)
                             this_period_debit_sum,
                          (  i.this_period_gl_balance
                           + e.this_period_gl_balance)
                             this_period_gl_balance
                     FROM income_balance i, expences_balance e)
            LOOP
               UPDATE finance_ledger_report_balance
                  SET ason_gl_balance =
                         rec_parent_ledger_balance.ason_gl_balance,
                      ason_debit_sum =
                         rec_parent_ledger_balance.ason_debit_sum,
                      ason_credit_sum =
                         rec_parent_ledger_balance.ason_credit_sum,
                      asof_debit_sum =
                         rec_parent_ledger_balance.asof_debit_sum,
                      asof_credit_sum =
                         rec_parent_ledger_balance.asof_credit_sum,
                      asof_gl_balance =
                         rec_parent_ledger_balance.asof_gl_balance,
                      this_month_debit_sum =
                         rec_parent_ledger_balance.this_month_debit_sum,
                      this_month_credit_sum =
                         rec_parent_ledger_balance.this_month_credit_sum,
                      this_month_gl_balance =
                         rec_parent_ledger_balance.this_month_gl_balance,
                      past_month_debit_sum =
                         rec_parent_ledger_balance.past_month_debit_sum,
                      past_month_credit_sum =
                         rec_parent_ledger_balance.past_month_credit_sum,
                      past_month_gl_balance =
                         rec_parent_ledger_balance.past_month_gl_balance,
                      this_quarter_credit_sum =
                         rec_parent_ledger_balance.this_quarter_credit_sum,
                      this_quarter_debit_sum =
                         rec_parent_ledger_balance.this_quarter_debit_sum,
                      this_quarter_gl_balance =
                         rec_parent_ledger_balance.this_quarter_gl_balance,
                      past_quarter_credit_sum =
                         rec_parent_ledger_balance.past_quarter_credit_sum,
                      past_quarter_debit_sum =
                         rec_parent_ledger_balance.past_quarter_debit_sum,
                      past_quarter_gl_balance =
                         rec_parent_ledger_balance.past_quarter_gl_balance,
                      this_halfyear_credit_sum =
                         rec_parent_ledger_balance.this_halfyear_credit_sum,
                      this_halfyear_debit_sum =
                         rec_parent_ledger_balance.this_halfyear_debit_sum,
                      this_halfyear_gl_balance =
                         rec_parent_ledger_balance.this_halfyear_gl_balance,
                      past_halfyear_credit_sum =
                         rec_parent_ledger_balance.past_halfyear_credit_sum,
                      past_halfyear_debit_sum =
                         rec_parent_ledger_balance.past_halfyear_debit_sum,
                      past_halfyear_gl_balance =
                         rec_parent_ledger_balance.past_halfyear_gl_balance,
                      this_year_credit_sum =
                         rec_parent_ledger_balance.this_year_credit_sum,
                      this_year_debit_sum =
                         rec_parent_ledger_balance.this_year_debit_sum,
                      this_year_gl_balance =
                         rec_parent_ledger_balance.this_year_gl_balance,
                      past_year_credit_sum =
                         rec_parent_ledger_balance.past_year_credit_sum,
                      past_year_debit_sum =
                         rec_parent_ledger_balance.past_year_debit_sum,
                      past_year_gl_balance =
                         rec_parent_ledger_balance.past_year_gl_balance,
                      this_period_credit_sum =
                         rec_parent_ledger_balance.this_period_credit_sum,
                      this_period_debit_sum =
                         rec_parent_ledger_balance.this_period_debit_sum,
                      this_period_gl_balance =
                         rec_parent_ledger_balance.this_period_gl_balance
                WHERE     gl_code = w_profit_and_loss_ledger
                      AND app_user_id = p_app_user_id;
            END LOOP;
         END;
      END IF;

      --- Updating Parent Ledger agin for profit loss balance effect

      BEGIN
         FOR rec_parent_ledger IN (  SELECT DISTINCT gl_level, parent_code
                                       FROM finance_ledger_report_param
                                      WHERE app_user_id = p_app_user_id
                                   ORDER BY gl_level DESC)
         LOOP
            FOR rec_parent_ledger_balance
               IN (SELECT sum (ason_credit_sum)
                             ason_credit_sum,
                          sum (ason_debit_sum)
                             ason_debit_sum,
                          sum (ason_gl_balance)
                             ason_gl_balance,
                          sum (asof_credit_sum)
                             asof_credit_sum,
                          sum (asof_debit_sum)
                             asof_debit_sum,
                          sum (asof_gl_balance)
                             asof_gl_balance,
                          sum (this_month_credit_sum)
                             this_month_credit_sum,
                          sum (this_month_debit_sum)
                             this_month_debit_sum,
                          sum (this_month_gl_balance)
                             this_month_gl_balance,
                          sum (past_month_credit_sum)
                             past_month_credit_sum,
                          sum (past_month_debit_sum)
                             past_month_debit_sum,
                          sum (past_month_gl_balance)
                             past_month_gl_balance,
                          sum (this_quarter_credit_sum)
                             this_quarter_credit_sum,
                          sum (this_quarter_debit_sum)
                             this_quarter_debit_sum,
                          sum (this_quarter_gl_balance)
                             this_quarter_gl_balance,
                          sum (past_quarter_credit_sum)
                             past_quarter_credit_sum,
                          sum (past_quarter_debit_sum)
                             past_quarter_debit_sum,
                          sum (past_quarter_gl_balance)
                             past_quarter_gl_balance,
                          sum (this_halfyear_credit_sum)
                             this_halfyear_credit_sum,
                          sum (this_halfyear_debit_sum)
                             this_halfyear_debit_sum,
                          sum (this_halfyear_gl_balance)
                             this_halfyear_gl_balance,
                          sum (past_halfyear_credit_sum)
                             past_halfyear_credit_sum,
                          sum (past_halfyear_debit_sum)
                             past_halfyear_debit_sum,
                          sum (past_halfyear_gl_balance)
                             past_halfyear_gl_balance,
                          sum (this_year_credit_sum)
                             this_year_credit_sum,
                          sum (this_year_debit_sum)
                             this_year_debit_sum,
                          sum (this_year_gl_balance)
                             this_year_gl_balance,
                          sum (past_year_credit_sum)
                             past_year_credit_sum,
                          sum (past_year_debit_sum)
                             past_year_debit_sum,
                          sum (past_year_gl_balance)
                             past_year_gl_balance,
                          sum (this_period_credit_sum)
                             this_period_credit_sum,
                          sum (this_period_debit_sum)
                             this_period_debit_sum,
                          sum (this_period_gl_balance)
                             this_period_gl_balance
                     FROM finance_ledger_report_balance b,
                          (SELECT *
                             FROM finance_ledger_report_param
                            WHERE app_user_id = p_app_user_id) p
                    WHERE     b.gl_code = p.gl_code
                          AND p.parent_code = rec_parent_ledger.parent_code
                          AND p.app_user_id = b.app_user_id
                          AND p.app_user_id = p_app_user_id)
            LOOP
               UPDATE finance_ledger_report_balance
                  SET ason_gl_balance =
                         rec_parent_ledger_balance.ason_gl_balance,
                      ason_debit_sum =
                         rec_parent_ledger_balance.ason_debit_sum,
                      ason_credit_sum =
                         rec_parent_ledger_balance.ason_credit_sum,
                      asof_debit_sum =
                         rec_parent_ledger_balance.asof_debit_sum,
                      asof_credit_sum =
                         rec_parent_ledger_balance.asof_credit_sum,
                      asof_gl_balance =
                         rec_parent_ledger_balance.asof_gl_balance,
                      this_month_debit_sum =
                         rec_parent_ledger_balance.this_month_debit_sum,
                      this_month_credit_sum =
                         rec_parent_ledger_balance.this_month_credit_sum,
                      this_month_gl_balance =
                         rec_parent_ledger_balance.this_month_gl_balance,
                      past_month_debit_sum =
                         rec_parent_ledger_balance.past_month_debit_sum,
                      past_month_credit_sum =
                         rec_parent_ledger_balance.past_month_credit_sum,
                      past_month_gl_balance =
                         rec_parent_ledger_balance.past_month_gl_balance,
                      this_quarter_credit_sum =
                         rec_parent_ledger_balance.this_quarter_credit_sum,
                      this_quarter_debit_sum =
                         rec_parent_ledger_balance.this_quarter_debit_sum,
                      this_quarter_gl_balance =
                         rec_parent_ledger_balance.this_quarter_gl_balance,
                      past_quarter_credit_sum =
                         rec_parent_ledger_balance.past_quarter_credit_sum,
                      past_quarter_debit_sum =
                         rec_parent_ledger_balance.past_quarter_debit_sum,
                      past_quarter_gl_balance =
                         rec_parent_ledger_balance.past_quarter_gl_balance,
                      this_halfyear_credit_sum =
                         rec_parent_ledger_balance.this_halfyear_credit_sum,
                      this_halfyear_debit_sum =
                         rec_parent_ledger_balance.this_halfyear_debit_sum,
                      this_halfyear_gl_balance =
                         rec_parent_ledger_balance.this_halfyear_gl_balance,
                      past_halfyear_credit_sum =
                         rec_parent_ledger_balance.past_halfyear_credit_sum,
                      past_halfyear_debit_sum =
                         rec_parent_ledger_balance.past_halfyear_debit_sum,
                      past_halfyear_gl_balance =
                         rec_parent_ledger_balance.past_halfyear_gl_balance,
                      this_year_credit_sum =
                         rec_parent_ledger_balance.this_year_credit_sum,
                      this_year_debit_sum =
                         rec_parent_ledger_balance.this_year_debit_sum,
                      this_year_gl_balance =
                         rec_parent_ledger_balance.this_year_gl_balance,
                      past_year_credit_sum =
                         rec_parent_ledger_balance.past_year_credit_sum,
                      past_year_debit_sum =
                         rec_parent_ledger_balance.past_year_debit_sum,
                      past_year_gl_balance =
                         rec_parent_ledger_balance.past_year_gl_balance,
                      this_period_credit_sum =
                         rec_parent_ledger_balance.this_period_credit_sum,
                      this_period_debit_sum =
                         rec_parent_ledger_balance.this_period_debit_sum,
                      this_period_gl_balance =
                         rec_parent_ledger_balance.this_period_gl_balance
                WHERE     gl_code = rec_parent_ledger.parent_code
                      AND app_user_id = p_app_user_id;
            END LOOP;
         END LOOP;
      END;


      IF p_report_name IN
            ('finance_receipt_payment', 'finance_receipt_payment2')
      THEN
         FOR rec_cashnbank_list IN (SELECT gl_code
                                      FROM finance_cash_and_bank_ledger
                                     WHERE is_active)
         LOOP
            SELECT o_gl_balance
            INTO w_asonday_opening_bal
            FROM fn_finance_get_ason_glbal (p_branch_code,
                                            rec_cashnbank_list.gl_code,
                                            w_ason_date - 1);

            IF p_report_name = 'finance_receipt_payment2'
            THEN
               SELECT o_gl_balance
               INTO w_month_opening_bal
               FROM fn_finance_get_ason_glbal (p_branch_code,
                                               rec_cashnbank_list.gl_code,
                                               w_month_start_date - 1);
            ELSE
               SELECT o_gl_balance
               INTO w_month_opening_bal
               FROM fn_finance_get_ason_glbal (
                       p_branch_code,
                       rec_cashnbank_list.gl_code,
                       CAST (date_trunc ('month', w_ason_date) AS DATE) - 1);
            END IF;


            SELECT o_gl_balance
            INTO w_year_opening_bal
            FROM fn_finance_get_ason_glbal (
                    p_branch_code,
                    rec_cashnbank_list.gl_code,
                    CAST (date_trunc ('year', w_ason_date) AS DATE) - 1);


            SELECT o_gl_balance
            INTO w_asonday_closing_bal
            FROM fn_finance_get_ason_glbal (p_branch_code,
                                            rec_cashnbank_list.gl_code,
                                            w_ason_date);

            IF p_report_name = 'finance_receipt_payment2'
            THEN
               SELECT o_gl_balance
               INTO w_month_closing_bal
               FROM fn_finance_get_ason_glbal (p_branch_code,
                                               rec_cashnbank_list.gl_code,
                                               w_month_end_date);
            ELSE
               SELECT o_gl_balance
               INTO w_month_closing_bal
               FROM fn_finance_get_ason_glbal (
                       p_branch_code,
                       rec_cashnbank_list.gl_code,
                       CAST (
                            date_trunc ('month', w_ason_date)
                          + INTERVAL '1 months'
                          - INTERVAL '1 day'
                             AS DATE));
            END IF;

            SELECT o_gl_balance
            INTO w_year_closing_bal
            FROM fn_finance_get_ason_glbal (
                    p_branch_code,
                    rec_cashnbank_list.gl_code,
                    CAST (
                         date_trunc ('year', w_ason_date)
                       + INTERVAL '12 months'
                       - INTERVAL '1 day'
                          AS DATE));

            UPDATE finance_ledger_report_balance
               SET ason_credit_sum = w_asonday_opening_bal,
                   asof_credit_sum = NULL,
                   this_month_credit_sum = w_month_opening_bal,
                   this_year_credit_sum = w_year_opening_bal,
                   ason_debit_sum = w_asonday_closing_bal,
                   asof_debit_sum = NULL,
                   this_month_debit_sum = w_month_closing_bal,
                   this_year_debit_sum = w_year_closing_bal
             WHERE     gl_code = rec_cashnbank_list.gl_code
                   AND app_user_id = p_app_user_id;
         END LOOP;
      END IF;


      FOR rec_parent_ledger_balance
         IN (SELECT *
              FROM finance_ledger_report_balance
             WHERE     app_user_id = p_app_user_id
                   AND gl_code <> w_profit_and_loss_ledger)
      LOOP
         UPDATE finance_ledger_report_balance
            SET ason_gl_balance =
                   abs (rec_parent_ledger_balance.ason_gl_balance),
                ason_debit_sum =
                   abs (rec_parent_ledger_balance.ason_debit_sum),
                ason_credit_sum =
                   abs (rec_parent_ledger_balance.ason_credit_sum),
                asof_debit_sum =
                   abs (rec_parent_ledger_balance.asof_debit_sum),
                asof_credit_sum =
                   abs (rec_parent_ledger_balance.asof_credit_sum),
                asof_gl_balance =
                   abs (rec_parent_ledger_balance.asof_gl_balance),
                this_month_debit_sum =
                   abs (rec_parent_ledger_balance.this_month_debit_sum),
                this_month_credit_sum =
                   abs (rec_parent_ledger_balance.this_month_credit_sum),
                this_month_gl_balance =
                   abs (rec_parent_ledger_balance.this_month_gl_balance),
                past_month_debit_sum =
                   abs (rec_parent_ledger_balance.past_month_debit_sum),
                past_month_credit_sum =
                   abs (rec_parent_ledger_balance.past_month_credit_sum),
                past_month_gl_balance =
                   abs (rec_parent_ledger_balance.past_month_gl_balance),
                this_quarter_credit_sum =
                   abs (rec_parent_ledger_balance.this_quarter_credit_sum),
                this_quarter_debit_sum =
                   abs (rec_parent_ledger_balance.this_quarter_debit_sum),
                this_quarter_gl_balance =
                   abs (rec_parent_ledger_balance.this_quarter_gl_balance),
                past_quarter_credit_sum =
                   abs (rec_parent_ledger_balance.past_quarter_credit_sum),
                past_quarter_debit_sum =
                   abs (rec_parent_ledger_balance.past_quarter_debit_sum),
                past_quarter_gl_balance =
                   abs (rec_parent_ledger_balance.past_quarter_gl_balance),
                this_halfyear_credit_sum =
                   abs (rec_parent_ledger_balance.this_halfyear_credit_sum),
                this_halfyear_debit_sum =
                   abs (rec_parent_ledger_balance.this_halfyear_debit_sum),
                this_halfyear_gl_balance =
                   abs (rec_parent_ledger_balance.this_halfyear_gl_balance),
                past_halfyear_credit_sum =
                   abs (rec_parent_ledger_balance.past_halfyear_credit_sum),
                past_halfyear_debit_sum =
                   abs (rec_parent_ledger_balance.past_halfyear_debit_sum),
                past_halfyear_gl_balance =
                   abs (rec_parent_ledger_balance.past_halfyear_gl_balance),
                this_year_credit_sum =
                   abs (rec_parent_ledger_balance.this_year_credit_sum),
                this_year_debit_sum =
                   abs (rec_parent_ledger_balance.this_year_debit_sum),
                this_year_gl_balance =
                   abs (rec_parent_ledger_balance.this_year_gl_balance),
                past_year_credit_sum =
                   abs (rec_parent_ledger_balance.past_year_credit_sum),
                past_year_debit_sum =
                   abs (rec_parent_ledger_balance.past_year_debit_sum),
                past_year_gl_balance =
                   abs (rec_parent_ledger_balance.past_year_gl_balance),
                this_period_credit_sum =
                   abs (rec_parent_ledger_balance.this_period_credit_sum),
                this_period_debit_sum =
                   abs (rec_parent_ledger_balance.this_period_debit_sum),
                this_period_gl_balance =
                   abs (rec_parent_ledger_balance.this_period_gl_balance)
          WHERE     gl_code = rec_parent_ledger_balance.gl_code
                AND app_user_id = p_app_user_id;
      END LOOP;
   END;

   IF p_report_name IN ('finance_receipt_payment2')
   THEN
      DELETE FROM
         finance_ledger_report_balance
            WHERE     this_month_debit_sum = 0.00
                  AND this_month_credit_sum = 0.00;
   END IF;

   IF p_report_name IN
         ('finance_receipt_payment', 'finance_receipt_payment2')
   THEN
      SELECT *
        INTO w_status, w_errm
        FROM fn_run_finance_ledger_receipt_payment (p_app_user_id);
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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_run_finance_ledger_balance_headoffice
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_run_finance_ledger_balance_headoffice (
   IN      p_branch_code   INTEGER,
   IN      p_report_name   CHARACTER,
   IN      p_ason_date     DATE,
   IN      p_from_date     DATE,
   IN      p_upto_date     DATE,
   IN      p_app_user_id   CHARACTER,
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
   w_status                     VARCHAR;
   w_errm                       VARCHAR;
   rec_ledger_balance           RECORD;
   rec_parent_ledger            RECORD;
   rec_parent_ledger_balance    RECORD;
   rec_ledger_list              RECORD;
   rec_cashnbank_list           RECORD;
   w_parent_ledger_balance      NUMERIC (22, 2) := 0;
   w_total_debit_sum            NUMERIC (22, 2) := 0;
   w_total_credit_sum           NUMERIC (22, 2) := 0;
   w_total_income               NUMERIC (22, 2) := 0;
   w_total_expense              NUMERIC (22, 2) := 0;
   w_total_profit_and_loss      NUMERIC (22, 2) := 0;
   w_asonday_opening_bal        NUMERIC (22, 2) := 0;
   w_month_opening_bal          NUMERIC (22, 2) := 0;
   w_quarter_opening_bal        NUMERIC (22, 2) := 0;
   w_halfyear_opening_bal       NUMERIC (22, 2) := 0;
   w_year_opening_bal           NUMERIC (22, 2) := 0;
   w_asonday_closing_bal        NUMERIC (22, 2) := 0;
   w_month_closing_bal          NUMERIC (22, 2) := 0;
   w_quarter_closing_bal        NUMERIC (22, 2) := 0;
   w_halfyear_closing_bal       NUMERIC (22, 2) := 0;
   w_year_closing_bal           NUMERIC (22, 2) := 0;
   w_ason_date                  DATE;
   w_month_start_date           DATE;
   w_month_end_date             DATE;
   w_stock_in_hand_ledger       VARCHAR;
   w_cost_of_good_sold_ledger   VARCHAR;
   w_stock_parent_ledger        VARCHAR;
   w_total_purchase_amount      NUMERIC (22, 2) := 0;
   w_cost_of_good_sold          NUMERIC (22, 2) := 0;
   w_total_sales_amount         NUMERIC (22, 2) := 0;
   rec_branch_list              RECORD;
   rec_product_list             RECORD;
   w_this_year_month            INTEGER;
   w_past_year_month            INTEGER;
   w_year_start                 DATE;
   w_year_end                   DATE;

   w_current_month              INTEGER;
   w_past_month                 INTEGER;
   w_current_year               INTEGER;
   w_past_year                  INTEGER;
   w_branch_name                VARCHAR;
   w_branch_address             VARCHAR;
   w_asset_main_gl              VARCHAR;
   w_liabilities_main_gl        VARCHAR;
   w_income_main_gl             VARCHAR;
   w_expenses_main_gl           VARCHAR;
   w_profit_and_loss_ledger     VARCHAR;
BEGIN
   w_ason_date := p_ason_date;

   IF p_ason_date IS NULL
   THEN
      w_ason_date := p_upto_date;
   END IF;

   SELECT asset_main_gl,
          liabilities_main_gl,
          income_main_gl,
          expenses_main_gl,
          profit_and_loss_ledger
     INTO w_asset_main_gl,
          w_liabilities_main_gl,
          w_income_main_gl,
          w_expenses_main_gl,
          w_profit_and_loss_ledger
     FROM finance_application_settings;

   w_month_start_date := CAST (date_trunc ('month', w_ason_date) AS DATE);
   w_month_end_date :=
      CAST (
           date_trunc ('month', w_ason_date)
         + INTERVAL '1 months'
         - INTERVAL '1 day'
            AS DATE);

   w_past_year_month :=
      CAST (
            TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE) - 1,
                     'YYYY')
         || TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE) - 1,
                     'MM')
            AS INTEGER);
   w_this_year_month :=
      CAST (
            TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE),
                     'YYYY')
         || TO_CHAR (CAST (date_trunc ('month', w_ason_date) AS DATE), 'MM')
            AS INTEGER);

   w_year_end :=
      CAST (
           date_trunc ('year', w_ason_date)
         + INTERVAL '12 months'
         - INTERVAL '1 day'
            AS DATE);

   w_year_start := CAST (date_trunc ('year', w_ason_date) AS DATE);

   IF w_year_end > w_ason_date
   THEN
      w_year_end := w_ason_date;
   END IF;

   IF w_month_end_date > w_ason_date
   THEN
      w_month_end_date := w_ason_date;
   END IF;

   IF p_report_name = 'finance_receipt_payment2'
   THEN
      w_month_end_date := p_upto_date;
      w_month_start_date := p_from_date;
      w_ason_date := p_from_date;
   END IF;

   ---RAISE EXCEPTION USING message = w_month_start_date;

   DELETE FROM finance_ledger_report_param
         WHERE app_user_id = p_app_user_id;

   DELETE FROM finance_ledger_report_balance
         WHERE app_user_id = p_app_user_id;

   FOR rec_branch_list IN (SELECT * FROM appauth_branch)
   LOOP
      SELECT w_status, w_errm
        INTO w_status, w_errm
        FROM fn_finance_balance_history (rec_branch_list.branch_code);

      IF w_status = 'E'
      THEN
         RAISE EXCEPTION USING MESSAGE = w_errm;
      END IF;
   END LOOP;


   INSERT INTO finance_ledger_report_param (branch_code,
                                            gl_code,
                                            gl_level,
                                            gl_name,
                                            reporting_gl_code,
                                            reporting_gl_serial,
                                            parent_code,
                                            gl_level_class,
                                            income_gl,
                                            expense_gl,
                                            assets_gl,
                                            liabilities_gl,
                                            is_leaf_node,
                                            maintain_by_system,
                                            sundry_flag,
                                            app_user_id)
      WITH
         RECURSIVE root_data
         AS
            (SELECT gl_code,
                    gl_name,
                    reporting_gl_code,
                    reporting_gl_serial,
                    parent_code,
                    is_leaf_node,
                    income_gl,
                    expense_gl,
                    assets_gl,
                    liabilities_gl,
                    sundry_flag,
                    maintain_by_system,
                    1  AS level
               FROM finance_general_ledger
              WHERE parent_code IS NULL
             UNION ALL
             SELECT e.gl_code,
                    e.gl_name,
                    e.reporting_gl_code,
                    e.reporting_gl_serial,
                    e.parent_code,
                    e.is_leaf_node,
                    e.income_gl,
                    e.expense_gl,
                    e.assets_gl,
                    e.liabilities_gl,
                    e.sundry_flag,
                    e.maintain_by_system,
                    c.level + 1
               FROM root_data c
                    JOIN finance_general_ledger e
                       ON e.parent_code = c.gl_code)
        SELECT p_branch_code branch_code,
               gl_code,
               level gl_level,
               gl_name || COALESCE (' [' || reporting_gl_code || ']', ''),
               reporting_gl_code,
               reporting_gl_serial,
               parent_code,
                  'padding-left: '
               || 10 * level
               || 'px; '
               || (CASE
                      WHEN is_leaf_node THEN 'font-weight: normal'
                      ELSE 'font-weight: bold;'
                   END)
               || '; ' gl_level_class,
               income_gl,
               expense_gl,
               assets_gl,
               liabilities_gl,
               is_leaf_node,
               maintain_by_system,
               sundry_flag,
               p_app_user_id app_user_id
          FROM root_data
      ORDER BY reporting_gl_serial, reporting_gl_code, parent_code;


   --raise exception using message ='A';

   BEGIN
      FOR rec_ledger_list IN (SELECT DISTINCT branch_code, gl_code
                                FROM finance_ledger_balance)
      LOOP
         SELECT *
         INTO w_status, w_status
         FROM fn_finance_glbal_hist (rec_ledger_list.gl_code,
                                     rec_ledger_list.branch_code,
                                     w_ason_date);
      END LOOP;
   END;


   IF p_report_name = 'finance_trial_balance'
   THEN
      INSERT INTO finance_ledger_report_balance (branch_code,
                                                 gl_code,
                                                 ason_credit_sum,
                                                 ason_debit_sum,
                                                 this_period_credit_sum,
                                                 this_period_debit_sum,
                                                 asof_credit_sum,
                                                 asof_debit_sum,
                                                 app_user_id)
         WITH
            opening_balance
            AS
               (  SELECT b.gl_code,
                         sum (b.cum_debit_sum) opening_debit_sum,
                         sum (b.cum_credit_sum) opening_credit_sum,
                         SUM (b.cum_credit_sum - b.cum_debit_sum) asof_gl_balance
                    FROM finance_ledger_balance_hist b,
                         (  SELECT branch_code,
                                   gl_code,
                                   max (transaction_date) transaction_date
                              FROM finance_ledger_balance_hist
                             WHERE transaction_date < p_from_date
                          GROUP BY branch_code, gl_code) h
                   WHERE     h.gl_code = b.gl_code
                         AND h.branch_code = b.branch_code
                         AND h.transaction_date = b.transaction_date
                GROUP BY b.gl_code),
            periodic_balance
            AS
               (  SELECT b.gl_code,
                         sum (b.total_debit_sum) this_period_debit_sum,
                         sum (b.total_credit_sum) this_period_credit_sum
                    FROM finance_ledger_balance_hist b
                   WHERE b.transaction_date BETWEEN p_from_date AND p_upto_date
                GROUP BY b.gl_code),
            gl_balance
            AS
               (SELECT COALESCE (b.gl_code, m.gl_code)
                          gl_code,
                       COALESCE (b.opening_debit_sum, 0)
                          opening_debit_sum,
                       COALESCE (b.opening_credit_sum, 0)
                          opening_credit_sum,
                       COALESCE (m.this_period_debit_sum, 0)
                          this_period_debit_sum,
                       COALESCE (m.this_period_credit_sum, 0)
                          this_period_credit_sum
                  FROM opening_balance b
                       FULL OUTER JOIN periodic_balance m
                          ON (b.gl_code = m.gl_code))
         SELECT p_branch_code
                   branch_code,
                COALESCE (p.gl_code, b.gl_code)
                   gl_code,
                COALESCE (opening_credit_sum, 0.00)
                   opening_credit_sum,
                COALESCE (opening_debit_sum, 0.00)
                   opening_debit_sum,
                COALESCE (this_period_credit_sum, 0.00)
                   this_period_credit_sum,
                COALESCE (this_period_debit_sum, 0.00)
                   this_period_debit_sum,
                  COALESCE (opening_credit_sum, 0.00)
                + COALESCE (this_period_credit_sum, 0.00)
                   closing_credit_sum,
                  COALESCE (opening_debit_sum, 0.00)
                + COALESCE (this_period_debit_sum, 0.00)
                   closing_debit_sum,
                p_app_user_id
                   app_user_id
           FROM gl_balance b
                FULL OUTER JOIN (SELECT *
                                   FROM finance_ledger_report_param
                                  WHERE app_user_id = p_app_user_id) p
                   ON (b.gl_code = p.gl_code);
   END IF;

   IF p_report_name IN
         ('finance_receipt_payment', 'finance_receipt_payment2')
   THEN
      DELETE FROM finance_ledger_report_param
            WHERE sundry_flag AND app_user_id = p_app_user_id;

      BEGIN
         INSERT INTO finance_ledger_report_balance (branch_code,
                                                    gl_code,
                                                    ason_credit_sum,
                                                    ason_debit_sum,
                                                    ason_gl_balance,
                                                    asof_credit_sum,
                                                    asof_debit_sum,
                                                    asof_gl_balance,
                                                    this_month_credit_sum,
                                                    this_month_debit_sum,
                                                    this_month_gl_balance,
                                                    past_month_credit_sum,
                                                    past_month_debit_sum,
                                                    past_month_gl_balance,
                                                    this_quarter_credit_sum,
                                                    this_quarter_debit_sum,
                                                    this_quarter_gl_balance,
                                                    past_quarter_credit_sum,
                                                    past_quarter_debit_sum,
                                                    past_quarter_gl_balance,
                                                    this_halfyear_credit_sum,
                                                    this_halfyear_debit_sum,
                                                    this_halfyear_gl_balance,
                                                    past_halfyear_credit_sum,
                                                    past_halfyear_debit_sum,
                                                    past_halfyear_gl_balance,
                                                    this_year_credit_sum,
                                                    this_year_debit_sum,
                                                    this_year_gl_balance,
                                                    past_year_credit_sum,
                                                    past_year_debit_sum,
                                                    past_year_gl_balance,
                                                    this_period_credit_sum,
                                                    this_period_debit_sum,
                                                    this_period_gl_balance,
                                                    app_user_id)
            WITH
               ason_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.gl_balance) ason_gl_balance,
                            sum (b.total_debit_sum) ason_debit_sum,
                            sum (b.total_credit_sum) ason_credit_sum
                       FROM finance_led_rec_pay_bal_hist b
                      WHERE b.transaction_date = w_ason_date
                   GROUP BY b.gl_code),
               asof_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.cum_debit_sum) asof_debit_sum,
                            sum (b.cum_credit_sum) asof_credit_sum,
                            SUM (b.cum_credit_sum - b.cum_debit_sum) asof_gl_balance
                       FROM finance_led_rec_pay_bal_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_led_rec_pay_bal_hist
                                WHERE transaction_date <= w_ason_date
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               this_month_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) this_month_debit_sum,
                            sum (b.total_credit_sum) this_month_credit_sum,
                            SUM (b.gl_balance) this_month_gl_balance
                       FROM finance_led_rec_pay_bal_hist b
                      WHERE transaction_date BETWEEN w_month_start_date
                                                 AND w_month_end_date
                   GROUP BY b.gl_code),
               this_year_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) this_year_debit_sum,
                            sum (b.total_credit_sum) this_year_credit_sum,
                            SUM (b.gl_balance) this_month_gl_balance
                       FROM finance_led_rec_pay_bal_hist b
                      WHERE transaction_date BETWEEN w_year_start
                                                 AND w_year_end
                   GROUP BY b.gl_code)
            SELECT p_branch_code,
                   COALESCE (p.gl_code,
                             b.gl_code,
                             m.gl_code,
                             y.gl_code)
                      gl_code,
                   COALESCE (ason_credit_sum, 0.00)
                      ason_credit_sum,
                   COALESCE (ason_debit_sum, 0.00)
                      ason_debit_sum,
                   0.00
                      ason_gl_balance,
                   COALESCE (asof_credit_sum, 0.00)
                      asof_credit_sum,
                   COALESCE (asof_debit_sum, 0.00)
                      asof_debit_sum,
                   COALESCE (asof_gl_balance, 0.00)
                      asof_gl_balance,
                   COALESCE (this_month_credit_sum, 0.00)
                      this_month_credit_sum,
                   COALESCE (this_month_debit_sum, 0.00)
                      this_month_debit_sum,
                   0.00
                      this_month_gl_balance,
                   0.00
                      past_month_credit_sum,
                   0.00
                      past_month_debit_sum,
                   0.00
                      past_month_gl_balance,
                   0.00
                      this_quarter_credit_sum,
                   0.00
                      this_quarter_debit_sum,
                   0.00
                      this_quarter_gl_balance,
                   0.00
                      past_quarter_credit_sum,
                   0.00
                      past_quarter_debit_sum,
                   0.00
                      past_quarter_gl_balance,
                   0.00
                      this_halfyear_credit_sum,
                   0.00
                      this_halfyear_debit_sum,
                   0.00
                      this_halfyear_gl_balance,
                   0.00
                      past_halfyear_credit_sum,
                   0.00
                      past_halfyear_debit_sum,
                   0.00
                      past_halfyear_gl_balance,
                   COALESCE (this_year_credit_sum, 0.00)
                      this_year_credit_sum,
                   COALESCE (this_year_debit_sum, 0.00)
                      this_year_debit_sum,
                   0.00
                      this_year_gl_balance,
                   0.00
                      past_year_credit_sum,
                   0.00
                      past_year_debit_sum,
                   0.00
                      past_year_gl_balance,
                   0.00
                      this_period_credit_sum,
                   0.00
                      this_period_debit_sum,
                   0.00
                      this_period_gl_balance,
                   p_app_user_id
                      app_user_id
              FROM (SELECT *
                      FROM finance_ledger_report_param
                     WHERE app_user_id = p_app_user_id) p
                   FULL OUTER JOIN asof_day_bal o ON (p.gl_code = o.gl_code)
                   FULL OUTER JOIN this_month_bal m
                      ON (p.gl_code = m.gl_code)
                   FULL OUTER JOIN this_year_bal y ON (p.gl_code = y.gl_code)
                   FULL OUTER JOIN ason_day_bal b ON (p.gl_code = b.gl_code);
      END;
   END IF;

   IF p_report_name IN
         ('finance_asset_liabilities', 'finance_income_expenses')
   THEN
      DELETE FROM finance_ledger_report_param
            WHERE sundry_flag AND app_user_id = p_app_user_id;

      BEGIN
         INSERT INTO finance_ledger_report_balance (branch_code,
                                                    gl_code,
                                                    ason_credit_sum,
                                                    ason_debit_sum,
                                                    ason_gl_balance,
                                                    asof_credit_sum,
                                                    asof_debit_sum,
                                                    asof_gl_balance,
                                                    this_month_credit_sum,
                                                    this_month_debit_sum,
                                                    this_month_gl_balance,
                                                    past_month_credit_sum,
                                                    past_month_debit_sum,
                                                    past_month_gl_balance,
                                                    this_quarter_credit_sum,
                                                    this_quarter_debit_sum,
                                                    this_quarter_gl_balance,
                                                    past_quarter_credit_sum,
                                                    past_quarter_debit_sum,
                                                    past_quarter_gl_balance,
                                                    this_halfyear_credit_sum,
                                                    this_halfyear_debit_sum,
                                                    this_halfyear_gl_balance,
                                                    past_halfyear_credit_sum,
                                                    past_halfyear_debit_sum,
                                                    past_halfyear_gl_balance,
                                                    this_year_credit_sum,
                                                    this_year_debit_sum,
                                                    this_year_gl_balance,
                                                    past_year_credit_sum,
                                                    past_year_debit_sum,
                                                    past_year_gl_balance,
                                                    this_period_credit_sum,
                                                    this_period_debit_sum,
                                                    this_period_gl_balance,
                                                    app_user_id)
            WITH
               ason_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.gl_balance) ason_gl_balance,
                            sum (b.total_debit_sum) ason_debit_sum,
                            sum (b.total_credit_sum) ason_credit_sum
                       FROM finance_ledger_balance_hist b
                      WHERE b.transaction_date = w_ason_date
                   GROUP BY b.gl_code),
               asof_day_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.cum_debit_sum) asof_debit_sum,
                            sum (b.cum_credit_sum) asof_credit_sum,
                            SUM (b.cum_credit_sum - b.cum_debit_sum) asof_gl_balance
                       FROM finance_ledger_balance_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balance_hist
                                WHERE transaction_date <= w_ason_date
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               past_month_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) past_month_debit_sum,
                            sum (b.total_credit_sum) past_month_credit_sum,
                            SUM (b.gl_balance) past_month_gl_balance
                       FROM finance_ledger_balmon_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balmon_hist
                                WHERE transaction_date <= w_month_start_date - 1
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               this_month_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) this_month_debit_sum,
                            sum (b.total_credit_sum) this_month_credit_sum,
                            SUM (b.gl_balance) this_month_gl_balance
                       FROM finance_ledger_balance_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balance_hist
                                WHERE transaction_date <= w_month_end_date
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code),
               past_year_bal
               AS
                  (  SELECT b.gl_code,
                            sum (b.total_debit_sum) past_year_debit_sum,
                            sum (b.total_credit_sum) past_year_credit_sum,
                            SUM (b.gl_balance) past_year_gl_balance
                       FROM finance_ledger_balmon_hist b,
                            (  SELECT branch_code,
                                      gl_code,
                                      max (transaction_date) transaction_date
                                 FROM finance_ledger_balmon_hist
                                WHERE transaction_date <= w_year_start - 1
                             GROUP BY branch_code, gl_code) h
                      WHERE     h.gl_code = b.gl_code
                            AND h.branch_code = b.branch_code
                            AND h.transaction_date = b.transaction_date
                   GROUP BY b.gl_code)
            SELECT p_branch_code,
                   COALESCE (p.gl_code,
                             b.gl_code,
                             m.gl_code,
                             y.gl_code)
                      gl_code,
                   COALESCE (ason_credit_sum, 0.00)
                      ason_credit_sum,
                   COALESCE (ason_debit_sum, 0.00)
                      ason_debit_sum,
                   COALESCE (ason_gl_balance, 0.00)
                      ason_gl_balance,
                   COALESCE (asof_credit_sum, 0.00)
                      asof_credit_sum,
                   COALESCE (asof_debit_sum, 0.00)
                      asof_debit_sum,
                   COALESCE (asof_gl_balance, 0.00)
                      asof_gl_balance,
                   COALESCE (this_month_credit_sum, 0.00)
                      this_month_credit_sum,
                   COALESCE (this_month_debit_sum, 0.00)
                      this_month_debit_sum,
                   COALESCE (this_month_gl_balance, 0.00)
                      this_month_gl_balance,
                   COALESCE (past_month_credit_sum, 0.00)
                      past_month_credit_sum,
                   COALESCE (past_month_debit_sum, 0.00)
                      past_month_debit_sum,
                   COALESCE (past_month_gl_balance, 0.00)
                      past_month_gl_balance,
                   0.00
                      this_quarter_credit_sum,
                   0.00
                      this_quarter_debit_sum,
                   0.00
                      this_quarter_gl_balance,
                   0.00
                      past_quarter_credit_sum,
                   0.00
                      past_quarter_debit_sum,
                   0.00
                      past_quarter_gl_balance,
                   0.00
                      this_halfyear_credit_sum,
                   0.00
                      this_halfyear_debit_sum,
                   0.00
                      this_halfyear_gl_balance,
                   0.00
                      past_halfyear_credit_sum,
                   0.00
                      past_halfyear_debit_sum,
                   0.00
                      past_halfyear_gl_balance,
                   0.00
                      this_year_credit_sum,
                   0.00
                      this_year_debit_sum,
                   0.00
                      this_year_gl_balance,
                   COALESCE (past_year_credit_sum, 0.00)
                      past_year_credit_sum,
                   COALESCE (past_year_debit_sum, 0.00)
                      past_year_debit_sum,
                   COALESCE (past_year_gl_balance, 0.00)
                      past_year_gl_balance,
                   0.00
                      this_period_credit_sum,
                   0.00
                      this_period_debit_sum,
                   0.00
                      this_period_gl_balance,
                   p_app_user_id
                      app_user_id
              FROM (SELECT *
                      FROM finance_ledger_report_param
                     WHERE app_user_id = p_app_user_id) p
                   FULL OUTER JOIN asof_day_bal o ON (p.gl_code = o.gl_code)
                   FULL OUTER JOIN past_month_bal m
                      ON (p.gl_code = m.gl_code)
                   FULL OUTER JOIN past_year_bal y ON (p.gl_code = y.gl_code)
                   FULL OUTER JOIN this_month_bal t
                      ON (p.gl_code = t.gl_code)
                   FULL OUTER JOIN ason_day_bal b ON (p.gl_code = b.gl_code);
      END;
   END IF;

   --- Updating Parent Ledger Balance

   BEGIN
      FOR rec_parent_ledger IN (  SELECT DISTINCT gl_level, parent_code
                                    FROM finance_ledger_report_param
                                   WHERE app_user_id = p_app_user_id
                                ORDER BY gl_level DESC)
      LOOP
         FOR rec_parent_ledger_balance
            IN (SELECT sum (ason_credit_sum)
                          ason_credit_sum,
                       sum (ason_debit_sum)
                          ason_debit_sum,
                       sum (ason_gl_balance)
                          ason_gl_balance,
                       sum (asof_credit_sum)
                          asof_credit_sum,
                       sum (asof_debit_sum)
                          asof_debit_sum,
                       sum (asof_gl_balance)
                          asof_gl_balance,
                       sum (this_month_credit_sum)
                          this_month_credit_sum,
                       sum (this_month_debit_sum)
                          this_month_debit_sum,
                       sum (this_month_gl_balance)
                          this_month_gl_balance,
                       sum (past_month_credit_sum)
                          past_month_credit_sum,
                       sum (past_month_debit_sum)
                          past_month_debit_sum,
                       sum (past_month_gl_balance)
                          past_month_gl_balance,
                       sum (this_quarter_credit_sum)
                          this_quarter_credit_sum,
                       sum (this_quarter_debit_sum)
                          this_quarter_debit_sum,
                       sum (this_quarter_gl_balance)
                          this_quarter_gl_balance,
                       sum (past_quarter_credit_sum)
                          past_quarter_credit_sum,
                       sum (past_quarter_debit_sum)
                          past_quarter_debit_sum,
                       sum (past_quarter_gl_balance)
                          past_quarter_gl_balance,
                       sum (this_halfyear_credit_sum)
                          this_halfyear_credit_sum,
                       sum (this_halfyear_debit_sum)
                          this_halfyear_debit_sum,
                       sum (this_halfyear_gl_balance)
                          this_halfyear_gl_balance,
                       sum (past_halfyear_credit_sum)
                          past_halfyear_credit_sum,
                       sum (past_halfyear_debit_sum)
                          past_halfyear_debit_sum,
                       sum (past_halfyear_gl_balance)
                          past_halfyear_gl_balance,
                       sum (this_year_credit_sum)
                          this_year_credit_sum,
                       sum (this_year_debit_sum)
                          this_year_debit_sum,
                       sum (this_year_gl_balance)
                          this_year_gl_balance,
                       sum (past_year_credit_sum)
                          past_year_credit_sum,
                       sum (past_year_debit_sum)
                          past_year_debit_sum,
                       sum (past_year_gl_balance)
                          past_year_gl_balance,
                       sum (this_period_credit_sum)
                          this_period_credit_sum,
                       sum (this_period_debit_sum)
                          this_period_debit_sum,
                       sum (this_period_gl_balance)
                          this_period_gl_balance
                  FROM finance_ledger_report_balance b,
                       (SELECT *
                          FROM finance_ledger_report_param
                         WHERE app_user_id = p_app_user_id) p
                 WHERE     b.gl_code = p.gl_code
                       AND p.parent_code = rec_parent_ledger.parent_code
                       AND p.app_user_id = b.app_user_id
                       AND p.app_user_id = p_app_user_id)
         LOOP
            UPDATE finance_ledger_report_balance
               SET ason_gl_balance =
                      rec_parent_ledger_balance.ason_gl_balance,
                   ason_debit_sum = rec_parent_ledger_balance.ason_debit_sum,
                   ason_credit_sum =
                      rec_parent_ledger_balance.ason_credit_sum,
                   asof_debit_sum = rec_parent_ledger_balance.asof_debit_sum,
                   asof_credit_sum =
                      rec_parent_ledger_balance.asof_credit_sum,
                   asof_gl_balance =
                      rec_parent_ledger_balance.asof_gl_balance,
                   this_month_debit_sum =
                      rec_parent_ledger_balance.this_month_debit_sum,
                   this_month_credit_sum =
                      rec_parent_ledger_balance.this_month_credit_sum,
                   this_month_gl_balance =
                      rec_parent_ledger_balance.this_month_gl_balance,
                   past_month_debit_sum =
                      rec_parent_ledger_balance.past_month_debit_sum,
                   past_month_credit_sum =
                      rec_parent_ledger_balance.past_month_credit_sum,
                   past_month_gl_balance =
                      rec_parent_ledger_balance.past_month_gl_balance,
                   this_quarter_credit_sum =
                      rec_parent_ledger_balance.this_quarter_credit_sum,
                   this_quarter_debit_sum =
                      rec_parent_ledger_balance.this_quarter_debit_sum,
                   this_quarter_gl_balance =
                      rec_parent_ledger_balance.this_quarter_gl_balance,
                   past_quarter_credit_sum =
                      rec_parent_ledger_balance.past_quarter_credit_sum,
                   past_quarter_debit_sum =
                      rec_parent_ledger_balance.past_quarter_debit_sum,
                   past_quarter_gl_balance =
                      rec_parent_ledger_balance.past_quarter_gl_balance,
                   this_halfyear_credit_sum =
                      rec_parent_ledger_balance.this_halfyear_credit_sum,
                   this_halfyear_debit_sum =
                      rec_parent_ledger_balance.this_halfyear_debit_sum,
                   this_halfyear_gl_balance =
                      rec_parent_ledger_balance.this_halfyear_gl_balance,
                   past_halfyear_credit_sum =
                      rec_parent_ledger_balance.past_halfyear_credit_sum,
                   past_halfyear_debit_sum =
                      rec_parent_ledger_balance.past_halfyear_debit_sum,
                   past_halfyear_gl_balance =
                      rec_parent_ledger_balance.past_halfyear_gl_balance,
                   this_year_credit_sum =
                      rec_parent_ledger_balance.this_year_credit_sum,
                   this_year_debit_sum =
                      rec_parent_ledger_balance.this_year_debit_sum,
                   this_year_gl_balance =
                      rec_parent_ledger_balance.this_year_gl_balance,
                   past_year_credit_sum =
                      rec_parent_ledger_balance.past_year_credit_sum,
                   past_year_debit_sum =
                      rec_parent_ledger_balance.past_year_debit_sum,
                   past_year_gl_balance =
                      rec_parent_ledger_balance.past_year_gl_balance,
                   this_period_credit_sum =
                      rec_parent_ledger_balance.this_period_credit_sum,
                   this_period_debit_sum =
                      rec_parent_ledger_balance.this_period_debit_sum,
                   this_period_gl_balance =
                      rec_parent_ledger_balance.this_period_gl_balance
             WHERE     gl_code = rec_parent_ledger.parent_code
                   AND app_user_id = p_app_user_id;
         END LOOP;
      END LOOP;

      -- RAISE EXCEPTION USING MESSAGE = w_income_main_gl||w_expenses_main_gl;
      IF p_report_name = 'finance_asset_liabilities'
      THEN
         BEGIN
            FOR rec_parent_ledger_balance
               IN (WITH
                      income_balance
                      AS
                         (SELECT *
                           FROM finance_ledger_report_balance
                          WHERE     app_user_id = p_app_user_id
                                AND gl_code = w_income_main_gl),
                      expences_balance
                      AS
                         (SELECT *
                           FROM finance_ledger_report_balance
                          WHERE     app_user_id = p_app_user_id
                                AND gl_code = w_expenses_main_gl)
                   SELECT (i.ason_credit_sum + e.ason_credit_sum)
                             ason_credit_sum,
                          (i.ason_debit_sum + e.ason_debit_sum)
                             ason_debit_sum,
                          (i.ason_gl_balance + e.ason_gl_balance)
                             ason_gl_balance,
                          (i.asof_credit_sum + e.asof_credit_sum)
                             asof_credit_sum,
                          (i.asof_debit_sum + e.asof_debit_sum)
                             asof_debit_sum,
                          (i.asof_gl_balance + e.asof_gl_balance)
                             asof_gl_balance,
                          (i.this_month_credit_sum + e.this_month_credit_sum)
                             this_month_credit_sum,
                          (i.this_month_debit_sum + e.this_month_debit_sum)
                             this_month_debit_sum,
                          (i.this_month_gl_balance + e.this_month_gl_balance)
                             this_month_gl_balance,
                          (i.past_month_credit_sum + e.past_month_credit_sum)
                             past_month_credit_sum,
                          (i.past_month_debit_sum + e.past_month_debit_sum)
                             past_month_debit_sum,
                          (i.past_month_gl_balance + e.past_month_gl_balance)
                             past_month_gl_balance,
                          (  i.this_quarter_credit_sum
                           + e.this_quarter_credit_sum)
                             this_quarter_credit_sum,
                          (  i.this_quarter_debit_sum
                           + e.this_quarter_debit_sum)
                             this_quarter_debit_sum,
                          (  i.this_quarter_gl_balance
                           + e.this_quarter_gl_balance)
                             this_quarter_gl_balance,
                          (  i.past_quarter_credit_sum
                           + e.past_quarter_credit_sum)
                             past_quarter_credit_sum,
                          (  i.past_quarter_debit_sum
                           + e.past_quarter_debit_sum)
                             past_quarter_debit_sum,
                          (  i.past_quarter_gl_balance
                           + e.past_quarter_gl_balance)
                             past_quarter_gl_balance,
                          (  i.this_halfyear_credit_sum
                           + e.this_halfyear_credit_sum)
                             this_halfyear_credit_sum,
                          (  i.this_halfyear_debit_sum
                           + e.this_halfyear_debit_sum)
                             this_halfyear_debit_sum,
                          (  i.this_halfyear_gl_balance
                           + e.this_halfyear_gl_balance)
                             this_halfyear_gl_balance,
                          (  i.past_halfyear_credit_sum
                           + e.past_halfyear_credit_sum)
                             past_halfyear_credit_sum,
                          (  i.past_halfyear_debit_sum
                           + e.past_halfyear_debit_sum)
                             past_halfyear_debit_sum,
                          (  i.past_halfyear_gl_balance
                           + e.past_halfyear_gl_balance)
                             past_halfyear_gl_balance,
                          (i.this_year_credit_sum + e.this_year_credit_sum)
                             this_year_credit_sum,
                          (i.this_year_debit_sum + e.this_year_debit_sum)
                             this_year_debit_sum,
                          (i.this_year_gl_balance + e.this_year_gl_balance)
                             this_year_gl_balance,
                          (i.past_year_credit_sum + e.past_year_credit_sum)
                             past_year_credit_sum,
                          (i.past_year_debit_sum + e.past_year_debit_sum)
                             past_year_debit_sum,
                          (i.past_year_gl_balance + e.past_year_gl_balance)
                             past_year_gl_balance,
                          (  i.this_period_credit_sum
                           + e.this_period_credit_sum)
                             this_period_credit_sum,
                          (i.this_period_debit_sum + e.this_period_debit_sum)
                             this_period_debit_sum,
                          (  i.this_period_gl_balance
                           + e.this_period_gl_balance)
                             this_period_gl_balance
                     FROM income_balance i, expences_balance e)
            LOOP
               UPDATE finance_ledger_report_balance
                  SET ason_gl_balance =
                         rec_parent_ledger_balance.ason_gl_balance,
                      ason_debit_sum =
                         rec_parent_ledger_balance.ason_debit_sum,
                      ason_credit_sum =
                         rec_parent_ledger_balance.ason_credit_sum,
                      asof_debit_sum =
                         rec_parent_ledger_balance.asof_debit_sum,
                      asof_credit_sum =
                         rec_parent_ledger_balance.asof_credit_sum,
                      asof_gl_balance =
                         rec_parent_ledger_balance.asof_gl_balance,
                      this_month_debit_sum =
                         rec_parent_ledger_balance.this_month_debit_sum,
                      this_month_credit_sum =
                         rec_parent_ledger_balance.this_month_credit_sum,
                      this_month_gl_balance =
                         rec_parent_ledger_balance.this_month_gl_balance,
                      past_month_debit_sum =
                         rec_parent_ledger_balance.past_month_debit_sum,
                      past_month_credit_sum =
                         rec_parent_ledger_balance.past_month_credit_sum,
                      past_month_gl_balance =
                         rec_parent_ledger_balance.past_month_gl_balance,
                      this_quarter_credit_sum =
                         rec_parent_ledger_balance.this_quarter_credit_sum,
                      this_quarter_debit_sum =
                         rec_parent_ledger_balance.this_quarter_debit_sum,
                      this_quarter_gl_balance =
                         rec_parent_ledger_balance.this_quarter_gl_balance,
                      past_quarter_credit_sum =
                         rec_parent_ledger_balance.past_quarter_credit_sum,
                      past_quarter_debit_sum =
                         rec_parent_ledger_balance.past_quarter_debit_sum,
                      past_quarter_gl_balance =
                         rec_parent_ledger_balance.past_quarter_gl_balance,
                      this_halfyear_credit_sum =
                         rec_parent_ledger_balance.this_halfyear_credit_sum,
                      this_halfyear_debit_sum =
                         rec_parent_ledger_balance.this_halfyear_debit_sum,
                      this_halfyear_gl_balance =
                         rec_parent_ledger_balance.this_halfyear_gl_balance,
                      past_halfyear_credit_sum =
                         rec_parent_ledger_balance.past_halfyear_credit_sum,
                      past_halfyear_debit_sum =
                         rec_parent_ledger_balance.past_halfyear_debit_sum,
                      past_halfyear_gl_balance =
                         rec_parent_ledger_balance.past_halfyear_gl_balance,
                      this_year_credit_sum =
                         rec_parent_ledger_balance.this_year_credit_sum,
                      this_year_debit_sum =
                         rec_parent_ledger_balance.this_year_debit_sum,
                      this_year_gl_balance =
                         rec_parent_ledger_balance.this_year_gl_balance,
                      past_year_credit_sum =
                         rec_parent_ledger_balance.past_year_credit_sum,
                      past_year_debit_sum =
                         rec_parent_ledger_balance.past_year_debit_sum,
                      past_year_gl_balance =
                         rec_parent_ledger_balance.past_year_gl_balance,
                      this_period_credit_sum =
                         rec_parent_ledger_balance.this_period_credit_sum,
                      this_period_debit_sum =
                         rec_parent_ledger_balance.this_period_debit_sum,
                      this_period_gl_balance =
                         rec_parent_ledger_balance.this_period_gl_balance
                WHERE     gl_code = w_profit_and_loss_ledger
                      AND app_user_id = p_app_user_id;
            END LOOP;
         END;
      END IF;

      --- Updating Parent Ledger agin for profit loss balance effect

      BEGIN
         FOR rec_parent_ledger IN (  SELECT DISTINCT gl_level, parent_code
                                       FROM finance_ledger_report_param
                                      WHERE app_user_id = p_app_user_id
                                   ORDER BY gl_level DESC)
         LOOP
            FOR rec_parent_ledger_balance
               IN (SELECT sum (ason_credit_sum)
                             ason_credit_sum,
                          sum (ason_debit_sum)
                             ason_debit_sum,
                          sum (ason_gl_balance)
                             ason_gl_balance,
                          sum (asof_credit_sum)
                             asof_credit_sum,
                          sum (asof_debit_sum)
                             asof_debit_sum,
                          sum (asof_gl_balance)
                             asof_gl_balance,
                          sum (this_month_credit_sum)
                             this_month_credit_sum,
                          sum (this_month_debit_sum)
                             this_month_debit_sum,
                          sum (this_month_gl_balance)
                             this_month_gl_balance,
                          sum (past_month_credit_sum)
                             past_month_credit_sum,
                          sum (past_month_debit_sum)
                             past_month_debit_sum,
                          sum (past_month_gl_balance)
                             past_month_gl_balance,
                          sum (this_quarter_credit_sum)
                             this_quarter_credit_sum,
                          sum (this_quarter_debit_sum)
                             this_quarter_debit_sum,
                          sum (this_quarter_gl_balance)
                             this_quarter_gl_balance,
                          sum (past_quarter_credit_sum)
                             past_quarter_credit_sum,
                          sum (past_quarter_debit_sum)
                             past_quarter_debit_sum,
                          sum (past_quarter_gl_balance)
                             past_quarter_gl_balance,
                          sum (this_halfyear_credit_sum)
                             this_halfyear_credit_sum,
                          sum (this_halfyear_debit_sum)
                             this_halfyear_debit_sum,
                          sum (this_halfyear_gl_balance)
                             this_halfyear_gl_balance,
                          sum (past_halfyear_credit_sum)
                             past_halfyear_credit_sum,
                          sum (past_halfyear_debit_sum)
                             past_halfyear_debit_sum,
                          sum (past_halfyear_gl_balance)
                             past_halfyear_gl_balance,
                          sum (this_year_credit_sum)
                             this_year_credit_sum,
                          sum (this_year_debit_sum)
                             this_year_debit_sum,
                          sum (this_year_gl_balance)
                             this_year_gl_balance,
                          sum (past_year_credit_sum)
                             past_year_credit_sum,
                          sum (past_year_debit_sum)
                             past_year_debit_sum,
                          sum (past_year_gl_balance)
                             past_year_gl_balance,
                          sum (this_period_credit_sum)
                             this_period_credit_sum,
                          sum (this_period_debit_sum)
                             this_period_debit_sum,
                          sum (this_period_gl_balance)
                             this_period_gl_balance
                     FROM finance_ledger_report_balance b,
                          (SELECT *
                             FROM finance_ledger_report_param
                            WHERE app_user_id = p_app_user_id) p
                    WHERE     b.gl_code = p.gl_code
                          AND p.parent_code = rec_parent_ledger.parent_code
                          AND p.app_user_id = b.app_user_id
                          AND p.app_user_id = p_app_user_id)
            LOOP
               UPDATE finance_ledger_report_balance
                  SET ason_gl_balance =
                         rec_parent_ledger_balance.ason_gl_balance,
                      ason_debit_sum =
                         rec_parent_ledger_balance.ason_debit_sum,
                      ason_credit_sum =
                         rec_parent_ledger_balance.ason_credit_sum,
                      asof_debit_sum =
                         rec_parent_ledger_balance.asof_debit_sum,
                      asof_credit_sum =
                         rec_parent_ledger_balance.asof_credit_sum,
                      asof_gl_balance =
                         rec_parent_ledger_balance.asof_gl_balance,
                      this_month_debit_sum =
                         rec_parent_ledger_balance.this_month_debit_sum,
                      this_month_credit_sum =
                         rec_parent_ledger_balance.this_month_credit_sum,
                      this_month_gl_balance =
                         rec_parent_ledger_balance.this_month_gl_balance,
                      past_month_debit_sum =
                         rec_parent_ledger_balance.past_month_debit_sum,
                      past_month_credit_sum =
                         rec_parent_ledger_balance.past_month_credit_sum,
                      past_month_gl_balance =
                         rec_parent_ledger_balance.past_month_gl_balance,
                      this_quarter_credit_sum =
                         rec_parent_ledger_balance.this_quarter_credit_sum,
                      this_quarter_debit_sum =
                         rec_parent_ledger_balance.this_quarter_debit_sum,
                      this_quarter_gl_balance =
                         rec_parent_ledger_balance.this_quarter_gl_balance,
                      past_quarter_credit_sum =
                         rec_parent_ledger_balance.past_quarter_credit_sum,
                      past_quarter_debit_sum =
                         rec_parent_ledger_balance.past_quarter_debit_sum,
                      past_quarter_gl_balance =
                         rec_parent_ledger_balance.past_quarter_gl_balance,
                      this_halfyear_credit_sum =
                         rec_parent_ledger_balance.this_halfyear_credit_sum,
                      this_halfyear_debit_sum =
                         rec_parent_ledger_balance.this_halfyear_debit_sum,
                      this_halfyear_gl_balance =
                         rec_parent_ledger_balance.this_halfyear_gl_balance,
                      past_halfyear_credit_sum =
                         rec_parent_ledger_balance.past_halfyear_credit_sum,
                      past_halfyear_debit_sum =
                         rec_parent_ledger_balance.past_halfyear_debit_sum,
                      past_halfyear_gl_balance =
                         rec_parent_ledger_balance.past_halfyear_gl_balance,
                      this_year_credit_sum =
                         rec_parent_ledger_balance.this_year_credit_sum,
                      this_year_debit_sum =
                         rec_parent_ledger_balance.this_year_debit_sum,
                      this_year_gl_balance =
                         rec_parent_ledger_balance.this_year_gl_balance,
                      past_year_credit_sum =
                         rec_parent_ledger_balance.past_year_credit_sum,
                      past_year_debit_sum =
                         rec_parent_ledger_balance.past_year_debit_sum,
                      past_year_gl_balance =
                         rec_parent_ledger_balance.past_year_gl_balance,
                      this_period_credit_sum =
                         rec_parent_ledger_balance.this_period_credit_sum,
                      this_period_debit_sum =
                         rec_parent_ledger_balance.this_period_debit_sum,
                      this_period_gl_balance =
                         rec_parent_ledger_balance.this_period_gl_balance
                WHERE     gl_code = rec_parent_ledger.parent_code
                      AND app_user_id = p_app_user_id;
            END LOOP;
         END LOOP;
      END;


      IF p_report_name IN
            ('finance_receipt_payment', 'finance_receipt_payment2')
      THEN
         FOR rec_cashnbank_list IN (SELECT gl_code
                                      FROM finance_cash_and_bank_ledger
                                     WHERE is_active)
         LOOP
            SELECT o_gl_balance
            INTO w_asonday_opening_bal
            FROM fn_finance_get_ason_glbal (p_branch_code,
                                            rec_cashnbank_list.gl_code,
                                            w_ason_date - 1);

            SELECT o_gl_balance
            INTO w_month_opening_bal
            FROM fn_finance_get_ason_glbal (
                    p_branch_code,
                    rec_cashnbank_list.gl_code,
                    CAST (date_trunc ('month', w_ason_date) AS DATE) - 1);

            SELECT o_gl_balance
            INTO w_year_opening_bal
            FROM fn_finance_get_ason_glbal (
                    p_branch_code,
                    rec_cashnbank_list.gl_code,
                    CAST (date_trunc ('year', w_ason_date) AS DATE) - 1);


            SELECT o_gl_balance
            INTO w_asonday_closing_bal
            FROM fn_finance_get_ason_glbal (p_branch_code,
                                            rec_cashnbank_list.gl_code,
                                            w_ason_date);

            SELECT o_gl_balance
            INTO w_month_closing_bal
            FROM fn_finance_get_ason_glbal (
                    p_branch_code,
                    rec_cashnbank_list.gl_code,
                    CAST (
                         date_trunc ('month', w_ason_date)
                       + INTERVAL '1 months'
                       - INTERVAL '1 day'
                          AS DATE));

            SELECT o_gl_balance
            INTO w_year_closing_bal
            FROM fn_finance_get_ason_glbal (
                    p_branch_code,
                    rec_cashnbank_list.gl_code,
                    CAST (
                         date_trunc ('year', w_ason_date)
                       + INTERVAL '12 months'
                       - INTERVAL '1 day'
                          AS DATE));

            UPDATE finance_ledger_report_balance
               SET ason_credit_sum = w_asonday_opening_bal,
                   asof_credit_sum = NULL,
                   this_month_credit_sum = w_month_opening_bal,
                   this_year_credit_sum = w_year_opening_bal,
                   ason_debit_sum = w_asonday_closing_bal,
                   asof_debit_sum = NULL,
                   this_month_debit_sum = w_month_closing_bal,
                   this_year_debit_sum = w_year_closing_bal
             WHERE     gl_code = rec_cashnbank_list.gl_code
                   AND app_user_id = p_app_user_id;
         END LOOP;
      END IF;


      FOR rec_parent_ledger_balance
         IN (SELECT *
              FROM finance_ledger_report_balance
             WHERE     app_user_id = p_app_user_id
                   AND gl_code <> w_profit_and_loss_ledger)
      LOOP
         UPDATE finance_ledger_report_balance
            SET ason_gl_balance =
                   abs (rec_parent_ledger_balance.ason_gl_balance),
                ason_debit_sum =
                   abs (rec_parent_ledger_balance.ason_debit_sum),
                ason_credit_sum =
                   abs (rec_parent_ledger_balance.ason_credit_sum),
                asof_debit_sum =
                   abs (rec_parent_ledger_balance.asof_debit_sum),
                asof_credit_sum =
                   abs (rec_parent_ledger_balance.asof_credit_sum),
                asof_gl_balance =
                   abs (rec_parent_ledger_balance.asof_gl_balance),
                this_month_debit_sum =
                   abs (rec_parent_ledger_balance.this_month_debit_sum),
                this_month_credit_sum =
                   abs (rec_parent_ledger_balance.this_month_credit_sum),
                this_month_gl_balance =
                   abs (rec_parent_ledger_balance.this_month_gl_balance),
                past_month_debit_sum =
                   abs (rec_parent_ledger_balance.past_month_debit_sum),
                past_month_credit_sum =
                   abs (rec_parent_ledger_balance.past_month_credit_sum),
                past_month_gl_balance =
                   abs (rec_parent_ledger_balance.past_month_gl_balance),
                this_quarter_credit_sum =
                   abs (rec_parent_ledger_balance.this_quarter_credit_sum),
                this_quarter_debit_sum =
                   abs (rec_parent_ledger_balance.this_quarter_debit_sum),
                this_quarter_gl_balance =
                   abs (rec_parent_ledger_balance.this_quarter_gl_balance),
                past_quarter_credit_sum =
                   abs (rec_parent_ledger_balance.past_quarter_credit_sum),
                past_quarter_debit_sum =
                   abs (rec_parent_ledger_balance.past_quarter_debit_sum),
                past_quarter_gl_balance =
                   abs (rec_parent_ledger_balance.past_quarter_gl_balance),
                this_halfyear_credit_sum =
                   abs (rec_parent_ledger_balance.this_halfyear_credit_sum),
                this_halfyear_debit_sum =
                   abs (rec_parent_ledger_balance.this_halfyear_debit_sum),
                this_halfyear_gl_balance =
                   abs (rec_parent_ledger_balance.this_halfyear_gl_balance),
                past_halfyear_credit_sum =
                   abs (rec_parent_ledger_balance.past_halfyear_credit_sum),
                past_halfyear_debit_sum =
                   abs (rec_parent_ledger_balance.past_halfyear_debit_sum),
                past_halfyear_gl_balance =
                   abs (rec_parent_ledger_balance.past_halfyear_gl_balance),
                this_year_credit_sum =
                   abs (rec_parent_ledger_balance.this_year_credit_sum),
                this_year_debit_sum =
                   abs (rec_parent_ledger_balance.this_year_debit_sum),
                this_year_gl_balance =
                   abs (rec_parent_ledger_balance.this_year_gl_balance),
                past_year_credit_sum =
                   abs (rec_parent_ledger_balance.past_year_credit_sum),
                past_year_debit_sum =
                   abs (rec_parent_ledger_balance.past_year_debit_sum),
                past_year_gl_balance =
                   abs (rec_parent_ledger_balance.past_year_gl_balance),
                this_period_credit_sum =
                   abs (rec_parent_ledger_balance.this_period_credit_sum),
                this_period_debit_sum =
                   abs (rec_parent_ledger_balance.this_period_debit_sum),
                this_period_gl_balance =
                   abs (rec_parent_ledger_balance.this_period_gl_balance)
          WHERE     gl_code = rec_parent_ledger_balance.gl_code
                AND app_user_id = p_app_user_id;
      END LOOP;
   END;

   IF p_report_name IN ('finance_receipt_payment2')
   THEN
      DELETE FROM
         finance_ledger_report_balance
            WHERE     this_month_debit_sum = 0.00
                  AND this_month_credit_sum = 0.00;
   END IF;

   IF p_report_name IN
         ('finance_receipt_payment', 'finance_receipt_payment2')
   THEN
      SELECT *
        INTO w_status, w_errm
        FROM fn_run_finance_ledger_receipt_payment (p_app_user_id);
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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_run_finance_ledger_receipt_payment
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_run_finance_ledger_receipt_payment (
   IN      p_app_user_id   CHARACTER,
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
   w_status    VARCHAR;
   w_errm      VARCHAR;
   w_counter   INTEGER;
BEGIN
   DELETE FROM appauth_report_table_tabular
         WHERE app_user_id = P_app_user_id;

   INSERT INTO appauth_report_table_tabular (report_column1,
                                             report_column2,
                                             report_column3,
                                             report_column4,
                                             report_column5,
                                             report_column6,
                                             report_column7,
                                             report_column8,
                                             report_column9,
                                             app_user_id)
      SELECT 1
                receipt_serial_number,
             'OPENING'
                receipt_gl_name,
             'padding-left: 10px; font-weight: bold;;'
                receipt_gl_level_class,
             NULL
                ason_credit_sum,
             NULL
                asof_credit_sum,
             NULL
                this_month_credit_sum,
             NULL
                this_year_credit_sum,
             'O'
                receipt_payment_type,
             FALSE
                is_leaf_node,
             p_app_user_id
                app_user_id;

   INSERT INTO appauth_report_table_tabular (report_column1,
                                             report_column2,
                                             report_column3,
                                             report_column4,
                                             report_column5,
                                             report_column6,
                                             report_column7,
                                             report_column8,
                                             report_column9,
                                             app_user_id)
      SELECT *
      FROM (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) + 1
                        receipt_serial_number,
                     p.gl_name
                        receipt_gl_name,
                     p.gl_level_class
                        receipt_gl_level_class,
                     ason_credit_sum,
                     asof_credit_sum,
                     this_month_credit_sum,
                     this_year_credit_sum,
                     'O'
                        receipt_payment_type,
                     FALSE
                        is_leaf_node,
                     p_app_user_id
                        app_user_id
                FROM finance_ledger_report_balance b,
                     finance_ledger_report_param p
               WHERE     b.gl_code = p.gl_code
                     AND b.app_user_id = p.app_user_id
                     AND p.app_user_id = p_app_user_id
                     AND asof_credit_sum IS NULL
            ORDER BY p.reporting_gl_serial) T;

   SELECT COUNT (app_user_id)
     INTO w_counter
     FROM appauth_report_table_tabular
    WHERE app_user_id = P_app_user_id AND report_column8 IN ('O');

   INSERT INTO appauth_report_table_tabular (report_column1,
                                             report_column2,
                                             report_column3,
                                             report_column4,
                                             report_column5,
                                             report_column6,
                                             report_column7,
                                             report_column8,
                                             report_column9,
                                             app_user_id)
        SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) + w_counter
                  receipt_serial_number,
               p.gl_name
                  receipt_gl_name,
               p.gl_level_class
                  receipt_gl_level_class,
               ason_credit_sum,
               asof_credit_sum,
               this_month_credit_sum,
               this_year_credit_sum,
               'R'
                  receipt_payment_type,
               is_leaf_node,
               p_app_user_id
                  app_user_id
          FROM finance_ledger_report_balance b, finance_ledger_report_param p
         WHERE     b.gl_code = p.gl_code
               AND b.app_user_id = p.app_user_id
               AND p.app_user_id = p_app_user_id
               AND (   ason_credit_sum > 0
                    OR asof_credit_sum > 0
                    OR this_month_credit_sum > 0
                    OR this_year_credit_sum > 0)
               AND asof_credit_sum IS NOT NULL
      ORDER BY p.reporting_gl_serial;

   INSERT INTO appauth_report_table_tabular (report_column1,
                                             report_column2,
                                             report_column3,
                                             report_column4,
                                             report_column5,
                                             report_column6,
                                             report_column7,
                                             report_column8,
                                             report_column9,
                                             app_user_id)
        SELECT row_number () OVER (ORDER BY p.reporting_gl_serial)
                  payment_serial_number,
               p.gl_name
                  payment_gl_name,
               p.gl_level_class
                  payment_gl_level_class,
               ason_debit_sum,
               asof_debit_sum,
               this_month_debit_sum,
               this_year_debit_sum,
               'P'
                  receipt_payment_type,
               is_leaf_node,
               p_app_user_id
                  app_user_id
          FROM finance_ledger_report_balance b, finance_ledger_report_param p
         WHERE     b.gl_code = p.gl_code
               AND b.app_user_id = p.app_user_id
               AND p.app_user_id = p_app_user_id
               AND (   ason_debit_sum > 0
                    OR asof_debit_sum > 0
                    OR this_month_debit_sum > 0
                    OR this_year_debit_sum > 0)
               AND asof_debit_sum IS NOT NULL
      ORDER BY p.reporting_gl_serial;

   SELECT COUNT (app_user_id) + 1
     INTO w_counter
     FROM appauth_report_table_tabular
    WHERE app_user_id = P_app_user_id AND report_column8 = 'P';

   INSERT INTO appauth_report_table_tabular (report_column1,
                                             report_column2,
                                             report_column3,
                                             report_column4,
                                             report_column5,
                                             report_column6,
                                             report_column7,
                                             report_column8,
                                             report_column9,
                                             app_user_id)
      SELECT w_counter
                receipt_serial_number,
             'CLOSING'
                receipt_gl_name,
             'padding-left: 10px; font-weight: bold;;'
                receipt_gl_level_class,
             NULL
                ason_credit_sum,
             NULL
                asof_credit_sum,
             NULL
                this_month_credit_sum,
             NULL
                this_year_credit_sum,
             'C'
                receipt_payment_type,
             FALSE
                is_leaf_node,
             p_app_user_id
                app_user_id;

   INSERT INTO appauth_report_table_tabular (report_column1,
                                             report_column2,
                                             report_column3,
                                             report_column4,
                                             report_column5,
                                             report_column6,
                                             report_column7,
                                             report_column8,
                                             report_column9,
                                             app_user_id)
      SELECT *
      FROM (  SELECT   row_number () OVER (ORDER BY p.reporting_gl_serial)
                     + w_counter payment_serial_number,
                     p.gl_name payment_gl_name,
                     p.gl_level_class payment_gl_level_class,
                     ason_debit_sum,
                     asof_debit_sum,
                     this_month_debit_sum,
                     this_year_debit_sum,
                     'C' receipt_payment_type,
                     FALSE is_leaf_node,
                     p_app_user_id app_user_id
                FROM finance_ledger_report_balance b,
                     finance_ledger_report_param p
               WHERE     b.gl_code = p.gl_code
                     AND b.app_user_id = p.app_user_id
                     AND p.app_user_id = p_app_user_id
                     AND asof_debit_sum IS NULL
            ORDER BY p.reporting_gl_serial) t;

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
         o_errm := SQLERRM;
         o_status := 'E';
      END IF;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_run_report
-- ----------------------------------------------------------------

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
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_set_final_exam_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_set_final_exam_mark (
   IN      p_academic_year_id   INTEGER,
   IN      p_term_id            INTEGER,
   IN      p_class_id           CHARACTER,
   IN      p_student_roll       CHARACTER,
   IN      p_app_user_id        CHARACTER,
       OUT o_gpa                NUMERIC,
       OUT o_grate              CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
   w_class_id      VARCHAR;

   w_gpa           RECORD;

   w_obtain_mark   NUMERIC;

   w_total_mark    NUMERIC;
BEGIN
   SELECT sum (obtain_marks), sum (total_exam_marks)
     INTO w_obtain_mark, w_total_mark
     FROM edu_exam_marks_by_subject e
    WHERE     e.academic_year = p_academic_year_id
          AND e.term_id = p_term_id
          AND e.class_id = p_class_id
          AND e.student_roll = p_student_roll;



   SELECT *
     INTO w_gpa
     FROM fn_get_final_result_gpa (p_academic_year_id,
                                   p_term_id,
                                   p_class_id,
                                   p_student_roll,
                                   p_app_user_id);



   INSERT INTO edu_exam_marks_final (branch_code,
                                     academic_year,
                                     term_id,
                                     class_id,
                                     class_group_id,
                                     student_roll,
                                     total_exam_marks,
                                     obtain_marks,
                                     result_grade,
                                     grade_point_average,
                                     app_user_id,
                                     app_data_time)
        VALUES ((SELECT branch_code
                   FROM edu_students_info
                  WHERE student_roll = p_student_roll),
                p_academic_year_id,
                p_term_id,
                p_class_id,
                (SELECT class_group_id
                   FROM edu_students_info
                  WHERE student_roll = p_student_roll),
                p_student_roll,
                w_total_mark,
                w_obtain_mark,
                w_gpa.grade_name,
                w_gpa.result_gpa,
                p_app_user_id,
                current_timestamp);



   o_gpa := w_gpa.result_gpa;

   o_grate := w_gpa.grade_name;
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_set_single_exam_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_set_single_exam_mark (
   IN      p_academic_year_id   INTEGER,
   IN      p_branch_code        INTEGER,
   IN      p_class_id           CHARACTER,
   IN      p_class_group_id     CHARACTER,
   IN      p_student_roll       CHARACTER,
   IN      p_subject_id         CHARACTER,
   IN      p_exam_id            CHARACTER,
   IN      p_out_of             NUMERIC,
   IN      p_app_user_id        CHARACTER,
       OUT o_total_mark         NUMERIC,
       OUT o_obtain_mark        NUMERIC,
       OUT o_result_gpa         NUMERIC,
       OUT o_grade_name         CHARACTER,
       OUT o_status             CHARACTER,
       OUT o_errm               CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
   w_class_id      VARCHAR;

   r_gpa           RECORD;

   w_obtain_mark   NUMERIC;

   w_total_mark    NUMERIC;

   w_exam          RECORD;
BEGIN
   BEGIN
      SELECT *
        INTO w_exam
        FROM edu_exam_setup E
       WHERE E.exam_id = p_exam_id;



      IF w_exam.cal_condition = 'Avg'
      THEN
         SELECT sum (obtain_marks)
          INTO w_obtain_mark
          FROM edu_exam_marks_details r
         WHERE     r.academic_year = p_academic_year_id
               AND r.branch_code = p_branch_code
               AND r.class_id = p_class_id
               AND r.subject_id = p_subject_id
               AND r.exam_id = w_exam.exam_id
               AND r.student_roll = p_student_roll;



         w_obtain_mark := w_obtain_mark / w_exam.no_of_exam;
      ELSIF w_exam.cal_condition = 'Max'
      THEN
         SELECT max (obtain_marks)
          INTO w_obtain_mark
          FROM edu_exam_marks_details r
         WHERE     r.academic_year = p_academic_year_id
               AND r.branch_code = p_branch_code
               AND r.class_id = p_class_id
               AND r.subject_id = p_subject_id
               AND r.exam_id = w_exam.exam_id
               AND r.student_roll = p_student_roll;
      ELSIF w_exam.cal_condition = 'Min'
      THEN
         SELECT min (obtain_marks)
          INTO w_obtain_mark
          FROM edu_exam_marks_details r
         WHERE     r.academic_year = p_academic_year_id
               AND r.branch_code = p_branch_code
               AND r.class_id = p_class_id
               AND r.subject_id = p_subject_id
               AND r.exam_id = w_exam.exam_id
               AND r.student_roll = p_student_roll;
      ELSE
         SELECT sum (obtain_marks)
          INTO w_obtain_mark
          FROM edu_exam_marks_details r
         WHERE     r.academic_year = p_academic_year_id
               AND r.branch_code = p_branch_code
               AND r.class_id = p_class_id
               AND r.subject_id = p_subject_id
               AND r.exam_id = w_exam.exam_id
               AND r.student_roll = p_student_roll;
      END IF;


      w_total_mark := w_exam.total_exam_marks;

      SELECT *
        INTO r_gpa
        FROM fn_get_result_gpa (w_obtain_mark, w_total_mark, p_out_of);



      SELECT class_id
       INTO STRICT w_class_id
       FROM edu_exam_single_mark e
      WHERE     e.academic_year = p_academic_year_id
            AND e.branch_code = p_branch_code
            AND e.class_id = p_class_id
            AND e.subject_id = p_subject_id
            AND e.student_roll = p_student_roll
            AND e.exam_id = p_exam_id;



      UPDATE edu_exam_single_mark m
         SET total_exam_marks = w_total_mark,
             obtain_marks = w_obtain_mark,
             result_grade = r_gpa.grade_name,
             grade_point_average = r_gpa.result_gpa
       WHERE     m.academic_year = p_academic_year_id
             AND m.branch_code = p_branch_code
             AND m.class_id = p_class_id
             AND m.subject_id = p_subject_id
             AND m.student_roll = p_student_roll
             AND m.exam_id = p_exam_id;
   EXCEPTION
      WHEN NO_DATA_FOUND
      THEN
         IF r_gpa.grade_name IS NOT NULL
         THEN
            INSERT INTO edu_exam_single_mark (academic_year,
                                              term_id,
                                              class_id,
                                              class_group_id,
                                              exam_id,
                                              subject_id,
                                              student_roll,
                                              total_exam_marks,
                                              obtain_marks,
                                              result_grade,
                                              grade_point_average,
                                              app_user_id,
                                              app_data_time,
                                              branch_code)
                 VALUES (p_academic_year_id,
                         w_exam.term_id,
                         p_class_id,
                         p_class_group_id,
                         p_exam_id,
                         p_subject_id,
                         p_student_roll,
                         w_total_mark,
                         w_obtain_mark,
                         r_gpa.grade_name,
                         r_gpa.result_gpa,
                         p_app_user_id,
                         current_timestamp,
                         p_branch_code);
         END IF;
   END;



   o_total_mark := w_total_mark;

   o_obtain_mark := w_obtain_mark;

   o_grade_name := r_gpa.grade_name;

   o_result_gpa := r_gpa.result_gpa;

   o_status := 'S';

   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;

      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_set_subject_mark_by_student
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_set_subject_mark_by_student (
   IN      p_academic_year_id   INTEGER,
   IN      p_term_id            INTEGER,
   IN      p_class_id           CHARACTER,
   IN      p_class_group_id     CHARACTER,
   IN      p_student_roll       CHARACTER,
   IN      p_subject_id         CHARACTER,
   IN      p_app_user_id        CHARACTER,
       OUT o_gpa                NUMERIC,
       OUT o_grate              CHARACTER,
       OUT o_status             CHARACTER,
       OUT o_errm               CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
   w_total_subject_op_mark   NUMERIC := 0;

   w_subject_total_mark      NUMERIC;

   r_exams                   RECORD;

   out_of                    NUMERIC;

   W_total_exam_mark         NUMERIC;

   w_temp                    RECORD;

   w_gpa                     RECORD;

   w_exam_id                 CHARACTER VARYING (200);

   w_grade_name              CHARACTER VARYING (200);

   w_result_gpa              NUMERIC := 0;

   w_single_result           RECORD;
BEGIN
   SELECT maximum_marks
     INTO w_subject_total_mark
     FROM edu_subject_list e
    WHERE e.class_id = p_class_id AND e.subject_id = p_subject_id;

   -- RAISE EXCEPTION USING MESSAGE = w_subject_total_mark;



   FOR r_exams
      IN (SELECT *
           FROM edu_exam_setup E
          WHERE     E.academic_year = p_academic_year_id
                AND E.class_id = p_class_id
                AND CASE
                       WHEN p_class_group_id IS NULL
                       THEN
                          E.class_group_id IS NULL
                       ELSE
                          E.class_group_id = p_class_group_id
                    END
                AND E.subject_id = p_subject_id)
   LOOP
      w_exam_id := r_exams.exam_id;

      out_of := r_exams.out_of;



      SELECT *
        INTO w_single_result
        FROM fn_set_single_exam_mark (p_academic_year_id,
                                      p_class_id,
                                      p_class_group_id,
                                      p_student_roll,
                                      p_subject_id,
                                      w_exam_id,
                                      out_of,
                                      p_app_user_id);
   --    IF w_status <> 'S'

   --    THEN

   --    RAISE EXCEPTION

   --    USING MESSAGE =

   --    'Error in single result calculation for student '

   --    || p_student_roll

   --    || ' Exam '

   --    || w_exam_id

   --    || w_error;

   --    END IF;



   END LOOP;



   SELECT sum (obtain_marks)
    INTO w_total_subject_op_mark
    FROM edu_exam_single_mark s
   WHERE     s.academic_year = p_academic_year_id
         AND s.class_id = p_class_id
         AND s.student_roll = p_student_roll
         AND s.subject_id = p_subject_id;



   IF     w_total_subject_op_mark IS NOT NULL
      AND w_subject_total_mark IS NOT NULL
   THEN
      SELECT result_gpa, grade_name
        INTO w_result_gpa, w_grade_name
        FROM fn_get_result_gpa (w_total_subject_op_mark,
                                w_subject_total_mark,
                                out_of);

      --RAISE EXCEPTION USING MESSAGE = w_exam_id;

      --'Error in single result calculation for student '-- || w_students.student_roll || 'Subject' || w_subjects.subject_id;


      DELETE FROM
         edu_exam_marks_by_subject
            WHERE     academic_year = p_academic_year_id
                  AND class_id = p_class_id
                  AND subject_id = p_subject_id
                  AND student_roll = p_student_roll;



      INSERT INTO edu_exam_marks_by_subject (academic_year,
                                             term_id,
                                             class_id,
                                             class_group_id,
                                             subject_id,
                                             student_roll,
                                             total_exam_marks,
                                             obtain_marks,
                                             result_grade,
                                             grade_point_average,
                                             app_user_id,
                                             app_data_time)
           VALUES (p_academic_year_id,
                   p_term_id,
                   p_class_id,
                   p_class_group_id,
                   p_subject_id,
                   p_student_roll,
                   w_subject_total_mark,
                   w_total_subject_op_mark,
                   w_grade_name,
                   w_result_gpa,
                   p_app_user_id,
                   current_timestamp);


      o_gpa := w_result_gpa;

      o_grate := w_grade_name;

      o_status := 'S';

      o_errm := '';
   ELSE
      o_errm := SQLERRM;

      o_status := 'E';
   END IF;
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;

      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_store_single_exam_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_store_single_exam_mark (
   IN      p_academic_year_id   INTEGER,
   IN      p_term_id            INTEGER,
   IN      p_class_id           CHARACTER,
   IN      p_class_group_id     CHARACTER,
   IN      p_app_user_id        CHARACTER,
       OUT o_status             CHARACTER,
       OUT o_errm               CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
BEGIN
   BEGIN
      INSERT INTO edu_store_exam_single_mark (academic_year,
                                              term_id,
                                              class_id,
                                              class_group_id,
                                              exam_id,
                                              subject_id,
                                              student_roll,
                                              total_exam_marks,
                                              obtain_marks,
                                              result_grade,
                                              grade_point_average,
                                              app_user_id,
                                              app_data_time)
         (SELECT p_academic_year_id,
                 term_id,
                 p_class_id,
                 class_group_id,
                 exam_id,
                 subject_id,
                 student_roll,
                 total_exam_marks,
                 obtain_marks,
                 result_grade,
                 grade_point_average,
                 p_app_user_id,
                 current_timestamp
            FROM edu_exam_single_mark r
           WHERE     r.academic_year = p_academic_year_id
                 AND r.class_id = p_class_id
                 AND CASE
                        WHEN p_class_group_id IS NULL
                        THEN
                           r.class_group_id IS NULL
                        ELSE
                           r.class_group_id = p_class_group_id
                     END
                 AND r.term_id = p_term_id);



      DELETE FROM
         edu_exam_single_mark s
            WHERE     s.academic_year = p_academic_year_id
                  AND s.class_id = p_class_id
                  AND CASE
                         WHEN p_class_group_id IS NULL
                         THEN
                            s.class_group_id IS NULL
                         ELSE
                            s.class_group_id = p_class_group_id
                      END
                  AND s.term_id = p_term_id;
   END;



   o_status := 'S';

   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;

      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_storing_dtails_exam_marks
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_storing_dtails_exam_marks (
   IN      p_academic_year_id   INTEGER,
   IN      p_term_id            INTEGER,
   IN      p_class_id           CHARACTER,
   IN      p_class_group_id     CHARACTER,
   IN      p_app_user_id        CHARACTER,
       OUT o_status             CHARACTER,
       OUT o_errm               CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
   w_mark_details   RECORD;
BEGIN
   BEGIN
      INSERT INTO edu_storing_exam_marks_details (academic_year,
                                                  term_id,
                                                  class_id,
                                                  class_group_id,
                                                  exam_id,
                                                  exam_no,
                                                  subject_id,
                                                  student_roll,
                                                  total_exam_marks,
                                                  obtain_marks,
                                                  result_grade,
                                                  grade_point_average,
                                                  app_user_id,
                                                  app_data_time)
         SELECT p_academic_year_id,
                r.term_id,
                p_class_id,
                r.class_group_id,
                r.exam_id,
                r.exam_no,
                r.subject_id,
                r.student_roll,
                r.total_exam_marks,
                r.obtain_marks,
                r.result_grade,
                r.grade_point_average,
                p_app_user_id,
                current_timestamp
           FROM edu_exam_marks_details r
          WHERE     r.academic_year = p_academic_year_id
                AND r.class_id = p_class_id
                AND r.term_id = p_term_id
                AND CASE
                       WHEN p_class_group_id IS NULL
                       THEN
                          r.class_group_id IS NULL
                       ELSE
                          r.class_group_id = p_class_group_id
                    END;



      DELETE FROM
         edu_exam_marks_details d
            WHERE     d.academic_year = p_academic_year_id
                  AND d.class_id = p_class_id
                  AND d.term_id = p_term_id
                  AND CASE
                         WHEN p_class_group_id IS NULL
                         THEN
                            d.class_group_id IS NULL
                         ELSE
                            d.class_group_id = p_class_group_id
                      END;
   END;



   o_status := 'S';

   o_errm := '';
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;

      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_view_class_subject_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_view_class_subject_mark (
   IN      p_academic_year_id   INTEGER,
   IN      p_term_id            INTEGER,
   IN      p_class_id           CHARACTER,
   IN      p_class_group_id     CHARACTER,
   IN      p_app_user_id        CHARACTER,
       OUT o_status             CHARACTER,
       OUT o_errm               CHARACTER)
   RETURNS RECORD
   LANGUAGE 'plpgsql'
   VOLATILE
   NOT LEAKPROOF
   SECURITY INVOKER
   PARALLEL UNSAFE
AS
$$

DECLARE
   w_student_marks   RECORD;
   w_all_subject     RECORD;
   w_status          CHARACTER;
   w_errm            CHARACTER;
BEGIN
   --TRUNCATE TABLE edu_subjectmarktemp;

   DELETE FROM edu_subjectmarktemp
         WHERE app_user_id = p_app_user_id;

   FOR w_all_subject
      IN (SELECT subject_id
           FROM edu_subject_list
          WHERE     class_id = p_class_id
                AND CASE
                       WHEN p_class_group_id IS NULL
                       THEN
                          class_group_id IS NULL
                       ELSE
                          class_group_id = p_class_group_id
                    END)
   LOOP
      INSERT INTO edu_subjectmarktemp (student_roll,
                                       academic_year,
                                       class_id,
                                       class_group_id,
                                       subject_id,
                                       total_marks,
                                       total_obtain_marks,
                                       result_gpa,
                                       grade_name,
                                       app_user_id,
                                       app_data_time)
         WITH
            exams
            AS
               (SELECT *
                 FROM edu_exam_single_mark
                WHERE     academic_year = p_academic_year_id
                      AND class_id = p_class_id
                      AND term_id = p_term_id
                      AND subject_id = w_all_subject.subject_id),
            student_marks
            AS
               (  SELECT student_roll,
                         sum (total_exam_marks) AS total_marks,
                         sum (obtain_marks) AS total_obtain_marks
                    FROM exams
                GROUP BY student_roll)
         SELECT DISTINCT (e.student_roll),
                         e.academic_year,
                         e.class_id,
                         e.class_group_id,
                         e.subject_id,
                         m.total_marks,
                         m.total_obtain_marks,
                         (SELECT result_gpa
                          FROM fn_get_result_gpa (
                                  m.total_obtain_marks,
                                  m.total_marks,
                                  (SELECT out_of
                                     FROM edu_exam_setup
                                    WHERE exam_id = e.exam_id))) result_gpa,
                         (SELECT grade_name
                          FROM fn_get_result_gpa (
                                  m.total_obtain_marks,
                                  m.total_marks,
                                  (SELECT out_of
                                     FROM edu_exam_setup
                                    WHERE exam_id = e.exam_id))) grade_name,
                         p_app_user_id,
                         current_timestamp
           FROM student_marks m
                LEFT JOIN exams e ON e.student_roll = m.student_roll;
   END LOOP;


   SELECT *
   INTO w_status, w_errm
   FROM fn_edu_result_grade_update (p_academic_year_id,
                                    p_term_id,
                                    p_class_id);

   o_status := 'S';
   o_errm := NULL;
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;
      o_status := 'E';
END;
$$;


