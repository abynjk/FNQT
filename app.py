import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from web3 import Web3

# === CONFIG ===
RPC_URL = "https://polygon-rpc.com"
CONTRACT_ADDRESS = "0xfD5a2488f3ea1F61FF462730B14f57a108a7f9eC"
ABI = [
    {
        "inputs": [],
        "name": "getNAV",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# === Web3 Connection ===
web3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

# === Get live on-chain values ===
live_nav = contract.functions.getNAV().call() / 1e18
token_name = contract.functions.name().call()
token_symbol = contract.functions.symbol().call()
total_supply = contract.functions.totalSupply().call() / 1e18

# === Load historical NAV data ===
nav_df = pd.read_csv("nav_log.csv")
nav_df['Date'] = pd.to_datetime(nav_df['date'], format='mixed', dayfirst=False, errors='coerce')
nav_df['NAV'] = nav_df['nav']
nav_df['Daily Return'] = nav_df['return']
nav_df.drop(columns=['date', 'nav', 'return'], inplace=True)
nav_df.sort_values('Date', inplace=True)

# === UI ===
st.set_page_config(page_title="FNQT NAV Dashboard", layout="wide")
st.title("📊 FNQT Token NAV Dashboard")

st.metric("🔵 Live NAV (on-chain)", f"{live_nav:.4f}")
st.metric("🪙 Total Supply", f"{total_supply:,.0f} {token_symbol}")

# === NAV Chart ===
st.subheader("📈 NAV Trend (Historical)")
plot_df = nav_df.tail(90)
fig = px.line(plot_df, x='Date', y='NAV', title='NAV Over Time', markers=True)
st.plotly_chart(fig, use_container_width=True)

# === Daily Returns ===
st.subheader("📅 Daily Returns")
st.dataframe(nav_df.tail(30)[['Date', 'NAV', 'Daily Return']].sort_values('Date', ascending=False), use_container_width=True)

# === Token Info ===
st.markdown("---")
st.subheader("ℹ️ Token Info")
st.markdown(f"""
- **Token Name:** {token_name}  
- **Symbol:** {token_symbol}  
- **Polygon Contract:** [View on Polygonscan](https://polygonscan.com/address/{CONTRACT_ADDRESS})  
""")
