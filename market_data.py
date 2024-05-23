# market_data.py
import yfinance as yf
import streamlit as st


def get_market_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="2d")
    current_price = hist['Close'][-1]
    previous_price = hist['Close'][-2]
    change = ((current_price - previous_price) / previous_price) * 100
    return current_price, change


def display_market_data(ticker, name):
    price, change = get_market_data(ticker)
    st.metric(name, f"{price:.2f}", f"{change:.2f}%")


def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

# Show stock cards


def show_stock_cards(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    x1, x2, x3 = st.columns(3)
    with x1:
        st.metric("Market Cap",  f"{info['marketCap']/1e9:.2f} B$")
    with x2:
        trailing_pe = info.get('trailingPE', 'N/A')
        st.metric("P/E Ratio",  trailing_pe)
    with x3:
        st.metric("P/S Ratio", f"{info['priceToSalesTrailing12Months']:.2f}")


def get_stock_card(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    st.metric(info['sector'],  info['shortName'])


# news table
def get_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    for new in news:
        st.write(new['title'])
        x1, x2 = st.columns(2)
        with x1:
            st.text(new['publisher'])
        with x2:
            related_tickers = ', '.join(new.get('relatedTickers', []))
            st.text(related_tickers)
#    df_news = pd.DataFrame(news)[['title', 'publisher', 'relatedTickers']]
 #   st.table(df_news)
#


def show_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info


def sh_list_table(ticker, list):
    data_table = pd.DataFrame(columns=['Financial Metric', 'Value'])
    info = get_stock_info(ticker)
    for i, ticker in enumerate(list):
        current_price, change = get_market_data(ticker)
        # color = 'red' if change < 0 else 'green'
        # Append the data to the DataFrame
        data_table.loc[i] = [
            ticker, f"${current_price:.2f}", f"{change:.2f}%"]
        # data_table = data_table.append(
        #   {'Ticker': ticker, 'Price': f"${current_price:.2f}", 'Change %': f"{change:.2f}%"}, ignore_index=True)
    st.table(data_table)
