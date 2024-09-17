import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Function to call the external API with the given PAN number
def fetch_info_from_api(pan):
    api_url = f"https://www.apitest.freewebhostmost.com/info.php?pan={pan}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to process uploaded file
def process_uploaded_file(uploaded_file):
    # Read the uploaded Excel or CSV file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Check if the first column contains PAN numbers
    if 'PAN' not in df.columns:
        st.error("Uploaded file must contain a column named 'PAN' with the PAN numbers.")
        return None

    results = []
    for index, row in df.iterrows():
        pan = row['PAN']
        api_data = fetch_info_from_api(pan)
        if api_data:
            # Add API result to results list
            results.append({
                'PAN': api_data.get('pan'),
                'Name': api_data.get('name'),
                'VAT Registration Date': api_data.get('vatRegDate'),
                'Tax Clearance Date': api_data.get('taxclearance'),
                'Return Verified Date': api_data.get('returnVerifiedDate'),
                'Tax Returns Status': api_data.get('taxreturns'),
                'VAT Returns Status': api_data.get('vatreturns')
            })
        else:
            results.append({
                'PAN': pan,
                'Name': 'Not found',
                'VAT Registration Date': '',
                'Tax Clearance Date': '',
                'Return Verified Date': '',
                'Tax Returns Status': '',
                'VAT Returns Status': ''
            })
    
    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)
    return results_df

# Function to convert DataFrame to Excel format
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    processed_data = output.getvalue()
    return processed_data

# Streamlit App
def main():
    st.title("PAN Search App with File Upload")
    st.write("Upload an Excel or CSV file with a column named 'PAN' containing PAN numbers, and we'll generate results for each PAN.")

    # File uploader
    uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"])

    if uploaded_file:
        # Process the uploaded file
        results_df = process_uploaded_file(uploaded_file)

        if results_df is not None:
            st.write("### Results")
            st.dataframe(results_df)

            # Generate and allow download of the results in Excel format
            excel_data = to_excel(results_df)
            st.download_button(label="Download results as Excel", data=excel_data, file_name='pan_results.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    main()
