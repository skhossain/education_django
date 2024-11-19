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


