import streamlit as st
import requests

# Function to call the external API with the given PAN number
def fetch_info_from_api(pan):
    api_url = f"https://www.apitest.freewebhostmost.com/info.php?pan={pan}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit App
def main():
    st.title("PAN Search App")
    st.write("Enter the PAN number to retrieve the information.")
    
    # Input for PAN number
    pan = st.text_input("Enter PAN number")
    
    if st.button("Search"):
        if pan:
            with st.spinner("Fetching data..."):
                # Call the external API
                data = fetch_info_from_api(pan)
                
                # Display the results
                if data:
                    st.write("### Business Details")
                    st.write(f"**PAN**: {data.get('pan')}")
                    st.write(f"**Name**: {data.get('name')}")
                    st.write(f"**VAT Registration Date**: {data.get('vatRegDate')}")
                    st.write(f"**Tax Clearance Date**: {data.get('taxclearance')}")
                    st.write(f"**Return Verified Date**: {data.get('returnVerifiedDate')}")
                    st.write(f"**Tax Returns Status**: {data.get('taxreturns')}")
                    st.write(f"**VAT Returns Status**: {data.get('vatreturns')}")
                else:
                    st.write("No data found for the given PAN number.")
        else:
            st.warning("Please enter a PAN number.")

if __name__ == '__main__':
    main()
