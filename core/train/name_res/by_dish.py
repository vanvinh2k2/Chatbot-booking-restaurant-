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
        confidence = 0.93
        if len(getName(str(input_statement))) > 0:
            for name in getName(str(input_statement)):
                if(getRole(name, str(input_statement)) == False):
                    name_dish = name
                    break
        
        if(name_dish == ""): selected_statement = Statement("Please tell me the dishes name?")
        else: 
            if self.cate == 0: selected_statement = Statement("List featured Restaurant: 1, 2, .. of dish ")
            elif self.cate == 1: selected_statement = Statement("Restaurant high: Abc of dish")
            elif self.cate == 2: selected_statement = Statement("Restaurant low: Xyz of dish")
            elif self.cate == 3: selected_statement = Statement("List Restaurant: 1, 2, 3, ... of dish")
        selected_statement.confidence = confidence
        return selected_statement