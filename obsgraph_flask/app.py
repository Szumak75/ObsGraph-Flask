"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Main Flask application for ObsGraph.
"""

from datetime import datetime
from typing import List
from flask import Flask, render_template, request


app: Flask = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    """Main page with year and month selection.

    ### Returns:
    str - Rendered HTML template with date selection form.
    """
    current_year: int = datetime.now().year
    current_month: int = datetime.now().month

    # Generate year list (current year + 3 years back)
    years: List[int] = list(range(current_year, current_year - 4, -1))

    # Generate month list (1-12)
    months: List[int] = list(range(1, 13))

    # Get selected values from form or use defaults
    selected_year: int = request.form.get("year", current_year, type=int)
    selected_month: int = request.form.get("month", current_month, type=int)

    # Format selected date
    selected_date: str = f"{selected_year:04d}-{selected_month:02d}"

    return render_template(
        "index.html",
        years=years,
        months=months,
        selected_year=selected_year,
        selected_month=selected_month,
        selected_date=selected_date,
    )


if __name__ == "__main__":
    app.run(debug=True)
