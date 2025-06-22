import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Spendr", page_icon="🪙", layout="centered")

# Function to set dark background using encoded local image
def set_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #E0E0E0;
    }}
    h1, h2, h3, h4, h5, h6, label, p, span, div {{
        color: #E0E0E0 !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #00BFFF, #0066CC);
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input {{
        background-color: rgba(30, 144, 255, 0.2);
        color: #E0E0E0;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #00BFFF;
    }}
    .stSelectbox>div>select {{
        background-color: rgba(30, 144, 255, 0.2);
        color: #E0E0E0;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #00BFFF;
    }}
    .css-1aumxhk {{
        background-color: rgba(30, 144, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
    }}
    /* Sidebar styling - Updated to golden gradient */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #D4AF37 0%, #996515 100%);
        color: white;
    }}
    .sidebar .sidebar-content {{
        color: white;
    }}
    /* Radio button styling for golden theme */
    div[role="radiogroup"] > label {{
        background-color: rgba(212, 175, 55, 0.2);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px 0;
        transition: all 0.3s;
    }}
    div[role="radiogroup"] > label:hover {{
        background-color: rgba(212, 175, 55, 0.4);
    }}
    div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {{
        background-color: rgba(153, 101, 21, 0.6);
        border-left: 4px solid #D4AF37;
        font-weight: bold;
    }}
    /* Metric styling for golden theme */
    [data-testid="stMetric"] {{
        background-color: rgba(153, 101, 21, 0.3);
        border-radius: 8px;
        padding: 10px;
        border-left: 3px solid #D4AF37;
    }}
    [data-testid="stMetricLabel"] {{
        color: #D4AF37 !important;
    }}
    [data-testid="stMetricValue"] {{
        color: white !important;
    }}
    /* Coin logo styling */
    .coin-logo {{
        filter: drop-shadow(0 0 5px rgba(212, 175, 55, 0.7));
        transition: transform 0.3s;
    }}
    .coin-logo:hover {{
        transform: rotate(15deg);
    }}
    /* Loading bar styling */
    .gold-loading-bar {{
        height: 8px;
        background: linear-gradient(90deg, #D4AF37, #F1C40F, #D4AF37);
        border-radius: 4px;
        width: 100%;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }}
    .gold-loading-bar::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 5s infinite;
    }}
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    /* Wider chart styling */
    .stPlotlyChart {{
        width: 100% !important;
    }}
    /* Delete button styling */
    .delete-button {{
        background: linear-gradient(135deg, #FF0000, #990000) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        margin-top: 20px !important;
    }}
    /* About page styling */
    .about-card {{
        background: linear-gradient(135deg, rgba(30, 144, 255, 0.2), rgba(0, 102, 204, 0.2)) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        border-left: 5px solid #D4AF37 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }}
    .about-header {{
        color: #D4AF37 !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        font-size: 2.5rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3) !important;
    }}
    .about-subheader {{
        color: #00BFFF !important;
        border-bottom: 2px solid #D4AF37 !important;
        padding-bottom: 5px !important;
        margin-top: 20px !important;
    }}
    .skill-pill {{
        display: inline-block !important;
        background: rgba(212, 175, 55, 0.3) !important;
        color: #D4AF37 !important;
        padding: 5px 15px !important;
        border-radius: 20px !important;
        margin: 5px !important;
        font-weight: bold !important;
        border: 1px solid #D4AF37 !important;
    }}
    .social-icon {{
        font-size: 30px !important;
        margin: 10px !important;
        color: #00BFFF !important;
        transition: all 0.3s !important;
    }}
    .social-icon:hover {{
        color: #D4AF37 !important;
        transform: scale(1.2) !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set background
set_bg_from_local("newbg.png")

# CSV file path
CSV_FILE = "expenses.csv"

# Initialize CSV if not exists
def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(CSV_FILE, index=False)

# Load existing expenses - FIXED VERSION
def load_expenses():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    df = df.dropna(subset=['Date'])
    return df

# Save a new expense
def save_expense(date, category, amount, description):
    if amount <= 0:
        st.error("Amount must be greater than 0! Please enter a valid amount.")
        return False
    
    df = load_expenses()
    if isinstance(date, str):
        date = pd.to_datetime(date).date()
    elif hasattr(date, 'date'):
        date = date.date()
    
    new_data = pd.DataFrame([[date, category, amount, description]], 
                            columns=["Date", "Category", "Amount", "Description"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return True

# Edit an expense by index
def update_expense(index, date, category, amount, description):
    if amount <= 0:
        st.error("Amount must be greater than 0! Please enter a valid amount.")
        return False
    
    df = load_expenses()
    if 0 <= index < len(df):
        if isinstance(date, str):
            date = pd.to_datetime(date).date()
        elif hasattr(date, 'date'):
            date = date.date()
        df.loc[index] = [date, category, amount, description]
        df.to_csv(CSV_FILE, index=False)
        return True
    return False

# Delete all expenses
def delete_all_expenses():
    try:
        os.remove(CSV_FILE)
        init_csv()
        return True
    except:
        return False

# Loading Page
def loading_screen():
    st.markdown("""<h1 style='text-align:center; font-size: 72px;'></h1>""", unsafe_allow_html=True)

# Add Expense
def add_expense():
    st.subheader("➕ Add a New Expense")
    date = st.date_input("Date", datetime.now(), key="date_picker")
    category = st.selectbox("Category", ["Food", "Transport", "Stationery", "Internet", "Recreation", "Other"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    if st.button("Add Expense", key="add_expense_button"):
        if save_expense(date, category, amount, description):
            st.success("Expense added successfully!")
            st.balloons()

# Create colorful Plotly pie chart
def create_pie_chart(data, title):
    colors = px.colors.qualitative.Vivid + px.colors.qualitative.Pastel
    fig = px.pie(data, values='Amount', names='Category', title=title, color_discrete_sequence=colors, hole=0.3)
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1)),
        textfont=dict(size=14, color='white'),
        pull=[0.05] * len(data)
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(size=20, color='white', family="Arial Black"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        hoverlabel=dict(bgcolor="black", font_size=14, font_family="Arial")
    )
    return fig

# Table Styling
def gradient_style(df):
    styled_df = df.copy()
    if 'Date' in styled_df.columns:
        styled_df['Date'] = styled_df['Date'].astype(str)
    return (
        styled_df.style
        .format({"Amount": "{:,.2f}"})
        .background_gradient(cmap="Blues", subset=['Amount'])
        .set_properties(**{
            'color': 'white',
            'font-weight': 'bold',
            'background-color': '#111111',
            'border': '1px solid rgba(255, 255, 255, 0.2)',
            'text-align': 'left'
        })
        .set_table_styles([{
            'selector': 'th',
            'props': [
                ('background-color', '#0066CC'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('border', '1px solid rgba(255, 255, 255, 0.2)'),
                ('text-align', 'left')
            ]
        }, {
            'selector': 'td',
            'props': [('padding', '8px 12px')]
        }])
        .highlight_max(subset=['Amount'], color='#0066CC', props='color: white; font-weight: bold;')
    )

# View Expenses
def view_expenses():
    st.subheader("📋 All Expenses")
    df = load_expenses()
    st.dataframe(gradient_style(df), use_container_width=True, height=400)

    if not df.empty:
        st.subheader("📊 Visual Analysis")

        # Overall Pie Chart
        st.markdown("### 🎯 Overall Expense Distribution")
        category_totals = df.groupby("Category")["Amount"].sum().reset_index()
        fig1 = create_pie_chart(category_totals, "Total Expenses by Category")
        st.plotly_chart(fig1, use_container_width=True)

        # Monthly Pie Charts
        st.markdown("### 📅 Monthly Expense Breakdown")
        df_monthly = df.copy()
        df_monthly['Month'] = pd.to_datetime(df_monthly['Date']).dt.to_period('M').astype(str)
        monthly_totals = df_monthly.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
        months = df_monthly['Month'].unique()
        tabs = st.tabs([f"📌 {month}" for month in months])

        for tab, month in zip(tabs, months):
            with tab:
                month_data = monthly_totals[monthly_totals['Month'] == month]
                if not month_data.empty:
                    fig_month = create_pie_chart(month_data, f"Expenses for {month}")
                    st.plotly_chart(fig_month, use_container_width=True)
                else:
                    st.info(f"No expenses recorded for {month}")

        # Daily Trend
        st.markdown("### ⏳ Daily Expense Trend")
        daily_totals = df.groupby('Date')['Amount'].sum().reset_index()
        fig4 = px.line(daily_totals, x='Date', y='Amount', title="Daily Expense Trend", markers=True,
                       color_discrete_sequence=['#00BFFF'])
        fig4.update_traces(line_color='#B8860B', line_width=3,
                           marker=dict(size=8, color='#0066CC', line=dict(width=1, color='DarkSlateGrey')))
        fig4.update_layout(
            xaxis_title="Date",
            yaxis_title="Amount",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font=dict(size=20, color='white', family="Arial Black"),
            hovermode="x unified",
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showline=True, linecolor='rgba(255,255,255,0.5)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showline=True, linecolor='rgba(255,255,255,0.5)')
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Monthly Trend Graph (NEW) - Wider version
        st.markdown("### 📈 Monthly Expense Trends")
        df_monthly_line = df.copy()
        df_monthly_line['Month'] = pd.to_datetime(df_monthly_line['Date']).dt.to_period("M").astype(str)
        monthly_trends = df_monthly_line.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
        fig5 = px.line(monthly_trends, x='Month', y='Amount', color='Category', markers=True,
                       title='Monthly Trends by Category',
                       color_discrete_sequence=px.colors.sequential.Plasma)
        fig5.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(size=20, color='white'),
            width=1200
        )
        st.plotly_chart(fig5, use_container_width=True)

# Dashboard
def dashboard():
    # Display the image
    st.image("https://github.com/HarisFarooq23/FirstApp/blob/main/pic.png?raw=true", use_container_width=True)
    
    # Add beautiful golden loading bar
    st.markdown('<div class="gold-loading-bar"></div>', unsafe_allow_html=True)
    
    # Add two pie charts below the image
    df = load_expenses()
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Overall Pie Chart
            category_totals = df.groupby("Category")["Amount"].sum().reset_index()
            fig1 = create_pie_chart(category_totals, "Total Expenses by Category")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Current Month Pie Chart
            current_month = datetime.now().strftime("%Y-%m")
            monthly_expenses = df[pd.to_datetime(df['Date']).dt.to_period('M').astype(str) == current_month]
            if not monthly_expenses.empty:
                month_totals = monthly_expenses.groupby("Category")["Amount"].sum().reset_index()
                fig2 = create_pie_chart(month_totals, f"Expenses for {current_month}")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info(f"No expenses recorded for {current_month}")

# Edit Expenses
def edit_expense():
    st.subheader("✏️ Edit Existing Expense")
    df = load_expenses()
    if df.empty:
        st.info("No expenses to edit.")
        return
    st.dataframe(gradient_style(df), use_container_width=True)
    index = st.number_input("Enter the index number of the expense to edit", min_value=0, max_value=len(df)-1)
    date = st.date_input("New Date", df.loc[index, "Date"])
    category = st.selectbox("New Category", 
                            ["Food", "Transport", "Stationery", "Internet", "Recreation", "Other"], 
                            index=["Food", "Transport", "Stationery", "Internet", "Recreation", "Other"].index(df.loc[index, "Category"]))
    amount = st.number_input("New Amount", min_value=0.0, format="%.2f", value=float(df.loc[index, "Amount"]))
    description = st.text_input("New Description", value=df.loc[index, "Description"])
    if st.button("Update Expense", key="update_expense_button"):
        if update_expense(index, date, category, amount, description):
            st.success("Expense updated successfully!")
            st.balloons()
    
    # Add delete all button with confirmation
    st.markdown("---")
    st.subheader("⚠️ Danger Zone")
    if st.button("❌ Delete ALL Expenses", key="delete_all_button", help="This will permanently delete all your expense records"):
        if st.warning("Are you sure you want to delete ALL expenses? This action cannot be undone!"):
            if delete_all_expenses():
                st.error("All expenses have been deleted!")
                st.balloons()
            else:
                st.error("Failed to delete expenses. Please try again.")

# About Page
def about_page():
    st.balloons()
    st.markdown('<h1 class="about-header">About Spendr</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 18px; color: #888888;'>
        Spendr is a personal expense tracking application designed to help you monitor your spending habits 
        and gain financial awareness. With beautiful visualizations and intuitive controls, managing your 
        money has never been easier.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🌍 About the Developer</h2>', unsafe_allow_html=True)
    
    # Developer info in columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
                    <br><br> 
        <div style='text-align: center;'>
            <img src='https://media.licdn.com/dms/image/v2/D4D03AQHnjp96gkwCZA/profile-displayphoto-shrink_400_400/B4DZVRSQG5HIAg-/0/1740825496309?e=1756339200&v=beta&t=zOwgJ-pTDxNpTzLHJ7pzer2RFHtDVd_GhwJKQrMzG4E' 
                 style='width: 150px; height: 150px; border-radius: 50%; border: 4px solid #D4AF37;'>
            <h3 style='color:#666666; margin-top: 10px;'>-Haris Farooq</h3>
            <p style='color: #888888;' > UI/UX Enthusiast</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <p style='font-size: 16px; color: #888888;'>
        <br><br>
            Hi! I'm Haris Farooq, a student of BS Artificial Intelligence (Batch 34) at GIK Institute. I’m passionate about using technology to solve real-world problems, especially in the fields of AI, data science, and automation. I love taking on creative challenges and constantly seek opportunities to learn and grow.This is my first Streamlit app, and I'm excited to share it as part of my journey into building interactive, user-friendly tools with real-world impact!
        </p>
        <p style='font-size: 16px;'>
            When I'm not coding, you can find me exploring new technologies, contributing to 
            open-source projects, or enjoying outdoor activities.
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🛠️ Technical Skills</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center;'>
        <span class='skill-pill'>Python</span>
        <span class='skill-pill'>Streamlit</span>
        <span class='skill-pill'>Pandas</span>
        <span class='skill-pill'>Plotly</span>
        <span class='skill-pill'>Data Visualization</span>
        <span class='skill-pill'>Web Development</span>
        <span class='skill-pill'>UI/UX Design</span>
        <span class='skill-pill'>Data Analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🌍 Connect With Me</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center;'>
        <a href='https://github.com/HarisFarooq23' class='social-icon'>GitHub</a>
        <a href='https://www.linkedin.com/in/harisfarooq23/' class='social-icon'>LinkedIn</a>
        
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🌍 Special Thanks</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 16px;color: #888888;'>
        Thank you for using Spendr! If you enjoy this application, please consider starring 
        the project on GitHub or sharing it with friends who might find it useful.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main App
init_csv()
if "page_loaded" not in st.session_state:
    loading_screen()
    st.session_state.page_loaded = True

# Sidebar navigation with golden theme
with st.sidebar:
    # Coin Logo and Title with golden styling
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <svg width="60" height="60" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="margin:0 auto;" class="coin-logo">
            <circle cx="12" cy="12" r="10" fill="#D4AF37" stroke="#996515" stroke-width="2"/>
            <text x="12" y="16" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#000000">$</text>
        </svg>
        <h1 style="color:#D4AF37; margin-top:5px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Spendr</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation with golden selection effect
    menu = st.radio(
        "Navigation",
        ["Dashboard", "Add Expense", "View Expenses", "Edit Expenses", "About"],
        index=0,
        key="nav"
    )
    
    # Footer with golden accent
    st.markdown("---")
    st.markdown(
        """<div style="text-align:center; color:#D4AF37; font-size:12px;">
        Track every penny • Spend wisely
        </div>""",
        unsafe_allow_html=True
    )

# Main content area
if menu == "Dashboard":
    dashboard()
elif menu == "Add Expense":
    add_expense()
elif menu == "View Expenses":
    view_expenses()
elif menu == "Edit Expenses":
    edit_expense()
elif menu == "About":
    about_page()
