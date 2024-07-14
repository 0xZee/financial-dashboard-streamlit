import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="Financial Stock", page_icon="📈")

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info, stock

def get_stock_history(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5y")
    return hist

def get_nasdaq_history():
    nasdaq = yf.Ticker("^IXIC")
    hist = nasdaq.history(period="5y")
    return hist

# Custom CSS to improve app appearance
st.markdown("""
<style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.subheader('📊 Stock :orange-background[Financial] Data', divider='grey')

# Input for stock ticker
ticker = st.text_input('🔍 Enter Stock Ticker:', 'AAPL', placeholder='NVDA, PLTR, TSLA...')

# main section
if st.button('Get Stock Info', use_container_width=True):
    # Get stock info
    info, stock = get_stock_info(ticker)
    
    st.divider()
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([f"💧 {ticker} Info", "📊 Financial Ratios", "📚 Financial Statements", "📰  News"])


    
    # Tab 1: Info
    with tab1:

        st.subheader(f'🏷️ {info.get("longName", "N/A")} :orange-background[{ticker}]', divider='violet')
        
        # Current price and day change
        current_price = info.get('currentPrice', 'N/A')
        previous_close = info.get('previousClose', 'N/A')
        if current_price != 'N/A' and previous_close != 'N/A':
            day_change = current_price - previous_close
            day_change_percent = (day_change / previous_close) * 100
    
            col0, col1, col2, col3, col4 = st.columns([2,2,2,3,4])
            with col0:
                st.image(f"https://logos.stockanalysis.com/{ticker.lower()}.svg", width=60)
            with col1:
                st.metric(f"📈 {ticker}", f"$ {current_price:.2f}", f"{day_change_percent:.2f} %")
            with col2:
                st.metric("💰 Market Cap", f"{info.get('marketCap', 'N/A') / 1e9:.2f} B$")
    
            # Company long description
            with col3:
                st.metric("🏭 Sector", f"{info.get('sector', 'N/A')}")
            with col4:
                st.metric("🔧 Industry", f"{info.get('industry', 'N/A')}")
    

        # Display company description
        with st.expander(f"🏢 {ticker} Company Description"):
            st.write(info.get('longBusinessSummary', 'N/A'))
        
        # Display financial ratios in cards
        st.subheader('📊 Financial Ratios', divider='grey')
        col1, col2, col3, col4 = st.columns(4)
        ratios = [
            ('P/S Ratio', 'priceToSalesTrailing12Months', '💹'),
            ('P/E Ratio', 'trailingPE', '📊'),
            ('Forward P/E', 'forwardPE', '🔮'),
            ('1Q Earnings Growth', 'earningsQuarterlyGrowth', '🌱'),
            ('Recommendation', 'recommendationKey', '🎯'),
            ('Target Price', 'targetMedianPrice', '💲'),
            ('Short Ratio', 'shortRatio', '📉'),
            ('Profit Margin', 'profitMargins', '📈'),
        ]
    
        for i, (label, key, emoji) in enumerate(ratios):
            with [col1, col2, col3, col4][i % 4]:
                value = info.get(key, 'N/A')
                if isinstance(value, float):
                    value = f"{value:.2f}"
                st.metric(f"{emoji} {label}", value)
    
        #st.markdown('---')

    
        # Get historical data and create an interactive chart
        hist = get_stock_history(ticker)
        nasdaq_hist = get_nasdaq_history()
    
        #st.subheader('📉 Interactive Stock Chart', divider='violet')
    
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Close'), secondary_y=False)
        fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color='grey', width=0.1), secondary_y=True)
    
        # Calculate the 20-day moving average
        hist['MA100'] = hist['Close'].rolling(window=100).mean()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['MA100'], name='MA100'), secondary_y=False)
    
        fig.update_layout(title=f'📉 {ticker} Price Chart', xaxis_title='Date', yaxis_title='Price')
        fig.update_yaxes(title_text="Volume", secondary_y=True, range=[0, hist['Volume'].max() * 5])
        st.plotly_chart(fig, use_container_width=True)
    
        st.divider()


    # Tab 2: Financial Ratios
    with tab2:
        
        # Display financial ratios in cards
        st.subheader('📊 Financial Ratios', divider='violet')
        col1, col2, col3, col4 = st.columns(4)
        ratios = [
            ('P/S Ratio', 'priceToSalesTrailing12Months', '💹'),
            ('P/E Ratio', 'trailingPE', '📊'),
            ('Forward P/E', 'forwardPE', '🔮'),
            ('PEG Ratio', 'pegRatio', '🌱'),
            ('Price to Book', 'priceToBook', '📚'),
            ('Dividend Yield', 'dividendYield', '💵'),
            ('Profit Margin', 'profitMargins', '📈'),
            ('EV/EBITDA', 'enterpriseToEbitda', '🏦')
        ]
    
        for i, (label, key, emoji) in enumerate(ratios):
            with [col1, col2, col3, col4][i % 4]:
                value = info.get(key, 'N/A')
                if isinstance(value, float):
                    value = f"{value:.2f}"
                st.metric(f"{emoji} {label}", value)
    
        st.markdown('---')
    
    
        # Cards for Growth Metrics
        st.subheader('📈 Growth Metrics', divider='violet')
        growth_metrics = [
            ('Earnings Quarterly Growth', 'earningsQuarterlyGrowth', '📊'),
            ('Revenue Quarterly Growth', 'revenueQuarterlyGrowth', '📈'),
            ('Earnings Growth', 'earningsGrowth', '💹'),
            ('Revenue Growth', 'revenueGrowth', '💵'),
            ('Gross Margins', 'grossMargins', '📊'),
            ('EBITDA Margins', 'ebitdaMargins', '📈'),
            ('Operating Margins', 'operatingMargins', '💹'),
            ('Profit Margins', 'profitMargins', '💵')
        ]
    
        cols = st.columns(4)
        for i, (label, key, emoji) in enumerate(growth_metrics):
            with cols[i % 4]:
                value = info.get(key, 'N/A')
                if isinstance(value, (int, float)):
                    value = f"{value:.2f}"
                st.metric(f"{emoji} {label}", value)
    
        # Display Rsik cards
        st.divider()
    
        # Risk Metrics
        st.subheader('🎢 Risk Metrics', divider='violet')
        risk_metrics = [
            ('Total Debt', 'totalDebt', '💳'),
            ('Quick Ratio', 'quickRatio', '⚡'),
            ('Current Ratio', 'currentRatio', '💧'),
            ('Debt to Equity', 'debtToEquity', '📊'),
            ('Short Ratio', 'shortRatio', '📉'),
            ('Short Percent of Float', 'shortPercentOfFloat', '📈'),
            ('Audit Risk', 'auditRisk', '🔍'),
            ('Overall Risk', 'overallRisk', '⚠️')
        ]
    
        cols = st.columns(4)
        for i, (label, key, emoji) in enumerate(risk_metrics):
            with cols[i % 4]:
                value = info.get(key, 'N/A')
                if isinstance(value, (int, float)):
                    value = f"{value:.2f}"
                st.metric(f"{emoji} {label}", value)
    
        st.divider()
    
        # Recommendations
        st.subheader('🕵️‍♂️ Analyst Recommendations', divider='violet')
        risk_metrics = [
            ('Recommendation', 'recommendationKey', '🎯'),
            ('Target Price', 'targetMedianPrice', '💲'),
            ('Recommendation Mead', 'recommendationMean', '🔍'),
            ('Target Mean Price', 'targetMeanPrice', '💧'),
            ('Target High Price', 'targetHighPrice', '📈'),
            ('Target Low Price', 'targetLowPrice', '📉'),
        ]
    
        cols = st.columns(3)
        for i, (label, key, emoji) in enumerate(risk_metrics):
            with cols[i % 3]:
                value = info.get(key, 'N/A')
                if isinstance(value, (int, float)):
                    value = f"{value:.2f}"
                st.metric(f"{emoji} {label}", value)
    
        st.divider()
    

    # tab 3: Financial Statements
    with tab3:
        
        # Financial Statements
        st.subheader('📑 Financial Statements')
    
        # Income Statement
        income_stmt = stock.income_stmt
        if not income_stmt.empty:
            st.write("💰 Income Statement")
            income_stmt_metrics = ['Total Revenue', 'Operating Revenue','Net Income', 'Gross Profit', 'Operating Income', 'EBITDA' , 'EBIT', ]
            fig = go.Figure()
            for metric in income_stmt_metrics:
                if metric in income_stmt.index:
                    fig.add_trace(go.Bar(x=income_stmt.columns, y=income_stmt.loc[metric], name=metric))
            fig.update_layout(title='Income Statement Metrics', barmode='group')
            st.plotly_chart(fig, use_container_width=True)
    
        # Balance Sheet
        balance_sheet = stock.balance_sheet
        if not balance_sheet.empty:
            st.write("📊 Balance Sheet")
            balance_sheet_metrics = ['Total Assets', 'Total Debt', 'Current Liabilities', 'Long Term Debt', 'Cash And Cash Equiv']
            fig = go.Figure()
            for metric in balance_sheet_metrics:
                if metric in balance_sheet.index:
                    fig.add_trace(go.Bar(x=balance_sheet.columns, y=balance_sheet.loc[metric], name=metric))
            fig.update_layout(title='Balance Sheet Metrics', barmode='group')
            st.plotly_chart(fig, use_container_width=True)
    
        # Cash Flow
        cash_flow = stock.cashflow
        if not cash_flow.empty:
            st.write("💸 Cash Flow")
            cash_flow_metrics = ['Free Cash Flow', 'Operating Cash Flow', 'Financing Cash Flow', 'Investing Cash Flow','Capital Expenditures', 'Long Term Debt Payments']
            fig = go.Figure()
            for metric in cash_flow_metrics:
                if metric in cash_flow.index:
                    fig.add_trace(go.Bar(x=cash_flow.columns, y=cash_flow.loc[metric], name=metric))
            fig.update_layout(title='Cash Flow Metrics', barmode='group')
            st.plotly_chart(fig, use_container_width=True)
    
        st.markdown('---')

    # Tab 4: News
    with tab4:
        
        # News
        st.subheader('📰 Recent News')
        news = stock.news
        for article in news[:10]:  # Display the 10 most recent news articles
            st.markdown(f"> 📄 **{article['title']}** . 🔗 [Link]({article['link']})")
            st.text(f"📰 {article['publisher']} | 📆 {pd.to_datetime(article['providerPublishTime'], unit='s')} | 🌐 {', '.join(article['relatedTickers'])}")
            #st.markdown(f"🔗 [Article]({article['link']})")
        #st.markdown('---')
        st.divider()



st.text('Note: This app uses Yahoo Finance data which may be delayed.')
