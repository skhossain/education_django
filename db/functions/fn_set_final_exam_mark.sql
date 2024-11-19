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


