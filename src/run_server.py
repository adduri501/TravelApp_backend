import uvicorn

if __name__=="__main__":
    uvicorn.run("app.app_definition:travel_agency_api",host="127.0.0.1",port=9000,reload=True)
