from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from core.logic.search_word import search_word
from core.logic.object_recognition import getName, getRole
from core.logic.customer_word import remove_stopwords
from core .logic.table import get_table_all

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['seat', "restaurant"]
        words2 = ['table', "restaurant"]
        
        statement = remove_stopwords(str(statement));
        data_set = statement
        check = search_word(words, data_set, True)
        if(check == False):
            check = search_word(words2, data_set, True)
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
            
        if name_res != "":
            tables = get_table_all(f"SELECT t.tid, t.title, t.number_seat FROM core_table AS t, core_restaurant AS r WHERE r.rid = t.restaurant_id AND r.title LIKE '%{name_res}%'")
            if len(tables) > 0:
                response = f"Restaurant {name_res} has {len(tables)} tables including: "
                count = 0
                for table in tables:
                    if count != 0: response += ", "
                    response += table['title'] + "(" + str(table['number_seat'])  + " persons)"
                    count += 1 
            else: response = f"No information was found about restaurant {name_res}"
        else: response = "No restaurant name yet" 
        selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement