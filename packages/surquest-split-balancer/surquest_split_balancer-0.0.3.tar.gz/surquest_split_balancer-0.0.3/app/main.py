
import enum
from typing import List
import requests
from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse



app = FastAPI()

@app.post("/pmp/integration/test")
def integrate(
    actions: Action = Query(
        ...,
        description="Action to perform"
    ),
    country: Country = Query(
        ...,
        description="Country code of PMP system"
    ),
    integration_channels: List[IntegrationChannel] = Query(
        [IntegrationChannel.restapi.value],
        alias="integrationChannels",
        description="List of integration channels"
    ),	
    data: dict = Body(
        ...,
        description="Campaign payload"
    )

):



    if IntegrationChannel.restapi.value in integration_channels:
        url = f"https://pmp.pos-media.eu/{country.name}/ws/ConnectMedia.php?WS_action={actions.name}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                url,
                headers=headers,
                json=[data]
            )
        except BaseException as e:
            return JSONResponse(
                content={
                    "status": 500,
                    "data": str(e)
                }
            )
        
        try:
            data = response.json()
        except BaseException as e:
            data = response.text

        return JSONResponse(
            content={
                "status": response.status_code,
                "data": data
            }
        )
    
    return JSONResponse(
            content={
                "status": "Error",
                "data": "Integration channel not supported"
            },
            status_code=422
        )