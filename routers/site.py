from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from BASE.database import get_db
from models import Site, SiteCreate, SiteResponse

router = APIRouter(prefix="/sites", tags=["Sites"])

@router.post("/", response_model=SiteResponse)
def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    db_site = Site(name=site.name)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site