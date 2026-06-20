import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Instrument Stock Finder")

# Upload files
@st.cache_data
def load_data():

    devices_url = "..."

    stock_url = "..."

    devices_df = pd.read_excel(devices_url)

    stock_df = pd.read_excel(stock_url)

    return devices_df, stock_df


    devices_df, stock_df = load_data()


    # Remove spaces from column names
    devices_df.columns = devices_df.columns.str.strip()
    stock_df.columns = stock_df.columns.str.strip()

    tag = st.text_input("Enter Tag Name")

    if st.button("Search"):

        device = devices_df[
            devices_df["Tag Name"].astype(str).str.upper()
            ==
            tag.upper()
        ]

        if device.empty:

            st.error("Tag not found")

        else:

            instrument_range = str(
                device.iloc[0]["Instrument Range"]
            ).strip()

            size = str(
                device.iloc[0]["Size"]
            ).strip()

            st.subheader("Device Information")

            st.write("Tag Name :", tag)
            st.write("Range :", instrument_range)
            st.write("Size :", size)

            matches = stock_df[
                (
                    stock_df["Instrument Range"]
                    .astype(str)
                    .str.strip()
                    ==
                    instrument_range
                )
                &
                (
                    stock_df["Size"]
                    .astype(str)
                    .str.strip()
                    ==
                    size
                )
            ]

            if matches.empty:

                st.warning(
                    "No matching stock items found"
                )

            else:

                st.subheader(
                    "Matching Stock Codes"
                )

                result = matches[
                    ["Code", "Description"]
                ]

                st.dataframe(
                    result,
                    use_container_width=True
                )

                # Excel export

                output = BytesIO()

                with pd.ExcelWriter(
                    output,
                    engine='xlsxwriter'
                ) as writer:

                    result.to_excel(
                        writer,
                        index=False,
                        sheet_name='Result'
                    )

                excel_data = output.getvalue()

                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"{tag}_result.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
