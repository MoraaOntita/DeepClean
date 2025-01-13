import streamlit as st
import os
import pandas as pd
from pathlib import Path

def process_data_for_brand(brand, file_path):
    if brand == "SleekLady":
        # Call SleekLady-specific cleaning functions
        return format_excel(file_path)  # Add all necessary functions here

    # Handle other brands similarly
    # Add conditions for QuickMart, Carrefour, Naivas as needed

# Streamlit UI
def main():
    st.title("Welcome to Alkhemy Brands Data Cleaning Tool")
    st.sidebar.header("Menu")
    menu = ["Home", "Clean Data"]
    choice = st.sidebar.selectbox("Navigate", menu)

    if choice == "Home":
        st.subheader("Welcome!")
        st.write("Select an option from the menu to start.")
    
    elif choice == "Clean Data":
        st.subheader("Clean Data")
        brand_choice = st.selectbox(
            "Select a brand for data cleaning",
            ["SleekLady", "QuickMart", "Carrefour", "Naivas"]
        )

        if brand_choice:
            st.write(f"Upload your Excel file for {brand_choice}.")
            uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

            if uploaded_file:
                # Save uploaded file to a temporary location
                upload_dir = "uploaded_files"
                Path(upload_dir).mkdir(exist_ok=True)
                file_path = os.path.join(upload_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())

                st.write("File uploaded successfully! Starting cleaning process...")

                # Process and clean the data
                try:
                    cleaned_data = process_data_for_brand(brand_choice, file_path)
                    
                    # Provide download link for final Excel
                    final_file = "artifacts/final_excel/transformed_file.xlsx"
                    cleaned_data.to_excel(final_file, index=False)
                    st.success("Data cleaned successfully!")
                    st.download_button(
                        "Download Cleaned Excel File",
                        data=open(final_file, "rb"),
                        file_name="Cleaned_Data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
