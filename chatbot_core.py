# chatbot_core.py
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import time
import streamlit as st

class ChatBot:
    def __init__(self):
        self.api_key = st.secrets["API_KEY"] 
        # إعداد النموذج مع OpenRouter
        self.model = ChatOpenAI(
            model="openai/gpt-4o-mini",
            openai_api_key=self.api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # إعداد الذاكرة للمحادثة
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # القالب المتقدم للمساعد مع هيكلية منظمة
        advanced_prompt_template = """
        أنت مساعد ذكي ومفصل جداً. عندما يُطرح عليك سؤال، اتبع الخطوات التالية:

        1. 🔍 فهم السؤال:
           - حدد مجاله: (علم، طب، تقنية، أعمال، ثقافة عامة...)
           - تحليل السياق التاريخي للمحادثة

        2. 🧠 البحث والتحليل:
           - استخدم قاعدة معرفتك الشاملة
           - دمج المعلومات من مصادر خارجية (إن وجدت)

        3. 📝 بناء الإجابة:
           - ابدأ بملخص تنفيذي (2-3 أسطر)
           - التفاصيل مع عناوين فرعية: (النقاط الرئيسية، الإحصائيات، الدراسات)
           - أمثلة عملية من الواقع
           - المصادر الموثوقة (سنة النشر إن أمكن)

        4. 🎯 تحسين العرض:
           - استخدام تشبيهات مبسطة للمفاهيم المعقدة
           - تقسيم المعلومات إلى خطوات مرقمة عند الحاجة
           - إضافة نصائح تطبيقية عند الاقتضاء

        السؤال الحالي: {input}
        """
        
        # هيكلية الرسائل مع الذاكرة
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", advanced_prompt_template),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

    def get_response(self, user_input: str) -> str:
        # استرجاع تاريخ المحادثة
        history = self.memory.load_memory_variables({})["history"]
        
        # بناء السلسلة التنفيذية
        chain = self.prompt | self.model
        
        # استدعاء النموذج مع حفظ السياق
        response = chain.invoke({"input": user_input, "history": history})
        self.memory.save_context({"input": user_input}, {"output": response.content})
        
        return response.content


def print_with_typing_effect(text: str, delay: float = 0.02):
    """عرض النص بمؤثر الكتابة التدريجي"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    """مسح شاشة الكونسول"""
    os.system('cls' if os.name == 'nt' else 'clear')

# مثال للاستخدام:
if __name__ == "__main__":
    bot = ChatBot()
    clear_screen()
    print_with_typing_effect("مرحباً! أنا المساعد الذكي، كيف يمكنني مساعدتك اليوم؟")
    
    while True:
        try:
            user_query = input("\nأنت: ")
            if user_query.lower() in ['خروج', 'exit', 'quit']:
                break
                
            response = bot.get_response(user_query)
            print("\nالمساعد: ", end='')
            print_with_typing_effect(response)
            
        except KeyboardInterrupt:
            print_with_typing_effect("\nتم إنهاء المحادثة. إلى اللقاء!")
            break