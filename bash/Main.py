import os
import pandas as pd
import unicodedata

# Specify the folder where your CSV files are located
folder_path = "gate/"

# List all CSV and Excel files in the folder
file_paths = [file for file in os.listdir(folder_path)
              if file.lower().endswith('.csv') or file.lower().endswith('.xlsx')]

# Initialize an empty list to store DataFrames
dfs = []

# Loop through each CSV file and merge into the DataFrame
for csv_file in file_paths:
    file_path = os.path.join(folder_path, csv_file)

    # Normalize the file name to ensure compatibility
    normalized_file_name = unicodedata.normalize('NFC', csv_file)

    # Check file type and read accordingly
    if csv_file.lower().endswith('.csv'):
        df = pd.read_csv(file_path, dtype={'TRANSACTION ID': str}, encoding='utf-8')
    elif csv_file.lower().endswith('.xlsx'):
        df = pd.read_excel(file_path, dtype={'TRANSACTION ID': str})

    # Check if the DataFrame is not empty
    if not df.empty:
        # Create a new column 'File_Name' and fill it with the current file name
        df['File_Name'] = normalized_file_name

        # Your existing logic here...
        # If 'TimeZone' and 'Time zone' columns exist, merge them into a new column 'Merged_Timezone'
        if 'TimeZone' in df.columns and 'Time zone' in df.columns:
            df['Merged_Timezone'] = df['TimeZone'].fillna(df['Time zone'])
            # Drop the original 'TimeZone' and 'Time zone' columns
            df.drop(['TimeZone', 'Time zone'], axis=1, inplace=True)
        elif 'TimeZone' in df.columns:
            df.rename(columns={'TimeZone': 'Merged_Timezone'}, inplace=True)
        elif 'Time zone' in df.columns:
            df.rename(columns={'Time zone': 'Merged_Timezone'}, inplace=True)

        # If 'TimeZone' and 'Time zone' columns exist, merge them into a new column 'Merged_Timezone'
        if 'Shipping and Handling Amount' in df.columns and 'Postage and Packaging Amount' in df.columns:
            df['Shipping_and_handling_amount'] = df['Shipping and Handling Amount'].fillna(
                df['Postage and Packaging Amount'])
            # Drop the original 'TimeZone' and 'Time zone' columns
            df.drop(['Shipping and Handling Amount', 'Postage and Packaging Amount'], axis=1, inplace=True)
        elif 'Shipping and Handling Amount' in df.columns:
            df.rename(columns={'Shipping and Handling Amount': 'Shipping_and_handling_amount'}, inplace=True)
        elif 'Postage and Packaging Amount' in df.columns:
            df.rename(columns={'Postage and Packaging Amount': 'Shipping_and_handling_amount'}, inplace=True)

        # If 'TimeZone' and 'Time zone' columns exist, merge them into a new column 'Merged_Timezone'
        if 'Sales Tax' in df.columns and 'VAT' in df.columns:
            df['Sale_tax'] = df['Sales Tax'].fillna(df['VAT'])
            # Drop the original 'TimeZone' and 'Time zone' columns
            df.drop(['Sales Tax', 'VAT'], axis=1, inplace=True)
        elif 'Sales Tax' in df.columns:
            df.rename(columns={'Sales Tax': 'Sale_tax'}, inplace=True)
        elif 'VAT' in df.columns:
            df.rename(columns={'VAT': 'Sale_tax'}, inplace=True)

        # If 'TimeZone' and 'Time zone' columns exist, merge them into a new column 'Merged_Timezone'
        if 'Address Line 2/District/Neighborhood' in df.columns and 'Address Line 2/District/Neighbourhood' in df.columns:
            df['Address_line_2_district_neighborhood'] = df['Address Line 2/District/Neighborhood'].fillna(
                df['Address Line 2/District/Neighbourhood'])
            # Drop the original 'TimeZone' and 'Time zone' columns
            df.drop(['Address Line 2/District/Neighborhood', 'Address Line 2/District/Neighbourhood'], axis=1,
                    inplace=True)
        elif 'Address Line 2/District/Neighborhood' in df.columns:
            df.rename(columns={'Address Line 2/District/Neighborhood': 'Address_line_2_district_neighborhood'},
                      inplace=True)
        elif 'Address Line 2/District/Neighbourhood' in df.columns:
            df.rename(columns={'Address Line 2/District/Neighbourhood': 'Address_line_2_district_neighborhood'},
                      inplace=True)

        # If 'TimeZone' and 'Time zone' columns exist, merge them into a new column 'Merged_Timezone'
        if 'State/Province/Region/County/Territory/Prefecture/Republic' in df.columns and 'County' in df.columns:
            df['Country_State'] = df['State/Province/Region/County/Territory/Prefecture/Republic'].fillna(df['County'])
            # Drop the original 'TimeZone' and 'Time zone' columns
            df.drop(['State/Province/Region/County/Territory/Prefecture/Republic', 'County'], axis=1, inplace=True)
        elif 'State/Province/Region/County/Territory/Prefecture/Republic' in df.columns:
            df.rename(columns={'State/Province/Region/County/Territory/Prefecture/Republic': 'Country_State'},
                      inplace=True)
        elif 'County' in df.columns:
            df.rename(columns={'County': 'Country_State'}, inplace=True)

        # If 'TimeZone' and 'Time zone' columns exist, merge them into a new column 'Merged_Timezone'
        if 'Zip/Postal Code' in df.columns and 'Postcode' in df.columns:
            df['PostCode'] = df['Zip/Postal Code'].fillna(df['Postcode'])
            # Drop the original 'TimeZone' and 'Time zone' columns
            df.drop(['Zip/Postal Code', 'Postcode'], axis=1, inplace=True)
        elif 'Zip/Postal Code' in df.columns:
            df.rename(columns={'Zip/Postal Code': 'PostCode'}, inplace=True)
        elif 'Postcode' in df.columns:
            df.rename(columns={'Postcode': 'PostCode'}, inplace=True)

        # Append the modified DataFrame into the list
        dfs.append(df)
    else:
        print(f"Warning: The file {csv_file} is empty and has been skipped.".encode('utf-8'))

# Concatenate all DataFrames in the list with ignore_index=True
merged_df = pd.concat(dfs, ignore_index=True)

# Reorder columns to have 'File_Name' as the first column
merged_df = merged_df[['File_Name'] + [col for col in merged_df.columns if col != 'File_Name']]

# Save the merged DataFrame to a new CSV file with proper encoding
output_file = "merged_file.xlsx"
merged_df.to_excel(output_file, index=False)

print("Merging complete. Merged data saved to:", output_file)
