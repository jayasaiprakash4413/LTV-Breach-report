# # import streamlit as st
# # import pandas as pd
# # import gspread
# # from google.oauth2.service_account import Credentials
# # # from oauth2client.service_account import ServiceAccountCredentials

# # # ---------------------------
# # # 🔐 Google Sheets Connection
# # # ---------------------------
# # scope = [
# #     "https://www.googleapis.com/auth/spreadsheets",
# #     "https://www.googleapis.com/auth/drive"
# # ]

# # creds = Credentials.from_service_account_file(
# #     "credentials.json",
# #     scopes=scope
# # )
# # client = gspread.authorize(creds)

# # # Open your sheet
# # sheet = client.open("LTV Breach Cases").sheet1

# # # Load data into dataframe
# # data = sheet.get_all_records()
# # df = pd.DataFrame(data)

# # # ---------------------------
# # # 🎯 Streamlit UI
# # # ---------------------------
# # st.title("🔍 Loan Details Lookup")

# # # Input box
# # loan_id = st.text_input("Enter Loan ID")

# # # Search logic
# # if loan_id:
# #     result = df[df["sec_los_id"].astype(str) == loan_id]

# #     if not result.empty:
# #         st.success("Loan found ✅")
# #         st.dataframe(result)
# #     else:
# #         st.error("Loan ID not found ❌")






# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials

# # ---------------------------
# # 🔐 Google Sheets Connection
# # ---------------------------
# scope = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# creds = Credentials.from_service_account_file(
#     "credentials.json",
#     scopes=scope
# )

# client = gspread.authorize(creds)

# # Open spreadsheet
# spreadsheet = client.open("LTV Breach Cases")

# # ---------------------------
# # 📌 Get all sheet tabs
# # ---------------------------
# worksheets = spreadsheet.worksheets()
# sheet_names = [ws.title for ws in worksheets]

# # ---------------------------
# # 🎯 Streamlit UI
# # ---------------------------
# st.title("🔍 Loan Details Lookup")

# # Dropdown to select tab
# selected_tab = st.selectbox("Select Sheet Tab", sheet_names)

# # Load selected sheet
# sheet = spreadsheet.worksheet(selected_tab)
# data = sheet.get_all_records()
# df = pd.DataFrame(data)

# # Input Loan ID
# loan_id = st.text_input("Enter Loan ID (sec_los_id)")

# # ---------------------------
# # 🔍 Search Logic
# # ---------------------------
# if loan_id:

#     # Check if column exists
#     if "sec_los_id" not in df.columns:
#         st.error("❌ 'sec_los_id' column not found in this tab")
#     else:
#         result = df[df["sec_los_id"].astype(str) == loan_id]

#         if not result.empty:

#             # ✅ Select only required columns
#             required_cols = [
#                 "Final_NW",
#                 "sec_los_id",
#                 "total_sanction",
#                 "Total_OS_LTV",
#                 "Resolution_Status",
#                 "Final_Min_Amt_to_be_Collected",
#                 "Final_Max_Amt_to_be_Collected"
#             ]

#             # Handle missing columns safely
#             available_cols = [col for col in required_cols if col in result.columns]

#             filtered_result = result[available_cols]

#             st.success(f"✅ Loan found in '{selected_tab}'")

#             # Display nicely
#             row = filtered_result.iloc[0]

#             st.write("### 📄 Loan Details")
#             for col in available_cols:
#                 st.write(f"**{col}** : {row[col]}")

#         else:
#             st.error("❌ Loan ID not found in selected tab")






# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials

# # ---------------------------
# # 🔐 Google Sheets Connection
# # ---------------------------
# scope = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# creds = Credentials.from_service_account_file(
#     "credentials.json",
#     scopes=scope
# )

# client = gspread.authorize(creds)

# # ---------------------------
# # 📌 FIXED TAB NAME (CHANGE HERE)
# # ---------------------------
# spreadsheet = client.open("LTV Breach Cases")

# sheet = spreadsheet.worksheet("LTV Breach - 30_Mar")  # 👈 FIXED TAB

# # ---------------------------
# # 📥 Load Data (safe method)
# # ---------------------------
# data = sheet.get_all_values()

# headers = data[0]

# # Clean headers (handle blanks)
# clean_headers = []
# for i, h in enumerate(headers):
#     if h == "":
#         clean_headers.append(f"column_{i}")
#     else:
#         clean_headers.append(h)

# rows = data[1:]
# df = pd.DataFrame(rows, columns=clean_headers)

# # ---------------------------
# # 🎯 UI
# # ---------------------------
# st.title("🔍 Loan Details Lookup")

# loan_id = st.text_input("Enter Loan ID (sec_los_id)")

# # ---------------------------
# # 🔍 Search Logic
# # ---------------------------
# if loan_id:

#     if "sec_los_id" not in df.columns:
#         st.error("❌ 'sec_los_id' column not found")
#     else:
#         result = df[df["sec_los_id"].astype(str) == loan_id]

#         if not result.empty:

#             row = result.iloc[0]

#             # ✅ Check Resolution Status
#             if "Resolution_Status" in df.columns and str(row["Resolution_Status"]).strip().lower() == "resolved":
#                 st.success("✅ Los id issues resolved")
#             else:
#                 # Show required fields
#                 required_cols = [
#                     "Final_NW",
#                     "sec_los_id",
#                     "total_sanction",
#                     "Total_OS_LTV",
#                     "Resolution_Status",
#                     "Final_Min_Amt_to_be_Collected",
#                     "Final_Max_Amt_to_be_Collected"
#                 ]

#                 available_cols = [col for col in required_cols if col in result.columns]

#                 st.success("✅ Loan found")

#                 st.write("### 📄 Loan Details")
#                 for col in available_cols:
#                     st.write(f"**{col}** : {row[col]}")

#         else:
#             st.error("❌ Loan ID not found")






import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------
# 🔐 Google Sheets Connection
# ---------------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
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
