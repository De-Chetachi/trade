# Trading Script

This Python script gathers price action data for tokens following tweets that mention them.

* if you dont have a twitter and coingecko enterprise api key
* checkout the limited version in the trade folder


## Prerequisites

Ensure the following Python modules are installed:

* `requests`
* `pandas`
* `pymongo[srv]`

You can install them using pip:

```bash
python3 -m pip install  requests pandas "pymongo[srv]"
```

## Command-Line Arguments

The script accepts the following command-line arguments:
1.  **Usernamee:**
    * the username of the twitter influencer

2.  **Coin Name:**
    * The name of the cryptocurrency (e.g., `Pepe`).
3.  **Coin Ticker:**
    * The coin's ticker symbol (e.g., `\$PEPE`). Note the backslash (`\`) to escape the dollar sign (`$`) in the command line.
4.  **Timeframe (Days):**
    * The number of days to analyze the price action from the tweet time (must be a numerical value).

## Environment Variables

Set the following environment variable:

```bash
export GECKO_KEY=<your_gecko_api_key>
export TWITTER_TOKEN=<your_twitter_api_key>
export MONGO_URL=<your mongo database connection string>
```
Execute the script from your terminal using the following format:

```bash
./request.py <username> <coin_name> <coin_ticker> <timeframe_days>
```

example

```bash
./request.py ViperMasol solana \$SOL 5
```
