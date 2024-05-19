from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core.logic.search_word import search_word
from core.logic.restaurant import get_restaurant_with_id_title

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ["famous", 'restaurant']
        words2 = ["like", 'restaurant', 'high']
        words3 = ["like", 'restaurant', 'low']
        words4 = ['system', 'restaurant']
        
        name_res =""
        if len(getName(str(statement))) > 0:
            for name in getName(str(statement)):
                if(getRole(name, str(statement)) == True):
                    name_res = name
        if name_res != "": return False

        self.cate = 0
        statement = remove_stopwords(str(statement));
        data_set = statement
        check = search_word(words, data_set, True)
        if(check == False):
            self.cate = 1
            check = search_word(words2, data_set, True)
        if(check == False):
            self.cate = 2
            check = search_word(words3, data_set, True)
        if(check == False):
            self.cate = 3
            check = search_word(words4, data_set, True)
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        confidence = 0.9
        if self.cate == 0: 
            selected_statement = Statement("Restaurant famous")
        elif self.cate == 1: 
            restaurants = get_restaurant_with_id_title(
                f"SELECT rid, title FROM core_restaurant WHERE like = (SELECT MAX(like) FROM core_restaurant)"
            )
            if(len(restaurants) > 0):
                res_name = restaurants[0]['title'] 
                response = f"It's {res_name} restaurant" ;
            else: response = "Currently not available"
            selected_statement = Statement(response)
        elif self.cate == 2: 
            restaurants = get_restaurant_with_id_title(
                f"SELECT rid, title FROM core_restaurant WHERE like = (SELECT MIN(like) FROM core_restaurant)"
            )
            if(len(restaurants) > 0):
                res_name = restaurants[0]['title'] 
                response = f"It's {res_name} restaurant" ;
            else: response = "Currently not available"
            selected_statement = Statement(response)
        elif self.cate == 3: 
            restaurants = get_restaurant_with_id_title(
                f"SELECT rid, title FROM core_restaurant"
            )
            if(len(restaurants) > 0):
                count = 0
                response = "List restaurant of system: "
                for res in restaurants:
                    if count != 0: response += ", "
                    response += res['title']
                    count += 1 
            else: response = "Currently not available"
            selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement