from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv
import os

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data or "properties" not in points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    try:
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await make_nws_request(forecast_url)
    except KeyError:
        return "Invalid response format from weather service."

    if not forecast_data or "properties" not in forecast_data or "periods" not in forecast_data["properties"]:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.tool()
async def create_freshdesk_ticket(subject: str, requester_id: str,description:str) -> str:
    """Create a Freshdesk ticket.

    Args:
        subject: Subject of the ticket
        requester_id: Email or ID of the requester
        description: Description of the issue
    """
    freshdesk_url = os.getenv("FRESHDESK_API")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {os.getenv('FRESHDESK_API_AUTH')}"
    }
    data = {
        "subject": subject,
        "description": description,
        "email": requester_id,
        "priority": 1,
        "status": 2
    }
    
    {
    "custom_fields": {
        "cf_closure_test": "TEST Balu",
        "cf_number": 994354681,
        "cf_single_line_text": "test",
        "cf_dropdown": "First Choice"
    },
    "status": 2,
    "priority": 1,
    "responder_id": 26010786932,
    "type": "Trustpilot Review",
    "subject": subject,
    "email": requester_id,
    "description": description
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(freshdesk_url, json=data, headers=headers)
            response.raise_for_status()
            return f"Ticket created successfully with ID: {response.json().get('id')}"
        except Exception as e:
            return f"Failed to create ticket: {e}"

if __name__ == "__main__":
    # Initialize and run the server
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        print("Server shutting down")
    except Exception as e:
        print(f"Error starting server: {e}")