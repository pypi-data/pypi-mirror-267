from __future__ import annotations

import datetime
import io
import re
from typing import Optional

from ormspace import functions
from spacestar.model import SpaceModel, SpaceSearchModel
from ormspace.model import modelmap
from ormspace.annotations import DateField, PositiveDecimalField, TitleField
from ormspace.enum import Gender
from pydantic import computed_field, EmailStr, field_validator
from typing_extensions import Self

from detadoc.enum import CashFlow, PaymentMethod



class EmailBase(SpaceModel):
    email: str
    
    @classmethod
    async def get_by_email(cls, email: str) -> Optional[Self]:
        if data := await cls.instances_list(query={'email': email}):
            assert len(data) == 1
            return data[0]
        return None


@modelmap
class Person(SpaceSearchModel):
    EXIST_QUERY = ['code', 'cpf']
    fname: TitleField
    lname: TitleField
    gender: Gender
    bdate: DateField
    cpf: Optional[str] = None
    sname: Optional[str] = None
    
    @property
    def fullname(self):
        return self.sname if self.sname else ' '.join([self.fname, self.lname])
    
    @property
    def name(self):
        words = self.fullname.split()
        if len(words) >= 2:
            return f'{words[0]} {words[-1]}'
        return self.fullname

    
    def __str__(self):
        return self.fullname
    
    @property
    def age(self):
        return functions.years(datetime.date.today(), self.bdate)
    
    # noinspection PyNestedDecorators
    @field_validator('cpf')
    @classmethod
    def _cpf_validator(cls, v: str) -> str:
        if v:
            digits = ''.join(functions.find_digits(v))
            if len(digits) != 11:
                raise ValueError('CPF deve ter 11 digitos')
            return digits
        return v
    
    @computed_field
    @property
    def code(self) -> str:
        with io.StringIO() as f:
            f.write(self.bdate.isoformat().replace('-', ''))
            f.write(self.gender.name)
            f.write(self.fname[:2])
            f.write(self.lname.split()[-1][:2])
            return functions.normalize(f.getvalue().upper())
        
    async def save_new(self):
        data = self.asjson()
        if self.cpf:
            query = [{'cpf': self.cpf}, {'code': self.code}]
        else:
            query = {'code': self.code}
        exist = await self.fetch_all(query=query)
        if not exist:
            new = await self.Database.save(data)
            if new:
                return new
        return None


class ContactBase(SpaceModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    
    # noinspection PyNestedDecorators
    @field_validator('phone')
    @classmethod
    def _phone_validator(cls, v: str) -> str:
        if v:
            digits = ''.join(re.findall(r'\+|\d', v))
            return digits
        return v


class Profile(Person, ContactBase):
    MODEL_GROUPS = ['Provider', 'Employee', 'Patient']


class Staff(Profile):
    MODEL_GROUPS = ['Provider', 'Employee']
    cpf: str
    phone: str
    email: EmailStr
    address: str
    city: str


class FinancialBase(SpaceSearchModel):
    description: str
    amount: PositiveDecimalField
    created: DateField
    creator: str = 'Doctor.admin'
    method: PaymentMethod
    notes: Optional[str] = None
    date: DateField
    flow: CashFlow
    
    
    def __lt__(self, other):
        assert isinstance(other, type(self))
        if self.date == other.date:
            return self.amount < other.amount
        return self.date < other.date
        
    
    def __str__(self):
        return f' R$ {self.amount} {self.flow} {self.date} {self.description}'

