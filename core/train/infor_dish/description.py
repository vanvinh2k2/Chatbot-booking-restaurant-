from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.search_word import search_word
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core .logic.dish import get_dish_all

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['dish', 'information', "restaurant"]
        words2 = ['dish', 'introduce', "restaurant"]
        words3 = ['dish', 'describe', "restaurant"]

        name_dish =""
        if len(getName(str(statement))) > 0:
            for name in getName(str(statement)):
                if(getRole(name, str(statement)) == False):
                    name_dish = name
        if name_dish == "": return False
        
        statement = remove_stopwords(str(statement));
        print(statement)
        data_set = statement
        check = search_word(words, data_set, True)
        if(check == False):
            check = search_word(words2, data_set, True)
        if(check == False):
            check = search_word(words3, data_set, True)
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        confidence = 0.965
        name_dish = ""
        name_res = ""
        
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == False):
                    name_dish = name
                elif (getRole(name, str(input_statement)) == True):
                    name_res = name

        if(name_res != ""):
            dishes = get_dish_all(f"SELECT d.did, d.title, d.description FROM core_dish AS d, core_restaurant AS r WHERE d.restaurant_id=r.rid AND r.title LIKE '%{name_res}%' AND d.title LIKE '%{name_dish}%'")
            if len(dishes) > 0:
                response = f"Information for restaurant {name_res}'s dish {name_dish}: " + dishes[0]['description']
            else: response = f"There is no information for restaurant {name_res}'s dish {name_dish}"
        else:
            dishes = get_dish_all(f"SELECT d.did, d.title, d.description FROM core_dish AS d WHERE d.title LIKE '%{name_dish}%'")
            if len(dishes) > 0:
                    response = f"Information for {name_dish} dish: " + dishes[0]['description']
            else: response = "There is currently no information for this item"
        selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement