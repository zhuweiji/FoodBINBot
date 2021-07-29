import sqlite3
import uuid


class DAO:
    """ Database Access Object, consolidating all Database Access logic into one single source"""
    con = sqlite3.connect('datastore.db')
    cur = con.cursor()

    @classmethod
    def insert(cls, table, *values):
        """ Insert a new row into the database, and returns an Exception instance if operation fails"""
        VALUES = ""
        for index, i in enumerate(list(map(str, values))):
            VALUES += f"'{i}'"
            if index < len(values)-1:
                VALUES += ','

        query = f"INSERT INTO {table} Values({VALUES})"
        result = cls.raw_query(query)
        return True if not isinstance(result, Exception) else result
            
    @classmethod
    def select(cls, table, columns=None, condition=None):
        """ Selects rows from a table with SQL SELECT FROM WHERE syntax 
        Args:
            table: table name in database
            columns: Column names of database to select
            condition: SQL WHERE condition (eg. food='Hokkien Mee';)
            
            returns rows which match the conditions
            """
        columns = columns or '*'
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        result = cls.raw_query(query)
        if not isinstance(result, Exception):
            return [row for row in result]
        else:
            return result

    @classmethod
    def delete_table(cls, table):
        """ Delete table in database """
        query = f"DROP TABLE {table}"
        result = cls.raw_query(query)
        print(result)
        return True if not isinstance(result, Exception) else result

    @classmethod
    def check_table_exists(cls, table):
        """ Check if the table exists in the database and return matching tables"""
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';"
        result = cls.raw_query(query) 
        if not isinstance(result, Exception):
            return result.fetchall()
        else:
            return result


    @classmethod
    def raw_query(cls, QUERY: str):
        """ Makes raw SQL query to the sqlite3 database.
            args: SQL string
            return: True if transaction is successful, otherwise returns an Exception instance"""
        try:
            result = cls.cur.execute(QUERY)
            cls.con.commit()
            return result
        except Exception as E:
            print(f'Exception {E} raised on insert operation\n Query:{QUERY}')
            return E


class FoodDate:
    db_table_name = 'FoodDate'
    fact_attributes = ['id','food','location','location_link','cuisine']

    def __init__(self, id=None,  food_name=None, location=None, link=None, reservation=None, cuisine=None) -> None:
        if not food_name and location:
            raise ValueError('Either food name or location must be entered.')

        self.id = id or str(uuid.uuid4())      # Create unique ID for a FoodDate instance
        self.food = Food(name=food_name) if food_name else None
        self.location = location
        self.location_link = link #google maps location
        self.reservation = reservation # reservation date and time
        self.people_invited = None 
        self.cuisine = cuisine
        self.visited = False

        # TODO send reservation messages to other users
        # TODO add reservation date and time function to bot
        # TODO fix google map links
        # TODO modify FoodDate
        # TODO send payment requests to people in food date
        # TODO keep track of outstanding requests

    @classmethod
    def db_initalise(cls):
        DAO.raw_query(f"CREATE TABLE IF NOT EXISTS FoodDate ({','.join(FoodDate().fact_attributes)})")

    def visit(self):
        self.visited = True

    def isVisited(self):
        return self.visited

    def __str__(self) -> str:
        return f'{self.food.name} at {self.location}'

    def make_str(self):
        return self.__str__

    def add_to_db(self):
        #  ['id','food','location','location_link','cuisine']
        id = self.id
        food = str(self.food) or ''
        location = self.location or ''
        location_link = self.location_link or ''
        cuisine = self.cuisine or ''
        
        fact_values = [id, food, location, location_link, cuisine]
        assert len(fact_values) == len(self.fact_attributes), "The number of columns in the data being inserted must be equal the number of columns of this object in the database"

        res = DAO.insert(self.db_table_name, id, food, location, location_link, cuisine)
        if isinstance(res, Exception):
            raise res

    @classmethod
    def get_all_db(cls):
        res = DAO.select(cls.db_table_name)
        if isinstance(res, Exception):
            raise res
        return res

    def get_self_fm_db(self):
        DAO.select(self.db_table_name, condition=f"id={self.id}")
    
    @classmethod
    def get_fm_db_with_id(cls, id):
        DAO.select(cls.db_table_name, condition=f"id={id}")


class Food:
    def __init__(self, name=None, price=None) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
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
        return str(self.name)


FoodDate.db_initalise()
