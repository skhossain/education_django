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
       OUT o_student_marks      CHARACTER,
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
BEGIN
   --    TRUNCATE TABLE edu_subjectmarktemp;

   DELETE FROM edu_subjectmarktemp
         WHERE app_user_id = p_app_user_id;


   IF p_class_group_id IS NULL
   THEN
      FOR w_all_subject IN (SELECT subject_id
                              FROM edu_subject_list
                             WHERE class_id = p_class_id)
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
            SELECT DISTINCT
                   (e.student_roll),
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
                              WHERE exam_id = e.exam_id)))
                      result_gpa,
                   (SELECT grade_name
                      FROM fn_get_result_gpa (m.total_obtain_marks,
                                              m.total_marks,
                                              (SELECT out_of
                                                 FROM edu_exam_setup
                                                WHERE exam_id = e.exam_id)))
                      grade_name,
                   p_app_user_id,
                   current_timestamp
              FROM student_marks m
                   LEFT JOIN exams e ON e.student_roll = m.student_roll;
      END LOOP;
   ELSE
      FOR w_all_subject
         IN (SELECT subject_id
              FROM edu_subject_list
             WHERE     class_id = p_class_id
                   AND class_group_id = p_class_group_id)
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
            SELECT DISTINCT
                   (e.student_roll),
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
                              WHERE exam_id = e.exam_id)))
                      result_gpa,
                   (SELECT grade_name
                      FROM fn_get_result_gpa (m.total_obtain_marks,
                                              m.total_marks,
                                              (SELECT out_of
                                                 FROM edu_exam_setup
                                                WHERE exam_id = e.exam_id)))
                      grade_name,
                   p_app_user_id,
                   current_timestamp
              FROM student_marks m
                   LEFT JOIN exams e ON e.student_roll = m.student_roll;
      END LOOP;
   END IF;
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
--  FUNCTION fn_set_single_exam_mark
-- ----------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.fn_set_single_exam_mark (
   IN      p_academic_year_id   INTEGER,
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
               AND r.class_id = p_class_id
               AND r.subject_id = p_subject_id
               AND r.exam_id = w_exam.exam_id
               AND r.student_roll = p_student_roll;
      ELSE
         SELECT sum (obtain_marks)
          INTO w_obtain_mark
          FROM edu_exam_marks_details r
         WHERE     r.academic_year = p_academic_year_id
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
                                              app_data_time)
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
                         current_timestamp);
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


