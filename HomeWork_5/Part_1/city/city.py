from city.person import Person

class City():
    __max_count = 100
    __free_city_space = 100
    __cur_count = 0
    __family_count = 0

    def __init__(self, name : str, count : int):
        val = min(count, City.__free_city_space)
        self._name = name
        self._max_count = val
        self._cur_count = 0
        self._family_count = 0
        City.__free_city_space -= val

    def add_person(self) -> bool:
        if(self._cur_count < self._max_count):
            self._cur_count += 1
            City.__cur_count += 1
            return True
        return False

    def remove_person(self) -> bool:
        if(self._cur_count > 0):
            self._cur_count -= 1
            City.__cur_count -= 1
            return True
        return False
    def add_family(self) -> bool:
        if self._cur_count < self._max_count:
            self._family_count += 1
            City.__family_count += 1
            return True
        return False

    def remove_family(self) -> bool:
        if self._family_count > 0:
            self._family_count -= 1
            City.__family_count -= 1
            return True
        return False

    def __str__(self) -> str:

        s = []
        s.append("------------------------ \n")
        s.append("City: \n")
        s.append("------------------------\n")
        s.append("\n")
        s.append("Name: {}\n".format(self._name))
        s.append("Max_person_count: {}\n".format(self._max_count))
        s.append("Cur_person_count: {}\n".format(self._cur_count))
        s.append("Cur_family_count: {}\n".format(self._family_count))
        s.append("\n")

        s.append(self.info())

        return ''.join(s)
    
    
    @classmethod
    def info(cls) -> str:
        s = []

        s.append("------------------------ \n")
        s.append("Agglomeration: \n")
        s.append("------------------------\n")
        s.append("\n")
        s.append("Max_person_count: {}\n".format(City.__max_count))
        s.append("Free_counts_for_city: {}\n".format(City.__free_city_space))
        s.append("Agglomeration resident count: {}\n".format(City.__cur_count))
        s.append("Agglomeration family count: {}\n".format(City.__family_count))
        s.append("\n")

        return ''.join(s)
    
    @staticmethod
    def global_info() -> str:
        return 'no additional information'

    