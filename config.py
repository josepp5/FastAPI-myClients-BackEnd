from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

SQLALCHEMY_DATABASE_URL = "postgresql://root:root@localhost:5432/i.DEMO_GESTION_INTEGRAQS_S_L_.2023.0"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
#Base = declarative_base()

# Crear un objeto de metadatos
#metadata = MetaData()

# Obtener la tabla de la base de datos
#customerTable = sqlalchemy.Table('CUSTOMER_CUS', metadata, autoload=True, autoload_with=engine)

# Obtener el esquema de la tabla
#CustomerSchema = repr(customerTable)

# Crear la base automap
Base = automap_base()

# Reflejar las tablas existentes
Base.prepare(engine, reflect=True)

# Acceder a la tabla que quieres convertir en modelo
Customer = Base.classes.CUSTOMER_CUS

# Ahora puedes utilizar el modelo "customers" para interactuar con la tabla
