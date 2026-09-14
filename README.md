# Investment Dashboard

Small home-use investment dashboard.

## Responsibilities

- Reminder Manager
  - Tracks RD / FD maturity dates
  - Skips rows without maturity dates
  - Shows 0–30 day, 31–60 day and matured investments
  - Flags missing IDs

- Projection Manager
  - Reads aggregated portfolio data
  - Projects future values for configured time periods
  - Uses current amount, expected annual return and monthly investment

## Expected sheets

### RD

`Name | Type | ID | Start Date | Maturity Date | MonthlyAmount | MonthsPassed | AmountAccumulated(L)`

### FD

`Name | Type | ID | Maturity Date | AmountAccumulated(L)`

### Portfolio

`Portfolio | Amount in Lakhs | Rates(%) | Monthly Investment (L)`

## Run

1. Put your workbook at:

   `data/InvestmentsTracker.xlsx`

2. Install dependencies:

   `pip install -r requirements.txt`

3. Run:

   `python app.py`

4. Open:

   `report/dashboard.html`

## Notes

All investment amounts are assumed to be in lakhs.
