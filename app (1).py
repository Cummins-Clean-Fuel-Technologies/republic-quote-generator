
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("republic_configurator_with_pricing.xlsx", sheet_name="Sheet1", header=None)
    df = df.iloc[2:].reset_index(drop=True)
    df.columns = pd.read_excel("republic_configurator_with_pricing.xlsx", sheet_name="Sheet1", header=None).iloc[1]
    return df[1:].reset_index(drop=True)

df = load_data()

st.title("Republic Services - Cummins Clean Fuel Technologies Configurator")
st.markdown("Generate a custom quote with part numbers and pricing.")

# Dropdown inputs
app_type = st.selectbox("Application Type", sorted(df["Application"].dropna().unique()))
body_mfg = st.selectbox("Body Manufacturer", sorted(df["BODY MFG INPUTS"].dropna().unique()))
body_model = st.selectbox("Body Model", sorted(df["BODY MODEL INPUTS"].dropna().unique()))
chassis_mfg = st.selectbox("Chassis Manufacturer", sorted(df["CHASSIS MANUFACTURE INPUTS"].dropna().unique()))
chassis_model = st.selectbox("Chassis Model", sorted(df["CHASSIS MODEL INPUTS"].dropna().unique()))
chassis_type = st.selectbox("Chassis Type", sorted(df["Chassis Type"].dropna().unique()))
cab_type = st.selectbox("Chassis Cab", sorted(df["CHASSIS CAB"].dropna().unique()))
mounting = st.selectbox("CNG Mounting", sorted(df["CNG MOUNTING INPUTS"].dropna().unique()))
system_type = st.selectbox("System Type", sorted(df["System Type"].dropna().unique()))
dge = st.selectbox("System DGE", sorted(df["System DGE"].dropna().unique()))

# Filter based on all selected inputs
query = (
    (df["Application"] == app_type) &
    (df["BODY MFG INPUTS"] == body_mfg) &
    (df["BODY MODEL INPUTS"] == body_model) &
    (df["CHASSIS MANUFACTURE INPUTS"] == chassis_mfg) &
    (df["CHASSIS MODEL INPUTS"] == chassis_model) &
    (df["Chassis Type"] == chassis_type) &
    (df["CHASSIS CAB"] == cab_type) &
    (df["CNG MOUNTING INPUTS"] == mounting) &
    (df["System Type"] == system_type) &
    (df["System DGE"] == dge)
)

result = df[query]

if not result.empty:
    st.success("Configuration found. Here is your quote:")

    st.write("### **Configuration Summary**")
    st.markdown(f"""
    - **Application:** {app_type}
    - **Body Manufacturer:** {body_mfg}
    - **Body Model:** {body_model}
    - **Chassis Manufacturer:** {chassis_mfg}
    - **Chassis Model:** {chassis_model}
    - **Chassis Type:** {chassis_type}
    - **Cab Type:** {cab_type}
    - **Mounting:** {mounting}
    - **System Type:** {system_type}
    - **DGE:** {dge}
    """)

    st.write("### **System Part Numbers**")
    st.write(result["System Part Numbers"].values[0])

    st.write("### **Pricing**")
    st.write(f"**Total Price:** ${result['Pricing:'].values[0]}")

else:
    st.warning("No matching configuration found. Please check your selections.")
