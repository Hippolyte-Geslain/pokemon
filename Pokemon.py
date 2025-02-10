class Pokemon():
    def __init__(self, name, hpMax, type, attack, defense):
        self.name = name
        self.hp_max = hpMax
        self.hp = self.hp_max
        self.type = type
        self.attack = attack
        self.defense = defense
        self.ko = False
        self.pokedex = False
        self.niveau = 1

    def take_dmg(self, amount):
        self.hp -= amount

    def heal_hp(self,amount):
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def is_ko(self):
        self.ko = True

    def is_in_pokedex(self):
        self.pokedex = True