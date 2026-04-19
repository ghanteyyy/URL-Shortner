import re
import secrets
import datetime
from urllib.parse import urlparse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth.jwt import get_current_user
from auth.models import User
from db.session import get_db
from .models import ShortUrl
from .schemas import ShortenUrlCreate, ShortenUrlOut

URL_REGEX = re.compile(r"^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/[^\s]*)?$", re.IGNORECASE)

router = APIRouter()

@router.get('/shorten/url', response_model=list[ShortenUrlOut])
def shorten_url(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    short_urls = db.query(ShortUrl).filter(ShortUrl.user_id == current_user.id)

    return short_urls


@router.post('/shorten/url', response_model=ShortenUrlOut)
def shorten_url(url: ShortenUrlCreate = Depends(ShortenUrlCreate.as_form), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    original_url = url.original_url

    if not URL_REGEX.match(original_url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    code = secrets.token_urlsafe(6)[:8]
    expiry_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)

    short_url = ShortUrl(
        code=code,
        original_url=str(original_url),
        expires_at=expiry_time,
        user_id=current_user.id
    )

    db.add(short_url)
    db.commit()
    db.refresh(short_url)

    return short_url


@router.get("/redirect/{code}")
def redirect(code:str, db: Session = Depends(get_db)):
    short_url = db.query(ShortUrl).filter(ShortUrl.code==code).first()

    original_url = short_url.original_url

    if not urlparse(original_url).scheme:
        original_url = "https://" + original_url

    return RedirectResponse(url=original_url)
