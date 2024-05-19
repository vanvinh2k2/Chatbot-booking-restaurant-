from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.search_word import search_word
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core .logic.restaurant import get_restaurant_with_id_title

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['phone', "restaurant"]
        words2 = ['contact', "restaurant"]
        statement = remove_stopwords(str(statement));
        data_set = statement
        check = search_word(words, data_set, True)
        if check == False: 
            check = search_word(words2, data_set, True)
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        name_res = ""
        confidence = 0.9
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == True):
                    name_res = name
                    break
        
        if name_res == "": selected_statement = Statement("Restaurant name?")
        else:
            restaurants = get_restaurant_with_id_title(f"SELECT r.phone FROM core_restaurant AS r WHERE r.title LIKE '%{name_res}%'")
            if len(restaurants) > 0: 
                response = "You can contact via phone " + restaurants[0]['phone']
            else: response = f"There are no {name_res} restaurants"
            selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement