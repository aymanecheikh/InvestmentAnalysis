# Quant Project
## Client
### Current Design
#### Fetch Data
- **Source:** Yahoo Finance
- **Data:** Historical Stock Prices since IPO
- **Index:** Date
- **Columns:** Open, High, Low, Close, Volume, Dividends, Stock Splits
- **Format:** pandas.DataFrame
#### Process Data
- Only keep Open, High, Low, Close, and Volume
- Reset index so that Date is transformed into a column
- Convert DataFrame to json format containing a list of records.
- Ensure that Date values are converted to iso format for compatibility.
#### Send Data
- Client sends a POST request to the API, passing the processed JSON object as a payload.
#### Receive Data
- Client receives Closing Price predictions for the next 10 days.
### Next Steps
#### Fetch Data
##### Yahoo Finance
- Explore intraday data (high priority)
- Explore other Yahoo Finance endpoints (low priority)
##### Other Data Sources
- Interactive Broker API Integration (high priority)
- Binance API Integration (medium priority)
#### Process Data
- Include Dividends and Stock Splits (low priority)
#### Send Data
- Think about what can be configurable to the client. What aspects of the model can be specified by the client and passed to params of classes and methods within the model?
#### Receive Data
- What does the client ultimately want from the model?
- How can we design the response payload for ease of integration with order execution, dashboards, presentations, marketing material, and inputs to other downstream systems?
## API

## Analysis

