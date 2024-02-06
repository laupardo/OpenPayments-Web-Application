from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
import requests
from django.conf import settings
import csv
from .models import Payment
from datetime import datetime
def import_payments_data():
    BASE_DIR = settings.BASE_DIR
    # Set the media directory to save files
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    # URL of the Open Payments dataset
    open_payments_url = 'https://www.cms.gov/priorities/key-initiatives/open-payments/data/dataset-downloads'
    # Fetch the HTML content
    ans = requests.get(open_payments_url)
    # Parse HTML content
    soup = BeautifulSoup(ans.content, 'html.parser')
    # Initialize variables
    download_link = None
    filename = ''

    # Find the download link for the Open Payments dataset
    for link in soup.find_all('a'):
        if link.get('title') is not None and "Program Year Open Payments Dataset" in link.get('title'):
            download_link = link.get('href')
            filename = download_link.split('/')[-1]
            break

    print(filename)
    # Fetch the dataset
    data = requests.get(download_link)

    # Save the dataset to the media directory
    file_path = os.path.join(MEDIA_ROOT, filename)
    with open(file_path, "wb") as f:
        f.write(data.content)

    # Extract the contents of the ZIP file to the media directory
    extracted_folder_path = os.path.join(MEDIA_ROOT, "extracted_data")
    target_file_prefix = "OP_DTL_GNRL_"
    general_payments_file = ''

    # Ensure the extraction directory exists
    os.makedirs(extracted_folder_path, exist_ok=True)

    with ZipFile(file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            # Check if the file starts with the specified prefix
            if file_name.startswith(target_file_prefix):
                # Extract the file to the specified folder
                zip_ref.extract(file_name, os.path.join(extracted_folder_path, file_name))
                general_payments_file = file_name
                break

    # Process the extracted CSV file, create records in bulk
    csv_file_path = os.path.join(extracted_folder_path, general_payments_file, general_payments_file)
    payments = []
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            entry = Payment(
                Change_Type=row['Change_Type'],
                Covered_Recipient_Type=row['Covered_Recipient_Type'],
                Teaching_Hospital_CCN=row['Teaching_Hospital_CCN'],
                Teaching_Hospital_ID=row['Teaching_Hospital_ID'],
                Teaching_Hospital_Name=row['Teaching_Hospital_Name'],
                Covered_Recipient_Profile_ID=row['Covered_Recipient_Profile_ID'],
                Covered_Recipient_NPI=row['Covered_Recipient_NPI'],
                Covered_Recipient_First_Name=row['Covered_Recipient_First_Name'],
                Covered_Recipient_Middle_Name=row['Covered_Recipient_Middle_Name'],
                Covered_Recipient_Last_Name=row['Covered_Recipient_Last_Name'],
                Covered_Recipient_Name_Suffix=row['Covered_Recipient_Name_Suffix'],
                Recipient_Primary_Business_Street_Address_Line1=row[
                    'Recipient_Primary_Business_Street_Address_Line1'],
                Recipient_Primary_Business_Street_Address_Line2=row[
                    'Recipient_Primary_Business_Street_Address_Line2'],
                Recipient_City=row['Recipient_City'],
                Recipient_State=row['Recipient_State'],
                Recipient_Zip_Code=row['Recipient_Zip_Code'],
                Recipient_Country=row['Recipient_Country'],
                Recipient_Province=row['Recipient_Province'],
                Recipient_Postal_Code=row['Recipient_Postal_Code'],
                Covered_Recipient_Primary_Type_1=row['Covered_Recipient_Primary_Type_1'],
                Covered_Recipient_Primary_Type_2=row['Covered_Recipient_Primary_Type_2'],
                Covered_Recipient_Primary_Type_3=row['Covered_Recipient_Primary_Type_3'],
                Covered_Recipient_Primary_Type_4=row['Covered_Recipient_Primary_Type_4'],
                Covered_Recipient_Primary_Type_5=row['Covered_Recipient_Primary_Type_5'],
                Covered_Recipient_Primary_Type_6=row['Covered_Recipient_Primary_Type_6'],
                Covered_Recipient_Specialty_1=row['Covered_Recipient_Specialty_1'],
                Covered_Recipient_Specialty_2=row['Covered_Recipient_Specialty_2'],
                Covered_Recipient_Specialty_3=row['Covered_Recipient_Specialty_3'],
                Covered_Recipient_Specialty_4=row['Covered_Recipient_Specialty_4'],
                Covered_Recipient_Specialty_5=row['Covered_Recipient_Specialty_5'],
                Covered_Recipient_Specialty_6=row['Covered_Recipient_Specialty_6'],
                Covered_Recipient_License_State_code1=row['Covered_Recipient_License_State_code1'],
                Covered_Recipient_License_State_code2=row['Covered_Recipient_License_State_code2'],
                Covered_Recipient_License_State_code3=row['Covered_Recipient_License_State_code3'],
                Covered_Recipient_License_State_code4=row['Covered_Recipient_License_State_code4'],
                Covered_Recipient_License_State_code5=row['Covered_Recipient_License_State_code5'],
                Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name=row[
                    'Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name'],
                Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID=row[
                    'Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID'],
                Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name=row[
                    'Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name'],
                Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_State=row[
                    'Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_State'],
                Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Country=row[
                    'Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Country'],
                Total_Amount_of_Payment_USDollars=float(row['Total_Amount_of_Payment_USDollars']),
                Date_of_Payment=datetime.strptime(row['Date_of_Payment'], '%m/%d/%Y').date(),
                Number_of_Payments_Included_in_Total_Amount=int(row['Number_of_Payments_Included_in_Total_Amount']),
                Form_of_Payment_or_Transfer_of_Value=row['Form_of_Payment_or_Transfer_of_Value'],
                Nature_of_Payment_or_Transfer_of_Value=row['Nature_of_Payment_or_Transfer_of_Value'],
                City_of_Travel=row['City_of_Travel'],
                State_of_Travel=row['State_of_Travel'],
                Country_of_Travel=row['Country_of_Travel'],
                Physician_Ownership_Indicator=row['Physician_Ownership_Indicator'].lower() == 'yes',
                Third_Party_Payment_Recipient_Indicator=row['Third_Party_Payment_Recipient_Indicator'].lower() == 'yes',
                Name_of_Third_Party_Entity_Receiving_Payment_or_Transfer_of_Value=row[
                    'Name_of_Third_Party_Entity_Receiving_Payment_or_Transfer_of_Value'],
                Charity_Indicator=row['Charity_Indicator'],
                Third_Party_Equals_Covered_Recipient_Indicator=row[
                    'Third_Party_Equals_Covered_Recipient_Indicator'],
                Contextual_Information=row['Contextual_Information'],
                Delay_in_Publication_Indicator=row['Delay_in_Publication_Indicator'],
                Record_ID=row['Record_ID'],
                Dispute_Status_for_Publication=row['Dispute_Status_for_Publication'],
                Related_Product_Indicator=row['Related_Product_Indicator'],
                Covered_or_Noncovered_Indicator_1=row['Covered_or_Noncovered_Indicator_1'],
                Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_1=row[
                    'Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_1'],
                Product_Category_or_Therapeutic_Area_1=row['Product_Category_or_Therapeutic_Area_1'],
                Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1=row[
                    'Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1'],
                Associated_Drug_or_Biological_NDC_1=row['Associated_Drug_or_Biological_NDC_1'],
                Associated_Device_or_Medical_Supply_PDI_1=row['Associated_Device_or_Medical_Supply_PDI_1'],
                Covered_or_Noncovered_Indicator_2=row['Covered_or_Noncovered_Indicator_2'],
                Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_2=row[
                    'Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_2'],
                Product_Category_or_Therapeutic_Area_2=row['Product_Category_or_Therapeutic_Area_2'],
                Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_2=row[
                    'Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_2'],
                Associated_Drug_or_Biological_NDC_2=row['Associated_Drug_or_Biological_NDC_2'],
                Associated_Device_or_Medical_Supply_PDI_2=row['Associated_Device_or_Medical_Supply_PDI_2'],
                Covered_or_Noncovered_Indicator_3=row['Covered_or_Noncovered_Indicator_3'],
                Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_3=row[
                    'Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_3'],
                Product_Category_or_Therapeutic_Area_3=row['Product_Category_or_Therapeutic_Area_3'],
                Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_3=row[
                    'Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_3'],
                Associated_Drug_or_Biological_NDC_3=row['Associated_Drug_or_Biological_NDC_3'],
                Associated_Device_or_Medical_Supply_PDI_3=row['Associated_Device_or_Medical_Supply_PDI_3'],
                Covered_or_Noncovered_Indicator_4=row['Covered_or_Noncovered_Indicator_4'],
                Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_4=row[
                    'Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_4'],
                Product_Category_or_Therapeutic_Area_4=row['Product_Category_or_Therapeutic_Area_4'],
                Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_4=row[
                    'Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_4'],
                Associated_Drug_or_Biological_NDC_4=row['Associated_Drug_or_Biological_NDC_4'],
                Associated_Device_or_Medical_Supply_PDI_4=row['Associated_Device_or_Medical_Supply_PDI_4'],
                Covered_or_Noncovered_Indicator_5=row['Covered_or_Noncovered_Indicator_5'],
                Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_5=row[
                    'Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_5'],
                Product_Category_or_Therapeutic_Area_5=row['Product_Category_or_Therapeutic_Area_5'],
                Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_5=row[
                    'Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_5'],
                Associated_Drug_or_Biological_NDC_5=row['Associated_Drug_or_Biological_NDC_5'],
                Associated_Device_or_Medical_Supply_PDI_5=row['Associated_Device_or_Medical_Supply_PDI_5'],
                Program_Year=row['Program_Year'],
                Payment_Publication_Date=datetime.strptime(row['Payment_Publication_Date'], '%m/%d/%Y').date()
            )
            payments.append(entry)

            # in batches to avoid memory issues
            if len(payments) == 1000:
                Payment.objects.bulk_create(payments)
                payments = []

