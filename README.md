# SOLID Score Module

This SOLID Score Module is build to indicate the level of “credibility”  
associated with the given Solana wallet addresses using on-chain data analysis. 


# Overview

The model utilizes K-Means clustering, NFT interaction analysis, and 
risk scores obtained from Breadcrumbs API to achieve this objective.

See https://docs.google.com/document/d/1nCSYwIekbrm7q1V0bLAcvehA75mBYfUgRHSE4odg2vo/edit?usp=sharing for full Algorithm documentation.


File structure explaination:

.
├── flask app                           # A flask app where the analysis are integrated [kmeans, nft-analysis (only using magiceden data) and breadcrumbs score]
|    └── static
|    └── templates
|    └── app.py
|    └── kmeans_model.joblib             
|    └── scalar.joblib
|    └── requirements.txt
├── test_model_kmeans.ipynb             # Code to test the trained k-Means model
├── train_model_Kmeans.ipynb            # Code to train the k-means model
├── nft_activities.ipynb                # code to analyse the nft activities using magiceden endpoint




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
