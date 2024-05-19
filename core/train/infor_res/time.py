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
        words = ['open', "restaurant", 'time']
        words2 = ['open', "restaurant"]
        words3 = ['close', "restaurant", 'time']
        words4 = ['close', "restaurant"]
        words5 = ['time', "restaurant"]

        name_res =""
        if len(getName(str(statement))) > 0:
            for name in getName(str(statement)):
                if(getRole(name, str(statement)) == True):
                    name_res = name
        if name_res == "": return False

        statement = remove_stopwords(str(statement));
        data_set = statement
        check = search_word(words, data_set, True)
        self.cate = 0
        if(check == False):
            check = search_word(words2, data_set, True)
            self.cate = 0
        if(check == False):
            check = search_word(words3, data_set, True)
            self.cate = 1
        if(check == False):
            check = search_word(words4, data_set, True)
            self.cate = 1
        if(check == False):
            check = search_word(words5, data_set, True)
            self.cate = 2
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        name_res = ""
        confidence = 0.962

        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == True):
                    name_res = name
                    break
    
        if name_res != "":
            restaurants = get_restaurant_with_id_title(f"SELECT r.rid, r.title, r.time_open, r.time_close FROM core_restaurant AS r WHERE r.title LIKE '%{name_res}%'")
            if len(restaurants) > 0:
                time_open = str(restaurants[0]['time_open'])
                time_close = str(restaurants[0]['time_close'])
                if self.cate == 0:
                    response = f"Restaurant {restaurants[0]['title']} opens at " + time_open
                elif self.cate == 1:
                    response = f"Restaurant {restaurants[0]['title']} closes at " + time_close
                else: response = f"Restaurant {restaurants[0]['title']} closes at {time_open} and closes at {time_close}"
            else: response = f"No information found for {name_res} restaurant"
        else: response = "No restaurant name yet"
        selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement