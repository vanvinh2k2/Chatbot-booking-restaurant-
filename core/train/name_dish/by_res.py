from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.search_word import search_word
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords

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
        confidence = 0.92
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == True):
                    name_res = name
                    break
        if(name_res == ""):
            if(self.cate == 0 or self.cate == 3): selected_statement = Statement("Please tell me the restaurant name?")
            elif self.cate == 1: selected_statement = Statement("Dish high: Abc")
            elif self.cate == 2: selected_statement = Statement("Dish low: Xyz")
        else: 
            if self.cate == 0: selected_statement = Statement("List featured: 1, 2, .. of A")
            elif self.cate == 1: selected_statement = Statement("Dish high: Abc of A")
            elif self.cate == 2: selected_statement = Statement("Dish low: Xyz of A")
            elif self.cate == 3: selected_statement = Statement("List: 1, 2, 3, ... of A")
        selected_statement.confidence = confidence
        return selected_statement