import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP
from workshop_smolagents_mcp.event import Event

# TODO: name your mcp server
mcp = FastMCP("firsts-mcp")

# TODO: name the mcp tool
@mcp.tool(name=parse_datacraft_events, description="Parse events from datacraft.paris agenda page")
async def parse_datacraft_events() -> list[Event]:
    """Parse events from datacraft.paris agenda page"""
    # TODO: Fill the url variable with the correct url (datacraft.paris agenda page)
    url = "https://datacraft.paris/agenda"
    async with httpx.AsyncClient() as client:
        # TODO: use the client to get the url using the `get` method of the client.
        response = await client.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    events = []

    # Find events container
    # TODO: find the events container using the `find` method of the soup object, with parameters class_="tribe-events-calendar-list"
    events_container = soup.find(class_="tribe-events-calendar-list")
    event_containers = events_container.find_all(
        class_="tribe-events-calendar-list__event-wrapper"
    )

    for event_container in event_containers:
        event_title_component = event_container.find(
            class_="tribe-events-calendar-list__event-title-link"
        )
        event_title = event_title_component.text.strip().strip()
        event_url = event_title_component["href"].strip()
        event_datetime_component = event_container.find(
            class_="tribe-events-calendar-list__event-datetime"
        )
        event_date = event_datetime_component.find(class_="dateshed").text.strip()
        event_time = event_datetime_component.find(class_="timeshed").text.strip()
        event_location = event_container.find(
            class_="tribe-events-calendar-list__event-venue"
        ).text.strip()
        # TODO: using variables event_title, event_url, event_date, event_time, event_location, append a new Event object to the events list
        events.append(
            Event(
                title=event_title,
                url=event_url,
                date=event_date,
                time=event_time,
                location=event_location
            )
        )

    return events

# TODO: run the server using the `run` method of the mcp object, by wrapping it in a if __name__ == "__main__" block
if __name__ == "__main__":
    mcp.run()