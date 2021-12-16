from dataclasses import dataclass, InitVar, field
from typing import Any, Union, List

from typeguard import typechecked
from valid8 import validate
from valid8 import ValidationError
from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Name:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=5, max_len=25, custom=pattern(r'[A-Za-z0-9 \-\_]+'))

    def __str__(self):
        return self.value

@typechecked
@dataclass(frozen=True, order=True)
class Number:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,min_value=1 )

    def __int__(self):
        return self.value

    @staticmethod
    def create(num: str) -> 'Number':
       return Number(int(num))






@typechecked
@dataclass(frozen=True, order=True)
class Price:
    value: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 500

    def __post_init__(self, create_key):
        validate_dataclass(self)

    def __int__(self):
        return self.value

    @staticmethod
    def create(euro: str) -> 'Price':
        price= int(euro)
        validate('euro', price, min_value=1, max_value=Price.__max_value)
        return Price(price)




@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=100,
                 custom=pattern(r'[A-Za-z0-9\_\-\(\)\.\,\;\&\:\=\è\'\"\! ]*'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=8, max_len=25, custom=pattern(r'[A-Za-z0-9]+'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=8, max_len=25,
                 custom=pattern(r'[A-Za-z0-9]+[\.]*[A-Za-z]*@[A-Za-z]+\.[a-z]+'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Password:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=6, max_len=25)

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Football:
    field_id:Number
    field_number: Number
    price: Price
    description: Description

    def is_equal(self, other):
        return isinstance(other,
                          Football) and self.field_number.value == other.field_number.value and other.sport_type == self.sport_type

    @property
    def sport_type(self) -> str:
        return 'Football'


@typechecked
@dataclass(frozen=True, order=True)
class PhoneNumber:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,
                 custom=pattern(r'^[0-9]{8,10}$'))

    @property
    def __str__(self) :
        return self.value

@typechecked
@dataclass(frozen=True, order=True)
class City:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,
                 custom=pattern(r'^[A-Za-z]{3,30}$'))

    @property
    def __str__(self) :
        return self.value

@typechecked
@dataclass(frozen=True, order=True)
class Volleyball:
    field_id: Number
    field_number: Number
    price: Price
    description: Description

    def is_equal(self, other):
        return isinstance(other,
                          Volleyball) and self.field_number.value == other.field_number.value and other.sport_type==Volleyball.sport_type

    @property
    def sport_type(self) -> str:
        return 'Volleyball'

@typechecked
@dataclass(frozen=True, order=True)
class Basketball:
    field_id: Number
    field_number: Number
    price: Price
    description: Description

    def is_equal(self, other):
        return isinstance(other,
                          Basketball) and self.field_number.value== other.field_number.value and other.sport_type==Basketball.sport_type


    @property
    def sport_type(self) -> str:
        return 'Basketball'


@typechecked
@dataclass(frozen=True)
class SportCenter:
    id:Number
    name:Name
    city : City
    phone_number :PhoneNumber
    __items: List[Union[Football, Volleyball,Basketball]] = field(default_factory=list, init=False)

    def items(self) -> int:
        return len(self.__items)

    def get_items(self) -> List[Union[Football, Volleyball,Basketball]]:
        return self.__items

    def item(self, index: int) -> Union[Football, Volleyball,Basketball]:
        validate('index', index, min_value=0)
        return self.__items[index]

    def clear(self) -> None:
        self.__items.clear()

    def add_football_campo(self, football: Football) -> None:
        validate('items', self.items())
        if self.there_are_duplicates(football):
            raise ValueError
        self.__items.append(football)

    def add_volleyball_campo(self, volleyball: Volleyball) -> None:
        validate('items', self.items())
        if self.there_are_duplicates(volleyball):
            raise ValueError
        self.__items.append(volleyball)
    def add_basketball_campo(self, basketball: Basketball) -> None:
        validate('items', self.items())
        if self.there_are_duplicates(basketball):
            raise ValueError
        self.__items.append(basketball)

    def there_are_duplicates(self, item) -> bool:
        for i in self.__items:
            if item.is_equal(i):
                return True
        return False

    def remove_campo(self, index: int) -> None:
        validate('index', index, min_value=1)
        for i in range (self.items()):
            get_item = self.__items[i]
            if get_item.field_id.value == index:
                del self.__items[i]
                return

    def change_price(self, index: int, price: Price):
        validate('index', index, min_value=0)
        for i in range(self.items()):
            get_item = self.__items[i]
            if get_item.field_id.value == index:
                self.remove_campo(index)
                if get_item.sport_type == "Football":
                    self.__items.insert(i,
                                        Football(get_item.field_id,get_item.field_number,  price,  get_item.description))
                elif get_item.sport_type == "Volleyball":
                        self.__items.insert(i,
                                            Volleyball(get_item.field_id,get_item.field_number, price,  get_item.description))
                elif get_item.sport_type == "Basketball":
                        self.__items.insert(i,
                                            Basketball(get_item.field_id,get_item.field_number, price, get_item.description))


    def sort_by_price(self) -> None:
        self.__items.sort(key=lambda x: x.price)
