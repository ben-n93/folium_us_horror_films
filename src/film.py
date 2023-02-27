"""Film class module."""

class Film:
    """A Film object"""
    def __init__(self, title, year_released=None, setting=None):
        if "film)" in title:
            if "(film)" not in title:
                title_characters = title.split()
                year_released = title_characters[-2:]
                year_released = year_released[0]
                year_released = year_released.replace("(", "")
                year_released = year_released.replace(")", "")
                self.year_released = year_released
                title_characters = title_characters[0:-2]
                title = " ".join(title_characters)
                self.title = title
            else:
                title_characters = title.split()
                title_characters = title_characters[0:-1]
                title = " ".join(title_characters)
                self.title = title
        else:
            self.title = title
        self.year_released = year_released
        self.setting = {setting}

    def __eq__(self, other):
        return self.title == other.title

    def __repr__(self):
        return f"Title: {self.title} Age: {self.year_released}"
