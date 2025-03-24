from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime


Base = declarative_base()

class SwaggerApiData(Base):
    __tablename__ = 'SwaggerApiData'

    id = Column(Integer, primary_key=True, index=True)
    api = Column(String, index=True)
    method_name = Column(String)
    platform = Column(String)
    priority = Column(Integer)
    group_name_id = Column(Integer, ForeignKey('GroupName.id'))

    input_data = relationship("InputData", back_populates="swagger_api")
    group_names = relationship("GroupName", back_populates="swagger_api")
    results = relationship("Results", back_populates="swagger_api")


class InputData(Base):
    __tablename__ = 'InputData'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    swagger_api_id = Column(Integer, ForeignKey('SwaggerApiData.id'))

    swagger_api = relationship("SwaggerApiData", back_populates="input_data")


class GroupName(Base):
    __tablename__ = 'GroupName'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)

    swagger_api = relationship("SwaggerApiData", back_populates="group_names")


class Results(Base):
    __tablename__ = 'Results'

    id = Column(Integer, primary_key=True, index=True)
    status_code = Column(Integer)
    response_data = Column(Text)
    error_message = Column(Text)
    status = Column(String)  # "Success" or "Failure"
    swagger_api_id = Column(Integer, ForeignKey('SwaggerApiData.id'))

    swagger_api = relationship("SwaggerApiData", back_populates="results")


class TestHistory(Base):
    __tablename__ = "test_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False)
    group_id = Column(Integer, nullable=False)
    api_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # 'Pass' or 'Fail'
    response_status_code = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now())
    error_message = Column(Text, nullable=True)
    response_body = Column(Text, nullable=True)
    time_taken = Column(Float, nullable=False)

    def __repr__(self):
        return f"<TestHistory(group_name={self.group_name}, api_name={self.api_name}, status={self.status})>"
