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
        words = ['dish', 'cost', "much"]
        words2 = ['dish', 'cost', "find"]
        words3 = ['dish', 'cost', "know"]
        words4 = ['dish', 'cost']
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
        confidence = 0.8
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == False):
                    name_dish = name
                    break
        
        if name_dish == "": selected_statement = Statement("Please tell me the name of that dish?")
        else: 
            response = f"Depending on each restaurant, dish {name_dish} has different prices. You can also refer to the price information of dish {name_dish} at the system's restaurants as follows: "
            restaurants = get_restaurant_with_id_title("SELECT rid, title FROM core_restaurant")
            dishes = get_dish_all("SELECT * FROM core_dish")
            count = 0;
            for dish in dishes:
                for restaurant in restaurants:
                    if dish['restaurant_id'] == restaurant['rid'] and (name_dish.lower() in dish['title'].lower()):
                        if count != 0: response += ", "
                        res_name = restaurant['title']
                        dish_price = dish['price']
                        response += f"restaurant {res_name} is {dish_price}$"
                        count +=1
                if count >5: break
            if count == 0: response = f"There is currently no price information for '{name_dish}' dish in the system"
            selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement