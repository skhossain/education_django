-- ----------------------------------------------------------------
--  FUNCTION fn_exam_mark_publish
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_exam_mark_publish (
   IN      p_academic_year_id   INTEGER,
   IN      p_term_id            INTEGER,
   IN      p_class_id           CHARACTER,
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
   w_single_result    RECORD;
BEGIN
   FOR w_students
      IN (SELECT student_roll
           FROM edu_students_info s
          WHERE     s.academic_year = p_academic_year_id
                AND s.class_id = p_class_id)
   LOOP
      FOR w_subjects IN (SELECT subject_id
                           FROM edu_subject_list sub
                          WHERE sub.class_id = p_class_id)
      LOOP
         SELECT *
           INTO w_subject_result
           FROM fn_set_subject_mark_by_student (p_academic_year_id,
                                                p_term_id,
                                                p_class_id,
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
                                        p_app_user_id);

   SELECT *
     INTO w_single_result
     FROM fn_store_single_exam_mark (p_academic_year_id,
                                     p_term_id,
                                     p_class_id,
                                     p_app_user_id);

   o_status := 'S';
EXCEPTION
   WHEN OTHERS
   THEN
      o_errm := SQLERRM;
      o_status := 'E';
END;
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_final_result_gpa
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_get_final_result_gpa (
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
   w_total_mark          NUMERIC := 0.00;
   w_total_grade_point   NUMERIC := 0.00;
   w_obtain_mark         NUMERIC := 0.00;
   w_out_of              NUMERIC := 0.00;
   w_credit              NUMERIC := 0.00;
   w_total_subjects      NUMERIC := 0;
   w_final_grade_name    CHARACTER VARYING (200);
   w_grade_point_s       NUMERIC := 0;
   w_subjects            RECORD;
   w_subject_mark_info   RECORD;
   w_grades              RECORD;
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
                       AND e.term_id = p_term_id)
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
         w_total_grade_point := 0;
         EXIT;
      END IF;

      w_credit := w_credit + w_subjects.credit;
      w_total_mark := w_total_mark + w_subject_mark_info.o_total_mark;
      w_total_grade_point :=
         w_total_grade_point + w_subject_mark_info.o_grade_point;
      w_obtain_mark :=
         w_obtain_mark + w_subject_mark_info.o_total_obtain_mark;
      w_total_subjects := w_total_subjects + 1;
   END LOOP;

   IF w_out_of = 5
   THEN
      result_gpa :=
         CAST ((w_total_grade_point / w_total_subjects) AS decimal (10, 2));
   ELSEIF w_out_of = 4
   THEN
      result_gpa :=
         CAST ((w_total_grade_point / w_credit) AS decimal (10, 2));
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

CREATE OR REPLACE FUNCTION fn_get_grade_nameby_point (
   IN      p_point      NUMERIC,
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
   w_grades             RECORD;
   w_grade_point_s      NUMERIC := 0;
   w_final_grade_name   CHARACTER VARYING (200);
BEGIN
   FOR w_grades IN (SELECT *
                      FROM edu_result_grade e
                     WHERE e.out_of = p_out_of)
   LOOP
      IF w_grades.result_gpa <= p_point
      THEN
         IF w_grades.result_gpa >= w_grade_point_s
         THEN
            w_grade_point_s := w_grades.result_gpa;
            w_final_grade_name := w_grades.grade_name;
         END IF;
      END IF;
   END LOOP;

   grade_name := w_final_grade_name;
END
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_inventory_number
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_get_inventory_number (
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
       WHERE s.inv_code = p_inv_code AND s.branch_code = p_branch_code;

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
         w_inv_prefix := P_inv_prefix;
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
--  FUNCTION fn_get_result_gpa
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_get_result_gpa (
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
    WHERE     g.out_of = p_out_of
          AND w_obtain_mark_prsent BETWEEN g.lowest_mark AND g.highest_mark;

   grade_name := w_grade_name;
   result_gpa := w_result_gpa;
END
$$;


-- ----------------------------------------------------------------
--  FUNCTION fn_get_student_subject_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_get_student_subject_mark (
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
--  FUNCTION fn_onlineexam_live
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_onlineexam_live (
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
--  FUNCTION fn_set_final_exam_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_set_final_exam_mark (
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

   INSERT INTO edu_exam_marks_final (academic_year,
                                     term_id,
                                     class_id,
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


