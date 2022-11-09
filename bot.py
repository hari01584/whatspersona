from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("Chatpot")


trainer = ListTrainer(chatbot)

from whatsapp_export_anay import WhatsappExport

wexport = WhatsappExport("./whatsapp_export/WhatsApp Chat with Abhinandan Bhai Thapar.txt")
trainer.train(wexport.corpus())
# trainer.*train([
#     "How are you?",
#     "I am good.",
#     "That is good to hear.",
#     "Thank you",
#     "You are welcome.",
# ])

exit_conditions = (":q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"🪴 {chatbot.get_response(query)}")