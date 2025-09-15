import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🏥 재활 상담 챗봇")
st.write(
     "아픈 부위를 입력하면 가능한 원인, 재활 방법, "
    "그리고 참고할 수 있는 유튜브 영상을 알려드립니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("API Key를 입력해야 챗봇을 사용할 수 있습니다.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.

     # 대화 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": (
                "너는 재활 상담 전문 챗봇이야. "
                "사용자가 아픈 부위를 말하면, 왜 아플 수 있는지 가능한 원인을 설명해주고 "
                "집에서 할 수 있는 간단한 재활 운동, 스트레칭 방법을 알려줘. "
                "추가로 도움이 될 만한 유튜브 영상 링크를 추천해."
            )}
        ]

    # 이전 대화 보여주기
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if user_input := st.chat_input("어디가 아프신가요? (예: 허리, 어깨, 무릎)"):
        # 대화 기록에 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # OpenAI API 호출 (스트리밍)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            )

            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response})
