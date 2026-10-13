
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# PAGE CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Crime Data Analysis",
    page_icon="🔎",
    layout="wide"
)

# ==========================
# PAGE HEADER
# ==========================

st.title("🔎 Crime Data Analysis Dashboard")

st.write(
    "Explore crime patterns, district distribution, "
    "crime hotspots, and case status using Python."
)

st.divider()

# ==========================
# CRIME DATASET
# ==========================

data = {
    "Crime ID": list(range(101, 121)),

    "Crime Type": [
        "Theft", "Assault", "Burglary", "Fraud", "Theft",
        "Robbery", "Assault", "Theft", "Fraud", "Burglary",
        "Theft", "Robbery", "Assault", "Fraud", "Theft",
        "Burglary", "Robbery", "Assault", "Theft", "Fraud"
    ],

    "Date": [
        "2025-01-05", "2025-01-10", "2025-02-12",
        "2025-02-15", "2025-03-01", "2025-03-05",
        "2025-03-20", "2025-04-01", "2025-04-10",
        "2025-04-15", "2025-05-02", "2025-05-10",
        "2025-05-18", "2025-06-01", "2025-06-05",
        "2025-06-12", "2025-07-01", "2025-07-08",
        "2025-07-15", "2025-08-01"
    ],

    "Time": [
        "10:00", "14:30", "18:00", "09:15", "20:00",
        "21:30", "16:00", "11:00", "13:00", "17:30",
        "19:00", "22:00", "15:00", "10:30", "18:45",
        "23:00", "20:15", "14:00", "12:30", "09:45"
    ],

    "Location": [
        "Market", "Bus Stand", "Mall", "Bank", "Market",
        "Railway Station", "College", "Market", "Bank",
        "Mall", "Market", "Railway Station", "College",
        "Bank", "Market", "Mall", "Railway Station",
        "College", "Market", "Bank"
    ],

    "District": [
        "North", "South", "East", "West", "North",
        "South", "East", "North", "West", "East",
        "North", "South", "East", "West", "North",
        "East", "South", "East", "North", "West"
    ],

    "Status": [
        "Solved", "Pending", "Solved", "Solved", "Pending",
        "Solved", "Pending", "Solved", "Solved", "Pending",
        "Solved", "Solved", "Pending", "Solved", "Solved",
        "Pending", "Solved", "Pending", "Solved", "Solved"
    ]
}

df = pd.DataFrame(data)

# ==========================
# DATA PREPROCESSING
# ==========================

df.drop_duplicates(inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.month_name()

# ==========================
# SIDEBAR FILTERS
# ==========================

st.sidebar.title("Dashboard Filters")

crime_types = st.sidebar.multiselect(
    "Select Crime Type",
    options=sorted(df["Crime Type"].unique()),
    default=sorted(df["Crime Type"].unique())
)

districts = st.sidebar.multiselect(
    "Select District",
    options=sorted(df["District"].unique()),
    default=sorted(df["District"].unique())
)

statuses = st.sidebar.multiselect(
    "Select Case Status",
    options=sorted(df["Status"].unique()),
    default=sorted(df["Status"].unique())
)

# Apply filters
filtered_df = df[
    df["Crime Type"].isin(crime_types)
    & df["District"].isin(districts)
    & df["Status"].isin(statuses)
]

# ==========================
# SUMMARY METRICS
# ==========================

st.header("Crime Overview")

total_crimes = len(filtered_df)

solved_cases = (
    filtered_df["Status"] == "Solved"
).sum()

pending_cases = (
    filtered_df["Status"] == "Pending"
).sum()

if not filtered_df.empty:
    top_location = filtered_df["Location"].mode().iloc[0]
else:
    top_location = "N/A"

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Crimes", total_crimes)
col2.metric("Solved Cases", int(solved_cases))
col3.metric("Pending Cases", int(pending_cases))
col4.metric("Top Reported Location", top_location)

st.divider()

# ==========================
# DISPLAY ANALYSIS
# ==========================

if filtered_df.empty:

    st.warning("No records match the selected filters.")

else:

    # --------------------------
    # GRAPH 1: CRIME TYPE
    # --------------------------

    st.subheader("Crime Type Distribution")

    crime_counts = filtered_df["Crime Type"].value_counts()

    st.bar_chart(crime_counts)

    # --------------------------
    # GRAPH 2: DISTRICT
    # --------------------------

    st.subheader("District-wise Crime Analysis")

    district_counts = filtered_df["District"].value_counts()

    st.bar_chart(district_counts)

    # --------------------------
    # GRAPH 3: CRIME STATUS
    # --------------------------

    st.subheader("Crime Status Distribution")

    status_counts = filtered_df["Status"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Solved vs Pending Cases")

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------
    # GRAPH 4: CRIME HOTSPOTS
    # --------------------------

    st.subheader("Location-wise Crime Hotspots")

    location_counts = filtered_df["Location"].value_counts()

    st.bar_chart(location_counts)

    # --------------------------
    # GRAPH 5: MONTHLY TREND
    # --------------------------

    st.subheader("Monthly Crime Trend")

    monthly_counts = (
        filtered_df.set_index("Date")
        .resample("MS")
        .size()
    )

    monthly_counts.index = monthly_counts.index.strftime("%b %Y")

    st.line_chart(monthly_counts)

# ==========================
# CRIME RECORDS TABLE
# ==========================

st.divider()

st.header("Crime Records")

display_df = filtered_df.copy()

display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

st.dataframe(
    display_df,
    use_container_width=True
)

# ==========================
# DOWNLOAD DATA
# ==========================

st.subheader("Download Crime Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Crime Data (CSV)",
    data=csv_data,
    file_name="crime_data.csv",
    mime="text/csv"
)

# ==========================
# PROJECT INSIGHTS
# ==========================

st.divider()

st.header("Project Insights")

if not filtered_df.empty:

    st.write(
        "**Most Common Crime Type:**",
        filtered_df["Crime Type"].mode().iloc[0]
    )

    st.write(
        "**Most Affected District:**",
        filtered_df["District"].mode().iloc[0]
    )

    st.write(
        "**Most Reported Location:**",
        filtered_df["Location"].mode().iloc[0]
    )

    st.write(
        "**Most Common Case Status:**",
        filtered_df["Status"].mode().iloc[0]
    )

# ==========================
# FOOTER
# ==========================

st.divider()

st.caption(
    "Crime Data Analysis Project | Python, Pandas, "
    "Matplotlib and Streamlit"
)

st.caption(
    "Note: This dashboard uses 20 sample crime records "
    "for academic demonstration. The records do not "
    "represent verified real-world crime statistics."
)
