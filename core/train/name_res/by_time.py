from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core.logic.search_word import search_word
from core.logic.get_time import extract_opening_hours

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ["open", 'restaurant', 'start', 'end']
        words2 = ['restaurant', 'operation']
        words3 = ["close", 'restaurant', 'start', 'end']
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
            self.cate = 1
            check = search_word(words3, data_set, True)
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
        
        if opening_time != None and closing_time != None: 
            if self.cate == 0:
                selected_statement = Statement("Restaurant open from %s to %s" %(opening_time, closing_time))
            elif self.cate == 1: selected_statement = Statement("Restaurant close from %s to %s" %(opening_time, closing_time))
            else: selected_statement = Statement("Restaurant open")
        elif opening_time != None: selected_statement = Statement("Restaurant start %s" %(opening_time))
        elif closing_time != None: selected_statement = Statement("Restaurant end %s" %(closing_time))

        selected_statement.confidence = confidence
        return selected_statement