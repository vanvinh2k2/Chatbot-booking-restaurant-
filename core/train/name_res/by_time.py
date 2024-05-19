from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core.logic.search_word import search_word
from core.logic.get_time import extract_opening_hours
from core.logic.restaurant import get_restaurant_with_id_title

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ["open", 'restaurant', 'start', 'end']
        words2 = ['restaurant', 'operation']
        words4 = ["open", 'restaurant']
        words5 = ["close", 'restaurant']
        
        name_res =""
        if len(getName(str(statement))) > 0:
            for name in getName(str(statement)):
                if(getRole(name, str(statement)) == True):
                    name_res = name
        if name_res != "": return False

        opening_time, closing_time = extract_opening_hours(str(statement))
        if opening_time == None and closing_time == None: return False

        self.cate = 0
        statement = remove_stopwords(str(statement))
        data_set = statement
        check = search_word(words, data_set, True)
        if(check == False):
            self.cate = 0
            check = search_word(words2, data_set, True)
        if(check == False):
            self.cate = 0
            check = search_word(words4, data_set, True)
        if(check == False):
            self.cate = 1
            check = search_word(words5, data_set, True)
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        confidence = 0.9
        opening_time, closing_time = extract_opening_hours(str(input_statement))
        print(opening_time, closing_time)
        
        if opening_time != None and closing_time != None:
            restaurants = get_restaurant_with_id_title(
                f"SELECT rid, title FROM core_restaurant WHERE time_open LIKE '%{opening_time}%' AND time_close LIKE '%{closing_time}%'"
                )
            if(len(restaurants) > 1): 
                response = f"Restaurants open from {opening_time} to {closing_time} include: " ;
                count = 0
                for res in restaurants:
                    if count != 0: response += ", "
                    response += res['title']
                    count += 1 
                    
            elif(len(restaurants) == 1):
                response = restaurants[0]['title'] + " restaurant"
            else: response = "Currently not found"
            selected_statement = Statement(response)
        elif opening_time != None: 
            restaurants = get_restaurant_with_id_title(
                f"SELECT rid, title FROM core_restaurant WHERE time_open LIKE '%{opening_time}%'"
            )
            if(len(restaurants) > 1): 
                response = f"List restaurants open {opening_time}: " ;
                count = 0
                for res in restaurants:
                    if count != 0: response += ", "
                    response += res['title']
                    count += 1 

            elif(len(restaurants) == 1):
                response = restaurants[0]['title'] + " restaurant"
            else: response = "Currently not found"
            selected_statement = Statement(response)
        elif closing_time != None: 
            restaurants = get_restaurant_with_id_title(
                f"SELECT rid, title FROM core_restaurant WHERE time_close LIKE '%{closing_time}%'"
            )
            if(len(restaurants) > 1): 
                response = f"List restaurants close {closing_time} include: " ;
                count = 0
                for res in restaurants:
                    if count != 0: response += ", "
                    response += res['title']
                    count += 1 

            elif(len(restaurants) == 1):
                response = restaurants[0]['title'] + " restaurant"
            else: response = "Currently not found"
            selected_statement = Statement(response)

        selected_statement.confidence = confidence
        return selected_statement