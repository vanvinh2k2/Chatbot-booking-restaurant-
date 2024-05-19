from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.search_word import search_word
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core.logic.restaurant import get_restaurant_with_id_title

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['dish', 'specialty', "restaurant"]
        words2 = ['dish', 'featured', "restaurant"]
        words3 = ['featured', "restaurant"]
        words4 = ['specialty', "restaurant"]
        words5 = ['dish', 'cost', "high", "restaurant"]
        words6 = ['dish', 'cost', 'expensive', "restaurant"]
        words9 = ['dish', 'cost', "low", "restaurant"]
        words10 = ['dish', 'cost', "cheap", "restaurant"]
        words13 = ['dish', 'restaurant']
        
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
            check = search_word(words2, data_set, True)
            self.cate = 0
        if(check == False):
            check = search_word(words3, data_set, True)
            self.cate = 0
        if(check == False):
            check = search_word(words4, data_set, True)
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
        if(check == False):
            check = search_word(words13, data_set, True)
            self.cate = 3
        if check: return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        name_dish = ""
        confidence = 0.96
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == False):
                    name_dish = name
                    break
        
        if(name_dish == ""): selected_statement = Statement("Please tell me the dishes name?")
        else: 
            if self.cate == 0:
                restaurants = get_restaurant_with_id_title(
                    f"SELECT r.rid, r.title FROM core_restaurant AS r, core_dish AS d WHERE r.rid = d.restaurant_id AND d.title LIKE '%{name_dish}%' AND d.featured = 1"
                )
                if(len(restaurants) > 1): 
                    response = f"Restaurants that have {name_dish} dishes as special dishes: " ;
                    count = 0
                    for res in restaurants:
                        if count != 0: response += ", "
                        response += res['title']
                        count += 1 
                elif len(restaurants) == 1:
                    response = "Currently there is only restaurant " + restaurants[0]['title']
                else: response = "No have"
                selected_statement = Statement(response)
            elif self.cate == 1: 
                restaurants = get_restaurant_with_id_title(
                    f"SELECT r.rid, r.title FROM core_restaurant AS r, core_dish AS d WHERE r.rid = d.restaurant_id AND d.title LIKE '%{name_dish}%' AND d.price = (SELECT MAX(d2.price) FROM core_dish AS d2 WHERE d2.title LIKE '%{name_dish}%')"
                )
                if(len(restaurants) > 1): 
                    response = f"The restaurant is " ;
                    count = 0
                    for res in restaurants:
                        if count != 0: response += ", "
                        response += res['title']
                        count += 1 
                elif len(restaurants) == 1:
                    response = "The restaurant is " + restaurants[0]['title']
                else: response = "No have"
                selected_statement = Statement(response)
            elif self.cate == 2: 
                restaurants = get_restaurant_with_id_title(
                    f"SELECT r.rid, r.title FROM core_restaurant AS r, core_dish AS d WHERE r.rid = d.restaurant_id AND d.title LIKE '%{name_dish}%' AND d.price = (SELECT MIN(d2.price) FROM core_dish AS d2 WHERE d2.title LIKE '%{name_dish}%')"
                )
                if(len(restaurants) > 1): 
                    response = f"The restaurant is " ;
                    count = 0
                    for res in restaurants:
                        if count != 0: response += ", "
                        response += res['title']
                        count += 1 
                elif len(restaurants) == 1:
                    response = "The restaurant is " + restaurants[0]['title']
                else: response = "No have"
                selected_statement = Statement(response)
            elif self.cate == 3: 
                restaurants = get_restaurant_with_id_title(
                    f"SELECT r.rid, r.title FROM core_restaurant AS r, core_dish AS d WHERE r.rid = d.restaurant_id AND d.title LIKE '%{name_dish}%'"
                )
                if(len(restaurants) > 1): 
                    response = f"Restaurants that have {name_dish} dishes: " ;
                    count = 0
                    for res in restaurants:
                        if count != 0: response += ", "
                        response += res['title']
                        count += 1 
                elif len(restaurants) == 1:
                    response = "Currently there is only restaurant " + restaurants[0]['title']
                else: response = "No have"
                selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement