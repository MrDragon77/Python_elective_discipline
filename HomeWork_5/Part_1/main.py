
import sys

from city.person import Person
from city.city import  City
from city.city_list import CityList
from city.family import Family, Son, Father, Grandfather
    
if __name__ == '__main__':

    print("Program is started \n")

    city = CityList("Moscow", 100)

    family = Family(surname="Ivanov")
    grandfather = Grandfather(_name="Sergei", _surname="Ivanov", _middle_name="Petrovich")
    father = Father(grandfather=grandfather, _name="Ivan")
    son = Son(father=father, _name="Nikolai")

    family.set_grandfather(grandfather)
    family.add_father(father)
    family.add_son(son, father)

    city.add_family(family)

    print(city)


