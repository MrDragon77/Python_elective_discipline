
from os import name
from city.person import Person

class Grandfather(Person):
    def __init__(self, _name='Ivan', _surname='Ivanov', _middle_name='Petrovich'):
        super().__init__(_name, _surname, _middle_name)
        self.fathers = []
    
    def add_father(self, father):
        self.fathers.append(father)
        print(f"Father {father._name} added to grandfather {self._name}")
    def __str__(self) -> str:
        return f"{self._name} {self._surname} {self._middle_name}"


class Father(Grandfather):
    def __init__(self, grandfather: Grandfather, _name='Ivan'):
        _surname = grandfather._surname
        
        _middle_name = grandfather._name + 'ovich'

        super().__init__(_name, _surname, _middle_name)
        self._grandfather = grandfather
        self.sons = []
    
    def add_son(self, son):
        self.sons.append(son)
        print(f"Son {son._name} added to father {self._name}")
    def __str__(self) -> str:
        return f"{self._name} {self._surname} {self._middle_name}"


class Son(Father):
    def __init__(self, father: Father, _name='Nikolai'):
        _surname = father._surname
        
        _middle_name = father._name + 'ovich'

        Person.__init__(self, _name, _surname, _middle_name)
        self.father = father
    def __str__(self) -> str:
        return f"{self._name} {self._surname} {self._middle_name}"

class Family:
    def __init__(self, surname: str):
        self._surname = surname
        self.grandfather = None
        self.fathers = []
        self.sons = []

    def set_grandfather(self, grandfather: Grandfather):
        self.grandfather = grandfather
        print(f"Grandfater {grandfather._name} added to family {self._surname}")

    def add_father(self, father: Father):
        self.fathers.append(father)
        if self.grandfather:
            self.grandfather.add_father(father)

    def add_son(self, son: Son, father: Father):
        self.sons.append(son)
        son.father = father
        father.add_son(son)
        
    def get_all_members(self):
        members = []
        if self.grandfather:
            members.append(self.grandfather)
        members.extend(self.fathers)
        members.extend(self.sons)
        return members

    def __str__(self) -> str:
        s = f"\nFamily {self._surname}:\n"
        if self.grandfather:
            s += f"  Grandfather: {self.grandfather}\n"
            for father in self.fathers:
                s += f"    Father: {father}\n"
                for son in self.sons:
                    if son.father == father:
                        s += f"      Son: {son}\n"
        return s

    def __del__(self) -> None:
        print(f"Family {self._surname} deleted")