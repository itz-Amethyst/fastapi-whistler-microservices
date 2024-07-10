from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import Cookie, FastAPI, Request, Response


cookies = dict()
app = FastAPI()

@app.post("set_cookie/")
def create_cookie(rep:Response,id :UUID, username: str ):
    rep.set_cookie(key="Username", value=username)
    rep.set_cookie(key="Identifier", value=id)

# managing cookies
@app.get("get_cookie/")
def get_cookie(userkey: Optional[str] = Cookie(None), identifier: Optional[str] = Cookie(None)):
    cookies['userkey'] = userkey
    cookies['identifier'] = identifier
    return cookies

@app.middleware("http")
async def log_transaction_filter(request: Request, call_next):
    start_time = datetime.now()
    query_params = request.query_params
    path_params = request.path_params
    method = request.method
    
    with open("request_log.txt", mode="a") as  req_file:
        content = f"method: {method}, query_params: {query_params}, path_params : {path_params}, recived: {datetime.now()}"
        req_file.write(content)
        
    response = call_next(request)
    process_time = datetime.now() - start_time
    request.headers["X-TIME-PROCESS"] = str(process_time)
    return response