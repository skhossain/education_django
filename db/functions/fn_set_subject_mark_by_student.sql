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


