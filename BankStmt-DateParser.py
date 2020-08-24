import pandas as pd
import numpy as np
import os
import datetime
from tabula import read_pdf
import PyPDF2
import re

def guess_date(string):
    #skipping for nans
    if string!=string:
        raise ValueError(string)

    #skipping if only alphabets
    if any(char.isdigit() for char in string):
        for fmt in ["%Y/%m/%d","%d-%m-%Y","%d/%m/%y","%d-%b-%Y %X","%d/%m/%Y","%d %b %y","%d %b %Y"]:
            try:
                return str(datetime.datetime.strptime(string, fmt).date())
            except:
                continue
    raise ValueError(string)

## Output-> YYYY-MM-DD

path='Bank Statements'

for pdf in os.listdir(path):
    try:
        pdf_path=os.path.join(path,pdf)

        print(pdf_path)
        bank_statements = read_pdf(pdf_path, stream=True , pages='all')

        #taking out first column as array of list
        dates_column =[]
        dates_list=[]
        for bank_statement in bank_statements:
            dates_column.append(bank_statement[bank_statement.columns[0]].to_list())
            for date_list in dates_column:
                dates_list.extend(date_list)

        # arranging in proper YYYY-MM-DD
        formatted_dates=[]
        for date in dates_list:
            try:
                if 'RBL' in pdf_path:
                    formatted_dates.append(guess_date(date[-8:]))
                else:
                    formatted_dates.append(guess_date(date))
            except:
                continue

        #getting oldest
        oldest = min(formatted_dates)
        print("Oldest: " +oldest)

        #getting newest
        youngest = max(formatted_dates)
        print("Newest: "+youngest)

    except:
        try:
            # icici-1 & Kotak
            #print(pdf_path)
            pdfReader = PyPDF2.PdfFileReader(pdf_path)
            pages = pdfReader.numPages
            extracted_text=''
            for pg in range(pages):
                page = pdfReader.getPage(pg)
                extracted_text += page.extractText()

            dates_parsed = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}',extracted_text)

            formatted_dates=[]
            for date in dates_parsed:
                try:
                    formatted_dates.append(guess_date(date))
                except:
                    continue

            if(formatted_dates[0]>formatted_dates[-1]):
                print("Oldest : "+formatted_dates[-1])
                print("Newest : "+formatted_dates[0])
            else:
                print("Oldest : "+formatted_dates[0])
                print("Newest : "+formatted_dates[-1])

        except:
            try:
                # For ICICI-2
                #print(pdf_path)
                bank_statements = read_pdf(pdf_path, stream=True , pages='all')

                #taking dates out from 2nd column
                dates=[]
                for bank_statement in bank_statements:
                    dates.append(bank_statement.columns.values[1])

                #getting dates in YYYY-MM-DD
                formatted_dates=[]
                for date in dates:
                    try:
                        formatted_dates.append(guess_date(date))
                    except:
                        continue

                if(formatted_dates[0]>formatted_dates[-1]):
                    print("Oldest : "+formatted_dates[-1])
                    print("Newest : "+formatted_dates[0])
                else:
                    print("Oldest : "+formatted_dates[0])
                    print("Newest : "+formatted_dates[-1])
            
            except:
                continue
            continue
        continue