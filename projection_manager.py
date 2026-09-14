from models import PortfolioItem, PortfolioProjection


class ProjectionManager:
    def __init__(
        self,
        portfolio_items: list[PortfolioItem],
        projection_years: list[int],
    ):
        self.portfolio_items = portfolio_items
        self.projection_years = projection_years

    @staticmethod
    def _future_value(
        current_value_lakhs: float,
        monthly_invest_lakhs: float,
        annual_rate_percent: float,
        years: int,
    ) -> float:
        """Calculate the future value of an investment given the current value, monthly investment, annual rate, and number of years."""
        months = years * 12
        monthly_rate = annual_rate_percent / 100 / 12

        if monthly_rate == 0:
            return current_value_lakhs + (monthly_invest_lakhs * months)

        current_value_future = current_value_lakhs * (
            (1 + monthly_rate) ** months
        )

        monthly_invest_future = monthly_invest_lakhs * (
            ((1 + monthly_rate) ** months - 1) / monthly_rate
        )

        return current_value_future + monthly_invest_future

    def get_projections(self) -> list[PortfolioProjection]:
        """Calculate the future value of each portfolio item for the specified projection years."""
        result: list[PortfolioProjection] = []

        for item in self.portfolio_items:
            projections = {
                year: self._future_value(
                    current_value_lakhs=item.current_amount,
                    monthly_invest_lakhs=item.monthly_invest,
                    annual_rate_percent=item.percent_return,
                    years=year,
                )
                for year in self.projection_years
            }

            result.append(
                PortfolioProjection(
                    name=item.name,
                    current_value=item.current_amount,
                    projections=projections,
                )
            )

        return result

    def get_total_projections(self) -> dict[int, float]:
        """Aggregate the projections across all portfolio items to get total projections for each year."""
        projections = self.get_projections()

        totals = {}

        for projection in projections:
            totals[0] = totals.get(0, 0) + projection.current_value
            for year, value in projection.projections.items():
                totals[year] = totals.get(year, 0) + value           
        totals = dict(sorted(totals.items()))
        return totals
