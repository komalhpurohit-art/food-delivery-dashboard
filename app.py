import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Food Delivery Analytics Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# WHITE + ORANGE THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
    color: #222222;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 2px solid #f28c28;
}

section[data-testid="stSidebar"] * {
    color: #222222 !important;
}

h1, h2, h3, h4 {
    color: #e87500 !important;
}

.main-title {
    color: #e87500;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    color: #666666;
    font-size: 17px;
    margin-bottom: 25px;
}

.metric-card {
    background-color: #ffffff;
    border: 2px solid #f28c28;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 8px rgba(232,117,0,0.10);
}

.metric-label {
    color: #666666;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #e87500;
    font-size: 28px;
    font-weight: 800;
}

.stButton > button {
    background-color: #f28c28;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #e87500;
    color: white;
}

hr {
    border-color: #f28c28 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🍔 Food Delivery Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze orders, revenue, customers, delivery performance and food preferences.</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    possible_files = [
        "food_delivery_data.csv",
        "Food_Delivery.csv",
        "Food Delivery Data.csv",
        "Food_Delivery_Data.csv",
        "data.csv"
    ]

    # Try to load CSV
    for file in possible_files:
        try:
            df = pd.read_csv(file)

            if len(df) > 0:
                return df

        except Exception:
            pass


    # ========================================================
    # DEMO DATA
    # ========================================================

    np.random.seed(42)

    n = 500

    areas = [
        "Ahmedabad",
        "Bopal",
        "Chandkheda",
        "Gandhinagar",
        "Maninagar",
        "Navrangpura",
        "Vastrapur",
        "Satellite"
    ]

    categories = [
        "Biryani",
        "Burger",
        "Chinese",
        "Dessert",
        "Gujarati",
        "Pizza",
        "South Indian"
    ]

    food_items = {
        "Biryani": [
            "Chicken Biryani",
            "Veg Biryani"
        ],
        "Burger": [
            "Paneer Burger",
            "Veg Burger"
        ],
        "Chinese": [
            "Manchurian",
            "Fried Rice",
            "Hakka Noodles"
        ],
        "Dessert": [
            "Ice Cream",
            "Gulab Jamun",
            "Brownie"
        ],
        "Gujarati": [
            "Dhokli",
            "Gujarati Thali",
            "Kathiyawadi Thali"
        ],
        "Pizza": [
            "Margherita Pizza",
            "Farmhouse Pizza"
        ],
        "South Indian": [
            "Masala Dosa",
            "Idli"
        ]
    }

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Wallet",
        "Cash on Delivery"
    ]

    statuses = [
        "Delivered",
        "Delivered",
        "Delivered",
        "Delivered",
        "Cancelled"
    ]

    dates = pd.date_range(
        start="2026-01-01",
        end="2026-09-30",
        periods=n
    )

    selected_categories = np.random.choice(
        categories,
        n
    )

    items = []

    prices = []

    for category in selected_categories:

        item = np.random.choice(
            food_items[category]
        )

        items.append(item)

        if "Biryani" in item:
            price = np.random.choice([199, 249, 299])

        elif "Burger" in item:
            price = np.random.choice([149, 179, 199])

        elif "Pizza" in item:
            price = np.random.choice([299, 349, 399])

        elif "Dosa" in item or "Idli" in item:
            price = np.random.choice([99, 129, 149])

        elif "Thali" in item:
            price = np.random.choice([199, 249, 299])

        elif "Dhokli" in item:
            price = np.random.choice([129, 149])

        elif "Noodles" in item or "Manchurian" in item:
            price = np.random.choice([129, 149, 159])

        else:
            price = np.random.choice([79, 89, 99, 129])

        prices.append(price)

    quantities = np.random.randint(1, 5, n)

    df = pd.DataFrame({
        "Order_ID": [
            f"FD{10001 + i}"
            for i in range(n)
        ],

        "Date": dates,

        "Customer_ID": [
            f"C{np.random.randint(100, 999):03d}"
            for _ in range(n)
        ],

        "Area": np.random.choice(
            areas,
            n
        ),

        "Food_Category": selected_categories,

        "Food_Item": items,

        "Quantity": quantities,

        "Price": prices,

        "Payment_Method": np.random.choice(
            payment_methods,
            n
        ),

        "Delivery_Time_Min": np.random.randint(
            15,
            61,
            n
        ),

        "Rating": np.round(
            np.clip(
                np.random.normal(
                    4.25,
                    0.55,
                    n
                ),
                2.5,
                5
            ),
            1
        ),

        "Order_Status": np.random.choice(
            statuses,
            n
        )
    })

    df["Order_Value"] = (
        df["Quantity"] *
        df["Price"]
    )

    return df


df = load_data()


# ============================================================
# DATA CLEANING
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
)

required_columns = [
    "Date",
    "Area",
    "Food_Category",
    "Food_Item",
    "Quantity",
    "Price",
    "Payment_Method",
    "Delivery_Time_Min",
    "Rating",
    "Order_Status"
]

for col in required_columns:

    if col not in df.columns:

        if col in [
            "Quantity",
            "Price",
            "Delivery_Time_Min",
            "Rating"
        ]:
            df[col] = 0

        else:
            df[col] = "Unknown"


df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

numeric_columns = [
    "Quantity",
    "Price",
    "Delivery_Time_Min",
    "Rating"
]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


df["Quantity"] = df["Quantity"].fillna(1)
df["Price"] = df["Price"].fillna(0)
df["Delivery_Time_Min"] = df[
    "Delivery_Time_Min"
].fillna(
    df["Delivery_Time_Min"].median()
)

df["Rating"] = df["Rating"].fillna(
    df["Rating"].median()
)

df["Area"] = df["Area"].fillna("Unknown")
df["Food_Category"] = df["Food_Category"].fillna("Unknown")
df["Food_Item"] = df["Food_Item"].fillna("Unknown")
df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")
df["Order_Status"] = df["Order_Status"].fillna("Unknown")

df["Order_Value"] = (
    df["Quantity"] *
    df["Price"]
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown(
    "<h2>🔎 Filters</h2>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# Date filter

valid_dates = df["Date"].dropna()

if len(valid_dates) > 0:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

else:

    date_range = None


# Area filter

area_options = sorted(
    df["Area"].dropna().unique().tolist()
)

selected_areas = st.sidebar.multiselect(
    "📍 Area",
    area_options,
    default=area_options
)


# Category filter

category_options = sorted(
    df["Food_Category"].dropna().unique().tolist()
)

selected_categories_filter = st.sidebar.multiselect(
    "🍔 Food Category",
    category_options,
    default=category_options
)


# Payment filter

payment_options = sorted(
    df["Payment_Method"].dropna().unique().tolist()
)

selected_payments = st.sidebar.multiselect(
    "💳 Payment Method",
    payment_options,
    default=payment_options
)


# Status filter

status_options = sorted(
    df["Order_Status"].dropna().unique().tolist()
)

selected_statuses = st.sidebar.multiselect(
    "📦 Order Status",
    status_options,
    default=status_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if date_range and len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        &
        (filtered_df["Date"] <= end_date)
    ]


filtered_df = filtered_df[
    filtered_df["Area"].isin(selected_areas)
]

filtered_df = filtered_df[
    filtered_df["Food_Category"].isin(
        selected_categories_filter
    )
]

filtered_df = filtered_df[
    filtered_df["Payment_Method"].isin(
        selected_payments
    )
]

filtered_df = filtered_df[
    filtered_df["Order_Status"].isin(
        selected_statuses
    )
]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = len(filtered_df)

total_revenue = filtered_df["Order_Value"].sum()

average_order_value = (
    filtered_df["Order_Value"].mean()
    if total_orders > 0
    else 0
)

average_delivery = (
    filtered_df["Delivery_Time_Min"].mean()
    if total_orders > 0
    else 0
)

average_rating = (
    filtered_df["Rating"].mean()
    if total_orders > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">📦 Total Orders</div>
            <div class="metric-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">💰 Total Revenue</div>
            <div class="metric-value">₹{total_revenue:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🧾 Avg Order Value</div>
            <div class="metric-value">₹{average_order_value:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🛵 Avg Delivery</div>
            <div class="metric-value">{average_delivery:.1f} min</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">⭐ Avg Rating</div>
            <div class="metric-value">{average_rating:.2f}/5</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("---")


# ============================================================
# NO DATA MESSAGE
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data available for the selected filters. "
        "Please change the filters."
    )

    st.stop()


# ============================================================
# REVENUE TREND
# ============================================================

st.subheader("📈 Revenue Trend")

daily_revenue = (
    filtered_df
    .groupby("Date", as_index=False)["Order_Value"]
    .sum()
    .sort_values("Date")
)

fig_revenue = px.line(
    daily_revenue,
    x="Date",
    y="Order_Value",
    markers=True,
    title="Daily Revenue"
)

fig_revenue.update_traces(
    line=dict(color="#f28c28", width=3),
    marker=dict(color="#e87500")
)

fig_revenue.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#222222"),
    xaxis_title="Date",
    yaxis_title="Revenue (₹)"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)


# ============================================================
# AREA + CATEGORY
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📍 Revenue by Area")

    area_revenue = (
        filtered_df
        .groupby("Area", as_index=False)["Order_Value"]
        .sum()
        .sort_values(
            "Order_Value",
            ascending=False
        )
    )

    fig_area = px.bar(
        area_revenue,
        x="Area",
        y="Order_Value",
        text_auto=".2s",
        title="Area-wise Revenue"
    )

    fig_area.update_traces(
        marker_color="#f28c28"
    )

    fig_area.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#222222"),
        xaxis_title="Area",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_area,
        use_container_width=True
    )


with col2:

    st.subheader("🍔 Food Category")

    category_revenue = (
        filtered_df
        .groupby(
            "Food_Category",
            as_index=False
        )["Order_Value"]
        .sum()
        .sort_values(
            "Order_Value",
            ascending=False
        )
    )

    fig_category = px.pie(
        category_revenue,
        names="Food_Category",
        values="Order_Value",
        title="Revenue by Food Category",
        hole=0.45
    )

    fig_category.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#222222")
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ============================================================
# PAYMENT + STATUS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("💳 Payment Method")

    payment_data = (
        filtered_df
        .groupby(
            "Payment_Method",
            as_index=False
        )
        .size()
        .rename(columns={"size": "Orders"})
    )

    fig_payment = px.bar(
        payment_data,
        x="Payment_Method",
        y="Orders",
        text="Orders",
        title="Orders by Payment Method"
    )

    fig_payment.update_traces(
        marker_color="#e87500"
    )

    fig_payment.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#222222"),
        xaxis_title="Payment Method",
        yaxis_title="Orders"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )


with col2:

    st.subheader("📦 Order Status")

    status_data = (
        filtered_df
        .groupby(
            "Order_Status",
            as_index=False
        )
        .size()
        .rename(columns={"size": "Orders"})
    )

    fig_status = px.pie(
        status_data,
        names="Order_Status",
        values="Orders",
        title="Order Status Distribution",
        hole=0.45
    )

    fig_status.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#222222")
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# ============================================================
# TOP FOOD ITEMS
# ============================================================

st.subheader("🏆 Top Food Items")

top_items = (
    filtered_df
    .groupby(
        "Food_Item",
        as_index=False
    )
    .agg(
        Orders=("Food_Item", "count"),
        Quantity=("Quantity", "sum"),
        Revenue=("Order_Value", "sum")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)

fig_items = px.bar(
    top_items.sort_values("Revenue"),
    x="Revenue",
    y="Food_Item",
    orientation="h",
    text_auto=".2s",
    title="Top 10 Food Items by Revenue"
)

fig_items.update_traces(
    marker_color="#f28c28"
)

fig_items.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#222222"),
    xaxis_title="Revenue (₹)",
    yaxis_title="Food Item"
)

st.plotly_chart(
    fig_items,
    use_container_width=True
)


# ============================================================
# DELIVERY PERFORMANCE
# ============================================================

st.subheader("🛵 Delivery Performance")

delivery_area = (
    filtered_df
    .groupby(
        "Area",
        as_index=False
    )
    .agg(
        Avg_Delivery_Time=(
            "Delivery_Time_Min",
            "mean"
        ),
        Avg_Rating=(
            "Rating",
            "mean"
        )
    )
    .sort_values(
        "Avg_Delivery_Time"
    )
)

fig_delivery = px.bar(
    delivery_area,
    x="Area",
    y="Avg_Delivery_Time",
    text_auto=".1f",
    title="Average Delivery Time by Area"
)

fig_delivery.update_traces(
    marker_color="#e87500"
)

fig_delivery.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#222222"),
    xaxis_title="Area",
    yaxis_title="Average Delivery Time (Minutes)"
)

st.plotly_chart(
    fig_delivery,
    use_container_width=True
)


# ============================================================
# DATA TABLE
# ============================================================

st.subheader("📋 Order Details")

display_columns = [
    "Order_ID",
    "Date",
    "Customer_ID",
    "Area",
    "Food_Category",
    "Food_Item",
    "Quantity",
    "Price",
    "Order_Value",
    "Payment_Method",
    "Delivery_Time_Min",
    "Rating",
    "Order_Status"
]

available_columns = [
    col
    for col in display_columns
    if col in filtered_df.columns
]

display_df = filtered_df[
    available_columns
].copy()

st.dataframe(
    display_df,
    use_container_width=True,
    height=400
)


# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="food_delivery_filtered_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#777777;
        padding:15px;
    ">
        🍔 Food Delivery Analytics Dashboard |
        Built with Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True
            )
