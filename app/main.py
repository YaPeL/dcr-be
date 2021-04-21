import os
from aiogmaps import Client
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from json.decoder import JSONDecodeError
from pydantic import ValidationError
import ptvsd

from dcr_point import DCRPoint, Point, Direction


"""
Enable remote debugging
"""

if os.getenv('ENVIRONMENT', 'PROD') != 'PROD':
    ptvsd.enable_attach()


app = FastAPI()


@app.post("/geo/reverse")
async def reverse(direction: Direction):
    api_key = os.getenv('GMAP_API_KEY', None)
    async with Client(api_key) as client:
        response = await client.geocode(str(direction))
        if not response:
            raise HTTPException(status_code=404, detail=f"Direction not found: {str(d)}")
        return JSONResponse(content=response[0]["geometry"]["location"])


@app.post("/geo/nearby")
async def nearby(point: Point):
    response = {"markers": []}
    try:
        dcrp = DCRPoint(point=point)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Bad request: {e.json()}")
    for point in dcrp.nearby_points():
        distance = dcrp.calculate_distance(point)
        if dcrp.point == point:
            marker = {"infoText": f"you are here!", "position": point.dict()}
        else:
            marker = {"infoText": f"{distance} Km", "position": point.dict()}
        response["markers"].append(marker)
    return JSONResponse(content=response)
