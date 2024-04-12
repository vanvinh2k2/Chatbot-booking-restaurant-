from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_first_response
from django.db import connection
from datetime import datetime

bot = ChatBot('My Chatbot',
              logic_adapters=[
                    {
                        'import_path': 'core.train.price.price_min_max.MyLogicAdapter',
                    },
                    {
                        'import_path': 'core.train.price.price_of_res.MyLogicAdapter',
                    },
                    {
                        'import_path': 'core.train.price.price.MyLogicAdapter',
                    },
                    {
                        'import_path': 'core.train.name_res.by_like.MyLogicAdapter',
                    },
                    {
                        'import_path': 'core.train.name_res.by_time.MyLogicAdapter',
                    },
                    {
                        'import_path': 'core.train.name_dish.by_res.MyLogicAdapter',
                    },
                    {
                        'import_path': 'core.train.name_res.by_dish.MyLogicAdapter',
                    },
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'I am sorry, but I do not understand.',
                        'maximum_similarity_threshold': 0.90,
                        "statement_comparison_function": LevenshteinDistance,
                        "response_selection_method": get_first_response
                    }
              ],
              preprocessors=[
                  'chatterbot.preprocessors.clean_whitespace'
              ],
)
trainer = ListTrainer(bot)
# trainer.train([
#     "How are you?",
#     "I am good.",
#     "That is good to hear.",
#     "Thank you",
#     "You are welcome.",
#     "Thanks",
#     "Bye",
# ])

@api_view(['POST'])
def reponse_chatbot(request, *args, **kwargs):
    # try:
        user_input = request.data.get("body")
        uid = kwargs.get("uid")
        bot_response = bot.get_response(user_input)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO chatterbot_chatbot (user_id, body_user, body_bot, date)\
                            VALUES (%s, %s, %s, %s)", (uid, user_input, str(bot_response), datetime.now()))
        connection.commit()
        return Response({'success': True, 'result': str(bot_response)}, status=status.HTTP_202_ACCEPTED)
    # except Exception as e: return Response({'success': False, 'result': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def list_chatbot(request, *args, **kwargs):
    try:
        uid = kwargs.get("uid") 
        chats = []
        with connection.cursor() as cursor:
            query = f"SELECT * FROM chatterbot_chatbot WHERE user_id='{uid}' ORDER BY date ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            for row in rows:
                data_col = dict(zip(columns, row))
                chats.append(data_col)
        return Response({'success': True, 'data': chats}, status=status.HTTP_202_ACCEPTED)
    except Exception as e: return Response({'success': False, 'data': str(e)}, status=status.HTTP_404_NOT_FOUND)


    