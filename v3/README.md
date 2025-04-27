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

2.  **Timeframe (Days):**
    * The number of days to analyze the price action from the tweet time (must be a numerical value).

