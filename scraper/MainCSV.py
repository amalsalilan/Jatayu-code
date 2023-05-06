import pandas as pd 
import os 
import re 
import csv 

class CompanyData:
    def __init__(self, csv_file_path):
        # Read CSV file using pandas and get a list of company names
        self.df = pd.read_csv(csv_file_path)
        self.org_names = list(self.df['Name'])
        self.csv_file_path = csv_file_path

    def find_company(self, input_str):
        # Use regex to search for the company name in the list
        regex = re.compile(re.escape(input_str), re.IGNORECASE)
        for i, company in enumerate(self.org_names):
            if regex.search(company):
                # If found, return the index of the company and its name
                return i, company
        # If not found, return None
        return None, None 

    def get_other_columns(self, row_number):
        # Unpack the column names
        column_names = ['Name', 'Symbols', 'Total ESG Score', 'Environment Score',
           'Social Score', 'Governance Score', 'Controversy Score',
           'Controversy Assessment']
        _, _, total_esg, environment, social, governance, controversy, assessment = column_names

        # Read the CSV file
        with open(self.csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip the header row
            next(csv_reader)
            # Loop through the rows until we reach the specified row number
            for i, row in enumerate(csv_reader):
                if i == row_number:
                    # Return the other columns' data in a dictionary
                    return {
                        total_esg: row[2],
                        environment: row[3],
                        social: row[4],
                        governance: row[5],
                        controversy: row[6],
                        assessment: row[7]
                    }
        # If the specified row number was not found, return None
        return None

if __name__ == '__main__':
    # Get current working directory
    curdir = str(os.getcwd())

    # Get user input for organization name to search for
    query = input("Enter the organization name: ").lower()

    # Create a CompanyData object
    company_data = CompanyData(f"{curdir}/integration/yfinance.csv")

    # Call the find_company method to get the index and name of the company
    index, company_name = company_data.find_company(query)  

    # Call the get_other_columns method to retrieve other columns of data for the specified company
    retrieved_values = company_data.get_other_columns(int(index))

    # Print the retrieved values
    print(retrieved_values)
