import json


class SavingManagement:
    """This class will manage the saving sistem."""

    FILE_NAME = "save.txt"

    def __init__(self, save_data):
        """Initialize 'SavingManagement' instance."""
        self.save_data = save_data

    def save(self):
        """Save data to file."""
        try:
            with open(self.FILE_NAME, 'w') as file:
                json.dump(self.save_data.get_data(), file)
        except FileNotFoundError as e:
            print(e)

    def get_saved_data(self):
        """Return saved data from file as json."""
        try:
            with open(self.FILE_NAME) as file:
                save_data_json = json.load(file)
        except FileNotFoundError:
            return None
        return save_data_json
