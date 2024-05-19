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
        words = ['dish', 'specialty', "restaurant"]
        words2 = ['dish', 'featured', "restaurant"]
        words3 = ['featured', "restaurant"]
        words4 = ['specialty', "restaurant"]
        words5 = ['dish', 'cost', "high"]
        words6 = ['dish', 'cost', 'expensive']
        words9 = ['dish', 'cost', "low"]
        words10 = ['dish', 'cost', "cheap"]
        words13 = ['dish', 'restaurant']
        
        name_dish =""
        if len(getName(str(statement))) > 0:
            for name in getName(str(statement)):
                if(getRole(name, str(statement)) == False):
                    name_dish = name
        if name_dish != "": return False
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
        name_res = ""
        confidence = 0.951
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == True):
                    name_res = name
                    break
        if(name_res == ""):
            if(self.cate == 0 or self.cate == 3): selected_statement = Statement("Please tell me the restaurant name?")
            elif self.cate == 1: 
                dishes = get_dish_all("SELECT did, title FROM core_dish WHERE price = (SELECT MAX(price) FROM core_dish)")
                if(len(dishes) > 1):
                    response = f"The dish currently with the highest price is "
                    count = 0
                    for dish in dishes:
                        if count != 0: response += ", "
                        response += dish['title']
                        count += 1

                elif len(dishes) == 1:
                    response = f"The dish currently with the highest price is {dishes[0]['title']} dish"
                else: response = "No have"
                selected_statement = Statement(response)
            elif self.cate == 2: 
                dishes = get_dish_all("SELECT did, title FROM core_dish WHERE price = (SELECT MIN(price) FROM core_dish)")
                if(len(dishes) > 1):
                    response = f"The dish currently with the lowest price is "
                    count = 0
                    for dish in dishes:
                        if count != 0: response += ", "
                        response += dish['title']
                        count += 1

                elif len(dishes) == 1:
                    response = f"The dish currently with the lowest price is {dishes[0]['title']} dish"
                else: response = "No have"
                selected_statement = Statement(response)
        else: 
            if self.cate == 0: 
                dishes = get_dish_all(f"SELECT d.did, d.title FROM core_dish AS d, core_restaurant AS r WHERE d.featured = 1 AND r.title LIKE '%{name_res}%' AND r.rid = d.restaurant_id")
                if(len(dishes) > 1):
                    response = f"List of featured dishes of {name_res} restaurant: "
                    count = 0
                    for dish in dishes:
                        if count != 0: response += ", "
                        response += dish['title']
                        count += 1

                elif len(dishes) == 1:
                    response = f"{dishes[0]['title']} dish"
                else: response = "This restaurant is currently unavailable"
                selected_statement = Statement(response)
            elif self.cate == 1: 
                dishes = get_dish_all(f"SELECT d.did, d.title FROM core_dish AS d, core_restaurant AS r WHERE r.title LIKE '%{name_res}%' AND r.rid = d.restaurant_id AND d.price = (SELECT MAX(d.price) FROM core_dish AS d, core_restaurant AS r WHERE r.title LIKE '%{name_res}%' AND r.rid = d.restaurant_id)")
                if(len(dishes) > 1):
                    response = ""
                    count = 0
                    for dish in dishes:
                        if count != 0: response += ", "
                        response += dish['title']
                        count += 1
                    response += f" has the highest price at {name_res} restaurant"
                elif len(dishes) == 1:
                    response = f"{dishes[0]['title']} dish has the highest price at {name_res} restaurant"
                else: response = "This restaurant is currently unavailable"
                selected_statement = Statement(response)
            elif self.cate == 2: 
                dishes = get_dish_all(f"SELECT d.did, d.title FROM core_dish AS d, core_restaurant AS r WHERE r.title LIKE '%{name_res}%' AND r.rid = d.restaurant_id AND d.price = (SELECT MIN(d.price) FROM core_dish AS d, core_restaurant AS r WHERE r.title LIKE '%{name_res}%' AND r.rid = d.restaurant_id)")
                if(len(dishes) > 1):
                    response = ""
                    count = 0
                    for dish in dishes:
                        if count != 0: response += ", "
                        response += dish['title']
                        count += 1
                    response += f" has the lowest price at {name_res} restaurant"
                elif len(dishes) == 1:
                    response = f"{dishes[0]['title']} dish has the lowest price at {name_res} restaurant"
                else: response = "This restaurant is currently unavailable"
                selected_statement = Statement(response)
            elif self.cate == 3: 
                dishes = get_dish_all(f"SELECT d.did, d.title FROM core_dish AS d, core_restaurant AS r WHERE r.title LIKE '%{name_res}%' AND r.rid = d.restaurant_id")
                if(len(dishes) > 1):
                    response = f"List of dishes of {name_res} restaurant: "
                    count = 0
                    for dish in dishes:
                        if count != 0: response += ", "
                        response += dish['title']
                        count += 1
                elif len(dishes) == 1:
                    response = f"{dishes[0]['title']} dish"
                else: response = "This restaurant is currently unavailable"
                selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement