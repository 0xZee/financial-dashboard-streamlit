import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit.components.v1 as components
#
from market_data import display_market_data, get_market_data, display_market_data, get_stock_info, get_stock_card, show_stock_cards, get_stock_news
from lists import list_keys, list1_keys
from widgets import widget_chart, mini_chart

# app
# SIDEBAR
with st.sidebar:
    try:
        # list indices
        mkt_list01 = [
            ('^IXIC', "NASDAQ"),
            ('^GSPC', "S&P 500"),
        ]
        # list indices
        mkt_list02 = [
            ('^RUT', "RUSSEL 2000"),
            ('FDN', "DOW JONES"),
        ]

        # list indices
        us_list01 = [
            ('^VIX', "VIX"),
            ('^TNX', "10Y Treasury"),
        ]
        # list indices 2
        us_list02 = [
            ('EURUSD=X', "EURO-USD"),
            ('CL=F', "Crude OIL"),
        ]
        # list ETF
        etf_list01 = [
            ('SOXX', "SOXX"),
            ('ARKK', "ARKK"),
        ]
        # list ETF
        etf_list02 = [
            ('HACK', "HACK"),
            ('ICLN', "ICLN"),
        ]

        # MKT
        st.subheader(':violet-background[US INDICES]', divider='gray')

        x = st.columns(2)
        for i, (ticker, name) in enumerate(mkt_list01):
            with x[i]:
                display_market_data(ticker, name)
        y = st.columns(2)
        for i, (ticker, name) in enumerate(mkt_list02):
            with y[i]:
                display_market_data(ticker, name)

        # MKT
        st.subheader(':violet-background[US MARKET]', divider='gray')

        x = st.columns(2)
        for i, (ticker, name) in enumerate(us_list01):
            with x[i]:
                display_market_data(ticker, name)
        y = st.columns(2)
        for i, (ticker, name) in enumerate(us_list02):
            with y[i]:
                display_market_data(ticker, name)

        # ETF
        st.subheader(':violet-background[US ETF]', divider='gray')

        x = st.columns(2)
        for i, (ticker, name) in enumerate(etf_list01):
            with x[i]:
                display_market_data(ticker, name)
        y = st.columns(2)
        for i, (ticker, name) in enumerate(etf_list02):
            with y[i]:
                display_market_data(ticker, name)

    except Exception as e:
        st.error(f"Error fetching market data: {e}")


# APP
# MAIN PAGE

st.header("Financial Stock Dashboard", divider='violet')

ticker = st.text_input("Stock")
if ticker:
    try:
        # finviz_url = f"https://finviz.com/published_idea.ashx?t={ticker}&f=052224&i={ticker}d102843436i"
        # st.image(finviz_url, caption=f"Stock Chart for {ticker}")
        # st.image(f'https://finviz.com/published_idea.ashx?t=IBM&f=052124&i=IBMd085868623i')
        # widget_chart(ticker)
        mini_chart(ticker)
        #
        info = get_stock_info(ticker)
        get_market_data(ticker)
        st.divider()
        x1, x2 = st.columns([2, 1])
        with x1:
            get_stock_card(ticker)
        with x2:
            display_market_data(ticker, ticker)
        st.divider()
        #
        show_stock_cards(ticker)
        st.divider()
        #
        st.write(f':violet-background[News for {ticker}]')
        get_stock_news(ticker)
        st.divider()
        #
        st.write(f':violet-background[Financial Metrics for {ticker}]')
        # data = pd.DataFrame([info])
        # data = pd.DataFrame(columns=list_keys)
        data = pd.DataFrame({key: info.get(key, 'N/A')
                            for key in list_keys}, index=[0]).transpose()
        # data = data.loc[list_keys]
        # data = data.transpose()
        st.table(data)

    except Exception as e:
        st.error(f"Error fetching market data: {e}")
