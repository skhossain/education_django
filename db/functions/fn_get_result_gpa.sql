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


