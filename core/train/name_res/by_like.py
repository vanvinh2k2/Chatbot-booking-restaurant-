from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core.logic.search_word import search_word

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
        
        if self.cate == 0: selected_statement = Statement("Restaurant famous")
        elif self.cate == 1: selected_statement = Statement("Restaurant like high")
        elif self.cate == 2: selected_statement = Statement("Restaurant like low")
        elif self.cate == 3: selected_statement = Statement("List restaurant of system")

        selected_statement.confidence = confidence
        return selected_statement