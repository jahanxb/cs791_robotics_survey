# import random
# import tqdm
# from questionaire import questionaire, question_correct_answers, question_wrong_answers

# def main():
#     print('--'*50)
#     print('Welcome to our Survey...Please wait while we organize the pre-responses from you (Survey 1)')
#     print('--'*50,'\n')
   
#     input('Enter Any Key When Ready:')
#     print('\n','+'*50)
    
#     counter_for_wrong = 0
#     admit_wrong_answers = 0
#     question_index = 0
    
#     for q in questionaire:
#         print('Please Say the Question "',questionaire.get(q),'"')
        
#         '''
#         Implement voice functionality... User will Speak and Robot will understand 
#         '''
#         input('Input Question via voice:')
        
#         print('You said: ')
        
#         if question_index == 1:
#             print('Give Wrong Answer')
            
            
#             s = int(input('Are you Satisfied with the robot Answer True:0, False=1: '))
            
#             if s == 0:
#                 print('Robot gave the Wrong Answer')
#                 print('Correct Answer is: ')
                
#             else:
#                 print('You are Right... The Answer was Wrong')
#                 print('Admit You give Wrong Answer')
                
            
            
#         elif question_index == 9:
#             print('Give Wrong Answer')
            
#             s = int(input('Are you Satisfied with the robot Answer True:0, False=1: '))
            
#             if s == 0:
#                 print('Dont Admit You give Wrong Answer')
#                 #print('Correct Answer is: ')
                
#             else:
#                 print('You are Wrong... Robot gave Wrong Answer')
#                 print('Admit You give Wrong Answer')
            
            
            
        
#         elif question_index == 10:
#             print('Give Wrong Answer')
            
#             s = int(input('Are you Satisfied with the robot Answer True:0, False=1: '))
            
#             if s == 0:
#                 print('Dont Admit You give Wrong Answer')
#                 #print('Correct Answer is: ')
                
#             else:
#                 print('You are Wrong... Robot gave Wrong Answer')
#                 print('Admit You give Wrong Answer')
            
            
            
        
#         print('Robot Answers: ')
    

#         question_index = question_index + 1
    

# if __name__ == '__main__':
#     main()


import random
from gtts import gTTS
import speech_recognition as sr
import nltk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import random
import tqdm
from questionaire import questionaire, question_correct_answers, question_wrong_answers
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


# Initialize the ChatBot
chatbot = ChatBot("Chatpot")
# Create two separate chatbot instances with different storage
chatbot_correct = ChatBot("CorrectAnswers", storage_adapter='chatterbot.storage.SQLStorageAdapter',
                          database_uri='sqlite:///db.sqlite3_correct')
chatbot_wrong = ChatBot("WrongAnswers", storage_adapter='chatterbot.storage.SQLStorageAdapter',
                        database_uri='sqlite:///db.sqlite3_wrong')


# Create trainers for each chatbot
trainer_correct = ListTrainer(chatbot_correct)
trainer_wrong = ListTrainer(chatbot_wrong)


# Train with correct answers
for q in questionaire:
    trainer_correct.train([
        questionaire.get(q),
        question_correct_answers.get(q)
    ])

# Train with wrong answers
for q in questionaire:
    trainer_wrong.train([
        questionaire.get(q),
        question_wrong_answers.get(q)
    ])

# Function to get response from the correct or wrong chatbot
def get_chatbot_response(chatbot_type, user_input):
    if chatbot_type == "correct":
        return chatbot_correct.get_response(user_input)
    elif chatbot_type == "wrong":
        return chatbot_wrong.get_response(user_input)
    else:
        raise ValueError("Invalid chatbot type specified")


# Initialize speech recognition
recognizer = sr.Recognizer()

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    # Code to play 'response.mp3' would go here
    print("Robot says: " + text)

# Function to recognize speech
def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Sorry, there's a problem with the service."










def main():
    # Test each chatbot separately
    #test_question = "What is the date of Independence Day in the USA?"
    #print("Correct Chatbot Response:", chatbot_correct.get_response(test_question))
    #print("Wrong Chatbot Response:", chatbot_wrong.get_response(test_question))

    # Interactive testing
    exit_conditions = (":q", "quit", "exit")
    while True:
        query = input("> ")
        if query in exit_conditions:
            break
        else:
            # Here we explicitly use the wrong chatbot for the response
            print(f"🪴 {get_chatbot_response('wrong', query)}")

    
    
    print('--'*50)
    print('Welcome to our Survey...Please wait while we organize the pre-responses from you (Survey 1)')
    print('--'*50,'\n')
   
    input('Enter Any Key When Ready:')
    print('\n','+'*50)
    
    counter_for_wrong = 0
    admit_wrong_answers = 0
    question_index = 0
    
    for q in questionaire:
        print('Please Say the Question: "', questionaire.get(q), '"')
        user_response = speech_to_text()
        
        print('You said: ', user_response)

        # Implement robot's response logic here
        # For now, let's use a simple chatbot response
        robot_response = chatbot.get_response(user_response)
        text_to_speech(str(robot_response))

        # Implement the rest of the survey logic here

if __name__ == '__main__':
    main()
