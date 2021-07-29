import sqlite3


class FoodDate:
    def __init__(self, food_name=None, location=None, link=None, reservation=None, cuisine=None) -> None:
        if not food_name and location:
            raise ValueError('Either food name or location must be entered.')

        self.food = Food(name=food_name)
        self.location = location
        self.location_link = link #google maps location
        self.reservation = reservation # reservation date and time
        self.people_invited = None 
        self.cuisine = cuisine
        self.visited = False

        # TODO make persistent database that can share data across users
        # TODO send reservation messages to other users
        # TODO add reservation date and time function to bot
        # TODO fix google map links
        # TODO modify FoodDate
        # TODO send payment requests to people in food date
        # TODO keep track of outstanding requests

    def visit(self):
        self.visited = True

    def isVisited(self):
        return self.visited

    def __str__(self) -> str:
        return f'{self.food.name} at {self.location}'

    def make_str(self):
        return self.__str__


class Food:
    def __init__(self, name=None, price=None) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return self.name


class Cuisine:
    def __init__(self, name, foods=None) -> None:
        self.name = name
        self.foods = foods

    def add_food(self, food: Food):
        if self.foods is None:
            self.foods = [food]
        else:
            self.foods.append(food)

    def remove_food(self, food: Food):
        self.foods = [i for i in self.foods if i is not food]

    def __str__(self) -> str:
        return self.name


class DAO:
    con = sqlite3.connect('datastore.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS FoodDate
               (food, location, location_link, reservation, people_invited, cuisine)''')

    @classmethod
    def insert(cls, table, *values):
        try:
            VALUES = ""
            for index, i in enumerate(list(map(str, values))):
                VALUES += f"'{i}'"
                if index < len(values)-1:
                    VALUES += ','

            QUERY = f"INSERT INTO {table} Values({VALUES})"
            cls.raw_query(QUERY)
        except Exception as E:
            return E

    @classmethod
    def select(cls, table, columns=None, condition=None):
        try:
            columns = columns or '*'
            QUERY = f"SELECT {columns} FROM {table}"
            if condition:
                QUERY += f" WHERE {condition}"
            print(QUERY)
            result = cls.cur.execute(QUERY)
            return [row for row in result]
        except Exception as E:
            return E

    @classmethod
    def raw_query(cls, QUERY: str):
        cls.cur.execute(QUERY)
        cls.con.commit()
