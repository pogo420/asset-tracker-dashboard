from dataclasses import dataclass, field
from datetime import date


@dataclass
class PortfolioItem:
    name: str
    monthly_invest: float
    current_amount: float
    percent_return: float


@dataclass
class InvestTracker:
    name: str
    asset_type: str
    id: str | None
    maturity_date: date | None
    start_date: date | None = None
    monthly_invest: float | None = None
    current_amount: float = 0.0


@dataclass
class Reminder:
    due_30_days: list[InvestTracker] = field(default_factory=list)
    due_60_days: list[InvestTracker] = field(default_factory=list)
    matured: list[InvestTracker] = field(default_factory=list)
    missing_id: list[InvestTracker] = field(default_factory=list)


@dataclass
class PortfolioProjection:
    name: str
    current_value: float
    projections: dict[int, float]
