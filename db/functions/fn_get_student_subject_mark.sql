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


