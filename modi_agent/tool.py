FAKE_AVAILABILITY = {
    "2026-08-09" : "Available from 10:00 AM to 4:00 PM",
    "2026-08-10" : "available from 1:00 PM to 5:00 PM",
    "2026-08-11" : "Available all day",
    "2026-08-12" : "Not Available",
    "2026-08-13" : "Available from 9:00 AM to 12:00 PM",
}

def get_modi_availability(date: str) -> dict[str, str]:
    """
    Check the availability for a given date for modi.

    Args:
        date (str): The date to check availability for in 'YYYY-MM-DD' format.

    Returns:
        dict: A small dictionary containing the date and its availability status.
    
    """
    if not date:
        return {"error": "Date parameter is missing."}
    availability = FAKE_AVAILABILITY.get(date, "No data available for this date.")

    if availability:
        return {
           "status": "success",
           "message": f"Availability for {date}, Modi is {availability}",
        }
    
    return {
        "status": "error",
        "message": f"No availability data found for {date}.",
    }

from crewai.tools import BaseTool


class ModiAvailabilityTool(BaseTool):
    name: str = "Modi's Availability Checker Tool"
    description: str = (
        "A tool to check Modi's availability on specific dates. "
        "Use this tool to find out if Modi is available on a given date."
    )

    def _run(self, date: str) -> str:
        return get_modi_availability(date)["message"]
