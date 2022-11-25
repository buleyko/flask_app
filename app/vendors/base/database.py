
from sqlalchemy.ext.horizontal_shard import ShardedSession
from flask_sqlalchemy.session import Session
from flask_sqlalchemy.model import Model
import sqlalchemy as sa
import sqlalchemy.orm


__all__ = ('AppModel', 'AppSession',)



class AppModel(Model):
	pass
	''' Add Id to all tables by default '''
	# @sa.orm.declared_attr
	# def id(cls):
	# 	return sa.Column(sa.Integer, primary_key=True)


class AppSession(Session): # ShardedSession
	pass





# ------------------------------------------------------

# from flask import Flask, request
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.future import select
# from sqlalchemy.orm import declarative_base, sessionmaker

# engine = create_async_engine('sqlite+aiosqlite:///./db.db')
# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )

# Base = declarative_base()


# class A(Base):
#     __tablename__ = 'a'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)


# app = Flask(__name__)


# @app.get('/person/<name>')
# async def person_get(name):
#     async with async_session() as session:
#         query = await session.execute(select(A).where(A.name == name))
#         result = query.scalar()

#     return {"name": result.name, "id": result.id}


# @app.post('/person/')
# async def person_post():
#     req = request.get_json()

#     async with async_session() as session:
#         session.add(A(name=req['name']))
#         await session.commit()

#     return 'created', 201


# app.run()

# ----------------------------------------------------------

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('sqlite:////tmp/test.db')
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     import yourapplication.models
#     Base.metadata.create_all(bind=engine)