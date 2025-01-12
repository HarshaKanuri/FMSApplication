import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page Config
st.set_page_config(page_title="Application Data Management", layout="wide")

# Sidebar Menu
with st.sidebar:
    st.image("https://cdn.freebiesupply.com/images/large/2x/wells-fargo-logo-transparent.png", width=100)
    st.title("APPLICATION DATA MANAGEMENT")
    st.markdown("### MAIN MENU")
    selected_page = st.selectbox(
        "Select a Page",
        ["Dashboard", "Feeds"]
    )
    st.markdown("### ACCOUNT")
    st.button("Account")
    st.button("Settings")
    st.button("Logout")

# Styling Functions
def feeds_status_color(status):
    if status == "Active":
        return "background-color: #d4edda; color: #155724;"
    elif status == "Inactive":
        return "background-color: #fff3cd; color: #856404;"
    elif status == "Error":
        return "background-color: #f8d7da; color: #721c24;"
    return ""

def transaction_status_color(status):
    if status == "Completed":
        return "background-color: #d4edda; color: #155724;"
    elif status == "Pending":
        return "background-color: #fff3cd; color: #856404;"
    elif status == "Failed":
        return "background-color: #f8d7da; color: #721c24;"
    return ""

# Setup GSheets connection
@st.cache_data
def get_gsheet_data(sheet_url):
    # Connect to Google Sheets using the streamlit_gsheets package
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Read data from the sheet
    data = conn.read(spreadsheet=sheet_url)

    return data

# Helper function to filter data by frequency
def filter_data_by_frequency(df, frequency):
    # Filter the data based on the 'Frequency' column
    df_filtered = df[df['Frequency'] == frequency]
    return df_filtered

# Main Content
if selected_page == "Dashboard":
    # Dashboard Header
    st.markdown(
        """
        <style>
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        </style>
        <div class="dashboard-header">
            <h1>Dashboard</h1>
            <div style="text-align: right;">
                <p>Hi! John Doe <span style="font-size: 24px;">👋</span></p>
                <p style="color: gray;">Good morning</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Snapshot Section
    st.markdown("### Snapshot")

    # Stats Data
    stats = [
        {"title": "Applications", "current": 72, "total": 95},
        {"title": "Datasets", "current": 102, "total": 135},
        {"title": "Feeds", "current": 381, "total": 404},
        {"title": "Alerts", "current": 12, "total": 24},
    ]

    # Responsive Metric Display
    cols = st.columns(len(stats))
    for idx, stat in enumerate(stats):
        with cols[idx]:
            st.metric(
                label=stat["title"],
                value=f"{stat['current']}/{stat['total']}",
                delta=f"{(stat['current'] / stat['total']) * 100:.1f}%",
            )
            st.progress(stat["current"] / stat["total"])

    # Transactional Log Table
    st.markdown("### Transactional Log")

    # Tabs for filtering frequency
    tabs = st.tabs(["Daily", "Hourly", "Weekly"])
    
    # URL of the Google Sheets document (replace with your own)
    url = "https://docs.google.com/spreadsheets/d/1hOTC_MTrWJ0PWg24zvmJFOX_SkSplHUAxXMu87QfpOw/edit?usp=sharing"
    
    # Fetch data from Google Sheets for Transactional Log
    df_transaction = get_gsheet_data(url)

    # Apply tab-specific filtering based on frequency
    with tabs[0]:  # Daily Tab
        frequency = "Daily"
        df_filtered_transaction = filter_data_by_frequency(df_transaction, frequency)
        styled_transaction_df = df_filtered_transaction.style.map(
            transaction_status_color, subset=["Status"]
        )
        st.dataframe(styled_transaction_df, use_container_width=True)

    with tabs[1]:  # Hourly Tab
        frequency = "Hourly"
        df_filtered_transaction = filter_data_by_frequency(df_transaction, frequency)
        styled_transaction_df = df_filtered_transaction.style.map(
            transaction_status_color, subset=["Status"]
        )
        st.dataframe(styled_transaction_df, use_container_width=True)

    with tabs[2]:  # Weekly Tab
        frequency = "Weekly"
        df_filtered_transaction = filter_data_by_frequency(df_transaction, frequency)
        styled_transaction_df = df_filtered_transaction.style.map(
            transaction_status_color, subset=["Status"]
        )
        st.dataframe(styled_transaction_df, use_container_width=True)

elif selected_page == "Feeds":
    # Feeds Page
    st.markdown("### Feeds")

    # Tabs for filtering frequency
    tabs = st.tabs(["Daily", "Hourly", "Weekly"])
    
    # URL of the Google Sheets document (replace with your own)
    url = "https://docs.google.com/spreadsheets/d/1K2YEA7OaHcLeGEKfklMZVFz6AuqP0W_AhtD8I4_zqIo/edit?usp=sharing"
    
    # Fetch data from Google Sheets for Feeds Log
    df_feeds = get_gsheet_data(url)

    # Apply tab-specific filtering based on frequency
    with tabs[0]:  # Daily Tab
        frequency = "Daily"
        df_filtered_feeds = filter_data_by_frequency(df_feeds, frequency)
        styled_feeds_df = df_filtered_feeds.style.map(feeds_status_color, subset=["Status"])
        st.dataframe(styled_feeds_df, use_container_width=True)

    with tabs[1]:  # Hourly Tab
        frequency = "Hourly"
        df_filtered_feeds = filter_data_by_frequency(df_feeds, frequency)
        styled_feeds_df = df_filtered_feeds.style.map(feeds_status_color, subset=["Status"])
        st.dataframe(styled_feeds_df, use_container_width=True)

    with tabs[2]:  # Weekly Tab
        frequency = "Weekly"
        df_filtered_feeds = filter_data_by_frequency(df_feeds, frequency)
        styled_feeds_df = df_filtered_feeds.style.map(feeds_status_color, subset=["Status"])
        st.dataframe(styled_feeds_df, use_container_width=True)

# Footer
st.markdown(
    """
    <style>
    .footer {
        text-align: center;
        font-size: 12px;
        color: gray;
        margin-top: 2rem;
    }
    </style>
    <div class="footer">
        <p>© 2025 Application Data Management. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True,
)