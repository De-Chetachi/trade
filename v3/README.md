# Trading Script

This Python script gathers price action data for tokens following tweets that mention them.

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

2.  **Timeframe (Days):**
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
./request.py <username> <timeframe_days>
```

example

```bash
./request.py ViperMasol 5
```
