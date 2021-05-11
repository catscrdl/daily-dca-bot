# Readme

Daily dollar cost averaging (DCA) using alpaca partial shares and their API.

Shares purchased based on input sources.

# Architecture

## Controller

Runs the app. Pulls in stocks to buy and sends them to the stock purchaser

## Stock Purchaser

Makes daily purchases using fractional shares and alpaca

## Inputs

### Motley Fool Premium

If you have premium fool services, you can enter your credentials and get collect their daily picks