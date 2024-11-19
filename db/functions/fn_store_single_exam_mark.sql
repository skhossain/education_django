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


