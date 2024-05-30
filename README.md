# SOLID Score Module
The SOLID Score Module is designed to assess the level of "credibility" associated with given Solana wallet addresses through on-chain data analysis. 
By leveraging K-Means clustering, NFT interaction analysis, and risk scores from the Breadcrumbs API and RainFi API, this module provides a comprehensive credibility score for Solana wallets.

# Overview
The SOLID Score Module integrates various analytical methods to evaluate the credibility of Solana wallet addresses:

## K-Means Clustering: This technique is used to categorize wallets based on their transaction patterns and behaviors.
NFT Interaction Analysis: This involves analyzing the interactions of wallets with Non-Fungible Tokens (NFTs) to assess engagement and activity levels.
##Risk Scores from Breadcrumbs API and RainFi API: The module retrieves risk scores from both the Breadcrumbs and RainFi APIs to incorporate external assessments of wallet risk into the overall credibility score.

# Features
## Clustering: 
Group wallets with similar behaviors using K-Means clustering.

## NFT Analysis: 
Evaluate wallet activity and engagement in the NFT ecosystem.

## Risk Assessment: 
Integrate risk scores from the Breadcrumbs API and RainFi API to enhance credibility evaluation.

See https://docs.google.com/document/d/1nCSYwIekbrm7q1V0bLAcvehA75mBYfUgRHSE4odg2vo/edit?usp=sharing for full Algorithm documentation.

# NOTE:

-   The flask app is just a simple implementation of the analysis which only integrates the results from various analysis. It doesn't give the breif understanding of the underlaying algorithms
-   Check the seperate .py or .ipynb files made to implement the algorithms to get better understanding of them. 


# Running the flask app:

1. Navigate to the "flask app" folder.
   
2. ```bash
   pip install -r requirements.txt
   ```
   to install the requirements
   
3. ```bash
   python run app.py
   ```
   to run the app
