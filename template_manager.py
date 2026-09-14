from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from models import InvestTracker, PortfolioProjection, Reminder


class TemplateManager:
    def __init__(
        self,
        reminders: Reminder,
        projections: list[PortfolioProjection],
        total_projections: dict[int, float],
        investments: list[InvestTracker],
        template_dir: str | Path,
    ):
        self.reminders = reminders
        self.projections = projections
        self.total_projections = total_projections
        self.investments = investments
        self.template_dir = Path(template_dir)

    def generate(
        self,
        output_path: str | Path = "dashboard.html",
    ) -> Path:
        """Generate the dashboard HTML file using the provided template and data."""
        env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

        template = env.get_template("dashboard.html")

        rendered = template.render(
            reminders=self.reminders,
            projections=self.projections,
            total_projections=self.total_projections,
            investments=self.investments,
        )

        output_path = Path(output_path)
        output_path.write_text(rendered, encoding="utf-8")
        return output_path
