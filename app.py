import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# पेज सेटअप
st.set_page_config(page_title="Technical Analysis Dashboard", layout="wide")

st.title("📊 TradingView Style Analysis Dashboard")

# साईडबार - इनपुट
ticker = st.sidebar.text_input("स्टॉक सिम्बॉल (उदा. RELIANCE.NS)", "RELIANCE.NS")
timeframe = st.sidebar.selectbox("Timeframe", ["5m", "15m", "1h", "1d"])

def get_technical_analysis(df):
    # RSI (Relative Strength Index)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    # 20 EMA
    df['EMA20'] = ta.ema(df['Close'], length=20)
    # MACD
    macd = ta.macd(df['Close'])
    df = pd.concat([df, macd], axis=1)
    return df

if st.sidebar.button("Analyze"):
    try:
        # डेटा डाऊनलोड
        df = yf.download(ticker, period="1mo", interval=timeframe)
        
        if df.empty:
            st.error("डेटा सापडला नाही, कृपया सिम्बॉल तपासा (उदा. TCS.NS).")
        else:
            df = get_technical_analysis(df)
            
            curr_price = df['Close'].iloc[-1]
            rsi = df['RSI'].iloc[-1]
            ema20 = df['EMA20'].iloc[-1]
            
            # TradingView सारखे लॉजिक
            signals = 0
            if rsi < 30: signals += 1 
            elif rsi > 70: signals -= 1
            
            if curr_price > ema20: signals += 1
            else: signals -= 1

            # Summary Display
            st.subheader("Technical Summary")
            if signals > 0:
                st.success("Strong Buy / Strong")
            elif signals < 0:
                st.error("Strong Sell / Weak")
            else:
                st.warning("Neutral")

            st.write(f"**Current Price:** {curr_price:.2f} | **RSI:** {rsi:.2f} | **EMA20:** {ema20:.2f}")
            st.line_chart(df[['Close', 'EMA20']])
            
    except Exception as e:
        st.error(f"काहीतरी तांत्रिक चूक झाली आहे: {e}")
else:
    st.info("स्टॉक सिम्बॉल टाकून 'Analyze' बटणावर क्लिक करा.")
