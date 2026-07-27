from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("WeatherService")

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get the weather forecast/details for a given city."""
    import requests
    
    if not city:
        return {"error": "City parameter is missing."}
        
    # Geocode city to coordinates
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    try:
        geo_res = requests.get(geocode_url).json()
        results = geo_res.get("results")
        if not results:
            return {"error": f"City '{city}' not found."}
        lat = results[0]["latitude"]
        lon = results[0]["longitude"]
    except Exception as e:
        return {"error": f"Geocoding failed for '{city}': {str(e)}"}
        
    # Fetch weather forecast (1 day only to keep response small)
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days=1"
    try:
        weather_res = requests.get(weather_url).json()
        return weather_res
    except Exception as e:
        return {"error": f"Weather lookup failed for coordinates ({lat}, {lon}): {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="stdio")