import json

class Config:
    _config = None

    @classmethod
    def load(cls, config_path):
        if cls._config is None:
            with open(config_path, 'r') as f:
                cls._config = json.load(f)

    @classmethod
    def get(cls, key):
        if cls._config is None:
            raise ValueError("Configuration not loaded")
        return cls._config.get(key)

# Charger la configuration au démarrage de l'application
Config.load('../repo1/config.json')

# Accéder à la configuration n'importe où dans ton code
valeur = Config.get('clé')
print(valeur)
