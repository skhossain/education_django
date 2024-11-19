from appauth.utils import fn_get_reports_parameter, fn_get_query_result
from appauth.models import Report_Table_Tabular, Report_Parameter, Query_Table
from django.db.models import FloatField, F, Func, Value, CharField, DateField
from django.db.models.functions import Cast
from finance.models import Deposit_Receive
from django.db.models.fields import IntegerField
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from decimal import Decimal
import logging
from django.utils import timezone
logger = logging.getLogger(__name__)

def fn_get_quick_collection(p_transaction_id):
    try: 
        sql = '''SELECT r.student_roll,
                        h.head_name,
                        r.receive_date,
                        r.due_date,
                        r.total_due,
                        r.total_paid,
                        r.total_waive,
                        r.total_overdue,
                        r.fine_paid,
                        r.fees_due,
                        r.fees_overdue,
                        r.fees_paid,
                        r.fees_waive,
                        r.fine_due,
                        r.fine_overdue,
                        r.fine_waive,
                        c.class_name
            FROM edu_fees_receive_student r, edu_fees_head_settings h, edu_academic_class c
            WHERE h.head_code = r.head_code 
            AND r.class_id = c.class_id
            AND r.transaction_id = ''' + "'"+p_transaction_id+"'"
            
        results = fn_get_query_result(sql)
        
        sql = '''SELECT f.receive_date, s.student_roll, s.student_name, f.receive_amount,  f.app_user_id, f.app_data_time, f.cancel_by, f.branch_code
                FROM edu_fees_receive_summary f, edu_students_info s
                WHERE f.student_roll = s.student_roll 
                AND f.transaction_id = ''' + "'"+p_transaction_id+"'"

        students = fn_get_query_result(sql)

        sql = '''
            SELECT sum (total_due) total_due,
                sum (total_paid) total_paid,
                sum (total_waive) total_waive,
                sum (total_overdue) total_overdue,
                sum (fine_paid) fine_paid,
                sum (fees_due) fees_due,
                sum (fees_overdue) fees_overdue,
                sum (fees_paid) fees_paid,
                sum (fees_waive) fees_waive,
                sum (fine_due) fine_due,
                sum (fine_overdue) fine_overdue,
                sum (fine_waive) fine_waive
            FROM (SELECT r.student_roll,
                        h.head_name,
                        r.receive_date,
                        r.total_due,
                        r.total_paid,
                        r.total_waive,
                        r.total_overdue,
                        r.fine_paid,
                        r.fees_due,
                        r.fees_overdue,
                        r.fees_paid,
                        r.fees_waive,
                        r.fine_due,
                        r.fine_overdue,
                        r.fine_waive
            FROM edu_fees_receive_student r, edu_fees_head_settings h
            Where h.head_code = r.head_code 
            and r.transaction_id =''' + "'"+p_transaction_id+"') t"
        
        sum_data = fn_get_query_result(sql)

        return results, students, sum_data
    except Exception as e:
        print(str(e))

def fn_get_studentfeescollection_details(p_app_user_id):
    try: 
        sql = '''
    SELECT student_roll,student_name,head_name,receive_date, sum (total_due) total_due,
        sum (total_paid) total_paid,
        sum (total_waive) total_waive,
        sum (total_overdue) total_overdue,
        sum (fine_paid) fine_paid,
        sum (fees_due) fees_due,
        sum (fees_overdue) fees_overdue,
        sum (fees_paid) fees_paid,
        sum (fees_waive) fees_waive,
        sum (fine_due) fine_due,
        sum (fine_overdue) fine_overdue,
        sum (fine_waive) fine_waive
    FROM (SELECT report_column1 student_roll,
                report_column2 student_name,
                report_column3 head_name,
                cast(report_column4 as date) receive_date,
                cast (report_column5 AS NUMERIC) total_due,
                cast (report_column6 AS NUMERIC) total_paid,
                cast (report_column7 AS NUMERIC) total_waive,
                cast (report_column8 AS NUMERIC) total_overdue,
                cast (report_column9 AS NUMERIC) fine_paid,
                cast (report_column10 AS NUMERIC) fees_due,
                cast (report_column11 AS NUMERIC) fees_overdue,
                cast (report_column12 AS NUMERIC) fees_paid,
                cast (report_column13 AS NUMERIC) fees_waive,
                cast (report_column14 AS NUMERIC) fine_due,
                cast (report_column15 AS NUMERIC) fine_overdue,
                cast (report_column16 AS NUMERIC) fine_waive
            FROM appauth_report_table_tabular 
            where app_user_id =''' + "'"+p_app_user_id+"') t group  by student_roll,student_name,head_name,receive_date order by cast(student_roll as bigint) ,head_name,receive_date"
  
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_studentfeescollection_summary(p_app_user_id):
    try: 
        sql = '''
    SELECT sum (total_due) total_due,
        sum (total_paid) total_paid,
        sum (total_waive) total_waive,
        sum (total_overdue) total_overdue,
        sum (fine_paid) fine_paid,
        sum (fees_due) fees_due,
        sum (fees_overdue) fees_overdue,
        sum (fees_paid) fees_paid,
        sum (fees_waive) fees_waive,
        sum (fine_due) fine_due,
        sum (fine_overdue) fine_overdue,
        sum (fine_waive) fine_waive
    FROM (SELECT cast (report_column5 AS NUMERIC) total_due,
                cast (report_column6 AS NUMERIC) total_paid,
                cast (report_column7 AS NUMERIC) total_waive,
                cast (report_column8 AS NUMERIC) total_overdue,
                cast (report_column9 AS NUMERIC) fine_paid,
                cast (report_column10 AS NUMERIC) fees_due,
                cast (report_column11 AS NUMERIC) fees_overdue,
                cast (report_column12 AS NUMERIC) fees_paid,
                cast (report_column13 AS NUMERIC) fees_waive,
                cast (report_column14 AS NUMERIC) fine_due,
                cast (report_column15 AS NUMERIC) fine_overdue,
                cast (report_column16 AS NUMERIC) fine_waive
            FROM appauth_report_table_tabular 
            where app_user_id =''' + "'"+p_app_user_id+"') t"
  
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_Month_Wise_Fess_Collection_Detais(p_app_user_id):
    try: 
        sql = '''select class_name,
       sum(CASE WHEN recive_month = 1 THEN total_paid ELSE 0 END) AS January,
       sum(CASE WHEN recive_month = 2 THEN total_paid ELSE 0 END) AS February,
       sum(CASE WHEN recive_month = 3 THEN total_paid ELSE 0 END) AS March,
       sum(CASE WHEN recive_month = 4 THEN total_paid ELSE 0 END) AS April,
       sum(CASE WHEN recive_month = 5 THEN total_paid ELSE 0 END) AS May,
       sum(CASE WHEN recive_month = 6 THEN total_paid ELSE 0 END) AS June,
       sum(CASE WHEN recive_month = 7 THEN total_paid ELSE 0 END) AS July,
       sum(CASE WHEN recive_month = 8 THEN total_paid ELSE 0 END) AS August,
       sum(CASE WHEN recive_month = 9 THEN total_paid ELSE 0 END) AS September,
       sum(CASE WHEN recive_month = 10 THEN total_paid ELSE 0 END) AS October,
       sum(CASE WHEN recive_month = 11 THEN total_paid ELSE 0 END) AS November,
       sum(CASE WHEN recive_month = 12 THEN total_paid ELSE 0 END) AS December,
       sum(total_paid) total_paid
   FROM (SELECT (SELECT a.class_name
                    FROM edu_academic_class a
                   WHERE a.class_id = P.report_column17) class_name,
                 cast (P.report_column17 AS NUMERIC),
                 cast (P.report_column18 AS NUMERIC) recive_month,
                 SUM (CAST (P.report_column6 AS NUMERIC)) total_paid
            FROM appauth_report_table_tabular P where p.app_user_id = ''' + "'"+p_app_user_id+"'" +'''
        GROUP BY P.report_column17, P.report_column18) t group by class_name''' 
  
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))        


def fn_get_Month_Wise_Fess_Collection_Summary(p_app_user_id):
    try: 
        sql = '''SELECT  
       sum(CASE WHEN recive_month = 1 THEN total_paid ELSE 0 END) AS January,
       sum(CASE WHEN recive_month = 2 THEN total_paid ELSE 0 END) AS February,
       sum(CASE WHEN recive_month = 3 THEN total_paid ELSE 0 END) AS March,
       sum(CASE WHEN recive_month = 4 THEN total_paid ELSE 0 END) AS April,
       sum(CASE WHEN recive_month = 5 THEN total_paid ELSE 0 END) AS May,
       sum(CASE WHEN recive_month = 6 THEN total_paid ELSE 0 END) AS June,
       sum(CASE WHEN recive_month = 7 THEN total_paid ELSE 0 END) AS July,
       sum(CASE WHEN recive_month = 8 THEN total_paid ELSE 0 END) AS August,
       sum(CASE WHEN recive_month = 9 THEN total_paid ELSE 0 END) AS September,
       sum(CASE WHEN recive_month = 10 THEN total_paid ELSE 0 END) AS October,
       sum(CASE WHEN recive_month = 11 THEN total_paid ELSE 0 END) AS November,
       sum(CASE WHEN recive_month = 12 THEN total_paid ELSE 0 END) AS December,
       sum(total_paid) total_paid
   FROM (SELECT (SELECT a.class_name
                    FROM edu_academic_class a
                   WHERE a.class_id = P.report_column17) class_name,
                 cast (P.report_column17 AS NUMERIC),
                 cast (P.report_column18 AS NUMERIC) recive_month,
                 SUM (CAST (P.report_column6 AS NUMERIC)) total_paid
            FROM appauth_report_table_tabular P where p.app_user_id = ''' + "'"+p_app_user_id+"'" +'''
        GROUP BY P.report_column17, P.report_column18) t''' 
  
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))    




def fn_get_class_wise_payment_status(p_app_user_id):
    try: 
        sql = '''SELECT (SELECT a.class_name
          FROM edu_academic_class a
         WHERE a.class_id = Q.class_id)
          class_name,
       Q.TOTAL_STUDENT,
       COALESCE (P.TOTAL_PAID_STUDENT, 0)
          TOTAL_PAID_STUDENT,
       (COALESCE (P.TOTAL_PAID_STUDENT, 0) * 100) / Q.TOTAL_STUDENT
          PAID_PERCENTAGE,
       Q.TOTAL_STUDENT - COALESCE (P.TOTAL_PAID_STUDENT, 0)
          TOTAL_NOT_PAID_STUDENT,
         ((Q.TOTAL_STUDENT - COALESCE (P.TOTAL_PAID_STUDENT, 0)) * 100)
       / Q.TOTAL_STUDENT
          NOT_PAID_percentage
  FROM (  SELECT S.class_id, COUNT (S.STUDENT_ROLL) TOTAL_STUDENT
            FROM edu_students_info S
        GROUP BY S.class_id
        ORDER BY S.class_id) Q
       LEFT JOIN
       (  SELECT a.report_column17, count (a.report_column1) TOTAL_PAID_STUDENT
            FROM appauth_report_table_tabular a
           WHERE  app_user_id = ''' + "'"+p_app_user_id+"'" +'''
           and a.report_column5  = a.report_column6
        GROUP BY a.report_column17
        ORDER BY a.report_column17) P
          ON P.report_column17 = Q.class_id'''

       ## print(sql)
  
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))    

def fn_edu_subjectlist_dtl(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)

        sql = ''' SELECT 
       s.subject_id,
       s.subject_name,
       c.class_name
  FROM  edu_subject_list s,edu_academic_class c
 WHERE s.class_id =  c.class_id  
  '''
        if rep_param["p_class_id"]:
            sql = sql+' and s.class_id='+"'" + \
                rep_param["p_class_id"]+"'"
        
        if rep_param["p_class_group_id"]:
            sql = sql+' and s.class_group_id='+"'" + \
                rep_param["p_class_group_id"]+"'"

        # print(sql)
        results = fn_get_query_result(sql)
        print(results)
        return results
    except Exception as e:
        print(str(e))

def fn_get_studentunpaidlist_details(p_app_user_id):
    try: 
        sql = '''  SELECT p.class_name,
         p.student_id,
         p.student_name,
         p.report_head,
         p.due_month,
         p.total_due,
         p.total_paid,
         CASE WHEN p.Unpaid < 0 THEN 0 ELSE p.unpaid END unpaid
    FROM (SELECT a.report_column2 class_name,
                 a.report_column3 Student_id,
                 a.report_column4 student_name,
                 a.report_column6 report_head,
                 cast(a.report_column7 as integer) reporting_order,
                 CASE
                    WHEN a.report_column7 = '1' THEN 'January'
                    WHEN a.report_column7 = '2' THEN 'February'
                    WHEN a.report_column7 = '3' THEN 'March'
                    WHEN a.report_column7 = '4' THEN 'April'
                    WHEN a.report_column7 = '5' THEN 'May'
                    WHEN a.report_column7 = '6' THEN 'June'
                    WHEN a.report_column7 = '7' THEN 'July'
                    WHEN a.report_column7 = '8' THEN 'August'
                    WHEN a.report_column7 = '9' THEN 'September'
                    WHEN a.report_column7 = '10' THEN 'October'
                    WHEN a.report_column7 = '11' THEN 'November'
                    WHEN a.report_column7 = '12' THEN 'December'
                    ELSE NULL
                 END due_month,
                 cast (a.report_column9 AS NUMERIC) total_due,
                 COALESCE (cast (a.report_column16 AS NUMERIC), 0) total_paid,
                   CAST (a.report_column9 AS NUMERIC)
                 - COALESCE (CAST (a.report_column16 AS NUMERIC), 0) Unpaid
            FROM appauth_report_table_tabular a
            where app_user_id =''' + "'"+p_app_user_id+"') P where unpaid>0 ORDER BY p.class_name, p.Student_id, p.student_name, p.report_head, p.reporting_order"
  
        results = fn_get_query_result(sql)
        print(results)
        return results
    except Exception as e:
        print(str(e))

def fn_get_studentunpaidlist_summary(p_app_user_id):
    try: 
        sql = '''
    SELECT sum(p.total_due) total_due,
         sum(p.total_paid) total_paid,
         sum(CASE WHEN p.Unpaid < 0 THEN 0 ELSE p.unpaid END) unpaid
    FROM (SELECT a.report_column2 class_name,
                 a.report_column3 Student_id,
                 a.report_column4 student_name,
                 a.report_column6 report_head,
                 CASE
                    WHEN a.report_column7 = '1' THEN 'January'
                    WHEN a.report_column7 = '2' THEN 'February'
                    WHEN a.report_column7 = '3' THEN 'March'
                    WHEN a.report_column7 = '4' THEN 'April'
                    WHEN a.report_column7 = '5' THEN 'May'
                    WHEN a.report_column7 = '6' THEN 'June'
                    WHEN a.report_column7 = '7' THEN 'July'
                    WHEN a.report_column7 = '8' THEN 'August'
                    WHEN a.report_column7 = '9' THEN 'September'
                    WHEN a.report_column7 = '10' THEN 'October'
                    WHEN a.report_column7 = '11' THEN 'November'
                    WHEN a.report_column7 = '12' THEN 'December'
                    ELSE NULL
                 END due_month,
                 cast (a.report_column9 AS NUMERIC) total_due,
                 COALESCE (cast (a.report_column16 AS NUMERIC), 0) total_paid,
                   CAST (a.report_column9 AS NUMERIC)
                 - COALESCE (CAST (a.report_column16 AS NUMERIC), 0) Unpaid
            FROM appauth_report_table_tabular a
            where app_user_id =''' + "'"+p_app_user_id+"') P where unpaid>0 "
  
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))



def fn_get_class_wise_unpaidlist_details(p_app_user_id):
    try: 
        sql = '''  SELECT p.class_name,
       p.report_head,
       p.due_month,
       sum(p.total_due) total_due,
        sum(p.total_paid) total_paid,
        sum(CASE WHEN p.Unpaid < 0 THEN 0 ELSE p.Unpaid END) Unpaid
  FROM (SELECT a.report_column2 class_name,
               a.report_column3 Student_id,
               a.report_column4 student_name,
               a.report_column6 report_head,
               a.report_column7 reporting_order,
               CASE
                  WHEN a.report_column7 = '1' THEN 'January'
                  WHEN a.report_column7 = '2' THEN 'February'
                  WHEN a.report_column7 = '3' THEN 'March'
                  WHEN a.report_column7 = '4' THEN 'April'
                  WHEN a.report_column7 = '5' THEN 'May'
                  WHEN a.report_column7 = '6' THEN 'June'
                  WHEN a.report_column7 = '7' THEN 'July'
                  WHEN a.report_column7 = '8' THEN 'August'
                  WHEN a.report_column7 = '9' THEN 'September'
                  WHEN a.report_column7 = '10' THEN 'October'
                  WHEN a.report_column7 = '11' THEN 'November'
                  WHEN a.report_column7 = '12' THEN 'December'
                  ELSE NULL
               END due_month,
               cast (a.report_column9 AS NUMERIC) total_due,
               COALESCE (cast (a.report_column16 AS NUMERIC),0) total_paid,
                 CAST (a.report_column9 AS NUMERIC)
               - COALESCE (CAST (a.report_column16 AS NUMERIC), 0) Unpaid
          FROM appauth_report_table_tabular a
            where app_user_id =''' + "'"+p_app_user_id+"') P group by p.class_name, p.report_head,p.due_month,p.reporting_order order by p.class_name,p.report_head,p.reporting_order"
  
        results = fn_get_query_result(sql)
        print(results)
        return results
    except Exception as e:
        print(str(e))


def fn_get_class_wise_unpaidlist_summary(p_app_user_id):
    try: 
        sql = '''  SELECT 
       sum(p.total_due) total_due,
        sum(p.total_paid) total_paid,
        sum(CASE WHEN p.Unpaid < 0 THEN 0 ELSE p.Unpaid END) Unpaid
  FROM (SELECT a.report_column2 class_name,
               a.report_column3 Student_id,
               a.report_column4 student_name,
               a.report_column6 report_head,
               a.report_column7 reporting_order,
               CASE
                  WHEN a.report_column7 = '1' THEN 'January'
                  WHEN a.report_column7 = '2' THEN 'February'
                  WHEN a.report_column7 = '3' THEN 'March'
                  WHEN a.report_column7 = '4' THEN 'April'
                  WHEN a.report_column7 = '5' THEN 'May'
                  WHEN a.report_column7 = '6' THEN 'June'
                  WHEN a.report_column7 = '7' THEN 'July'
                  WHEN a.report_column7 = '8' THEN 'August'
                  WHEN a.report_column7 = '9' THEN 'September'
                  WHEN a.report_column7 = '10' THEN 'October'
                  WHEN a.report_column7 = '11' THEN 'November'
                  WHEN a.report_column7 = '12' THEN 'December'
                  ELSE NULL
               END due_month,
               cast (a.report_column9 AS NUMERIC) total_due,
               COALESCE (cast (a.report_column16 AS NUMERIC),0) total_paid,
                 CAST (a.report_column9 AS NUMERIC)
               - COALESCE (CAST (a.report_column16 AS NUMERIC), 0) Unpaid
          FROM appauth_report_table_tabular a
            where app_user_id =''' + "'"+p_app_user_id+"') P "
  
        results = fn_get_query_result(sql)
        print(results)
        return results
    except Exception as e:
        print(str(e))        





def fn_get_monthly_unpaidlist_details(p_app_user_id):
    try: 
        sql = '''  SELECT p.class_name,
         sum (CASE WHEN due_month = 1 THEN Unpaid_s ELSE 0 END) AS january,
         sum (CASE WHEN due_month = 2 THEN Unpaid_s ELSE 0 END) AS february,
         sum (CASE WHEN due_month = 3 THEN Unpaid_s ELSE 0 END) AS march,
         sum (CASE WHEN due_month = 4 THEN Unpaid_s ELSE 0 END) AS april,
         sum (CASE WHEN due_month = 5 THEN Unpaid_s ELSE 0 END) AS may,
         sum (CASE WHEN due_month = 6 THEN Unpaid_s ELSE 0 END) AS june,
         sum (CASE WHEN due_month = 7 THEN Unpaid_s ELSE 0 END) AS july,
         sum (CASE WHEN due_month = 8 THEN Unpaid_s ELSE 0 END) AS august,
         sum (CASE WHEN due_month = 9 THEN Unpaid_s ELSE 0 END) AS september,
         sum (CASE WHEN due_month = 10 THEN Unpaid_s ELSE 0 END) AS october,
         sum (CASE WHEN due_month = 11 THEN Unpaid_s ELSE 0 END) AS november,
         sum (CASE WHEN due_month = 12 THEN Unpaid_s ELSE 0 END) AS december,
         sum(Unpaid_s) total
    FROM (  SELECT s.class_name,
                   s.due_month,
                   sum (CASE WHEN s.Unpaid < 0 THEN 0 ELSE s.Unpaid END) Unpaid_s
              FROM (SELECT a.report_column2 class_name,
                           CAST (a.report_column7 AS NUMERIC) due_month,
                           ((  CAST (a.report_column9 AS NUMERIC)
                             - COALESCE (CAST (a.report_column16 AS NUMERIC), 0))) Unpaid
                      FROM appauth_report_table_tabular  a
            where app_user_id =''' + "'"+p_app_user_id+"') s GROUP BY s.class_name, s.due_month) p GROUP BY p.class_name"
  
        results = fn_get_query_result(sql)
        print(results)
        return results
    except Exception as e:
        print(str(e))


def fn_get_monthly_unpaidlist_summary(p_app_user_id):
    try: 
        sql = '''  SELECT
         sum (CASE WHEN due_month = 1 THEN Unpaid_s ELSE 0 END) AS january,
         sum (CASE WHEN due_month = 2 THEN Unpaid_s ELSE 0 END) AS february,
         sum (CASE WHEN due_month = 3 THEN Unpaid_s ELSE 0 END) AS march,
         sum (CASE WHEN due_month = 4 THEN Unpaid_s ELSE 0 END) AS april,
         sum (CASE WHEN due_month = 5 THEN Unpaid_s ELSE 0 END) AS may,
         sum (CASE WHEN due_month = 6 THEN Unpaid_s ELSE 0 END) AS june,
         sum (CASE WHEN due_month = 7 THEN Unpaid_s ELSE 0 END) AS july,
         sum (CASE WHEN due_month = 8 THEN Unpaid_s ELSE 0 END) AS august,
         sum (CASE WHEN due_month = 9 THEN Unpaid_s ELSE 0 END) AS september,
         sum (CASE WHEN due_month = 10 THEN Unpaid_s ELSE 0 END) AS october,
         sum (CASE WHEN due_month = 11 THEN Unpaid_s ELSE 0 END) AS november,
         sum (CASE WHEN due_month = 12 THEN Unpaid_s ELSE 0 END) AS december,
         sum(Unpaid_s) total
    FROM (  SELECT s.class_name,
                   s.due_month,
                   sum (CASE WHEN s.Unpaid < 0 THEN 0 ELSE s.Unpaid END) Unpaid_s
              FROM (SELECT a.report_column2 class_name,
                           CAST (a.report_column7 AS NUMERIC) due_month,
                           ((  CAST (a.report_column9 AS NUMERIC)
                             - COALESCE (CAST (a.report_column16 AS NUMERIC), 0))) Unpaid
                      FROM appauth_report_table_tabular  a
            where app_user_id =''' + "'"+p_app_user_id+"') s GROUP BY s.class_name, s.due_month) p "
  
        results = fn_get_query_result(sql)
        print(results)
        return results
    except Exception as e:
        print(str(e))