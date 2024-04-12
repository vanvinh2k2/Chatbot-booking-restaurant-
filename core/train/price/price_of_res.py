from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core.logic.search_word import search_word
from core.logic.restaurant import *
from core.logic.dish import *

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['dish', 'cost', "much", 'restaurant']
        words2 = ['dish', 'cost', "find", 'restaurant']
        words3 = ['dish', 'cost', "know", 'restaurant']
        words4 = ['dish', 'cost', 'restaurant']
        statement = remove_stopwords(str(statement));
        data_set = statement
        check = search_word(words, data_set, True)
        if(check == False):
            check = search_word(words2, data_set, True)
        if(check == False):
            check = search_word(words3, data_set, True)
        if(check == False):
            check = search_word(words4, data_set, True)
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        name_dish = ""
        name_res = ""
        response = ""
        confidence = 0.94
        
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == False):
                    name_dish = name
                elif (getRole(name, str(input_statement)) == True):
                    name_res = name

        if name_res == "": selected_statement = Statement("Please tell me the name of that restaurant or dish?")
        elif name_res != "" and name_dish == "" : 
            restaurants = get_restaurant_with_id_title(f"SELECT rid, title FROM core_restaurant WHERE title LIKE '%{name_res}%'")
            if len(restaurants) > 0:
                res_name = restaurants[0]['title']
                res_id = restaurants[0]['rid'];
                dishes = get_dish_all(f"SELECT * FROM core_dish WHERE restaurant_id='{res_id}'")
                response = f"The list of menus of {res_name} restaurant is: "
                count = 0
                for dish in dishes:
                    if count != 0: response += ", "
                    response += dish['title']
                    count += 1

            else: response = f"Sorry, There is no such restaurant {name_res} on the system."
            dishes = get_dish_all(f"SELECT * from core_dish ")
            selected_statement = Statement(response)
        else: 
            restaurants = get_restaurant_with_id_title(f"SELECT rid, title FROM core_restaurant WHERE title LIKE '%{name_res}%'")
            if len(restaurants) > 0:
                res_id = restaurants[0]['rid']
                res_name = restaurants[0]['title']
                dishes = get_dish_all(f"SELECT * FROM core_dish WHERE restaurant_id='{res_id}'")
                kt = False
                for dish in dishes:
                    if name_dish.lower() in dish['title'].lower():
                        d_name = dish['title']
                        d_price = dish['price']
                        response = f"Currently, the price of dish {d_name} at restaurant {res_name} is: {d_price}$"
                        kt = True
                        break
                if kt == False: response = f"Restaurant {res_name} currently does not have dish {name_dish}"
            else: response = f"Sorry, There is no such restaurant {name_res} on the system."
            selected_statement = Statement(response)

        selected_statement.confidence = confidence
        return selected_statement