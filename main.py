from datetime import date

from db import Database
from file_ops import write_output
from email_ops import email_results
from dotenv import load_dotenv

load_dotenv()

export_date = date(2022, 12, 8)

def main():
    db = Database(export_date=export_date)
    conn = db.connect()
    data1 = db.execute_query(conn, db.query_header_row)
    data2 = db.execute_query(conn, db.query_agency_fees_data)

    output_file_name = write_output(data1, data2)
    
    email_results(output_file_name)

if __name__ == '__main__':
    main()
