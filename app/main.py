import os
from aiogmaps import Client
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from json.decoder import JSONDecodeError
from pydantic import ValidationError
import ptvsd

from dcr_point import DCRPoint, Point, Direction, Marker, Markers


"""
Enable remote debugging
"""

if os.getenv('ENVIRONMENT', 'PROD') != 'PROD':
    ptvsd.enable_attach()


app = FastAPI()


@app.post("/geo/reverse", response_model=Point)
async def reverse(direction: Direction):
    api_key = os.getenv('GMAP_API_KEY', None)
    async with Client(api_key) as client:
        response = await client.geocode(str(direction))
        if not response:
            raise HTTPException(status_code=404, detail=f"Direction not found: {str(direction)}")
        return JSONResponse(content=Point(**response[0]["geometry"]["location"]).dict())


@app.post("/geo/nearby", response_model=Markers)
def nearby(point: Point):
    markers = []
    dcrp = DCRPoint(point=point)
    for point in dcrp.nearby_points():
        distance = dcrp.calculate_distance(point)
        if dcrp.point == point:
            marker = Marker(infoText="you are here!", position=point)
        else:
            marker = Marker(infoText=f"{distance} Km", position=point)
        markers.append(marker)
    return JSONResponse(content=Markers(markers=markers).dict())
