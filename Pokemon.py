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
        
        # Initialize HP attributes
        self.hp_max = base['HP']
        self.hp = self.hp_max

    def take_dmg(self, amount):
        """Take damage and check if Pokemon is KO"""
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.is_ko()

    def heal_hp(self, amount):
        """Heal Pokemon's HP"""
        if self.ko:
            return
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def is_ko(self):
        """Set Pokemon's status to KO"""
        self.ko = True

    def is_in_pokedex(self):
        """Mark Pokemon as registered in Pokedex"""
        self.pokedex = True