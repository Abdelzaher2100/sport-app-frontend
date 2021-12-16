import pytest
from valid8 import ValidationError

from sport_center.domain import Name, Description, Price, \
    Username, Email, Password


def test_name_format():
    wrong_values = ['', 'Sport&s', '<script>alert()</script>', 'cs /90 30', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Name(value)

    correct_values = ['Sport Arca', 'Cus Cosenza', 'A' * 25]
    for value in correct_values:
        assert Name(value).value == value

#
# def test_manufacturer_format():
#     wrong_values = ['', 'A', 'APP%LE', '<script>alert()</script>', '8APPLE', 'Ciao /90 30', 'A' * 21]
#     for value in wrong_values:
#         with pytest.raises(ValidationError):
#             Manufacturer(value)
#
#     correct_values = ['Honor', 'Xiaomi', 'Dolce&Gabbana', 'Gigabyte-Haorus', 'A' * 20]
#     for value in correct_values:
#         assert Manufacturer(value).value == value
#
#
# def test_quantity_range():
#     wrong_quantities = [0, -5, 6]
#     for value in wrong_quantities:
#         with pytest.raises(ValidationError):
#             Quantity(value)
#
#     correct_quantities = [1, 3, 5]
#     for value in correct_quantities:
#         assert Quantity(value).value == value


def test_description_format():
    wrong_values = ['<script>alert()</script>', 'root/tree', '[:+%]{a}', 'A' * 101]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Description(value)

    correct_values = ['Campo di erba sintetico',
                      'Campo di erba naturalee', 'A' * 100]
    for value in correct_values:
        assert Description(value).value == value


def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)


def test_price_cannot_be_negative():
    with pytest.raises(ValidationError):
        Price.create("-1")




def test_username_format():
    wrong_values = ['', '_ciao_', '<script>alert()</script>', 'uno spazio', 'è accentata', '%', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Username(value)

    correct_values = ['MimoUser89', 'HassoMoha', 'francesco98', 'A' * 25]
    for value in correct_values:
        assert Username(value).value == value


def test_email_format():
    wrong_values = ['', '_ciao@gmail.com', 'erica@libero290.com', '...@gmail.com', 'x<>@asdkjasld.89it',
                    'erica.coppolillo@', 'mario@gmail', 'x@gmx.', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Email(value)

    correct_values = ['marioRossi99@gmail.com', 'mario.rossi@libero.it', 'mario1999@gmail.com', 'A' * 20 + '@' + 'a.it']
    for value in correct_values:
        assert Email(value).value == value


def test_password_format():
    wrong_values = ['', 'password@', '<script>alert()</script>', '...asjdjadljas', 'ciaoCiao!=?',
                    '19999akdoa', 'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Password(value)

    correct_values = ['marioRossi17?', 'MARIOROSSi2!', 'francescoRICCIO22#', 'A' * 10 + 'a' * 2 + '1' * 5 + '!' * 3]
    for value in correct_values:
        assert Password(value).value == value

