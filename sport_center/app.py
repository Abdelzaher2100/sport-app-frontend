from getpass import getpass
from wsgiref import headers

import csv
import sys
from pathlib import Path
from typing import Tuple, Callable, Any
import requests

from valid8 import validate, ValidationError

from domain import SportCenter, Username, Password, Email, Football, Volleyball, Price, Description, Name, Number, \
    Basketball, PhoneNumber, City
from menu import Menu, MenuDescription, Entry

api_server = 'http://localhost:8000/api/v1/'


class App:
    __filename = Path(__file__).parent.parent / 'shoppingList.csv'
    __delimiter = '\t'
    __logged = False
    __key = None
    __id_dictionary = []

    def __init__(self):
        self.__first_menu = self.init_first_menu()
        self.id_user = None
        self.__menu = self.__init_shopping_list_menu()
        self.__campilist=None

    def init_first_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('SPORT ZONE'), auto_select=lambda: print('Welcome please select!')) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.__login())) \
            .with_entry(Entry.create('2', 'Register', on_selected=lambda: self.__register())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye Bye!'), is_exit=True)) \
            .build()

    def __init_shopping_list_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Welcome to our SPORT-CENTER App'), auto_select=lambda: self.__print_items()) \
            .with_entry(Entry.create('1', 'Add Football Field', on_selected=lambda: self.__add_football_campo())) \
            .with_entry(Entry.create('2', 'Add Volleyball Field', on_selected=lambda: self.__add_volleyball_campo())) \
            .with_entry(Entry.create('3', 'Add Basketball Field', on_selected=lambda: self.__add_volleyball_campo())) \
            .with_entry(Entry.create('4', 'Remove Field', on_selected=lambda: self.__remove_campo())) \
            .with_entry(Entry.create('5', 'Change Price', on_selected=lambda: self.__change_price())) \
            .with_entry(Entry.create('6', 'Sort by Price', on_selected=lambda: self.__sort_by_price())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye Bye!'), is_exit=True)) \
            .build()

    def __login(self) -> bool:
        done=False
        while not done:
            username = self.__read("Username ", Username)
            if username.value == '0':
                return False

            password = self.__read("Password ", Password)
            if password.value == '0':
                return False

            res = requests.post(url=f'{api_server}auth/login/', data={'username': username, 'password': password})
            if res.status_code != 200:
                print('This user does not exist!')
            else:
                self.__key = res.json()['key']
                print('Login success')
                done = True
        return True


    def __register(self) -> None:
        username = self.__read("Username", Username)
        email = self.__read("Email", Email)
        password = self.__read("Password", Password)

        res = requests.post(url=f'{api_server}auth/registration/',
                            data={'username': username, 'email': email, 'password1': password,
                                  'password2': password})
        if res.status_code == 400:
            print('This user already exists!')
        if res.status_code == 200:
            print('Registration done!')

    def __print_items(self) -> None:
        if self.__campilist.items() == 0 :
            return
        print_sep = lambda: print('-' * 180)
        print_sep()
        fmt = '%-3s %-30s  %-30s  %-30s %-50s'
        print(fmt % ( 'Id', 'Field Number', 'Sport Type', 'PRICE','DESCRIPTION'))
        print_sep()
        for index in range(self.__campilist.items()):
            item = self.__campilist.item(index)
            print(fmt % (item.field_id.value, item.field_number.value, item.sport_type, item.price.value,
                         item.description))

        print_sep()

    def __add_football_campo(self) -> None:
        football_camp = Football(*self.__read_item())
        try:
            self.__campilist.add_football_campo(football_camp)
            self.__save(football_camp)
            print('Football field added!')
        except ValueError:
            print('this field number is already present for this sport type in the sportCenter!')

    def __add_volleyball_campo(self) -> None:
        volleyball_campo = Volleyball(*self.__read_item())
        try:
            self.__campilist.add_volleyball_campo(volleyball_campo)
            self.__save(volleyball_campo)
            print('Volleyball field added!')
        except ValueError:
            print('this field is already present in the sportCenter!')
    def __read_index(self)->int:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=1)
            return int(value)

        index_found = False
        index = self.__read('Insert the id of the field or 0 to cancel operation)', builder)
        while not index_found:
            for campo in self.__campilist.get_items():
                if campo.field_id.value == int(index):
                    index_found = True

            if index == 0:
                return index
            if not index_found:
                index = self.__read('Insert a valid id of the field  or 0 to cancel operation)', builder)
        return index
    def __remove_campo(self) -> None:
        index= self.__read_index()
        if index==0:
            print('Operation cancelled!')
            return

        self.__delete(index)
        self.__campilist.remove_campo(index)
        print('campo removed!')

    def __change_price(self) -> None:
        index= self.__read_index()
        if index == 0:
            print('Operation cancelled!')
            return

        price = self.__read('New Price', Price.create)

        self.__campilist.change_price(index, price)
        self.__update(index,price)
        print('price changed!')

    def __sort_by_price(self) -> None:
        self.__campilist.sort_by_price()

    def __run(self) -> None:
        while not self.__first_menu.run() == (True, False):
            try:
                self.__fetch()
            except ValueError as e:
                print('Continuing with an empty list of fields...')
            except RuntimeError:
                print('Failed to connect to the server! Try later!')
                return
            self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print(e)
            print('Panic error!', file=sys.stderr)

    def __create_sport_center(self) -> int:
        sport_center = SportCenter(*self.__read_sport_center())

        req = requests.post(url=f'{api_server}sport-center/add',
                            headers={'Authorization': f'Token {self.__key}'},
                            data={'author':self.iduser,'name': sport_center.name.value, 'city': sport_center.city.value,
                                  'phone_number': sport_center.phone_number.value})


    def __getcenter(self) -> int:
        res = requests.get(url=f'{api_server}sport-center/',
                           headers={'Authorization': f'Token {self.__key}'})
        if res.status_code != 200:
            raise RuntimeError()
        self.id_user = 1
        json = res.json()
        if json is None:
            return None

        for item in json:
            id_center = Number(item['id'])
            name = Name(item['name'])
            city = City(item['city'])
            phone_number=PhoneNumber(item['phone_number'])

            return SportCenter(id_center,name,city,phone_number)


    def __fetch(self) -> None:
        sport_center = self.__getcenter()

        while sport_center is None:
            self.__create_sport_center()
            sport_center = self.__getcenter()

        self.__campilist=sport_center

        res = requests.get(url=f'{api_server}sport-center/show/campi/id_center={sport_center.id.value}',
                           headers={'Authorization': f'Token {self.__key}'})

        if res.status_code != 200:
            raise RuntimeError()

        json = res.json()
        # if json is None:
        #     return
        for item in json:
            field_id = Number((item['id']))
            field_number = Number((item['field_number']))
            sport_type = str(item['sport_type'])
            price = Price((item['price']))


            description = Description(str(item['description']))


            if sport_type == 'Football':
                self.__campilist.add_football_campo(Football(field_id, field_number, price, description))
            elif sport_type == 'Volleyball':
                self.__campilist.add_volleyball_campo(Volleyball(field_id, field_number, price, description))
            elif sport_type == 'Basketball':
                self.__campilist.add_basketball_campo(Basketball(field_id, field_number, price, description))

            else:
                raise ValueError('Unknown Sport Type ')

    def __save(self, item: Any) -> None:
        sport_center = self.__getcenter()
        req = requests.post(url=f'{api_server}sport-center/add/campo/',
                            headers={'Authorization': f'Token {self.__key}'},
                            data={'field_number': item.field_number.value, 'sport_type': item.sport_type,
                                  'price': item.price.value,'id_center': sport_center.id.value,
                                  'description': item.description.value})


    def __update(self, index: int,price:Price) -> None:
            requests.patch(url=f'{api_server}sport-center/edit/{index}',
                           headers={'Authorization': f'Token {self.__key}'}, data={'price': price.value})

    def __delete(self, index: int) -> None:
            requests.delete(url=f'{api_server}sport-center/edit/{index}',
                        headers={'Authorization': f'Token {self.__key}'})


    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                if prompt != 'Password':
                    line = input(f'{prompt}: ')
                else:
                    line = input(f'{prompt}: ')
                    # line = getpass(f'{prompt}: ')

                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_item(self) -> Tuple[Number, Price, Description]:
        field_id=Number(self.__campilist.items()+1);
        field_number = self.__read('field_number', Number.create)
        price = self.__read('Price', Price.create)
        description = self.__read('Description', Description)
        return field_id,field_number, price, description

    def __read_sport_center(self) -> Tuple[Number, Price, Description]:
        print('Welcome to our app, please insert your sport center\'s information')
        center_name = self.__read('Sport center\'s  name', Name)
        center_city = self.__read('Sport center\'s city', City)
        phone_number = self.__read('Phone number', PhoneNumber)
        return None,center_name,center_city,phone_number

def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
