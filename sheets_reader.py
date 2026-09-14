from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pandas as pd

from constants import FD_SHEET, PORTFOLIO_SHEET, RD_SHEET
from models import InvestTracker, PortfolioItem


class SheetReader:
    RD_COLUMNS = {
        "Name",
        "Type",
        "ID",
        "Start Date",
        "Maturity Date",
        "MonthlyAmount",
        "MonthsPassed",
        "AmountAccumulated(L)",
    }

    FD_COLUMNS = {
        "Name",
        "Type",
        "ID",
        "Maturity Date",
        "AmountAccumulated(L)",
    }

    PORTFOLIO_COLUMNS = {
        "Portfolio",
        "Amount in Lakhs",
        "Rates(%)",
        "Monthly Investment (L)",
    }

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self._validate_file()

    def _validate_file(self) -> None:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Investment file not found: {self.file_path}")

    def _validate_columns(
        self,
        dataframe: pd.DataFrame,
        required_columns: set[str],
        sheet_name: str,
    ) -> None:
        missing = required_columns - set(dataframe.columns)
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ValueError(
                f"Missing column(s) in sheet '{sheet_name}': {missing_text}"
            )

    @staticmethod
    def _to_optional_date(value) -> date | None:
        if pd.isna(value) or value == "":
            return None

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
        if pd.isna(parsed):
            return None

        return parsed.date()

    @staticmethod
    def _to_optional_float(value) -> float | None:
        if pd.isna(value) or value == "":
            return None
        return float(value)

    @staticmethod
    def _to_optional_str(value) -> str | None:
        if pd.isna(value) or str(value).strip() == "":
            return None
        return str(value).strip()

    def get_portfolio_data(self) -> list[PortfolioItem]:
        """Read portfolio data from the Excel file and return a list of PortfolioItem objects."""
        df = pd.read_excel(self.file_path, sheet_name=PORTFOLIO_SHEET)
        self._validate_columns(df, self.PORTFOLIO_COLUMNS, PORTFOLIO_SHEET)

        items: list[PortfolioItem] = []

        for _, row in df.iterrows():
            items.append(
                PortfolioItem(
                    name=str(row["Portfolio"]).strip(),
                    monthly_invest=float(row["Monthly Investment (L)"]),
                    current_amount=float(row["Amount in Lakhs"]),
                    percent_return=float(row["Rates(%)"]),
                )
            )

        return items

    def get_rd_fds(self) -> list[InvestTracker]:
        """Read RD and FD data from the Excel file and return a list of InvestTracker objects."""
        trackers: list[InvestTracker] = []

        rd_df = pd.read_excel(self.file_path, sheet_name=RD_SHEET, header=3)
        self._validate_columns(rd_df, self.RD_COLUMNS, RD_SHEET)

        for _, row in rd_df.iterrows():
            trackers.append(
                InvestTracker(
                    name=str(row["Name"]).strip(),
                    asset_type=str(row["Type"]).strip(),
                    id=self._to_optional_str(row["ID"]),
                    start_date=self._to_optional_date(row["Start Date"]),
                    maturity_date=self._to_optional_date(row["Maturity Date"]),
                    monthly_invest=self._to_optional_float(row["MonthlyAmount"]),
                    current_amount=float(row["AmountAccumulated(L)"]),
                )
            )

        fd_df = pd.read_excel(self.file_path, sheet_name=FD_SHEET, header=4)
        self._validate_columns(fd_df, self.FD_COLUMNS, FD_SHEET)

        for _, row in fd_df.iterrows():
            trackers.append(
                InvestTracker(
                    name=str(row["Name"]).strip(),
                    asset_type=str(row["Type"]).strip(),
                    id=self._to_optional_str(row["ID"]),
                    maturity_date=self._to_optional_date(row["Maturity Date"]),
                    current_amount=float(row["AmountAccumulated(L)"]),
                )
            )

        return trackers
