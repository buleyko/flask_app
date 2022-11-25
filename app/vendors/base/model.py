from datetime import datetime
from app.extensions import db
from app.extensions import logger
from sqlalchemy import exc
from sqlalchemy import (
    func, 
    desc,
)
 

class BaseModel(db.Model):
    __abstract__ = True

    # @classmethod
    # def create(clx, **values):
    #     ''' Create New Entity ''' 
    #     new = clx(values) 
    #     return new

    # @classmethod
    # def createOrUpdate(clx, kyes, values):
    #     ''' Update Entity And Crate If Not Exist ''' 
    #     pass
    #     # item = clx.query
    #     # for (key, value) in keys.items():
    #     #     item = item.filter(getattr(clx, key)==value) 
    #     # item = item.first()
    #     # if item is not None:
    #     #     item.update(values) 
    #     # else:
    #     #     parms = values.update(keys) 
    #     #     item = ctl(**parms) 
    #     #     item.set_created()
    #     #     return item

    # def update(self, **values): 
    #     ''' Update Entity '''
    #     for key, value in values.items(): 
    #         setattr(self, key, value) 
    #         return self

    def save(self):
        ''' Save Entity '''
        try:
            db.session.add(self) 
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            # add error to log
            return False

    def destroy(self):
        ''' Delete Entity '''
        try:
            db.session.delete(self) 
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            # add error to log
            return False



