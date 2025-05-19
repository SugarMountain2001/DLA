
import streamlit as st
import pandas as pd

def load_excel(file):
    try:
        return pd.read_excel(file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def main():
    st.title("Library Inventory Comparison Tool")

    st.markdown("Upload your **export file** from the library system and the **scanned inventory file** from your wand.")

    export_file = st.file_uploader("Upload Horizon Export File", type=["xlsx"])
    scanned_file = st.file_uploader("Upload Scanned Inventory File", type=["xlsx"])

    if export_file and scanned_file:
        export_df = load_excel(export_file)
        scanned_df = load_excel(scanned_file)

        if export_df is not None and scanned_df is not None:
            try:
                export_df["Barcode"] = export_df["Barcode"].astype(str)
                scanned_df["Barcode"] = scanned_df["Barcode"].astype(str)

                filtered_export = export_df[export_df["Item Status"].isin(["Checked In", "Lost"])]
                missing_items = filtered_export[~filtered_export["Barcode"].isin(scanned_df["Barcode"])]

                st.success(f"Comparison complete. {len(missing_items)} items not found in scanned inventory.")
                st.dataframe(missing_items)

                csv = missing_items.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Missing Items Report",
                    data=csv,
                    file_name="missing_items.csv",
                    mime="text/csv",
                )

            except KeyError as e:
                st.error(f"Missing expected column: {e}")

if __name__ == "__main__":
    main()
