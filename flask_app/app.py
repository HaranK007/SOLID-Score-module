from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

scaler = joblib.load('scaler.joblib')
kmeans = joblib.load('kmeans_model.joblib')

def fetch_onchain_data(wallet_address):
    url = f"https://api.solana.fm/v0/accounts/{wallet_address}/transfers"
    response = requests.get(url)

    parssedTxResult = []
    if response.status_code == 200:
        data = response.json()
        
        results = data.get('results')

        for tx in results:
            data = tx.get('data',[])
            for i in data:
            
                parssedTxResult.append(
                    {
                        'status' : i.get('status'),
                        'action' : i.get('action'),
                        'amount' : i.get('amount'),
                        'counterparty' : i.get('destination'),
                        'timestamp' : datetime.fromtimestamp(i.get('timestamp')),
                    }
                )
    else:
        print(f"Request failed with status code {response.status_code}")
    return parssedTxResult

def calculate_total_transactions(transactions):
    return len(transactions)

def calculate_daily_transaction_count(transactions):
    daily_count = {}
    
    for tx in transactions:
        date = tx['timestamp'].strftime('%Y-%m-%d')
        if date not in daily_count:
            daily_count[date] = 1
        daily_count[date] += 1
    return daily_count

def calculate_transaction_intervals(transactions):
    intervals = []
    timestamps = [tx['timestamp'] for tx in transactions]
    timestamps.sort()
    for i in range(1, len(timestamps)):
        interval = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600.0
        intervals.append(interval)
    return intervals

def calculate_total_transaction_volume(transactions):
    return sum(tx['amount'] for tx in transactions)

def calculate_mean_transaction_amount(transactions):
    return np.mean([tx['amount'] for tx in transactions])

def calculate_variance_transaction_amount(transactions):
    return np.var([tx['amount'] for tx in transactions])

def calculate_unique_counterparties(transactions):
    counterparties = set(tx['counterparty'] for tx in transactions)
    return len(counterparties)

def detect_high_frequency_bursts(transactions, threshold=1):
    bursts = 0
    intervals = calculate_transaction_intervals(transactions)
    for interval in intervals:
        if interval < threshold:
            bursts += 1
    return bursts

def calculate_success_rate(transactions):
    total_transactions = len(transactions)
    successful_transactions = sum(1 for tx in transactions if tx['status'] == 'Successful')
    return successful_transactions / total_transactions if total_transactions > 0 else 0

def calculate_time_of_day_activity(transactions):
    hours = [tx['timestamp'].hour for tx in transactions]
    return np.mean(hours) if hours else 0

def calculate_transfer_counts(transactions):
    transfer_counts = [
        "transfer",
        "transferWithSeed",
        "transferChecked",
        "transferCheckedWithFee"
    ]

    transfer = 0
    for tx in transactions:
        tx_type = tx['action']
        if tx_type in transfer_counts:
            transfer += 1
    
    return transfer / len(transactions)

def calculate_mint_and_sig_counts(transactions):
    account_creation_counts = [
        "mintTo",
        "initializeMint",
        "initializeMint2",
        "initializeMultisig",
        "initializeMultisig2"
    ]

    count = 0
    for tx in transactions:
        tx_type = tx['action']
        if tx_type in account_creation_counts:
            count += 1
    
    return count / len(transactions)

def preprocess(transactions):
    features = []
    total_transactions = calculate_total_transactions(transactions)
    daily_transaction_count = calculate_daily_transaction_count(transactions)
    transaction_intervals = calculate_transaction_intervals(transactions)
    total_transaction_volume = calculate_total_transaction_volume(transactions)
    mean_transaction_amount = calculate_mean_transaction_amount(transactions)
    variance_transaction_amount = calculate_variance_transaction_amount(transactions)
    unique_counterparties = calculate_unique_counterparties(transactions)
    high_frequency_bursts = detect_high_frequency_bursts(transactions)
    success_rate = calculate_success_rate(transactions)
    time_of_day_activity = calculate_time_of_day_activity(transactions)

    transfer_counts = calculate_transfer_counts(transactions)
    mint_and_sig_counts = calculate_mint_and_sig_counts(transactions)

    feature_vector = [
        total_transactions,
        len(daily_transaction_count), 
        np.mean(transaction_intervals) if transaction_intervals else 0,
        total_transaction_volume,
        mean_transaction_amount,
        variance_transaction_amount,
        unique_counterparties,
        high_frequency_bursts,
        success_rate,
        time_of_day_activity,
        transfer_counts,
        mint_and_sig_counts
    ]
    
    feature_names = [
        'Total_Transactions',
        'Unique_Days',
        'Mean_Transaction_Interval',
        'Total_Transaction_Volume',
        'Mean_Transaction_Amount',
        'Variance_Transaction_Amount',
        'Unique_Counterparties',
        'High_Frequency_Bursts',
        'Success_Rate',
        'Time_Of_Activity',
        'Transfer_Counts',
        'Mint_And_Sig_Counts'
    ]

    features.append(feature_vector)
    features_df = pd.DataFrame(features, columns=feature_names)

    return features_df

def predict_cluster(features_df):
    scaled_features = scaler.transform(features_df)

    predicted_cluster = kmeans.predict(scaled_features)
    return predicted_cluster

def nft_analysis(address):
    url = f"https://api-mainnet.magiceden.dev/v2/wallets/{address}/activities"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    magic_eden_activities_data =[]

    if response.status_code == 200:
        result = response.json()
        
        for data in result:
            magic_eden_activities_data.append(
                {
                    'blockTime': data.get('blockTime'),
                    'type': data.get('type'),
                    'priceInfo': data.get('priceInfo'),
                    'price': data.get('price'),
                    'collection': data.get('collection'),
                }
            )
    else:
        print(f"Request failed with status code {response.status_code}")

    if len(magic_eden_activities_data) == 0:
        return None, None

    df = pd.DataFrame(magic_eden_activities_data)

    df['blockTime'] = pd.to_datetime(df['blockTime'], unit='s')

    plt.figure(figsize=(10, 6))
    plt.scatter(df['blockTime'], df['price'], c='blue', label='NFT Activities')
    plt.xlabel('Date')
    plt.ylabel('SOL spent')
    plt.title('NFT Activities Over Time')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    df['is_buy'] = df['type'].apply(lambda x: 1 if x == 'buyNow' else 0)
    df['is_sell'] = df['type'].apply(lambda x: 1 if x == 'list' else 0)
    df['is_mint'] = df['type'].apply(lambda x: 1 if x == 'mint' else 0)

    min_date = df['blockTime'].min()
    max_date = df['blockTime'].max()
    num_weeks = (max_date - min_date).days / 7
    avg_transactions_per_week = len(df) / num_weeks

    activity_span_in_months = (max_date - min_date).days / 30

    unique_transaction_types = df['type'].nunique()

    total_transactions = len(df)

    freq_criteria = avg_transactions_per_week >= 1
    consistency_criteria = activity_span_in_months >= 3
    diversity_criteria = unique_transaction_types >= 2
    volume_criteria = total_transactions >= 10

    is_regular = all([freq_criteria, consistency_criteria, diversity_criteria, volume_criteria])

    return is_regular, plot_url

def breadcrumbs_checker(address):
    url = "https://api.breadcrumbs.one/risk/address?chain=SOL&address=arsc4jbDnzaqcCLByyGo7fg7S2SmcFsWUzQuDtLZh2y&include_exposure=false"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "GXJDHW8DDIZPWWP5QMCBU5HLXTIX02"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        
        risk_score = result.get('risk_score')
        entity_tags = result.get('entity_tags')

        return risk_score,entity_tags

    else:
        print(f"Request failed with status code {response.status_code}")
        return None,None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score_wallet():
    wallet_address = request.form['wallet_address']
    
    onchain_data = fetch_onchain_data(wallet_address)
    
    features = preprocess(onchain_data)
    cluster = predict_cluster(features)

    nft_data, nft_activities_plot_url = nft_analysis(wallet_address)
    
    
    if nft_data == None:
        nft_user = 'no nft interactions'
    elif nft_data:
        nft_user = 'regular nft user'
    else:
        nft_user = 'not regular nft user'

    risk_score, tags = breadcrumbs_checker(wallet_address)

    return render_template('index.html', 
                           cluster=cluster[0], 
                           wallet_address=wallet_address, 
                           nft_user = nft_user,
                           risk_score = risk_score,
                           tags = tags,
                           nft_activities_plot_url = nft_activities_plot_url
    )

if __name__ == '__main__':
    app.run(debug=True)
