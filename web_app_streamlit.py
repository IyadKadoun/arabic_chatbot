import streamlit as st
from chatbot_core import ChatBot


# --- إعداد الصفحة ---
st.set_page_config(page_title="AI Bot - مساعد ذكاء اصطناعي", page_icon="🤖", layout="centered")

# --- تعريف CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    :root {
        direction: rtl;
    }
    
    body {
        font-family: 'Cairo', sans-serif;
        background-color: #f8f9fa;
        color: #000000;
        text-align: right;
    }

    .chat-message {
        padding: 12px 16px;
        border-radius: 18px;
        margin-bottom: 12px;
        max-width: 75%;
        line-height: 1.6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        animation: fadeIn 0.3s ease-in-out;
        direction: rtl;
        text-align: right;
    }

    .user {
        background-color: #DCF8C6;
        color: #000;
        margin-left: 0;
        margin-right: auto;
        border-bottom-right-radius: 4px;
        border-bottom-left-radius: 18px;
    }

    .bot {
        background-color: #ECECEC;
        color: #000;
        margin-left: auto;
        margin-right: 0;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 18px;
    }

    .title {
        text-align: center;
        color: #333;
        font-weight: bold;
        direction: rtl;
    }

    .footer {
        position: fixed;
        bottom: 0;
        left: 10px;
        right: auto;
        width: auto;
        text-align: left;
        font-size: 12px;
        color: #888;
        z-index: 100;
        background-color: white;
        padding: 6px 12px;
        border-radius: 0 10px 0 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        direction: ltr;
    }

    .button-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 10px;
        direction: rtl;
    }

    .message-container {
        display: flex;
        align-items: start;
        gap: 10px;
        flex-direction: row;
    }

    .avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }

    .user .avatar {
        background-color: #4CAF50;
        color: white;
    }

    .bot .avatar {
        background-color: #2196F3;
        color: white;
    }

    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    .stTextArea textarea {
        height: 150px;
        font-size: 16px;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #ccc;
        resize: none;
        direction: rtl;
        text-align: right;
    }
    
    /* تعديلات عامة للمحاذاة */
    .stTextInput input, .stSelectbox select, .stButton button {
        direction: rtl;
        text-align: right;
    }
    
    .st-b7, .st-b8, .st-b9 {
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

# --- حالة التطبيق ---
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatBot()
    st.session_state.messages = []

def handle_user_input(user_input):
    if user_input.strip() == "":
        return
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    bot = st.session_state.chatbot
    response = ""
    
    if user_input.lower() in ['/exit', '/quit']:
        response = "👋 شكراً لك! إلى اللقاء!"
    elif user_input.lower() == '/clear':
        bot.memory.clear()
        st.session_state.messages = []
        response = "🧹 تم مسح المحادثة."
    elif user_input.lower() == '/help':
        help_text = """
        📜 الأوامر المتاحة:
        /exit أو /quit : إنهاء المحادثة
        /clear : مسح التاريخ والشاشة
        /help : عرض هذه القائمة
        /log : عرض آخر المحادثات
        """
        response = help_text
    elif user_input.lower() == '/log':
        try:
            with open("chat_log.txt", "r", encoding="utf-8") as f:
                response = f.read() or "📂 لا يوجد سجل محادثات حتى الآن."
        except FileNotFoundError:
            response = "📂 لا يوجد ملف سجلات بعد."
    else:
        try:
            response = bot.get_response(user_input)
        except Exception as e:
            response = f"⚠️ حدث خطأ أثناء المعالجة: {str(e)}"
    
    st.session_state.messages.append({"role": "bot", "content": response})

def save_chat_to_txt():
    chat_text = ""
    for msg in st.session_state.messages:
        role = "👤 مستخدم" if msg["role"] == "user" else "🤖 بوت"
        chat_text += f"{role}:\n{msg['content']}\n\n{'-'*30}\n"
    return chat_text

# --- عنوان التطبيق ---
st.markdown("<h1 class='title'>🤖 مساعد ذكاء اصطناعي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>اكتب سؤالك وستجد المساعد يرد عليك فورياً</p>", unsafe_allow_html=True)

# --- منطقة المحادثة ---
chat_area = st.container()

# --- حقل الإدخال وأزرار التحكم ---
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_area("اكتب رسالتك هنا...", key="input", placeholder="مثال: اشرح لي ما هو الذكاء الاصطناعي؟")
    submit_button = st.form_submit_button(label="إرسال")

# --- أزرار إضافية ---
st.markdown('<div class="button-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("♻️ محادثة جديدة", use_container_width=True):
        handle_user_input("/clear")
with col2:
    if st.button("📜 عرض السجل", use_container_width=True):
        handle_user_input("/log")
with col3:
    chat_text = save_chat_to_txt()
    st.download_button(
        label="📥 حفظ المحادثة",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
        use_container_width=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- معالجة الإدخال ---
if submit_button and user_input:
    handle_user_input(user_input)

# --- عرض المحادثة ---
with chat_area:
    for msg in st.session_state.messages:
        role_class = "user" if msg["role"] == "user" else "bot"
        avatar = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f"""
        <div class="message-container {role_class}">
            <div class="avatar">{avatar}</div>
            <div class="chat-message {role_class}">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    هذا البوت مبني على النموذج المجاني gpt-4o-mini <br>
    والذي تم تدريبه في December-2023 <br>
    This software is developed by Iyad Kadoun
</div>
""", unsafe_allow_html=True)