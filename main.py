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
    print("Database connected")
    data1 = db.execute_query(conn, db.query_header_row)
    print("Query 1 complete")
    data2 = db.execute_query(conn, db.query_agency_fees_data)
    print("Query 2 complete")

    output_file_name = write_output(data1, data2)
    print("Output file written successfully")

    email_results(output_file_name)
    print("Email completed successfully")

if __name__ == '__main__':
    main()
