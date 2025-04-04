from datetime import datetime

import json

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.Text())
    jwt_auth_active = db.Column(db.Boolean())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"User {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_email(self, new_email):
        self.email = new_email

    def update_username(self, new_username):
        self.username = new_username

    def check_jwt_auth_active(self):
        return self.jwt_auth_active

    def set_jwt_auth_active(self, set_status):
        self.jwt_auth_active = set_status

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def toDICT(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['username'] = self.username
        cls_dict['email'] = self.email

        return cls_dict

    def toJSON(self):

        return self.to_dict()


class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jwt_token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"Expired Token: {self.jwt_token}"

    def save(self):
        db.session.add(self)
        db.session.commit()

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EducationData(db.Model):
    __tablename__ = 'education_data'

    id = db.Column(db.Integer(), primary_key=True)
    province = db.Column(db.String(255), nullable=True)
    series_name = db.Column(db.String(255), nullable=True)
    indicator_value = db.Column(db.Float(), nullable=True)
    indicator = db.Column(db.String(255), nullable=True)
    year = db.Column(db.String(4), nullable=True)
    series_code = db.Column(db.String(255), nullable=True)
    sector = db.Column(db.String(255), nullable=True)
    subsector_1 = db.Column(db.String(255), nullable=True)
    subsector_2 = db.Column(db.String(255), nullable=True)
    source = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.String(255), nullable=True)
    longitude = db.Column(db.String(255), nullable=True)
    indicator_unit = db.Column(db.String(255), nullable=True)
    tag = db.Column(db.String(255), nullable=True)
    filters = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"EducationData({self.province}, {self.series_name}, {self.indicator}, {self.year})"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_province(cls, province):
        return cls.query.filter_by(province=province).all()
    
    @classmethod
    def get_data(cls, **filters):
        query = cls.query
        
        # Apply filters for regular columns (e.g. 'province', 'sector', etc.)
        for column, value in filters.items():
            if value and column != "filters":  # Skip if the column is filters (to be handled separately)
                query = query.filter(getattr(cls, column) == value)

        # Apply filters for the 'filters' JSON column (if specified)
        if 'filters' in filters:
            for key, value in filters['filters'].items():
                query = query.filter(cls.filters[key].astext == value)  # Filter by key-value in the JSON column

        return query.all()

    def toDICT(self):
        return {
            'id': self.id,
            'province': self.province,
            'series_name': self.series_name,
            'indicator_value': self.indicator_value,
            'indicator': self.indicator,
            'year': self.year,
            'series_code': self.series_code,
            'sector': self.sector,
            'subsector_1': self.subsector_1,
            'subsector_2': self.subsector_2,
            'source': self.source,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'indicator_unit': self.indicator_unit,
            'tag': self.tag,
            'filters': self.filters
        }

    def toJSON(self):
        return self.to_dict()
