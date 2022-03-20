import pytest
from app import *
read_data_from_file_into_dict()

def test_info():
    assert isinstance(info(), str) == True

def test_get_epochs():
    assert isinstance(get_epochs(), str) == True
    assert isinstance(get_epochs(), float) == False

def test_get_EPOCH_data():
    assert isinstance(get_EPOCH_data('hello'), str) == False

def test_get_all_countries():
    assert isinstance(get_all_countries(), str) == True

def test_get_country_info():
    assert isinstance(get_country_info('hello'), str) == True

def test_get_all_regions():
    assert isinstance(get_all_regions('hello'), dict) == True

def test_get_region_data():
    assert isinstance(get_region_data('hello', 'hola'), str) == True

def test_get_all_cities():
    assert isinstance(get_all_cities('como', 'estas'), dict) == True

def test_get_city_data():
     assert isinstance(get_city_data('hello', 'hi', 'hola'), str) == True



