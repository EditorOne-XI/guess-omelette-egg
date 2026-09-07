from abc import ABC, abstractmethod
from math import inf
from random import randint
from time import time_ns

EGG_NAMES = (
    "Balut",
    "Basted egg",
    "Boiled egg",
    "Buttered egg",
    "Century egg",
    "Chinese steamed egg",
    "Chipsi mayai",
    "Çılbır",
    "Coddled egg",
    "Creamed egg on toast",
    "Deep fried egg",
    "Deviled egg",
    "Egg bhurji",
    "Egg butter",
    "Egg curry",
    "Egg sandwich",
    "Egg sausage",
    "Egg tart",
    "Eggah",
    "Eyerlekh",
    "Floating island",
    "French toast",
    "Fried egg",
    "Frozen custard",
    "Gyeranppang",
    "Iron egg",
    "Kai look koei",
    "Nargesi",
    "Omelette",
    "Onsen tamago",
    "Pasteis de nata",
    "Pickled egg",
    "Poached egg",
    "Scotch egg",
    "Scrambled egg",
    "Shirred egg",
    "Silog",
    "Smoked egg",
    "Soufflé",
    "Telur pindang",
    "Tokneneng"
)

EGG_SCORE = 5
OMELETTE_EGG_SCORE = inf

OMELETTE_RETURN_MAX = 100
OMELETTE_RETURN_SCALE = 50

# 4 Pillars of OOP
class Score(ABC):
    def __init__(self):
        self._score: int | float = 0
    @abstractmethod
    def get_score(self) -> int | float:
        pass
    @abstractmethod
    def add_score(self, score: int | float) -> None:
        pass
    @abstractmethod
    def deduct_score(self, score: int | float) -> None:
        pass
    @abstractmethod
    def punishment(self) -> int:
        pass
    @abstractmethod
    def reset_score(self, score: int = 0) -> bool:
        pass

class Egg(Score):
    def __init__(self, egg_name: str, sauce: str = "Vanilla"):
        super().__init__()
        self.name = egg_name
        self._sauce = egg_name + '_' + sauce
        len_sauce = len(self._sauce)
        self.score_amp = len_sauce if len_sauce < 8 else randint(1, 7)
        del len_sauce
    def __eq__(self, other_egg: object) -> bool:
        if isinstance(other_egg, Egg):
            return other_egg.name == self.name or other_egg._sauce == self._sauce
        return False
    def get_score(self):
        print(f"{self.name}'s Score: {self._score}")
        return self._score
    def add_score(self, score: int | float) -> None:
        self._score += score if score > 0 else 1
        self.score_amp += self._score
    def deduct_score(self, score: int | float) -> None:
        if self._score < 1:
            return
        self._score -= score if score > 0 else 1
    def punishment(self):
        pass
    def reset_score(self):
        pass

class OmeletteEgg(Score):
    def __init__(self):
        super().__init__()
        self.__omelette_return = 0
        self.__saved_score: int | float = 0
    def get_score(self):
        if self.__omelette_return >= OMELETTE_RETURN_MAX:
            # figlet -f "ANSI Shadow" "You Win!"
            print("""
██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗   ██╗██╗
╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗  ██║██║
 ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗ ██║██║
  ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚██╗██║╚═╝
   ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚████║██╗
   ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝
                 Omelette? Eggs! Master.
""")
            return OMELETTE_EGG_SCORE
        else:
            print(f"Omelette Return: {self.__omelette_return}")
            return self._score
    def add_score(self, score):
        if self.__saved_score != score:
            self._score += 1 if score >= OMELETTE_RETURN_SCALE else 0
            if self.__saved_score > 200 and self.__saved_score > score:
                self.__omelette_return //= 2
            else:
                self.__saved_score = score
                self.__omelette_return += self._score * 2
            print('Added score to Omelette Return.')
    def deduct_score(self):
        pass
    def punishment(self):
        pass
    def reset_score(self):
        pass

class Player(Score):
    def __init__(self, playername: str):
        super().__init__()
        self.name = playername if playername else f"player{time_ns()}"
        self.__eggs: list[Egg] = []
        self.__omelette_egg = OmeletteEgg()
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Player):
            return self.name == other.name
        return False
    def get_score(self, is_eval: bool = False) -> int | float:
        print(f"Total Score: {self._score}")
        if self._score >= EGG_SCORE * 5:
            # +1 score is determined if score >= OMELETTE_RETURN_SCALE
            if is_eval:
                self.__omelette_egg.add_score(self._score)
            print("You are amazing " + self.name + '!')
        else:
            print("You’re the architect of your own misfortune.")
        return self._score
    def add_score(self, score, amplifier: int = 1):
        self._score += score * amplifier if score > 0 else amplifier
    def deduct_score(self, score):
        self._score -= score if score > 0 else 1
    def punishment(self):
        if self._score >= 50:
            deduction = self._score
        else:
            deduction = 15
        self._score -= deduction
        return deduction
    def reset_score(self, score = 0):
        if self._score > 1 and score > 1:
            self._score = score
            return True
        else: return False
    # Player's methods
    def add_egg(self, egg: Egg):
        self.__eggs.append(egg)
    def clear_eggs(self):
        self.__eggs.clear()
    def get_eggs(self, is_list: bool = False) -> list[Egg]:
        if not is_list:
            print(f"\n{self.name}'s Egg Dishes:")
            for egg in self.__eggs:
                print(f"{self.__eggs.index(egg) + 1}. {egg.name}")
            print('')
        return self.__eggs   
    def has_egg(self, other_egg: Egg) -> bool | Egg:
        for egg in self.__eggs:
            if egg == other_egg:
                return egg
        return False
    def omelette_egg(self):
        return self.__omelette_egg
