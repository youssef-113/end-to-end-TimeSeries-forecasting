import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #06b6d4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 3px solid #06b6d4;
        margin: 0.5rem 0;
    }
    .stMetric {
        background-color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown('<div class="main-title">Marketing Campaign Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">End-to-End Analysis: Operations, QA & Sales Tracking</div>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('../data/data cleaned.csv')
        # Convert date columns to datetime first
        date_cols = ['Assign Date', 'Finish Date', 'Validation Date', 'Date of Sale', 
                     'Creation Date', 'Date of Payment', 'sale Week']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Convert numeric columns
        numeric_cols = ['Quality Score %', 'Monthly Price', 'Days To Payment']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    if 'Date of Sale' in df.columns:
        # Filter out NaT values for date range
        valid_dates = df['Date of Sale'].dropna()
        if len(valid_dates) > 0:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            if len(date_range) == 2:
                df = df[(df['Date of Sale'] >= pd.Timestamp(date_range[0])) & 
                        (df['Date of Sale'] <= pd.Timestamp(date_range[1]))]
    
    # Product filter
    if 'Product' in df.columns:
        products = df['Product'].dropna().unique().tolist()
        selected_products = st.sidebar.multiselect(
            "Select Products",
            products,
            default=products
        )
        if selected_products:
            df = df[df['Product'].isin(selected_products)]
    
    # State filter
    if 'State' in df.columns:
        states = df['State'].dropna().unique().tolist()
        selected_states = st.sidebar.multiselect(
            "Select States",
            states[:20],  # Limit to top 20 for performance
            default=states[:10]
        )
        if selected_states:
            df = df[df['State'].isin(selected_states)]
    
    # Team Leader filter
    if 'Team Leader' in df.columns:
        team_leaders = df['Team Leader'].dropna().unique().tolist()
        selected_leaders = st.sidebar.multiselect(
            "Select Team Leaders",
            team_leaders,
            default=team_leaders
        )
        if selected_leaders:
            df = df[df['Team Leader'].isin(selected_leaders)]
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["KPIs & Summary", "Phase 2 Analysis", "Time-Series Forecasting"])
    
    # Tab 1: KPIs & Summary
    with tab1:
        st.header("Key Performance Indicators")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_leads = len(df)
        with col1:
            st.metric("Total Leads", f"{total_leads:,}")
        
        if 'Is Approved' in df.columns:
            total_approved = df['Is Approved'].sum()
            approval_rate = (total_approved / total_leads * 100) if total_leads > 0 else 0
            with col2:
                st.metric("Approved Sales", f"{total_approved:,}")
            with col3:
                st.metric("Approval Rate", f"{approval_rate:.1f}%")
        
        if 'Payment Received' in df.columns:
            total_payments = df['Payment Received'].sum()
            payment_rate = (total_payments / total_leads * 100) if total_leads > 0 else 0
            with col4:
                st.metric("Payments Received", f"{total_payments:,}")
            with col5:
                st.metric("Payment Rate", f"{payment_rate:.1f}%")
        
        # Revenue KPIs
        if 'Monthly Price' in df.columns:
            total_revenue = df['Monthly Price'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        
        st.header("Lead Disposition Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Closing Status' in df.columns:
                status_counts = df['Closing Status'].value_counts()
                fig_status = px.bar(
                    x=status_counts.values,
                    y=status_counts.index,
                    orientation='h',
                    title='Leads by Closing Status',
                    color=status_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_status.update_layout(xaxis_title="Number of Leads", yaxis_title="")
                st.plotly_chart(fig_status, width='stretch')
        
        with col2:
            if 'Is Approved' in df.columns:
                approved = df['Is Approved'].sum()
                not_approved = len(df) - approved
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Approved', 'Not Approved'],
                    values=[approved, not_approved],
                    hole=.4,
                    marker=dict(colors=['#2ECC71', '#BDC3C7'])
                )])
                fig_pie.update_layout(title='Approval Rate')
                st.plotly_chart(fig_pie, width='stretch')
        
        st.header("Data Summary")
        
        # Show sample data
        st.subheader("Sample Data (First 100 Rows)")
        st.dataframe(df.head(100))
        
        # Data Summary
        st.subheader("Statistical Summary")
        st.write(df.describe())
        
        # Missing Values
        st.subheader("Missing Values")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        missing_df = pd.DataFrame({'Count': missing, 'Percentage': missing_pct})
        st.dataframe(missing_df[missing_df['Count'] > 0])
    
    # Tab 2: Phase 2 Analysis
    with tab2:
        st.header("Agent Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Closer Name' in df.columns and 'Is Approved' in df.columns:
                closer_perf = (
                    df[df['Closer Name'].notna()]
                    .groupby('Closer Name')
                    .agg(total=('Is Approved', 'count'), approved=('Is Approved', 'sum'))
                    .assign(approval_rate=lambda x: x.approved / x.total * 100)
                    .query('total >= 5')
                    .sort_values('approved', ascending=True)
                    .tail(10)
                )
                
                fig_closers = px.bar(
                    x=closer_perf['approved'],
                    y=closer_perf.index,
                    orientation='h',
                    title='Top Closers - Approved Sales Volume',
                    color=closer_perf['approved'],
                    color_continuous_scale='Blues'
                )
                fig_closers.update_layout(xaxis_title='Approved Sales', yaxis_title='Closer Name')
                st.plotly_chart(fig_closers, width='stretch')
        
        with col2:
            if 'Opener Name' in df.columns and 'Is Approved' in df.columns:
                opener_perf = (
                    df[df['Opener Name'].notna()]
                    .groupby('Opener Name')
                    .agg(total=('Is Approved', 'count'), approved=('Is Approved', 'sum'))
                    .assign(conv_rate=lambda x: x.approved / x.total * 100)
                    .query('total >= 5')
                    .sort_values('conv_rate', ascending=True)
                    .tail(10)
                )
                
                fig_openers = px.bar(
                    x=opener_perf['conv_rate'],
                    y=opener_perf.index,
                    orientation='h',
                    title='Top Openers - Lead Conversion Rate',
                    color=opener_perf['conv_rate'],
                    color_continuous_scale='Greens'
                )
                fig_openers.update_layout(xaxis_title='Conversion Rate (%)', yaxis_title='Opener Name')
                st.plotly_chart(fig_openers, width='stretch')
        
        st.header("Product Performance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Product' in df.columns:
                product_counts = df['Product'].value_counts()
                fig_product = px.pie(
                    values=product_counts.values,
                    names=product_counts.index,
                    title='Product Mix',
                    hole=0.4
                )
                st.plotly_chart(fig_product, width='stretch')
        
        with col2:
            if 'Product' in df.columns and 'Monthly Price' in df.columns:
                revenue_by_product = df.groupby('Product')['Monthly Price'].sum()
                fig_revenue = px.bar(
                    x=revenue_by_product.index,
                    y=revenue_by_product.values,
                    title='Total Revenue by Product',
                    color=revenue_by_product.index,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_revenue.update_layout(xaxis_title='Product', yaxis_title='Total Monthly Price')
                st.plotly_chart(fig_revenue, width='stretch')
        
        with col3:
            if 'Product' in df.columns and 'Monthly Price' in df.columns:
                avg_price = df.groupby('Product')['Monthly Price'].mean()
                fig_avg_price = px.bar(
                    x=avg_price.index,
                    y=avg_price.values,
                    title='Average Price by Product',
                    color=avg_price.index,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_avg_price.update_layout(xaxis_title='Product', yaxis_title='Average Monthly Price')
                st.plotly_chart(fig_avg_price, width='stretch')
        
        st.header("Geographical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'State' in df.columns:
                state_counts = df['State'].value_counts().head(15)
                fig_states = px.bar(
                    x=state_counts.index,
                    y=state_counts.values,
                    title='Top 15 States by Lead Volume',
                    color=state_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig_states.update_layout(xaxis_title='State', yaxis_title='Number of Leads')
                st.plotly_chart(fig_states, width='stretch')
        
        with col2:
            if 'State' in df.columns and 'Is Approved' in df.columns:
                state_conversion = (
                    df.groupby('State')
                    .agg(total=('Is Approved', 'count'), approved=('Is Approved', 'sum'))
                    .assign(conv_rate=lambda x: x.approved / x.total * 100)
                    .sort_values('conv_rate', ascending=False)
                    .head(15)
                )
                fig_state_conv = px.bar(
                    x=state_conversion.index,
                    y=state_conversion['conv_rate'],
                    title='Top 15 States by Conversion Rate',
                    color=state_conversion['conv_rate'],
                    color_continuous_scale='Plasma'
                )
                fig_state_conv.update_layout(xaxis_title='State', yaxis_title='Conversion Rate (%)')
                st.plotly_chart(fig_state_conv, width='stretch')
        
        st.header("Payment Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Days To Payment' in df.columns:
                fig_days = px.histogram(
                    df[df['Days To Payment'].notna()],
                    x='Days To Payment',
                    title='Days to Payment Distribution',
                    nbins=30,
                    color_discrete_sequence=['#06b6d4']
                )
                fig_days.update_layout(xaxis_title='Days to Payment', yaxis_title='Count')
                st.plotly_chart(fig_days, width='stretch')
        
        with col2:
            if 'Product' in df.columns and 'Days To Payment' in df.columns:
                payment_delay = df.groupby('Product')['Days To Payment'].mean().dropna()
                fig_delay = px.bar(
                    x=payment_delay.index,
                    y=payment_delay.values,
                    title='Average Days to Payment by Product',
                    color=payment_delay.index,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_delay.update_layout(xaxis_title='Product', yaxis_title='Average Days to Payment')
                st.plotly_chart(fig_delay, width='stretch')
        
        with col3:
            if 'Team Leader' in df.columns and 'Payment Received' in df.columns:
                payment_rate = df.groupby('Team Leader')['Payment Received'].mean() * 100
                payment_rate = payment_rate.sort_values(ascending=False).head(10)
                fig_payment_rate = px.bar(
                    x=payment_rate.index,
                    y=payment_rate.values,
                    title='Payment Rate by Team Leader (Top 10)',
                    color=payment_rate.values,
                    color_continuous_scale='RdYlGn'
                )
                fig_payment_rate.update_layout(xaxis_title='Team Leader', yaxis_title='Payment Rate (%)')
                st.plotly_chart(fig_payment_rate, width='stretch')
        
        st.header("Quality Assurance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Quality Score %' in df.columns:
                qa_df = df[df['Quality Score %'].notna()]
                if len(qa_df) > 0:
                    fig_qa_dist = px.histogram(
                        qa_df,
                        x='Quality Score %',
                        title='Quality Score Distribution',
                        nbins=20,
                        color_discrete_sequence=['#1ABC9C']
                    )
                    fig_qa_dist.update_layout(xaxis_title='Quality Score (%)', yaxis_title='Count')
                    st.plotly_chart(fig_qa_dist, width='stretch')
        
        with col2:
            if 'Has Qa' in df.columns:
                qa_coverage = df['Has Qa'].value_counts()
                # Fix: Use actual index from value_counts instead of hardcoded names
                label_map = {1: 'QA Reviewed', 0: 'Not Reviewed'}
                names = [label_map.get(idx, str(idx)) for idx in qa_coverage.index]
                fig_qa_coverage = px.pie(
                    values=qa_coverage.values,
                    names=names,
                    title='QA Coverage',
                    hole=0.4,
                    color_discrete_sequence=['#2ECC71', '#E74C3C']
                )
                st.plotly_chart(fig_qa_coverage, width='stretch')
        
        # QA Score vs Sales
        if 'Quality Score %' in df.columns and 'Is Approved' in df.columns:
            qa_sales = df[df['Quality Score %'].notna()]
            if len(qa_sales) > 0:
                fig_qa_sales = px.box(
                    qa_sales,
                    x='Is Approved',
                    y='Quality Score %',
                    title='Quality Score by Sale Status',
                    color='Is Approved',
                    color_discrete_map={0: '#E74C3C', 1: '#2ECC71'}
                )
                fig_qa_sales.update_layout(xaxis_title='Sale Made', yaxis_title='Quality Score (%)')
                st.plotly_chart(fig_qa_sales, width='stretch')
        
        st.header("Demographics Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Gender' in df.columns:
                gender_counts = df['Gender'].value_counts()
                fig_gender = px.pie(
                    values=gender_counts.values,
                    names=gender_counts.index,
                    title='Gender Distribution',
                    hole=0.4
                )
                st.plotly_chart(fig_gender, width='stretch')
        
        with col2:
            if 'City' in df.columns:
                city_counts = df['City'].value_counts().head(15)
                fig_city = px.bar(
                    x=city_counts.values,
                    y=city_counts.index,
                    orientation='h',
                    title='Top 15 Cities by Lead Volume',
                    color=city_counts.values,
                    color_continuous_scale='Blues'
                )
                fig_city.update_layout(xaxis_title='Number of Leads', yaxis_title='City')
                st.plotly_chart(fig_city, width='stretch')
    
    # Tab 3: Time-Series Forecasting
    with tab3:
        st.header("Time Series Analysis")
        
        if 'Date of Sale' in df.columns:
            # Daily sales trend
            daily_sales = df.groupby('Date of Sale').size().reset_index(name='Sales')
            daily_sales = daily_sales.sort_values('Date of Sale')
            
            fig_daily = px.line(
                daily_sales,
                x='Date of Sale',
                y='Sales',
                title='Daily Sales Trend',
                markers=True
            )
            fig_daily.update_layout(xaxis_title='Date', yaxis_title='Number of Sales')
            st.plotly_chart(fig_daily, width='stretch')
            
            # Weekly sales
            if 'sale Week' in df.columns:
                weekly_sales = df.groupby('sale Week').size().reset_index(name='Sales')
                weekly_sales = weekly_sales.sort_values('sale Week')
                
                fig_weekly = px.line(
                    weekly_sales,
                    x='sale Week',
                    y='Sales',
                    title='Weekly Sales Trend',
                    markers=True,
                    line_shape='spline'
                )
                fig_weekly.update_layout(xaxis_title='Week', yaxis_title='Number of Sales')
                st.plotly_chart(fig_weekly, width='stretch')
        
        # Revenue Trend
        if 'Date of Sale' in df.columns and 'Monthly Price' in df.columns:
            daily_revenue = df.groupby('Date of Sale')['Monthly Price'].sum().reset_index()
            daily_revenue = daily_revenue.sort_values('Date of Sale')
            
            fig_revenue = px.line(
                daily_revenue,
                x='Date of Sale',
                y='Monthly Price',
                title='Daily Revenue Trend',
                markers=True
            )
            fig_revenue.update_layout(xaxis_title='Date', yaxis_title='Revenue ($)')
            st.plotly_chart(fig_revenue, width='stretch')
        
        # Day of Week Analysis
        if 'sale Day' in df.columns:
            weekday_sales = df.groupby('sale Day').size().reset_index(name='Sales')
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekday_sales = weekday_sales[weekday_sales['sale Day'].isin(weekday_order)]
            weekday_sales['sale Day'] = pd.Categorical(weekday_sales['sale Day'], categories=weekday_order, ordered=True)
            weekday_sales = weekday_sales.sort_values('sale Day')
            
            fig_weekday = px.bar(
                weekday_sales,
                x='sale Day',
                y='Sales',
                title='Average Sales by Weekday',
                color='Sales',
                color_continuous_scale='Viridis'
            )
            fig_weekday.update_layout(xaxis_title='Weekday', yaxis_title='Number of Sales')
            st.plotly_chart(fig_weekday, width='stretch')
        
        st.header("Forecasting Model Information")
        st.info("""
        This section displays time-series analysis and forecasting capabilities.
        
        The notebook includes Prophet-based forecasting models for:
        - Lead creation forecasting
        - Sales forecasting
        - Revenue forecasting
        
        These models use historical data to predict future campaign performance
        with confidence intervals and trend components.
        """)
        
        # Display forecast images if available
        st.subheader("Forecast Visualizations")
        
        forecast_images = [
            'plot_08_forecast.png',
            'plot_09_forecast_components.png',
            'revenue_forecast.png',
            'revenue_forecast_components.png',
            'sales_trend_ma.png',
            'revenue_trend_ma.png'
        ]
        
        col1, col2 = st.columns(2)
        for i, img_name in enumerate(forecast_images):
            img_path = f'../images/{img_name}'
            try:
                if i % 2 == 0:
                    with col1:
                        st.image(img_path, caption=img_name.replace('_', ' ').replace('.png', ''), use_column_width=True)
                else:
                    with col2:
                        st.image(img_path, caption=img_name.replace('_', ' ').replace('.png', ''), use_column_width=True)
            except:
                pass

else:
    st.error("Unable to load data. Please check the data file path.")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #94a3b8; font-size: 0.9rem;">Marketing Campaign Dashboard - End-to-End Analysis</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 0.5rem;">Created by <a href="https://github.com/youssef-113" target="_blank" style="color: #06b6d4; text-decoration: none;">Eng: Youssef Bassiony</a></div>', unsafe_allow_html=True)