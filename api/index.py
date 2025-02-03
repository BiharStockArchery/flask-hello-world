import os
from flask import Flask, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)
 
# List of all stocks
all_stocks = [
    "AXISBANK.NS", "AUBANK.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS",
    "CANBK.NS", "CUB.NS", "FEDERALBNK.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "IDFCFIRSTB.NS", "INDUSINDBK.NS", "KOTAKBANK.NS", "PNB.NS", "RBLBANK.NS",
    "SBIN.NS", "YESBANK.NS", "ABCAPITAL.NS", "ANGELONE.NS", "BAJFINANCE.NS",
    "BAJAJFINSV.NS", "CANFINHOME.NS", "CHOLAFIN.NS", "HDFCAMC.NS", "HDFCLIFE.NS",
    "ICICIGI.NS", "ICICIPRULI.NS", "LICIHSGFIN.NS", "M&MFIN.NS", "MANAPPURAM.NS",
    "MUTHOOTFIN.NS", "PEL.NS", "PFC.NS", "POONAWALLA.NS", "RECLTD.NS", "SBICARD.NS",
    "SBILIFE.NS", "SHRIRAMFIN.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "BPCL.NS",
    "GAIL.NS", "GUJGASLTD.NS", "IGL.NS", "IOC.NS", "MGL.NS", "NTPC.NS", "OIL.NS",
    "ONGC.NS", "PETRONET.NS", "POWERGRID.NS", "RELIANCE.NS", "SJVN.NS", "TATAPOWER.NS",
    "ADANIENSOL.NS", "NHPC.NS", "ACC.NS", "AMBUJACEM.NS", "DALBHARAT.NS", "JKCEMENT.NS",
    "RAMCOCEM.NS", "SHREECEM.NS", "ULTRACEMCO.NS", "APLAPOLLO.NS", "HINDALCO.NS",
    "HINDCOPPER.NS", "JINDALSTEL.NS", "JSWSTEEL.NS", "NATIONALUM.NS", "NMDC.NS",
    "SAIL.NS", "TATASTEEL.NS", "VEDL.NS", "BSOFT.NS", "COFORGE.NS", "CYIENT.NS",
    "INFY.NS", "LTIM.NS", "LTTS.NS", "MPHASIS.NS", "PERSISTENT.NS", "TATAELXSI.NS",
    "TCS.NS", "TECHM.NS", "WIPRO.NS", "ASHOKLEY.NS", "BAJAJ-AUTO.NS", "BHARATFORG.NS",
    "EICHERMOT.NS", "HEROMOTOCO.NS", "M&M.NS", "MARUTI.NS", "MOTHERSON.NS",
    "TATAMOTORS.NS", "TVSMOTOR.NS", "ABFRL.NS", "DMART.NS", "NYKAA.NS", "PAGEIND.NS",
    "PAYTM.NS", "TRENT.NS", "VBL.NS", "ZOMATO.NS", "ASIANPAINT.NS", "BERGEPAINT.NS",
    "BRITANNIA.NS", "COLPAL.NS", "DABUR.NS", "GODREJCP.NS", "HINDUNILVR.NS",
    "ITC.NS", "MARICO.NS", "NESTLEIND.NS", "TATACONSUM.NS", "UBL.NS", "UNITEDSPR.NS",
    "VOLTAS.NS", "ALKEM.NS", "APLLTD.NS", "AUROPHARMA.NS", "BIOCON.NS", "CIPLA.NS",
    "DIVISLAB.NS "DRREDDY.NS", "GLAND.NS", "LUPIN.NS", "NATIONALUM.NS", "PHOENIXLTD.NS",
    "SUNPHARMA.NS", "TORNTPHARM.NS", "WOCKPHARMA.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "KOTAKBANK.NS", "PNB.NS", "SBIN.NS", "YESBANK.NS"
]

def get_previous_trading_day():
    today = pd.Timestamp.today()
    previous_day = today - pd.offsets.BDay(1)
    return previous_day

@app.route('/gainers', methods=['GET'])
def gainers():
    previous_day = get_previous_trading_day()
    stock_info = {}

    for stock in all_stocks:
        data = yf.download(stock, start=previous_day, end=previous_day + pd.Timedelta(days=1))
        if not data.empty:
            previous_close = data['Close'].iloc[0]
            current_data = yf.download(stock, period='1d')
            current_price = current_data['Close'].iloc[-1]
            percentage_change = ((current_price - previous_close) / previous_close) * 100
            
            if percentage_change > 0:
                stock_info[stock] = {
                    'previous_close': float(previous_close),
                    'current_price': float(current_price),
                    'percentage_change': float(percentage_change)
                }

    return jsonify(stock_info)

@app.route('/losers', methods=['GET'])
def losers():
    previous_day = get_previous_trading_day()
    stock_info = {}

    for stock in all_stocks:
        data = yf.download(stock, start=previous_day, end=previous_day + pd.Timedelta(days=1))
        if not data.empty:
            previous_close = data['Close'].iloc[0]
            current_data = yf.download(stock, period='1d')
            current_price = current_data['Close'].iloc[-1]
            percentage_change = ((current_price - previous_close) / previous_close) * 100
            
            if percentage_change < 0:
                stock_info[stock] = {
                    'previous_close': float(previous_close),
                    'current_price': float(current_price),
                    'percentage_change': float(percentage_change)
                }

    return jsonify(stock_info)

# Vercel requires the app to be exposed as a callable
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
