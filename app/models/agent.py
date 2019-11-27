# coding=utf8
from app.models.base import *


class Agent(Base):
    __tablename__ = 'agt_agents'
    grade_code = db.Column(db.String(50), nullable=False)
    province_code = db.Column(db.String(50), nullable=False)
    city_code = db.Column(db.String(50), nullable=False)
    agent_title = db.Column(db.String(200), nullable=False)

    def toJson(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
