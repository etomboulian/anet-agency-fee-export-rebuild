from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

output_folder = os.environ.get('OUTPUT_PATH')

date_description = datetime.now().strftime('%m-%d-%Y')
output_file_name = os.path.join(os.getcwd(), output_folder, f'agency_fee_export-{date_description}.csv')

def write_output(data1, data2):
    with open(output_file_name, 'w') as f:
        # Write the header row into the output csv file
        for row in data1:
            f.write(row[0] + ',' + str(row[1]) + ',' + str(row[2]) + '\n')
        # Write the export data into the output csv file
        for row in data2:
            for element in row:
                f.write(str(element) + ',')
            f.write('\n')

    return output_file_name