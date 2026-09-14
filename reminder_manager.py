from datetime import date

from models import InvestTracker, Reminder


class ReminderManager:
    def __init__(self, investments: list[InvestTracker]):
        self.investments = investments

    def get_reminders(self, today: date | None = None) -> Reminder:
        """Generate reminders for investments based on their maturity dates."""
        today = today or date.today()
        reminder = Reminder()

        for investment in self.investments:
            if not investment.id:
                reminder.missing_id.append(investment)

            if not investment.maturity_date:
                continue

            days_remaining = (investment.maturity_date - today).days

            if days_remaining < 0:
                reminder.matured.append(investment)
            elif days_remaining <= 30:
                reminder.due_30_days.append(investment)
            elif days_remaining <= 60:
                reminder.due_60_days.append(investment)

        return reminder
