# Algorithmic-Trading

This folder contains different options for attempting to trade stocks algorithmicly. DerivativeTrading.py is, as of yet, the most advanced one of these. It attempts to "buy low and sell high" by guessing when the derivitaves occur. It does this with a delay, since you cannot take a derivative on a one sided graph. Therefore, if the stock was going down and starts to go up, the program will trigger a buy. If the stock was going up and starts to go down, the program will trigger a sell. A graph showing the algorihtm's performance will appear upon the run. This program does operate under the assumption that, at least at a very low time scale, stocks act somewhat parabolic. I have not yet configured the program to actually buy and sell stock, as I do not have the $25k required by the SEC to avoid Patern Day Trading Restrictions.

```sh
To run this program, go to the DerivativeTrading.py file and run it. 
A simple GUI will pop up asking you to input a stock ticker and a start date (formatted like 2023-08-20). 
It is recommended that you use a date within the past few weeks, as historical stock data at 5 minute increments is not available. 
It is still a work in progress, as a CLI or more advanced GUI are yet to be implemented.
```
