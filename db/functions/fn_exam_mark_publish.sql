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


