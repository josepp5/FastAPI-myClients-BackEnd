from typing import Any, Dict, List, Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy import INTEGER, Column, MetaData, table
from fastapi.encoders import jsonable_encoder
from config import Customer

T = TypeVar('T')


class CustomerSchema(BaseModel):
    cus_id:Optional[int]=None
    cus_corporatename:Optional[str]=None
    cus_commercialname:Optional[str]=None
    cca_cus_fk:Optional[int]=None
    cus_entity:Optional[int]=None
    cus_alias:Optional[str]=None
    cus_unknown:Optional[bool]=None
    cus_country:Optional[str]="ES"
    cus_taxid:Optional[str]=None
    cus_taxidtype:Optional[str]=1
    cur_cus_fk: Optional[int]=1
    tas_cus_fk: Optional[int]=1
    pam_cus_fk: Optional[int]=3
    
    class Config:
        orm_mode = True

class CountrySchema(BaseModel):
    cou_id:Optional[str]=None
    cou_iso3:Optional[str]=None
    cou_countryname:Optional[str]=None
    cou_isocode:Optional[int]=None
    cou_flag:Optional[str]=None



class RequestCustomer(BaseModel):
    parameter: CustomerSchema = Field(...)
    
    
class Response (GenericModel,Generic[T]):
    code:str
    status:str
    message:str
    result:Optional[T]
        