




import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials

# ✅ DEBUG START
# st.write("Secrets loaded:", "gcp_service_account" in st.secrets)
# st.write(st.secrets)
# ✅ DEBUG END

# ---------------------------
# 🔐 Google Sheets Connection
# ---------------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

service_account_info = json.loads(st.secrets["gcp_credentials"])
# service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
# creds = Credentials.from_service_account_info(
#     dict(st.secrets["gcp_service_account"]),
#     scopes=scope
# )
client = gspread.authorize(creds)

# ---------------------------
# 📌 FIXED TAB NAME
# ---------------------------
spreadsheet = client.open("LTV Breach Cases")
sheet = spreadsheet.worksheet("LTV Breach - 30_Mar")

# ---------------------------
# 📥 Load Data (safe method)
# ---------------------------
data = sheet.get_all_values()

headers = data[0]

# Clean headers
clean_headers = []
for i, h in enumerate(headers):
    if h == "":
        clean_headers.append(f"column_{i}")
    else:
        clean_headers.append(h)

rows = data[1:]
df = pd.DataFrame(rows, columns=clean_headers)

# ---------------------------
# 🎯 UI
# ---------------------------
st.title("🔍 LTV Breach Checker")

loan_id = st.text_input("Enter Loan ID (sec_los_id)")

# ---------------------------
# 🔍 Column Mapping (NEW)
# ---------------------------
column_mapping = {
    "Final_NW": "Net weight (in gms)",
    "sec_los_id": "LOS ID",
    "total_sanction": "Total sanctioned loan amount",
    "Total_OS_LTV": "Total outstanding LTV (as of today)",
    "Final_Min_Amt_to_be_Collected": "Minimum amount to be repayed",
    "Final_Max_Amt_to_be_Collected": "Maximum amount to be repayed"
}

# ---------------------------
# 🔍 Search Logic
# ---------------------------
if loan_id:

    if "sec_los_id" not in df.columns:
        st.error("❌ 'sec_los_id' column not found")
    else:
        result = df[df["sec_los_id"].astype(str) == loan_id]

        if not result.empty:

            row = result.iloc[0]

            # ✅ Resolution check (but NOT displayed)
            if "Resolution_Status" in df.columns and str(row["Resolution_Status"]).strip().lower() == "resolved":
                st.success("✅ No repayment required for this LOS ID")
            else:
                st.success("✅ Loan found")

                st.write("### 📄 Loan Details")

                # ✅ Show mapped column names
                for actual_col, display_name in column_mapping.items():
                    if actual_col in row:
                        st.write(f"**{display_name}** : {row[actual_col]}")

        else:
            st.error("❌ Loan ID not found")
