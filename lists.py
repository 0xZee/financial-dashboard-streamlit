# tickers.py
# list indices
mkt_list01 = [
    ('^IXIC', "NASDAQ"),
    ('^GSPC', "S&P 500"),
]

mkt_list02 = [
    ('^RUT', "RUSSEL 2000"),
    ('FDN', "DOW JONES"),
]

mkt_list = [
    ('^IXIC', "NASDAQ"),
    ('^GSPC', "S&P 500"),
    ('^RUT', "RUSSEL 2000"),
    ('FDN', "DOW JONES"),
]

us_list = [
    ('^VIX', "VIX"),
    ('^TNX', "10Y Treasury"),
    ('TLT', "TLT"),
    ('^GSPC', "S&P 500"),
]

etf_list = [
    ('ARKK', "ARKK"),
    ('SOXX', "SOXX"),
    ('HACK', "HACK"),
    ('ICLN', "ICLN"),
]

# List of keys we want to extract
list_keys = [
    'currentPrice', 'marketCap', 'trailingPE', 'forwardPE', 'revenueGrowth',
    'pegRatio', 'trailingPegRatio', 'priceToBook', 'debtToEquity', 'dividendRate',
    'trailingAnnualDividendRate', 'profitMargins', 'trailingEps', 'forwardEps',
    'shortRatio', 'enterpriseToRevenue', 'enterpriseToEbitda', 'currentRatio',
    'freeCashflow', 'earningsGrowth', 'sector', 'website'
]

list1_keys = ['previousClose', 'dayLow', 'dayHigh', 'averageVolume', 'averageVolume10days', 'targetMeanPrice', 'targetHighPrice', 'targetLowPrice', 'recommendationKey']
