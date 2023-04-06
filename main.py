from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import engine ,SessionLocal, Customer,SQLALCHEMY_DATABASE_URL
from dotenv import load_dotenv
from ariadne import MutationType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from tortoise import Tortoise, fields
from tortoise.contrib.fastapi import register_tortoise
import config
import router
import jwt_auth_users
import crud

config.Base.metadata.create_all(bind=engine)

app = FastAPI()

load_dotenv()

app.include_router(router.router,tags=["customer crud"])
app.include_router(jwt_auth_users.app, tags=["login"])

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

type_defs = gql("""
    type Customer {
        cus_id: Int! 
        cus_corporatename: String! 
        cus_commercialname: String!
        cus_entity: Int!
        cca_cus_fk: Int! 
        cus_alias: String! 
        cus_unknown: Boolean! 
        cus_country: String!
        cus_taxid: String! 
        cus_taxidtype: Int! 
        cur_cus_fk: Int! 
        pan_cus_fk: Int!
        tas_cus_fk: Int!
    },
    
    type Query {
        hello: String!, 
        allcustomers: [Customer!]!
        customers(cus_id: [Int!]!): [Customer!]!
    }
    
    type Mutation {
        create_customer(cus_id: Int!, cus_corporatename: String!, cus_commercialname: String!, cus_entity: Int!, cca_cus_fk: Int!, cus_alias: String!, cus_unknown: Boolean!, cus_country: String!, cus_taxid: String!, cus_taxidtype:Int!,cur_cus_fk:Int!, pam_cus_fk: Int!): CreateCustomerResponse!
    }
    
    type CreateCustomerResponse {
        success: Boolean
        customer: Customer
    }

    type UpdateCustomerResponse {
        success: Boolean!
        customer: Customer!
    }
    
""")


mutation = MutationType()
query = QueryType()


@query.field("hello")
def resolve_hello(_,info):
    return "Hello world"

@query.field("allcustomers")
def resolve_customers(_,info):
    session = SessionLocal()
    customers = session.query(config.Customer).all()
    session.close()
    return [dict(customer.__dict__) for customer in customers]


@query.field("customers")
def resolve_customer(_,info,cus_id):
    session = SessionLocal()
    customers = crud.get_customers(session,0,100)
    session.close()
    print(customers)
    return [customer for customer in customers if customer["cus_id"] in cus_id]

@mutation.field("create_customer")
def create_customer_resolver(_, info,cus_id:int,cus_corporatename:str,cus_commercialname:str, cus_entity:int, cca_cus_fk:int,cus_alias:str,cus_unknown:bool,cus_country:str,cus_taxid:str,cus_taxidtype:int,cur_cus_fk:int, pam_cus_fk: int, tas_cus_fk:int):
    session = SessionLocal()
    new_customer = Customer(cus_id=cus_id,cus_corporatename=cus_corporatename,cus_commercialname=cus_commercialname,cus_entity=cus_entity,cca_cus_fk=cca_cus_fk,cus_alias=cus_alias,cus_unknown=cus_unknown,cus_country=cus_country,cus_taxid=cus_taxid, cus_taxidtype=cus_taxidtype, cur_cus_fk=cur_cus_fk, pam_cus_fk=pam_cus_fk, tas_cus_fk=tas_cus_fk)
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    response = {"success": True, "customer": new_customer}
    session.close()
    return response



schema = make_executable_schema(type_defs, query, mutation)
app.mount("/GraphQL",GraphQL(schema,debug=True))