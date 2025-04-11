# Trading Script

This Python script gathers price action data for tokens following tweets that mention them.

## Limitations

1.  **Real-time Tweet Data:**
    * The script cannot directly access real-time tweet data.
    * It relies on a user-specified object (`data` variable within the script) containing tweet information.
    * You must manually modify the `tweets` key within the `data` variable to simulate tweet data for testing.

2.  **Tweet Timeframe:**
    * For the script to function correctly, the `created_at` timestamp for each tweet must be within 24 hours of the current time.

## Prerequisites

Ensure the following Python modules are installed:

* `requests`
* `pandas`
* `pymongo[srv]`

You can install them using pip:

```bash
python3 -m pip install  requests pandas "pymongo[srv]"


## Command-Line Arguments

The script accepts the following command-line arguments:

1.  **Coin Name:**
    * The name of the cryptocurrency (e.g., `Pepe`).
2.  **Coin Ticker:**
    * The coin's ticker symbol (e.g., `\$PEPE`). Note the backslash (`\`) to escape the dollar sign (`$`) in the command line.
3.  **Timeframe (Days):**
    * The number of days to analyze the price action from the tweet time (must be a numerical value).

## Environment Variables

Set the following environment variable:

```bash
export GECKO_KEY=<your_gecko_api_key>

Execute the script from your terminal using the following format:

```bash
./request.py <coin_name> <coin_ticker> <timeframe_days>


example

./request.py Pepe \$PEPE 7

