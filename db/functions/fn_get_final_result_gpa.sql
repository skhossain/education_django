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


