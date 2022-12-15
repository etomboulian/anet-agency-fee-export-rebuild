from dataclasses import dataclass
from datetime import date
import pymssql, os
from dotenv import load_dotenv

load_dotenv()

server_address = os.environ.get('DB_SERVER')
db_name = os.environ.get('DB_NAME')
user_name = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
conn_string = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server_address+';DATABASE='+db_name+';ENCRYPT=yes;UID='+user_name+';PWD='+ password
print(conn_string)

@dataclass
class Database:
    export_date: date

    def __post_init__(self):
        self.query_header_row = f"declare @export_date date = '03/01/2012'; select 'ACTIVENet Daily Agency Fee Export', convert(varchar,getdate(),102), convert(varchar,@export_date, 102);"
        self.query_agency_fees_data = f"""
        declare @export_date date = '03/01/2012';

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
        """

    def connect(self):
        return pymssql.connect(server="127.0.0.1", port="1434", user="evan", password="evan", database="ljsupport12")

    def execute_query(self, conn, query):
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()