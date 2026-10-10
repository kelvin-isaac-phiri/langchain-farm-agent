from langchain_core.tools import tool
from ddgs import DDGS

from data import CROP_INFO
from db import get_farm


@tool
def get_farm_info(farm_id: str) -> str:
    """Get information about a farmer's farm from the agent_db database (farms table)."""

    farm = get_farm(farm_id)

    if not farm:
        return f"No farm found with ID {farm_id} in agent_db."

    return (
        f"Farmer: {farm['farmer']}\n"
        f"Crop: {farm['crop']}\n"
        f"Location: {farm['location']}\n"
        f"Soil: {farm['soil']}\n"
        f"Recent rainfall: {farm['last_rainfall']}\n"
        f"Irrigation: {farm['irrigation']}"
    )


@tool
def get_crop_information(crop: str) -> str:
    """Get common agricultural problems and possible causes of yellow leaves for a crop."""

    crop = crop.lower()

    info = CROP_INFO.get(crop)

    if not info:
        return f"No information available for {crop}."

    return (
        f"Crop: {crop}\n"
        f"Common problems: {', '.join(info['common_problems'])}\n"
        f"Possible causes of yellow leaves: "
        f"{', '.join(info['yellow_leaves'])}"
    )


@tool
def check_farm_weather(farm_id: str) -> str:
    """Get simple recent weather conditions for a farm (uses location from agent_db)."""

    farm = get_farm(farm_id)

    if not farm:
        return f"No farm found with ID {farm_id} in agent_db."

    # Fake weather data for the demo.
    if farm["location"] == "Lilongwe":
        return (
            "Recent weather in Lilongwe: "
            "low rainfall and several dry days."
        )

    if farm["location"] == "Dedza":
        return (
            "Recent weather in Dedza: "
            "high rainfall and several wet days."
        )

    return "Weather information is unavailable."


@tool
def search_web(query: str) -> str:
    """Search the web for recent farming advice, crop problems, or agricultural guidance.

    Use this when local farm/crop tools are not enough, or the farmer asks about
    a problem that needs outside information. Prefer a short, specific query.
    """

    query = query.strip()
    if not query:
        return "Please provide a search query."

    try:
        results = list(DDGS().text(query, max_results=5))
    except Exception as exc:
        return f"Web search failed: {exc}"

    if not results:
        return f"No web results found for: {query}"

    lines = [f"Web search results for: {query}", ""]
    for i, item in enumerate(results, start=1):
        title = item.get("title") or "Untitled"
        body = item.get("body") or ""
        href = item.get("href") or ""
        lines.append(f"{i}. {title}")
        if body:
            lines.append(f"   {body}")
        if href:
            lines.append(f"   Source: {href}")
        lines.append("")

    return "\n".join(lines).strip()
