FAKE_AVAILABILITY = {
    "2026-08-09" : "Available from 10:00 AM to 4:00 PM",
    "2026-08-10" : "Available from 5:00 PM to 10:00 PM",
    "2026-08-11" : "Not Available",
    "2026-08-12" : "Available from 9:00 AM to 10:00 PM",   
}

def get_ambani_availability(date: str) -> dict[str, str]:
    """
    Check the availability for a given date.

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
           "message": f"Availability for {date}, ambani is {availability}",
        }
    
    return {
        "status": "error",
        "message": f"No availability data found for {date}.",
    }