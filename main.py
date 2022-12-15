from datetime import date

from db import Database
from file_ops import write_output
from email_ops import email_results
from dotenv import load_dotenv

load_dotenv()

export_date = date(2012, 3, 1)

def main():
    db = Database(export_date=export_date)
    print("Database connected")
    data1 = db.header_row
    print("Create Header data complete")
    data2 = db.execute_query(db.conn, db.query_agency_fees_data)
    print("Agency Fee Data Query complete")

    output_file_name = write_output(data1, data2)
    print("Output file written successfully")

    #email_results(output_file_name)
    print("Email completed successfully")

if __name__ == '__main__':
    main()
