from city.city import City
import random
from city.person import Person
from city.family import Family

class CityList(City):

    def __init__(self, name: str, count: int):
        super(CityList, self).__init__(name, count)
        self.__person_list = []
        self.__family_list = []


    def add_person(self, p: Person) -> None:
        if super(CityList, self).add_person():
            self.__person_list.append(p)


    def add_person(self, *args: list) -> None:
        p = random.randint(1,100)
        s = str(p)
        if super().add_person():
            self.__person_list.append(Person(s,s+s, s+s+s))

    def remove_person(self, i: int) -> None:
        if super(CityList,self).remove_person():
            i = i % len(self.__person_list)
            del self.__person_list[i]
            
    def add_family(self, family: Family) -> None:
        if super(CityList, self).add_family():
            self.__family_list.append(family)
            
            family_members = family.get_all_members()
            for member in family_members:
                if super(CityList, self).add_person():
                    self.__person_list.append(member)
            
            print(f"Family {family._surname} with {len(family_members)} members added to {self._name}")
            
    def remove_family(self, i: int) -> None:
        if i < len(self.__family_list) and super(CityList, self).remove_family():
            removed_family = self.__family_list[i]
            family_members = removed_family.get_all_members()
            
            for member in family_members:
                if member in self.__person_list:
                    self.__person_list.remove(member)
                    super(CityList, self).remove_person()
            
            del self.__family_list[i]
            print(f"Family {removed_family._surname} removed from {self._name}")

    def remove_family(self, i: int) -> None:
        if i < len(self.__family_list) and super(CityList, self).remove_family():
            removed_family = self.__family_list[i]
            family_members = removed_family.get_all_members()
            
            for member in family_members:
                if member in self.__person_list:
                    self.__person_list.remove(member)
                    super(CityList, self).remove_person()
            
            del self.__family_list[i]
            print(f"Family {removed_family._surname} removed from {self._name}")
            
    def get_families(self):
        return self.__family_list
    def get_persons(self):
        return self.__person_list

    def __str__(self) -> str:
        s1 = super(CityList, self).__str__()
        s = []
        s.append(s1)
        s.append("List of families\n")
        for (i, family) in enumerate(self.__family_list):
            s.append(f" - Family {i}: {family._surname}\n")
            s.append(f"   Members: {len(family.get_all_members())}\n")
        s.append("List of residents \n")

        for (i,v) in enumerate(self.__person_list):
            s.append(" - {} - {} \n".format(i,str(v)))

        return ''.join(s)

    def __del__(self) -> None:
        print("The city {} was deleted from agglomeration".format(self._name))
