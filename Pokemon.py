class Pokemon():
    def __init__(self, id, nom, types, base, description, image):
        self.id = id
        self.nom = nom
        self.types = types
        self.base = base
        self.description = description
        self.image = image
        self.ko = False
        self.pokedex = False
        self.hp_max = base['HP']
        self.hp = self.hp_max
        self.lvl = 1
    
    def __str__(self):
        return self.nom

    def take_dmg(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.is_ko()

    def heal_hp(self, amount):
        if self.ko:
            return
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def is_ko(self):
        self.ko = True

    def is_in_pokedex(self):
        self.pokedex = True