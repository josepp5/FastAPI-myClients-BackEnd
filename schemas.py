from typing import List, Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from config import CustomerSchema

T = TypeVar('T')

class CustomerSchema(BaseModel):
    cus_id:Optional[int]=None
    cus_corporatename:Optional[str]=None
    cus_comercialname:Optional[str]=None
    cus_unknown:Optional[bool]=None
    cus_alias:Optional[str]=None
    cus_country:Optional[str]=None
    cus_taxID:Optional[str]=None
    cus_entity:Optional[int]=None
    cus_taxIDType:Optional[str]=None
    
    
    class Config:
        orm_mode = True
       


class RequestCustomer(BaseModel):
    parameter: CustomerSchema = Field(...)
    
    
class Response (GenericModel,Generic[T]):
    code:str
    status:str
    message:str
    result:Optional[T]
        
        
