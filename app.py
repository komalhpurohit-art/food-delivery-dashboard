import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Food Delivery Analytics Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# WHITE + ORANGE UI
# =========================================================
st.markdown("""
<style>
    /* Main application */
    .stApp {
        background-color: #ffffff;
        color: #222222;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #f28c28;
    }

    section[data-testid="stSidebar"] * {
        color: #222222 !important;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #e87500 !important;
    }

    /* Main title */
    .main-title {
        color: #e87500;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #666666;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #f28c28;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(232,117,0,0.10);
    }

    div[data-testid="stMetric"] label {
        color: #555555 !important;
    }

    div[data-testid="stMetric"] div {
        color: #e87500 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #f28c28;
        color: white;
        border: none;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: #e87500;
        color: white;
    }

    /* Success message */
    div[data-testid="stAlert"] {
        background-color: #fff4e6;
        border-left: 5px solid #f28c28;
        color: #e87500;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border: 2px solid #f28c28;
        border-radius: 10px;
    }

    /* Horizontal line */
    hr {
        border-color: #f28c28 !important;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    # Try different possible CSV names
    possible_files = [
        "food_delivery_data.csv",
        "food_delivery.csv",
        "Food_Delivery_Data.csv",
        "Food_Delivery.csv",
        "data.csv"
    ]

    for file in possible_files:
        try:
            df = pd.read_csv(file)
            if len(df) > 0:
                return df
        except:
            pass

    # -----------------------------------------------------
    # Backup demo dataset
    # -----------------------------------------------------
    np.random.seed(42)

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
        "Biryani": ["Chicken Biryani", "Veg Biryani"],
        "Burger": ["Paneer Burger", "Veg Burger"],
        "Chinese": ["Manchurian", "Fried Rice", "Hakka Noodles"],
        "Dessert": ["Ice Cream", "Gulab Jamun", "Brownie"],
        "Gujarati": ["Dal Dhokli", "Gujarati Thali", "Kathiyawadi Thali"],
        "Pizza": ["Margherita Pizza", "Farmhouse Pizza"],
        "South Indian": ["Masala Dosa", "Idli"]
    }

    payment_methods = [
        "Credit Card",
        "Wallet",
        "UPI",
        "Debit Card",
        "Cash on Delivery"
    ]

    n = 200

    dates = pd.date_range(
        start="2026-01-01",
        periods=n,
        freq="D"
    )

    selected_categories = np.random.choice(categories, n)

    items = [
        np.random.choice(food_items[c])
        for c in selected_categories
    ]

    quantities = np.random.randint(1, 4, n)

    prices = []

    for item in items:
        if "Biryani" in item:
            prices.append(np.random.choice([199, 249, 299]))
        elif "Burger" in item:
            prices.append(np.random.choice([149, 179, 199]))
        elif "Pizza" in item:
            prices.append(np.random.choice([249, 299, 349]))
        elif "Dosa" in item or "Idli" in item:
            prices.append(np.random.choice([99, 129, 149]))
        elif "Thali" in item:
            prices.append(np.random.choice([199, 249, 299]))
        elif "Dhokli" in item:
            prices.append(np.random.choice([129, 149]))
        elif "Noodles" in item or "Fried Rice" in item or "Manchurian" in item:
            prices.append(np.random.choice([129, 149, 159]))
        else:
            prices.append(np.random.choice([79, 89, 99, 129]))

    df = pd.DataFrame({
        "Order_ID": [f"FD{i:04d}" for i in range(1, n + 1)],
        "Date": dates,
        "Customer_ID": [
            f"C{np.random.randint(1, 100):03d}"
            for _ in range(n)
        ],
        "Area": np.random.choice(areas, n),
        "Food_Category": selected_categories,
        "Food_Item": items,
        "Quantity": quantities,
        "Price": prices,
        "Payment_Method": np.random.choice(payment_methods, n),
        "Delivery_Time_Min": np.random.randint(15, 55, n),
        "Rating": np.round(
            np.clip(np.random.normal(4.25, 0.55, n), 2.5, 5),
            1
        ),
        "Order_Status": np.random.choice(
            ["Delivered", "Delivered", "Delivered", "Cancelled"],
            n
        )
    })

    df["Order_Value"] = df["Quantity"] * df["Price"]

    return df


df = load_data()


# =========================================================
# CLEAN DATA
# =========================================================
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

numeric_columns = [
    "Quantity",
    "Price",
    "Order_Value",
    "Delivery_Time_Min",
    "Rating"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill missing values
for col in ["Area", "Food_Category", "Food_Item",
            "Payment_Method", "Order_Status"]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.markdown(
    "<h2 style='color:#e87500;'>🔎 Filters</h2>",
    unsafe_allow_html=True
)

areas = sorted(df["Area"].dropna().unique
