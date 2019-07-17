# Bexio

Algorithmic Trading using BitMEX

#### TODO Data Analysis

-   Normalization
-   Compute vwap
-   Triple barrier method

#### Improvements

-   use raw bid/ask quote as input (calculate dollar volume, bid/ask spread, hlc, etc.)

The following script can be used in console (developer tools) to retrieve the .csv url's, then copied from the console output to `data/quote_urls.txt` or `data/trade_urls.txt`

<https://public-testnet.bitmex.com/?prefix=data/quoteBin1m>
<https://public-testnet.bitmex.com/?prefix=data/tradeBin1m>

```javascript
for (let i = 0; i <document.links.length ; i++) {
    if (document.links[i].innerHTML.includes(".csv")) {
		console.log(document.links[i].href)
    }
}
```
