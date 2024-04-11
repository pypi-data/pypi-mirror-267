from download_models import FileDownloader
from superU_User_Persona import User_Persona
from superU_Intent_Classification import Intent_Classifier
from superU_LLM_Analytics import llm_analytics

class Build_User_Persona:
    def __init__(self, openai, llm_deploymentname):
        self.user_persona = User_Persona(openai, llm_deploymentname)
        
    def build(self, conversations):
        persona = self.user_persona.analyze_conversation(conversations)
        return persona
        

    
class Intent_Classification:
    def __init__(self):
        self.files = FileDownloader()
        self.files.download_files()
        self.intent_classifier = Intent_Classifier()
        
    def get_intent(self, user_question):
        intent = self.intent_classifier.get_intent(user_question)
        return intent
    
    
    
class LLM_Analytics:
    def __init__(self, public_key, secret_key):
        self.llm_analytics = llm_analytics(public_key=public_key, secret_key=secret_key)
    
    def analyse(self, data):
        print(self.llm_analytics.post_data(data))