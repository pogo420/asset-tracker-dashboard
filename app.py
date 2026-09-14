from constants import EXCEL_FILE, PROJECTION_YEARS
from projection_manager import ProjectionManager
from reminder_manager import ReminderManager
from sheets_reader import SheetReader
from template_manager import TemplateManager


def main() -> None:
    reader = SheetReader(EXCEL_FILE)

    portfolio_data = reader.get_portfolio_data()
    rd_fd_data = reader.get_rd_fds()

    reminder_data = ReminderManager(rd_fd_data).get_reminders()

    portfolio_projection_data = ProjectionManager(
        portfolio_items=portfolio_data,
        projection_years=PROJECTION_YEARS,
    )

    projections = portfolio_projection_data.get_projections()
    total_projections = portfolio_projection_data.get_total_projections()

    output = TemplateManager(
        reminders=reminder_data,
        projections=projections,
        total_projections=total_projections,
        investments=rd_fd_data,
        template_dir="templates",
    ).generate("report/dashboard.html")

    print(f"Dashboard generated: {output.resolve()}")


if __name__ == "__main__":
    main()
