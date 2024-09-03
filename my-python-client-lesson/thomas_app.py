import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Function to fetch data from the CoinGecko API
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,tether,ethereum,binancecoin,tron,cardano,weth,ripple,staked-ether,the-open-network,wrapped-steth,shiba-inu,avalanche-2,wrapped-bitcoin,dogecoin,usd-coin,blockstack,sui,okb,cosmos,eos,gala,neo"  # Add more cryptocurrency IDs separated by commas
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from CoinGecko API")
        return []

# Fetch data from API
data = fetch_crypto_data()

# Convert data into a pandas DataFrame
df = pd.DataFrame(data)

# Streamlit App
st.title("Cryptocurrency Dashboard")

# Loop through each cryptocurrency in the DataFrame and display its details
for i in range(len(df)):
    st.image(df['image'][i], width=100)
    st.header(f"{df['name'][i]} ({df['symbol'][i].upper()})")

    # Display current price and market cap
    st.metric("Current Price (USD)", f"${df['current_price'][i]:,.2f}")
    st.metric("Market Cap", f"${df['market_cap'][i]:,}")
    st.metric("Market Cap Rank", f"{df['market_cap_rank'][i]}")

    # Display additional details
    st.subheader("24h Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("24h High", f"${df['high_24h'][i]:,.2f}")
        st.metric("24h Low", f"${df['low_24h'][i]:,.2f}")
    with col2:
        st.metric("Price Change (24h)", f"${df['price_change_24h'][i]:,.2f}")
        st.metric("Price Change % (24h)", f"{df['price_change_percentage_24h'][i]:.2f}%")

    st.subheader("All-Time Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("All-Time High", f"${df['ath'][i]:,.2f}", delta=f"{df['ath_change_percentage'][i]:.2f}% from ATH")
    with col2:
        st.metric("All-Time Low", f"${df['atl'][i]:,.2f}", delta=f"{df['atl_change_percentage'][i]:.2f}% from ATL")

    # Display last updated time
    last_updated = datetime.fromisoformat(df['last_updated'][i].replace('Z', '+00:00'))
    st.write(f"Last Updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')} UTC")

    st.markdown("---")  # Separator between cryptocurrencies
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# # Function to fetch data from the CoinGecko API
# def fetch_crypto_data():
#     url = "https://api.coingecko.com/api/v3/coins/markets"
#     params = {
#         "vs_currency": "usd",
#         "ids": "bitcoin,tether,ethereum,binancecoin"  # Add more cryptocurrency IDs separated by commas
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error("Failed to fetch data from CoinGecko API")
#         return []

# # Fetch data from API
# data = fetch_crypto_data()

# # Convert data into a pandas DataFrame
# df = pd.DataFrame(data)

# # Streamlit App
# st.title("Cryptocurrency Dashboard")

# # Loop through each cryptocurrency in the DataFrame and display its details
# for i in range(len(df)):
#     st.image(df['image'][i], width=100)
#     st.header(f"{df['name'][i]} ({df['symbol'][i].upper()})")

#     # Display current price and market cap
#     st.metric("Current Price (USD)", f"${df['current_price'][i]:,.2f}")
#     st.metric("Market Cap", f"${df['market_cap'][i]:,}")
#     st.metric("Market Cap Rank", f"{df['market_cap_rank'][i]}")

#     # Display additional details
#     st.subheader("24h Statistics")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("24h High", f"${df['high_24h'][i]:,.2f}")
#         st.metric("24h Low", f"${df['low_24h'][i]:,.2f}")
#     with col2:
#         st.metric("Price Change (24h)", f"${df['price_change_24h'][i]:,.2f}")
#         st.metric("Price Change % (24h)", f"{df['price_change_percentage_24h'][i]:.2f}%")

#     st.subheader("All-Time Statistics")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("All-Time High", f"${df['ath'][i]:,.2f}", delta=f"{df['ath_change_percentage'][i]:.2f}% from ATH")
#     with col2:
#         st.metric("All-Time Low", f"${df['atl'][i]:,.2f}", delta=f"{df['atl_change_percentage'][i]:.2f}% from ATL")

#     # Display last updated time
#     last_updated = datetime.fromisoformat(df['last_updated'][i].replace('Z', '+00:00'))
#     st.write(f"Last Updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')} UTC")

#     st.markdown("---")  # Separator between cryptocurrencies
