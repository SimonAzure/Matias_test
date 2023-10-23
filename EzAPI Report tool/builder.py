import json
import datetime

def validate_inputs(report_type, columns, timezone, format, report_interval, start_date, end_date):
    # Check if report_type is valid
    valid_report_types = ["network_analytics", "seller_fill_and_delivery", "campaign_report"]
    if report_type not in valid_report_types:
        return False, "Invalid report type. Please select a valid report type."

    # Check if columns are provided and valid
    if not columns or not all(isinstance(column, str) for column in columns):
        return False, "Invalid columns. Please provide valid column names."

    # Check if timezone is valid
    valid_timezones = ["UTC", "Europe/London", "Europe/Paris", "Europe/Berlin"]
    if timezone not in valid_timezones:
        return False, "Invalid timezone. Please select a valid timezone."

    # Check if format is valid
    valid_format = ["csv", "excel", "html"]
    if format not in valid_format:
        return False, "Invalid format. Please select a valid format"

    # Check if report_interval is valid
    valid_report_interval = ["current_hour", "last_hour", "today", "yesterday", "last_48_hours", "last_7_days"]
    if report_interval not in valid_report_interval:
        return False, "Invalid report interval. Please select a valid one"


    # Check if start_date and end_date are in correct format
    try:
        datetime.datetime.strptime(start_date, "%d/%m/%Y")
        datetime.datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        return False, "Invalid date format. Please enter dates in the format dd/mm/yyyy."

    # Check if start_date is before end_date
    start_date_obj = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    end_date_obj = datetime.datetime.strptime(end_date, "%d/%m/%Y")
    if start_date_obj >= end_date_obj:
        return False, "Invalid date range. The start date must be before the end date."

    # Additional checks can be added here based on your specific requirements

    return True, ""

def build_json(report_type, columns, timezone, format, report_interval, start_date, end_date):
    # Construct the JSON object based on the user inputs
    report_config = {
        "report_type": report_type,
        "columns": columns,
        "timezone": timezone,
        "format": format,
	"report_interval": report_interval,
        "start_date": start_date,
        "end_date": end_date
    }
    report = {
        "report": report_config
    }

    return json.dumps(report, indent=4)

# User inputs (can be obtained from the UI)
report_type = "sales_report"
columns = ["revenue", "units_sold"]
timezone = "UTC"
format = "csv"
report_interval = "last_7_days"
start_date = "2023-01-01"
end_date = "2023-01-31"

# Validate inputs
if validate_inputs(report_type, columns, timezone, format, report_interval, start_date, end_date):
    # Build the JSON
    report_json = build_json(report_type, columns, timezone, format, report_interval, start_date, end_date)
    print(report_json)
else:
    print("Invalid inputs. Please check your inputs and try again.")
