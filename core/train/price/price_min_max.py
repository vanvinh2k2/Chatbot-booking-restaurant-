from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.search_word import search_word
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core.logic.restaurant import *
from core.logic.dish import *

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['dish', 'cost', 'expensive', 'cheap']
        words2 = ['dish', 'cost', 'low', 'high']
        words5 = ['dish', 'cost', "high"]
        words6 = ['dish', 'cost', 'expensive']
        words9 = ['dish', 'cost', "low"]
        words10 = ['dish', 'cost', "cheap"]
        
        statement = remove_stopwords(str(statement));
        data_set = statement
        check = search_word(words, data_set, True)
        self.cate = 0
        if(check == False):
            check = search_word(words2, data_set, True)
            self.cate = 0
        if(check == False):
            check = search_word(words5, data_set, True)
            self.cate = 1
        if(check == False):
            check = search_word(words6, data_set, True)
            self.cate = 1
        if(check == False):
            check = search_word(words9, data_set, True)
            self.cate = 2
        if(check == False):
            check = search_word(words10, data_set, True)
            self.cate = 2
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        name_dish = ""
        name_res = ""
        confidence = 0.95
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == False):
                    name_dish = name
                elif(getRole(name, str(input_statement)) == True):
                    name_res = name
        if name_dish == "": selected_statement = Statement("Please tell me the name of detail dish?")
        else:
            if(name_res == ""): 
                dishes = get_dish_all(f"SELECT * FROM core_dish WHERE title LIKE '%{name_dish}%'")
                if len(dishes) > 0:
                    n_dish = dishes[0]['title']
                    min_price = 0; max_price = 0
                    for dish in dishes:
                        if(dish['price'] > max_price): max_price = dish['price']
                        if(dish['price'] < min_price): min_price = dish['price']

                    if self.cate == 1: selected_statement = Statement(f"{n_dish} dish currently have the highest price of {max_price}$")
                    if self.cate == 2: selected_statement = Statement(f"{n_dish} dish currently have the lowest price of {min_price}$")
                    if self.cate == 0: selected_statement = Statement(f"The price of {n_dish} dish about {min_price}$ to {max_price}$")
                else: selected_statement = Statement(f"Sorry, There is no such dish {name_dish} on the system.")
            else: 
                restaurants = get_restaurant_with_id_title(f"SELECT rid, title FROM core_restaurant WHERE title LIKE '%{name_res}%'")
                if len(restaurants) > 0:
                    pass
                    # dishes = get_dish_all(f"SELECT d.did, d.title, d.price FROM core_dish AS d, core_restaurant AS r WHERE d.title LIKE '%{name_dish}%' AND d.restaurant_id = r.rid AND r.title LIKE '%{name_res}%'")
                #     if len(dishes>0):
                #         n_dish = dishes[0]['title']
                #         min_price = 0; max_price = 0
                #         for dish in dishes:
                #             if(dish['price'] > max_price): max_price = dish['price']
                #             if(dish['price'] < min_price): min_price = dish['price']

                #         if self.cate == 1: selected_statement = Statement(f"{n_dish} dish currently have the highest price of {max_price}$ of ABC restaurant")
                #         if self.cate == 2: selected_statement = Statement(f"{n_dish} dish currently have the lowest price of {min_price}$ of ABC restaurant")
                #         if self.cate == 0: selected_statement = Statement(f"The price of {n_dish} dish about {min_price}$ to {max_price}$ of ABC restaurant")
                #     else: selected_statement = Statement(f"Sorry, I couldn't find any dish named {name_dish}")
                # else: selected_statement = Statement(f"Sorry I couldn't find any restaurant named {name_res}")

        selected_statement.confidence = confidence
        return selected_statement