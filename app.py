# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our app
st.set_page_config(page_title="💿 Data Sweeper", layout='wide')
st.title("💿 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

df = None  # Ensure df is defined before usage
last_file_name = None  # Store the last file name

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            df = None  # Reset df to avoid errors
            continue  # Skip this file

        last_file_name = file.name  # Store the last file name

    # Only proceed if df is valid
    if df is not None:
        # Display info about the file
        st.write(f"**File Name:** {last_file_name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show 5 rows of our df
        st.write("🔍 Preview the Head of the DataFrame")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {last_file_name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {last_file_name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {last_file_name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

        # Choose Specific Columns to Keep or Convert
        st.subheader("🍭 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {last_file_name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Some Visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {last_file_name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the File -> CSV to Excel
        st.subheader("🔄️ Conversion Option")
        conversion_type = st.radio(f"Convert {last_file_name}", ["CSV", "Excel"], key=last_file_name)
        if st.button(f"Convert {last_file_name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = last_file_name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = last_file_name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"⬇️ Download {last_file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All Files processed!")
