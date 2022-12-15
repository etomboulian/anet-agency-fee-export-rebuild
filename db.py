import pymssql, os
from datetime import date, datetime
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

query_date_format = '%m/%d/%Y'
output_date_format = '%Y.%m.%d'

class SQLSettings(Enum):
    sql_address = os.environ.get('DB_SERVER')
    sql_port = os.environ.get('DB_PORT')
    sql_db_name = os.environ.get('DB_NAME')
    sql_user = os.environ.get('DB_USER')
    sql_password = os.environ.get('DB_PASSWORD')

class Database:
    def __init__(self, export_date: date):
        self.export_date = export_date
        self.header_row = [
            'ACTIVENet Daily Agency Fee Export', 
            datetime.now().strftime(output_date_format), 
            export_date.strftime(output_date_format)
            ] 
        self.query_agency_fees_data = """declare @export_date date = '{0}';
        with export_data_detail as (
            select cast(getdate() as date) as today, 
            cast(t.datestamp as date) as tx_date, 
            gla.ACCOUNTNAME as account_name, gla.ACCOUNTNUMBER as account_number, 
            ard.ELECTRONIC_PAYMENT_AMOUNT as cc_amount, 
            ard.ELECTRONIC_PAYMENT_FEE + ard.CONVENIENCE_FEE as cc_fee,
            ard.TRANSACTION_FEE as tx_fee , 
            (ard.ELECTRONIC_PAYMENT_AMOUNT - ard.ELECTRONIC_PAYMENT_FEE - ard.TRANSACTION_FEE) as amt_due_org,
            rs.SITENAME as revenue_site
            from AGENCY_RECEIPTDETAILS ard
            join RECEIPTDETAILS rd on ard.RECEIPTDETAIL_ID = rd.RECEIPTDETAIL_ID
            join TRANSACTIONS t on rd.TRANSACTION_ID = t.TRANSACTION_ID
            join SITES rs on rd.REVENUE_SITE_ID = rs.SITE_ID
            join GLACCOUNTS gla on ard.GLACCOUNT_ID = gla.GLACCOUNT_ID
            where cast(t.DATESTAMP as date) = @export_date
        )
        select convert(varchar,today, 102) as today, convert(varchar, tx_date, 102) as tx_date, account_name, account_number, sum(cc_amount) as cc_amt, sum(cc_fee) as cc_fee, sum(tx_fee) as tx_fee, sum(amt_due_org) as amt_due_org, revenue_site 
        from export_data_detail
        group by today, tx_date, revenue_site, account_name, account_number
        """.format(self.export_date.strftime(query_date_format))

    def connect(self):
        return pymssql.connect(
            server=SQLSettings.sql_address.value, 
            port=SQLSettings.sql_port.value, 
            user=SQLSettings.sql_user.value, 
            password=SQLSettings.sql_password.value, 
            database=SQLSettings.sql_db_name.value
            )

    def execute_query(self, conn, query):
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()