import json
import os

class PlayerManager:
    def __init__(self, save_file='players.json'):
        self.save_file = save_file
        self.players = self.load_players()

    def load_players(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return {}

    def save_players(self):
        with open(self.save_file, 'w') as f:
            json.dump(self.players, f, indent=4)

    def create_player(self, player_name):
        if player_name in self.players:
            raise ValueError("Player already exists")
        self.players[player_name] = {
            'fought_pokemon': [1,4,7],
            'current_pokemon': None
        }
        self.save_players()

    def delete_player(self, player_name):
        if player_name in self.players:
            del self.players[player_name]
            self.save_players()

    def get_player_data(self, player_name):
        return self.players.get(player_name)

    def update_player_data(self, player_name, data):
        if player_name in self.players:
            self.players[player_name].update(data)
            self.save_players()

    def add_fought_pokemon(self, player_name, pokemon_id):
        if player_name in self.players:
            if pokemon_id not in self.players[player_name]['fought_pokemon']:
                self.players[player_name]['fought_pokemon'].append(pokemon_id)
                self.save_players()

    def add_to_pokedex(self, player_name, pokemon_id, pokemon_data):
        if player_name in self.players:
            self.players[player_name]['pokedex'][pokemon_id] = pokemon_data
            self.save_players()

    def get_all_players(self):
        return list(self.players.keys())