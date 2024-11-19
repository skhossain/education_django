from django.db.models.fields import IntegerField
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
logger = logging.getLogger(__name__)
from django.db.models.functions import Cast
from django.db.models import FloatField, F, Func, Value, CharField, DateField

from finance.models import *
from appauth.models import Report_Table_Tabular, Report_Parameter, Query_Table
from appauth.utils import fn_get_reports_parameter, fn_get_query_result
from finance.utils import fn_get_accountinfo_byacnumber

def fn_get_acstat_details(p_app_user_id):
    try:
        row = Query_Table.objects.filter(app_user_id=p_app_user_id).values(row_serial=F("chr_column1"),
                                                                           tran_details=F("chr_column2"), credit_amount=F("dec_column1"), debit_amount=F("dec_column2"),
                                                                           tran_balance=F("dec_column3"), tran_date=Func(F('dat_column1'), Value('MM/DD/YYYY'), function='to_char',
                                                                                                                         output_field=CharField()
                                                                                                                         ))
        return row
    except Exception as e:
        logger.error("Error in fn_get_acstat_details on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(str(e))))
        pass


def fn_get_acstat_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Query_Table.objects.filter(
            app_user_id=p_app_user_id).aggregate(Sum('dec_column1'), Sum('dec_column2'))
        data['total_credit_amount'] = stock_summary['dec_column1__sum']
        data['total_debit_amount'] = stock_summary['dec_column2__sum']

        accounts = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_account_number', report_name='finance_account_statements')
        account_number = accounts.parameter_values

        account_number, client_id, account_type, account_title, account_address, account_balance, credit_limit = fn_get_accountinfo_byacnumber(
            account_number)
        data['account_balance'] = account_balance
        data['account_title'] = account_title
        data['account_address'] = account_address
        return data
    except Exception as e:
        logger.error("Error in fn_get_acstat_summary on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(str(e))))
        return data


def fn_get_receipt_payment_data(p_app_user_id):
    try:
        sql = '''WITH
   receipt_details
   AS
      (SELECT cast (report_column1 AS INTEGER) receipt_serial_number,
              report_column2 receipt_gl_name,
              report_column3 receipt_gl_level_class,
              cast (report_column4 AS NUMERIC) ason_credit_sum,
              cast (report_column5 AS NUMERIC) asof_credit_sum,
              cast (report_column6 AS NUMERIC) this_month_credit_sum,
              cast (report_column7 AS NUMERIC) this_year_credit_sum
         FROM appauth_report_table_tabular
        WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('O', 'R')),
   payment_details
   AS
      (SELECT cast (report_column1 AS INTEGER) payment_serial_number,
              report_column2 payment_gl_name,
              report_column3 payment_gl_level_class,
              cast (report_column4 AS NUMERIC) ason_debit_sum,
              cast (report_column5 AS NUMERIC) asof_debit_sum,
              cast (report_column6 AS NUMERIC) this_month_debit_sum,
              cast (report_column7 AS NUMERIC) this_year_debit_sum
         FROM appauth_report_table_tabular
        WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('C', 'P'))
  SELECT receipt_serial_number,
         receipt_gl_name,
         COALESCE (receipt_gl_level_class,payment_gl_level_class) receipt_gl_level_class,
         ason_credit_sum,
         asof_credit_sum,
         this_month_credit_sum,
         this_year_credit_sum,
         payment_serial_number,
         payment_gl_name,
         COALESCE (payment_gl_level_class, receipt_gl_level_class) payment_gl_level_class,
         ason_debit_sum,
         asof_debit_sum,
         this_month_debit_sum,
         this_year_debit_sum
    FROM receipt_details r
         FULL OUTER JOIN payment_details p
            ON (r.receipt_serial_number = p.payment_serial_number)
ORDER BY receipt_serial_number, payment_serial_number'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_receipt_payment_sum(p_app_user_id):
    try:
        sql = '''WITH
   total_receipt
   AS
      (  SELECT 1  sl,
                sum (cast (report_column4 AS NUMERIC)) ason_credit_sum,
                sum (cast (report_column5 AS NUMERIC)) asof_credit_sum,
                sum (cast (report_column6 AS NUMERIC)) this_month_credit_sum,
                sum (cast (report_column7 AS NUMERIC)) this_year_credit_sum
           FROM appauth_report_table_tabular
          WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('R') and report_column9='true'
       GROUP BY 1),
   total_payment
   AS
      (  SELECT 1  sl,
                sum (cast (report_column4 AS NUMERIC)) ason_debit_sum,
                sum (cast (report_column5 AS NUMERIC)) asof_debit_sum,
                sum (cast (report_column6 AS NUMERIC)) this_month_debit_sum,
                sum (cast (report_column7 AS NUMERIC)) this_year_debit_sum
           FROM appauth_report_table_tabular
          WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('P') and report_column9='true'
       GROUP BY 1)
SELECT ason_credit_sum total_ason_credit_sum,
       asof_credit_sum total_asof_credit_sum,
       this_month_credit_sum total_this_month_credit_sum,
       this_year_credit_sum total_this_year_credit_sum,
       ason_debit_sum total_ason_debit_sum,
       asof_debit_sum total_asof_debit_sum,
       this_month_debit_sum total_this_month_debit_sum,
       this_year_debit_sum total_this_year_debit_sum
  FROM total_receipt r FULL OUTER JOIN total_payment p ON (r.sl = p.sl)'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_receipt_payment_data_two(p_app_user_id):
    try:
        sql = '''WITH
   receipt_details
   AS
      (SELECT cast (report_column1 AS INTEGER) receipt_serial_number,
              report_column2 receipt_gl_name,
              report_column3 receipt_gl_level_class,
              cast (report_column4 AS NUMERIC) ason_credit_sum,
              cast (report_column5 AS NUMERIC) asof_credit_sum,
              cast (report_column6 AS NUMERIC) this_month_credit_sum,
              cast (report_column7 AS NUMERIC) this_year_credit_sum
         FROM appauth_report_table_tabular
        WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('O', 'R')),
   payment_details
   AS
      (SELECT cast (report_column1 AS INTEGER) payment_serial_number,
              report_column2 payment_gl_name,
              report_column3 payment_gl_level_class,
              cast (report_column4 AS NUMERIC) ason_debit_sum,
              cast (report_column5 AS NUMERIC) asof_debit_sum,
              cast (report_column6 AS NUMERIC) this_month_debit_sum,
              cast (report_column7 AS NUMERIC) this_year_debit_sum
         FROM appauth_report_table_tabular
        WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('C', 'P'))
  SELECT receipt_serial_number,
         receipt_gl_name,
         COALESCE (receipt_gl_level_class,payment_gl_level_class) receipt_gl_level_class,
         ason_credit_sum,
         asof_credit_sum,
         this_month_credit_sum,
         this_year_credit_sum,
         payment_serial_number,
         payment_gl_name,
         COALESCE (payment_gl_level_class, receipt_gl_level_class) payment_gl_level_class,
         ason_debit_sum,
         asof_debit_sum,
         this_month_debit_sum,
         this_year_debit_sum
    FROM receipt_details r
         FULL OUTER JOIN payment_details p
            ON (r.receipt_serial_number = p.payment_serial_number)
ORDER BY receipt_serial_number, payment_serial_number'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_receipt_payment_sum_two(p_app_user_id):
    try:
        sql = '''WITH
   total_receipt
   AS
      (  SELECT 1  sl,
                sum (cast (report_column4 AS NUMERIC)) ason_credit_sum,
                sum (cast (report_column5 AS NUMERIC)) asof_credit_sum,
                sum (cast (report_column6 AS NUMERIC)) this_month_credit_sum,
                sum (cast (report_column7 AS NUMERIC)) this_year_credit_sum
           FROM appauth_report_table_tabular
          WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('R') and report_column9='true'
       GROUP BY 1),
   total_payment
   AS
      (  SELECT 1  sl,
                sum (cast (report_column4 AS NUMERIC)) ason_debit_sum,
                sum (cast (report_column5 AS NUMERIC)) asof_debit_sum,
                sum (cast (report_column6 AS NUMERIC)) this_month_debit_sum,
                sum (cast (report_column7 AS NUMERIC)) this_year_debit_sum
           FROM appauth_report_table_tabular
          WHERE app_user_id = '''+"'"+p_app_user_id+"'"+''' AND report_column8 IN ('P') and report_column9='true'
       GROUP BY 1)
SELECT ason_credit_sum total_ason_credit_sum,
       asof_credit_sum total_asof_credit_sum,
       this_month_credit_sum total_this_month_credit_sum,
       this_year_credit_sum total_this_year_credit_sum,
       ason_debit_sum total_ason_debit_sum,
       asof_debit_sum total_asof_debit_sum,
       this_month_debit_sum total_this_month_debit_sum,
       this_year_debit_sum total_this_year_debit_sum
  FROM total_receipt r FULL OUTER JOIN total_payment p ON (r.sl = p.sl)'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_trialbalance_details(p_app_user_id):
    try:
        sql = '''SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) serial_number,
       p.gl_code,
       p.gl_name,
       p.gl_level_class,
       ason_credit_sum opening_credit_sum,
       ason_debit_sum opening_debit_sum,
       this_period_credit_sum,
       this_period_debit_sum,
       asof_credit_sum closing_credit_sum,
       asof_debit_sum closing_debit_sum
  FROM finance_ledger_report_balance b, finance_ledger_report_param p
 WHERE b.gl_code = p.gl_code AND p.app_user_id='''+"'"+p_app_user_id+"'"+''' AND b.app_user_id = p.app_user_id'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_trialbalancetab_details(p_app_user_id):
    try:
        sql = '''SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) serial_number,
       p.gl_code,
       p.gl_name,
       p.gl_level_class,
       ason_credit_sum opening_credit_sum,
       ason_debit_sum opening_debit_sum,
       this_period_credit_sum,
       this_period_debit_sum,
       asof_credit_sum closing_credit_sum,
       asof_debit_sum closing_debit_sum
  FROM finance_ledger_report_balance b, finance_ledger_report_param p
 WHERE b.gl_code = p.gl_code AND p.app_user_id='''+"'"+p_app_user_id+"'"+''' 
 AND (this_period_credit_sum>0.00 or this_period_debit_sum>0.00)
 AND b.app_user_id = p.app_user_id'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_assetliabilities_details(p_app_user_id):
    try:
        sql = '''WITH
   asset_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) asset_serial_number,
                p.gl_code asset_gl_code,
                p.gl_name asset_gl_name,
                p.is_leaf_node asset_is_leaf_node,
                p.gl_level_class asset_gl_level_class,
                ason_gl_balance asset_ason_gl_balance,
                asof_gl_balance asset_asof_gl_balance,
                this_month_gl_balance asset_this_month_gl_balance,
                past_month_gl_balance asset_past_month_gl_balance,
                past_year_gl_balance asset_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND assets_gl
                AND (ason_gl_balance>0.00 OR asof_gl_balance>0.00 OR this_month_gl_balance>0.00 OR past_month_gl_balance>0.00 
                OR past_year_gl_balance>0.00)
       ORDER BY p.reporting_gl_serial),
   liability_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial)
                   liability_serial_number,
                p.gl_code liability_gl_code,
                p.gl_name liability_gl_name,
                p.is_leaf_node liability_is_leaf_node,
                p.gl_level_class liability_gl_level_class,
                ason_gl_balance liability_ason_gl_balance,
                asof_gl_balance liability_asof_gl_balance,
                this_month_gl_balance liability_this_month_gl_balance,
                past_month_gl_balance liability_past_month_gl_balance,
                past_year_gl_balance liability_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND liabilities_gl
                AND (ason_gl_balance>0.00 OR asof_gl_balance>0.00 OR this_month_gl_balance>0.00 OR past_month_gl_balance>0.00 
                OR past_year_gl_balance>0.00)
       ORDER BY p.reporting_gl_serial)
  SELECT asset_gl_name,
         COALESCE (asset_gl_level_class, liability_gl_level_class)
            asset_gl_level_class,
         asset_ason_gl_balance,
         asset_asof_gl_balance,
         asset_this_month_gl_balance,
         asset_past_month_gl_balance,
         asset_past_year_gl_balance,
         liability_gl_name,
         COALESCE (liability_gl_level_class, asset_gl_level_class)
            liability_gl_level_class,
         liability_ason_gl_balance,
         liability_asof_gl_balance,
         liability_this_month_gl_balance,
         liability_past_month_gl_balance,
         liability_past_year_gl_balance
    FROM asset_detail r
         FULL OUTER JOIN liability_detail p
            ON (r.asset_serial_number = p.liability_serial_number)
ORDER BY r.asset_serial_number, p.liability_serial_number'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_assetliabilitiestab_details(p_app_user_id):
    try:
        sql = '''WITH
   asset_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) asset_serial_number,
                p.gl_code asset_gl_code,
                p.gl_name asset_gl_name,
                p.is_leaf_node asset_is_leaf_node,
                p.gl_level_class asset_gl_level_class,
                ason_gl_balance asset_ason_gl_balance,
                asof_gl_balance asset_asof_gl_balance,
                this_month_gl_balance asset_this_month_gl_balance,
                past_month_gl_balance asset_past_month_gl_balance,
                past_year_gl_balance asset_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id
                AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND assets_gl
       ORDER BY p.reporting_gl_serial),
   liability_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial)
                   liability_serial_number,
                p.gl_code
                   liability_gl_code,
                p.gl_name
                   liability_gl_name,
                p.is_leaf_node
                   liability_is_leaf_node,
                p.gl_level_class
                   liability_gl_level_class,
                ason_gl_balance
                   liability_ason_gl_balance,
                asof_gl_balance
                   liability_asof_gl_balance,
                this_month_gl_balance
                   liability_this_month_gl_balance,
                past_month_gl_balance
                   liability_past_month_gl_balance,
                past_year_gl_balance
                   liability_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id
                AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND liabilities_gl
       ORDER BY p.reporting_gl_serial)
SELECT asset_gl_code gl_code,
       asset_gl_name gl_name,
       COALESCE (asset_gl_level_class) gl_level_class,
       asset_ason_gl_balance ason_gl_balance,
       asset_asof_gl_balance asof_gl_balance,
       asset_this_month_gl_balance this_month_gl_balance,
       asset_past_month_gl_balance past_month_gl_balance,
       asset_past_year_gl_balance past_year_gl_balance
  FROM asset_detail r
 WHERE    asset_ason_gl_balance > 0
       OR asset_asof_gl_balance > 0
       OR asset_this_month_gl_balance > 0
       OR asset_past_month_gl_balance > 0
       OR asset_past_year_gl_balance > 0
UNION ALL
SELECT liability_gl_code gl_code,
       liability_gl_name gl_name,
       COALESCE (liability_gl_level_class) gl_level_class,
       liability_ason_gl_balance ason_gl_balance,
       liability_asof_gl_balance asof_gl_balance,
       liability_this_month_gl_balance this_month_gl_balance,
       liability_past_month_gl_balance past_month_gl_balance,
       liability_past_year_gl_balance past_year_gl_balance
  FROM liability_detail p
 WHERE    liability_ason_gl_balance > 0
       OR liability_asof_gl_balance > 0
       OR liability_this_month_gl_balance > 0
       OR liability_past_month_gl_balance > 0
       OR liability_past_year_gl_balance > 0'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_incomeexpenses_details(p_app_user_id):
    try:
        sql = '''WITH
   income_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) income_serial_number,
                p.gl_code income_gl_code,
                p.gl_name income_gl_name,
                p.is_leaf_node income_is_leaf_node,
                p.gl_level_class income_gl_level_class,
                ason_gl_balance income_ason_gl_balance,
                asof_gl_balance income_asof_gl_balance,
                this_month_gl_balance income_this_month_gl_balance,
                past_month_gl_balance income_past_month_gl_balance,
                past_year_gl_balance income_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND income_gl
                AND (ason_gl_balance>0.00 OR asof_gl_balance>0.00 OR this_month_gl_balance>0.00 OR past_month_gl_balance>0.00 
                OR past_year_gl_balance>0.00)
       ORDER BY p.reporting_gl_serial),
   expense_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial)
                   expense_serial_number,
                p.gl_code expense_gl_code,
                p.gl_name expense_gl_name,
                p.is_leaf_node expense_is_leaf_node,
                p.gl_level_class expense_gl_level_class,
                ason_gl_balance expense_ason_gl_balance,
                asof_gl_balance expense_asof_gl_balance,
                this_month_gl_balance expense_this_month_gl_balance,
                past_month_gl_balance expense_past_month_gl_balance,
                past_year_gl_balance expense_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND expense_gl
                AND (ason_gl_balance>0.00 OR asof_gl_balance>0.00 OR this_month_gl_balance>0.00 OR past_month_gl_balance>0.00 
                OR past_year_gl_balance>0.00)
       ORDER BY p.reporting_gl_serial)
  SELECT income_gl_name,
         COALESCE (income_gl_level_class, expense_gl_level_class)
            income_gl_level_class,
         income_ason_gl_balance,
         income_asof_gl_balance,
         income_this_month_gl_balance,
         income_past_month_gl_balance,
         income_past_year_gl_balance,
         expense_gl_name,
         COALESCE (expense_gl_level_class, income_gl_level_class)
            expense_gl_level_class,
         expense_ason_gl_balance,
         expense_asof_gl_balance,
         expense_this_month_gl_balance,
         expense_past_month_gl_balance,
         expense_past_year_gl_balance
    FROM income_detail r
         FULL OUTER JOIN expense_detail p
            ON (r.income_serial_number = p.expense_serial_number)
ORDER BY r.income_serial_number, p.expense_serial_number'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_incomeexpenses_summary(p_app_user_id):
    try:
        sql = '''WITH
   income_balance
   AS
      (SELECT ason_gl_balance income_ason_gl_balance,
              asof_gl_balance income_asof_gl_balance,
              this_month_gl_balance income_this_month_gl_balance,
              past_month_gl_balance income_past_month_gl_balance,
              past_year_gl_balance income_past_year_gl_balance
         FROM finance_ledger_report_balance
        WHERE     app_user_id = '''+"'"+p_app_user_id+"'"+'''
              AND gl_code =
                  (SELECT income_main_gl FROM finance_application_settings)),
   expences_balance
   AS
      (SELECT ason_gl_balance expense_ason_gl_balance,
              asof_gl_balance expense_asof_gl_balance,
              this_month_gl_balance expense_this_month_gl_balance,
              past_month_gl_balance expense_past_month_gl_balance,
              past_year_gl_balance expense_past_year_gl_balance
         FROM finance_ledger_report_balance
        WHERE     app_user_id = '''+"'"+p_app_user_id+"'"+'''
              AND gl_code =
                  (SELECT expenses_main_gl FROM finance_application_settings)),
   profit_loss_balance
   AS
      (SELECT income_ason_gl_balance - expense_ason_gl_balance
                 ason_gl_balance,
              income_asof_gl_balance - expense_asof_gl_balance
                 asof_gl_balance,
              income_this_month_gl_balance - expense_this_month_gl_balance
                 this_month_gl_balance,
              income_past_month_gl_balance - expense_past_month_gl_balance
                 past_month_gl_balance,
              income_past_year_gl_balance - expense_past_year_gl_balance
                 past_year_gl_balance
         FROM income_balance, expences_balance)
SELECT (CASE WHEN ason_gl_balance > 0 THEN ason_gl_balance ELSE 0 END)
          profit_ason_gl_balance,
       (CASE WHEN asof_gl_balance > 0 THEN asof_gl_balance ELSE 0 END)
          profit_asof_gl_balance,
       (CASE
           WHEN this_month_gl_balance > 0 THEN this_month_gl_balance
           ELSE 0
        END)
          profit_this_month_gl_balance,
       (CASE
           WHEN past_month_gl_balance > 0 THEN past_month_gl_balance
           ELSE 0
        END)
          profit_past_month_gl_balance,
       (CASE
           WHEN past_year_gl_balance > 0 THEN past_year_gl_balance
           ELSE 0
        END)
          profit_past_year_gl_balance,
       (CASE WHEN ason_gl_balance < 0 THEN abs (ason_gl_balance) ELSE 0 END)
          loss_ason_gl_balance,
       (CASE WHEN asof_gl_balance < 0 THEN abs (asof_gl_balance) ELSE 0 END)
          loss_asof_gl_balance,
       (CASE
           WHEN this_month_gl_balance < 0 THEN abs (this_month_gl_balance)
           ELSE 0
        END)
          loss_this_month_gl_balance,
       (CASE
           WHEN past_month_gl_balance < 0 THEN abs (past_month_gl_balance)
           ELSE 0
        END)
          loss_past_month_gl_balance,
       (CASE
           WHEN past_year_gl_balance < 0 THEN abs (past_year_gl_balance)
           ELSE 0
        END)
          loss_past_year_gl_balance
  FROM profit_loss_balance'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_incomeexpensestab_details(p_app_user_id):
    try:
        sql = '''WITH
   income_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) income_serial_number,
                p.gl_code income_gl_code,
                p.gl_name income_gl_name,
                p.is_leaf_node income_is_leaf_node,
                p.gl_level_class income_gl_level_class,
                ason_gl_balance income_ason_gl_balance,
                asof_gl_balance income_asof_gl_balance,
                this_month_gl_balance income_this_month_gl_balance,
                past_month_gl_balance income_past_month_gl_balance,
                past_year_gl_balance income_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id
                AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND income_gl
       ORDER BY p.reporting_gl_serial),
   expense_detail
   AS
      (  SELECT row_number () OVER (ORDER BY p.reporting_gl_serial) expense_serial_number,
                p.gl_code expense_gl_code,
                p.gl_name expense_gl_name,
                p.is_leaf_node expense_is_leaf_node,
                p.gl_level_class expense_gl_level_class,
                ason_gl_balance expense_ason_gl_balance,
                asof_gl_balance expense_asof_gl_balance,
                this_month_gl_balance expense_this_month_gl_balance,
                past_month_gl_balance expense_past_month_gl_balance,
                past_year_gl_balance expense_past_year_gl_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id
                AND p.app_user_id='''+"'"+p_app_user_id+"'"+'''
                AND expense_gl
       ORDER BY p.reporting_gl_serial)
SELECT income_gl_code gl_code,
       income_gl_name gl_name,
       COALESCE (income_gl_level_class) gl_level_class,
       income_ason_gl_balance ason_gl_balance,
       income_asof_gl_balance asof_gl_balance,
       income_this_month_gl_balance this_month_gl_balance,
       income_past_month_gl_balance past_month_gl_balance,
       income_past_year_gl_balance past_year_gl_balance
  FROM income_detail r
 WHERE    income_ason_gl_balance > 0
       OR income_asof_gl_balance > 0
       OR income_this_month_gl_balance > 0
       OR income_past_month_gl_balance > 0
       OR income_past_year_gl_balance > 0
UNION ALL
SELECT expense_gl_code gl_code,
       expense_gl_name gl_name,
       COALESCE (expense_gl_level_class) gl_level_class,
       expense_ason_gl_balance ason_gl_balance,
       expense_asof_gl_balance asof_gl_balance,
       expense_this_month_gl_balance this_month_gl_balance,
       expense_past_month_gl_balance past_month_gl_balance,
       expense_past_year_gl_balance past_year_gl_balance
  FROM expense_detail p
 WHERE    expense_ason_gl_balance > 0
       OR expense_asof_gl_balance > 0
       OR expense_this_month_gl_balance > 0
       OR expense_past_month_gl_balance > 0
       OR expense_past_year_gl_balance > 0'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_incomeexpensestab_summary(p_app_user_id):
    try:
        sql = '''WITH
   income_balance
   AS
      (SELECT ason_gl_balance income_ason_gl_balance,
              asof_gl_balance income_asof_gl_balance,
              this_month_gl_balance income_this_month_gl_balance,
              past_month_gl_balance income_past_month_gl_balance,
              past_year_gl_balance income_past_year_gl_balance
         FROM finance_ledger_report_balance
        WHERE     app_user_id = '''+"'"+p_app_user_id+"'"+'''
              AND gl_code =
                  (SELECT income_main_gl FROM finance_application_settings)),
   expences_balance
   AS
      (SELECT ason_gl_balance expense_ason_gl_balance,
              asof_gl_balance expense_asof_gl_balance,
              this_month_gl_balance expense_this_month_gl_balance,
              past_month_gl_balance expense_past_month_gl_balance,
              past_year_gl_balance expense_past_year_gl_balance
         FROM finance_ledger_report_balance
        WHERE     app_user_id = '''+"'"+p_app_user_id+"'"+'''
              AND gl_code =
                  (SELECT expenses_main_gl FROM finance_application_settings)),
   profit_loss_balance
   AS
      (SELECT income_ason_gl_balance - expense_ason_gl_balance
                 ason_gl_balance,
              income_asof_gl_balance - expense_asof_gl_balance
                 asof_gl_balance,
              income_this_month_gl_balance - expense_this_month_gl_balance
                 this_month_gl_balance,
              income_past_month_gl_balance - expense_past_month_gl_balance
                 past_month_gl_balance,
              income_past_year_gl_balance - expense_past_year_gl_balance
                 past_year_gl_balance
         FROM income_balance, expences_balance)
SELECT *
  FROM profit_loss_balance'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_profitloss_details(p_app_user_id):
    try:
        sql = '''WITH
   income_detail
   AS
      (  SELECT row_number ()
                   OVER (ORDER BY p.reporting_gl_serial, p.reporting_gl_code)
                   income_serial_number,
                p.gl_code
                   income_gl_code,
                p.gl_name
                   income_gl_name,
                p.is_leaf_node
                   income_is_leaf_node,
                p.gl_level_class
                   income_gl_level_class,
                ason_credit_sum
                   income_opening_credit_sum,
                ason_debit_sum
                   income_opening_debit_sum,
                this_period_credit_sum
                   income_period_credit_sum,
                this_period_debit_sum
                   income_period_debit_sum,
                asof_credit_sum
                   income_closing_credit_sum,
                asof_debit_sum
                   income_closing_debit_sum,
                abs (this_period_credit_sum - this_period_debit_sum)
                   income_this_period_balance,
                abs (asof_credit_sum - asof_debit_sum)
                   income_asof_debit_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id
                AND p.app_user_id = '''+"'"+p_app_user_id+"'"+'''
                AND income_gl
                AND (   this_period_credit_sum > 0.00
                     OR this_period_debit_sum > 0.00
                     OR asof_credit_sum > 0.00
                     OR asof_debit_sum > 0.00
                     OR ason_credit_sum > 0.00
                     OR ason_debit_sum > 0.00)
       ORDER BY p.reporting_gl_serial, p.reporting_gl_code),
   expense_detail
   AS
      (  SELECT row_number ()
                   OVER (ORDER BY p.reporting_gl_serial, p.reporting_gl_code)
                   expense_serial_number,
                p.gl_code
                   expense_gl_code,
                p.gl_name
                   expense_gl_name,
                p.is_leaf_node
                   expense_is_leaf_node,
                p.gl_level_class
                   expense_gl_level_class,
                ason_credit_sum
                   expense_opening_credit_sum,
                ason_debit_sum
                   expense_opening_debit_sum,
                this_period_credit_sum
                   expense_period_credit_sum,
                this_period_debit_sum
                   expense_period_debit_sum,
                asof_credit_sum
                   expense_closing_credit_sum,
                asof_debit_sum
                   expense_closing_debit_sum,
                abs (this_period_credit_sum - this_period_debit_sum)
                   expense_this_period_balance,
                abs (asof_credit_sum - asof_debit_sum)
                   expense_asof_debit_balance
           FROM finance_ledger_report_balance b, finance_ledger_report_param p
          WHERE     b.gl_code = p.gl_code
                AND b.app_user_id = p.app_user_id
                AND p.app_user_id = '''+"'"+p_app_user_id+"'"+'''
                AND expense_gl
                AND (   this_period_credit_sum > 0.00
                     OR this_period_debit_sum > 0.00
                     OR asof_credit_sum > 0.00
                     OR asof_debit_sum > 0.00
                     OR ason_credit_sum > 0.00
                     OR ason_debit_sum > 0.00)
       ORDER BY p.reporting_gl_serial, p.reporting_gl_code)
  SELECT income_gl_name,
         COALESCE (income_gl_level_class, expense_gl_level_class)
            income_gl_level_class,
         income_opening_credit_sum,
         income_opening_debit_sum,
         income_period_credit_sum,
         income_period_debit_sum,
         income_closing_credit_sum,
         income_closing_debit_sum,
         income_this_period_balance,
         income_asof_debit_balance,
         expense_gl_name,
         COALESCE (expense_gl_level_class, income_gl_level_class)
            expense_gl_level_class,
         expense_opening_credit_sum,
         expense_opening_debit_sum,
         expense_period_credit_sum,
         expense_period_debit_sum,
         expense_closing_credit_sum,
         expense_closing_debit_sum,
         expense_this_period_balance,
         expense_asof_debit_balance
    FROM income_detail r
         FULL OUTER JOIN expense_detail p
            ON (r.income_serial_number = p.expense_serial_number)
ORDER BY r.income_serial_number, p.expense_serial_number'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_profitloss_summary(p_app_user_id):
    try:
        sql = '''WITH
   income_balance
   AS
      (SELECT ason_credit_sum
                 income_opening_credit_sum,
              ason_debit_sum
                 income_opening_debit_sum,
              this_period_credit_sum
                 income_period_credit_sum,
              this_period_debit_sum
                 income_period_debit_sum,
              asof_credit_sum
                 income_closing_credit_sum,
              asof_debit_sum
                 income_closing_debit_sum,
              abs (this_period_credit_sum - this_period_debit_sum)
                 income_this_period_balance,
              abs (asof_credit_sum - asof_debit_sum)
                 income_asof_debit_balance
         FROM finance_ledger_report_balance
        WHERE     app_user_id = '''+"'"+p_app_user_id+"'"+'''
              AND gl_code =
                  (SELECT income_main_gl FROM finance_application_settings)),
   expences_balance
   AS
      (SELECT ason_credit_sum
                 expense_opening_credit_sum,
              ason_debit_sum
                 expense_opening_debit_sum,
              this_period_credit_sum
                 expense_period_credit_sum,
              this_period_debit_sum
                 expense_period_debit_sum,
              asof_credit_sum
                 expense_closing_credit_sum,
              asof_debit_sum
                 expense_closing_debit_sum,
              abs (this_period_credit_sum - this_period_debit_sum)
                 expense_this_period_balance,
              abs (asof_credit_sum - asof_debit_sum)
                 expense_asof_debit_balance
         FROM finance_ledger_report_balance
        WHERE     app_user_id = '''+"'"+p_app_user_id+"'"+'''
              AND gl_code =
                  (SELECT expenses_main_gl FROM finance_application_settings)),
   profit_loss_balance
   AS
      (SELECT income_opening_credit_sum - expense_opening_credit_sum
                 opening_credit_balance,
              income_opening_debit_sum - expense_opening_debit_sum
                 opening_debit_balance,
              income_period_credit_sum - expense_period_credit_sum
                 period_credit_balance,
              income_period_debit_sum - expense_period_debit_sum
                 period_debit_balance,
              income_closing_credit_sum - expense_closing_credit_sum
                 closing_credit_balance,
              income_closing_debit_sum - expense_closing_debit_sum
                 closing_debit_balance,
              income_this_period_balance - expense_this_period_balance
                 this_period_balance,
              income_asof_debit_balance - expense_asof_debit_balance
                 asof_balance
         FROM income_balance, expences_balance)
SELECT (CASE
           WHEN opening_credit_balance > 0 THEN opening_credit_balance
           ELSE 0
        END)
          profit_opening_credit_balance,
       (CASE
           WHEN opening_debit_balance > 0 THEN opening_debit_balance
           ELSE 0
        END)
          profit_opening_debit_balance,
       (CASE
           WHEN period_credit_balance > 0 THEN period_credit_balance
           ELSE 0
        END)
          profit_period_credit_balance,
       (CASE
           WHEN period_debit_balance > 0 THEN period_debit_balance
           ELSE 0
        END)
          profit_period_debit_balance,
       (CASE
           WHEN closing_credit_balance > 0 THEN closing_credit_balance
           ELSE 0
        END)
          profit_closing_credit_balance,
       (CASE
           WHEN closing_debit_balance > 0 THEN closing_debit_balance
           ELSE 0
        END)
          profit_closing_debit_balance,
       (CASE WHEN this_period_balance > 0 THEN this_period_balance ELSE 0 END)
          profit_this_period_balance,
       (CASE WHEN asof_balance > 0 THEN asof_balance ELSE 0 END)
          profit_asof_balance,
       (CASE
           WHEN opening_credit_balance < 0 THEN abs (opening_credit_balance)
           ELSE 0
        END)
          loss_opening_credit_balance,
       (CASE
           WHEN opening_debit_balance < 0 THEN abs (opening_debit_balance)
           ELSE 0
        END)
          loss_opening_debit_balance,
       (CASE
           WHEN period_credit_balance < 0 THEN abs (period_credit_balance)
           ELSE 0
        END)
          loss_period_credit_balance,
       (CASE
           WHEN period_debit_balance < 0 THEN abs (period_debit_balance)
           ELSE 0
        END)
          loss_period_debit_balance,
       (CASE
           WHEN closing_credit_balance < 0 THEN abs (closing_credit_balance)
           ELSE 0
        END)
          loss_closing_credit_balance,
       (CASE
           WHEN closing_debit_balance < 0 THEN abs (closing_debit_balance)
           ELSE 0
        END)
          loss_closing_debit_balance,
       (CASE
           WHEN this_period_balance < 0 THEN abs (this_period_balance)
           ELSE 0
        END)
          loss_this_period_balance,
       (CASE WHEN asof_balance < 0 THEN abs (asof_balance) ELSE 0 END)
          loss_asof_balance
  FROM profit_loss_balance'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_cashtrandetails_details(p_app_user_id):
    try:
        row = Query_Table.objects.filter(app_user_id=p_app_user_id).values(row_serial=F("chr_column1"),
                                                                           tran_details=F("chr_column2"), credit_amount=F("dec_column1"), debit_amount=F("dec_column2"),
                                                                           tran_balance=F("dec_column3"), tran_date=Func(F('dat_column1'), Value('MM/DD/YYYY'), function='to_char',
                                                                                                                         output_field=CharField()
                                                                                                                         )).order_by('id')
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_cashtrandetails_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Query_Table.objects.filter(
            app_user_id=p_app_user_id).aggregate(Sum('dec_column1'), Sum('dec_column2'))
        data['total_credit_amount'] = stock_summary['dec_column1__sum']
        data['total_debit_amount'] = stock_summary['dec_column2__sum']
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_accountbalance_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(client_id=F("report_column4"),
                                                                                    account_type=F("report_column5"), account_title=F("report_column6"), debit_amount=F("report_column7"),
                                                                                    credit_amount=F("report_column8"), account_balance=F("report_column9"), account_number=F("report_column1")
                                                                                    ).order_by('id')
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_accountbalance_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Report_Table_Tabular.objects.annotate(total_debit_amount=Cast('report_column7', output_field=FloatField()),
                                                              total_credit_amount=Cast(
                                                                  'report_column8', output_field=FloatField()),
                                                              total_account_balance=Cast(
                                                                  'report_column9', output_field=FloatField())
                                                              ).filter(app_user_id=p_app_user_id).aggregate(
            Sum('total_debit_amount'), Sum('total_credit_amount'), Sum('total_account_balance'))
        data['total_debit_amount'] = stock_summary['total_debit_amount__sum']
        data['total_credit_amount'] = stock_summary['total_credit_amount__sum']
        data['total_account_balance'] = stock_summary['total_account_balance__sum']
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_tellerbalance_details(p_app_user_id):
    try:
        sql = '''SELECT report_column1 teller_id,
       report_column2 employee_name,
       report_column3 opening_balance,
       report_column4 this_period_debit_sum,
       report_column5 this_period_credit_sum,
       report_column6 closing_balance,
       app_user_id
  FROM appauth_report_table_tabular 
  where app_user_id='''+"'"+p_app_user_id+"'"
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_tellertransaction_details(p_app_user_id):
    try:
        sql = '''SELECT report_column1 serial_number,
       to_char(cast(report_column2 as date),'DD-MM-YYYY') transaction_date,
       report_column3 transaction_narration,
       cast(report_column4 as numeric) credit_balance,
       cast(report_column5 as numeric) debit_balance,
       report_column6 app_user_id,
       report_column7 app_data_time
  FROM appauth_report_table_tabular 
  where app_user_id='''+"'"+p_app_user_id+"'"
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_tellertransaction_sum(p_app_user_id):
    try:
        sql = '''SELECT 
       sum(cast(report_column4 as numeric)) credit_balance,
       sum(cast(report_column5 as numeric)) debit_balance
  FROM appauth_report_table_tabular 
  where app_user_id='''+"'"+p_app_user_id+"'"
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

def fn_get_assetliabilities_summary(p_app_user_id):
    data = dict()
    try:
        apps = Application_Settings.objects.get()
        asset_main_gl = apps.asset_main_gl
        liabilities_main_gl = apps.asset_main_gl
        ason_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_ason_date', report_name='sales_asset_liabilities')
        data['p_ason_date'] = ason_date.parameter_values
        asset = Query_Table.objects.get(
            app_user_id=p_app_user_id, chr_column2=asset_main_gl)
        data['total_asset'] = asset.dec_column1
        liab = Query_Table.objects.get(
            app_user_id=p_app_user_id, chr_column2=liabilities_main_gl)
        data['total_liabilities'] = liab.dec_column1
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_trialbalance_summary(p_app_user_id):
    data = dict()
    try:
        from_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_from_date', report_name='sales_trial_balance')
        upto_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_upto_date', report_name='sales_trial_balance')
        data['p_from_date'] = from_date.parameter_values
        data['p_upto_date'] = upto_date.parameter_values
        return data
    except Exception as e:
        print(str(e))
        return data

def fn_get_cashnbank_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(row_serial=F("report_column1"),
                                                                                    transaction_date=F('report_column2'), transaction_naration=F("report_column4"),
                                                                                    cash_credit_amount=F("report_column5"), cash_debit_amount=F("report_column6"), cash_balance=F("report_column7"),
                                                                                    bank_credit_amount=F("report_column8"), bank_debit_amount=F("report_column9"), bank_balance=F("report_column10"))
        return row
    except Exception as e:
        print(str(e))
        pass

def fn_get_cashnbank_summary(p_app_user_id):
    try:
        sql = '''SELECT current_date print_date, abs(opening_cash) opening_cash,
       abs(opening_bank) opening_bank,
       cash_debit_amount
          cash_receipt,
       bank_debit_amount
          bank_receipt,
       cash_credit_amount
          cash_payment,
       bank_credit_amount
          bank_payment,
       cash_debit_amount + bank_debit_amount
          total_receipt,
       cash_credit_amount + bank_credit_amount
          total_payment,
       (  (cash_debit_amount + bank_debit_amount)
        - (cash_credit_amount + bank_credit_amount))
          balance_this_period,
       abs((opening_cash + (cash_debit_amount - cash_credit_amount)))
          closing_cash,
       abs((opening_bank + (bank_debit_amount - bank_credit_amount)))
          closing_bank,
       opening_cash_receipt + cash_debit_amount
          total_cash_receipt,
       opening_bank_receipt + bank_debit_amount
          total_bank_receipt,
       opening_cash_payment + cash_credit_amount
          total_cash_payment,
       opening_bank_payment + bank_credit_amount
          total_bank_payment
  FROM (SELECT COALESCE(sum (cast (report_column6 AS NUMERIC)),0.00) cash_debit_amount,
               COALESCE(sum (cast (report_column9 AS NUMERIC)),0.00) bank_debit_amount,
               COALESCE(sum (cast (report_column5 AS NUMERIC)),0.00) cash_credit_amount,
               COALESCE(sum (cast (report_column8 AS NUMERIC)),0.00) bank_credit_amount
          FROM appauth_report_table_tabular
         WHERE report_column3 <> '00000000'
          and app_user_id= '''+"'"+p_app_user_id+"'"''') a,
       (SELECT  COALESCE((cast (report_column7 AS NUMERIC)),0.00) opening_cash,
               COALESCE((cast (report_column10 AS NUMERIC)),0.00) opening_bank,
               COALESCE(abs (cast (report_column6 AS NUMERIC)),0.00) opening_cash_receipt,
               COALESCE(abs (cast (report_column9 AS NUMERIC)),0.00) opening_bank_receipt,
              COALESCE( abs (cast (report_column5 AS NUMERIC)),0.00) opening_cash_payment,
              COALESCE( abs (cast (report_column8 AS NUMERIC)),0.00) opening_bank_payment
          FROM appauth_report_table_tabular
         WHERE report_column3 = '00000000'
          and app_user_id= '''+"'"+p_app_user_id+"'"''') b'''

        results = fn_get_query_result(sql)
        sum_data = dict()
        print(results)
        for row in results:
            sum_data['print_date']= row['print_date']
            sum_data['opening_cash']= row['opening_cash']
            sum_data['opening_bank']= row['opening_bank']
            sum_data['opening_total']= row['opening_cash']+row['opening_bank']
            sum_data['cash_receipt']= row['cash_receipt']
            sum_data['bank_receipt']= row['bank_receipt']
            sum_data['cash_payment']= row['cash_payment']
            sum_data['bank_payment']= row['bank_payment']
            sum_data['total_receipt']= row['total_receipt']
            sum_data['total_payment']= row['total_payment']
            sum_data['balance_this_period']= row['balance_this_period']
            sum_data['closing_cash']= row['closing_cash']
            sum_data['closing_bank']= row['closing_bank']
            sum_data['closing_total']= row['closing_cash']+row['closing_bank']
            sum_data['total_cash_receipt']= row['total_cash_receipt']
            sum_data['total_bank_receipt']= row['total_bank_receipt']
            sum_data['total_cash_payment']= row['total_cash_payment']
            sum_data['total_bank_payment']= row['total_bank_payment']
        
        return sum_data
    except Exception as e:
        print(str(e))

def fn_get_coa_details(p_app_user_id):
    try:
        sql = '''WITH
   RECURSIVE root_data
   AS
      (SELECT gl_code,
              gl_name,
              reporting_gl_code,
              reporting_gl_serial,
              parent_code,
              is_leaf_node,
              income_gl,
              expense_gl,
              assets_gl,
              liabilities_gl,
              sundry_flag,
              maintain_by_system,
              1  AS level
         FROM finance_general_ledger
        WHERE parent_code IS NULL
       UNION ALL
       SELECT e.gl_code,
              e.gl_name,
              e.reporting_gl_code,
              e.reporting_gl_serial,
              e.parent_code,
              e.is_leaf_node,
              e.income_gl,
              e.expense_gl,
              e.assets_gl,
              e.liabilities_gl,
              e.sundry_flag,
              e.maintain_by_system,
              c.level + 1
         FROM root_data c
              JOIN finance_general_ledger e ON e.parent_code = c.gl_code)
  SELECT gl_code,
         level gl_level,
         gl_name,
         reporting_gl_code,
         parent_code,
            'padding-left: '
         || 10 * level
         || 'px; '
         || (CASE
                WHEN is_leaf_node THEN 'font-weight: normal'
                ELSE 'font-weight: bold;'
             END)
         || '; ' gl_level_class,
         (CASE
             WHEN income_gl THEN 'INCOME'
             WHEN expense_gl THEN 'EXPENSE'
             WHEN assets_gl THEN 'ASSET'
             WHEN liabilities_gl THEN 'LIABILITY'
             ELSE 'Others'
          END) account_type
    FROM root_data
ORDER BY reporting_gl_serial'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))
