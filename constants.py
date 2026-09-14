from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

EXCEL_FILE = DATA_DIR / "InvestmentsTracker.xlsx"

RD_SHEET = "RD tracker"
FD_SHEET = "FD tracker"
PORTFOLIO_SHEET = "MasterInvestment"

PROJECTION_YEARS = [1, 3, 5, 10, 15, 20]

REMINDER_30_DAYS = 30
REMINDER_60_DAYS = 60
