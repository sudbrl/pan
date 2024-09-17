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
    # Custom CSS to set the background color
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f6;  /* Light gray background */
            font-family: Arial, sans-serif;
        }
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .result-container {
            padding: 20px;
            border-radius: 8px;
            background-color: #ffffff;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("PAN Search App")
    st.write("Enter the PAN number to retrieve the information.")

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Input for PAN number in the center
            pan = st.text_input("Enter PAN number", key="pan_input")
            if st.button("Search"):
                if pan:
                    with st.spinner("Fetching data..."):
                        # Call the external API
                        data = fetch_info_from_api(pan)
                        
                        # Display the results
                        if data:
                            st.markdown('<div class="result-container">', unsafe_allow_html=True)
                            st.write("### Business Details")
                            st.write(f"**PAN**: {data.get('pan')}")
                            st.write(f"**Name**: {data.get('name')}")
                            st.write(f"**VAT Registration Date**: {data.get('vatRegDate')}")
                            st.write(f"**Tax Clearance Date**: {data.get('taxclearance')}")
                            st.write(f"**Return Verified Date**: {data.get('returnVerifiedDate')}")
                            st.write(f"**Tax Returns Status**: {data.get('taxreturns')}")
                            st.write(f"**VAT Returns Status**: {data.get('vatreturns')}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.write("No data found for the given PAN number.")
                else:
                    st.warning("Please enter a PAN number.")

if __name__ == '__main__':
    main()
