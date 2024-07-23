import base64
from datetime import datetime
import io
import random
import string
from typing import Optional
from uuid import UUID
from fastapi import Cookie, FastAPI, Request, Response
from captcha.image import ImageCaptcha
from fastapi.responses import StreamingResponse
from starlette.middleware.sessions import SessionMiddleware

cookies = dict()
app = FastAPI(docs_url='/docs')
app.add_middleware(SessionMiddleware,secret_key = "Some-secret-key")

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
def log_transaction_filter(request: Request, call_next):
    start_time = datetime.now()
    query_params = request.query_params
    path_params = request.path_params
    method = request.method
    
    with open("request_log.txt", mode="a") as  req_file:
        content = f"method: {method}, query_params: {query_params}, path_params : {path_params}, recived: {datetime.now()}"
        req_file.write(content)
        
    response = call_next(request)
    process_time = datetime.now() - start_time
    # request.headers["X-TIME-PROCESS"] = str(process_time)
    return response


def captcha_generator(size: int):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


def generate_captcha():
    captcha: str = captcha_generator(5)
    image = ImageCaptcha()
    data = image.generate(captcha)
    data = base64.b64encode(data.getvalue())
    return {"data": data, "captcha": captcha}

@app.get('/start-session')
def start_session(request: Request):
    captcha = generate_captcha()
    request.session["captcha"] = captcha['captcha']
    captcha_image = captcha["data"].decode("utf-8")
    return StreamingResponse(io.BytesIO(base64.b64decode(captcha_image)), media_type="image/png")
