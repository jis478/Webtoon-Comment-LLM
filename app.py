import pandas as pd
import streamlit as st 
import tempfile
from langchain.llms import Ollama
from summarizer import Summarizer
from langchain.prompts import PromptTemplate
from streamlit_chat import message

# Upload CSV file
with st.sidebar:
    uploaded_file = st.file_uploader("[Step 1] CSV 파일을 올려주세요", type="csv")

# Check if the form is submitted and a file is uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Get unique titles
    titles = df['title'].unique().tolist()

    # Select title
    title = st.selectbox("[Step 2] 작품을 선택해주세요", titles)

    # Filter episodes based on the selected title
    title_comments = df[df["title"] == title]
    episodes = list(set(title_comments["episode"]))

    # Display the Episode select box based on the selected title
    episode = st.selectbox("[Step 3] 회차를 선택해주세요", episodes)
    num_likes = st.slider("[Step 4] 'Likes' 기준 선택 댓글 수를 선택해주세요:", min_value=3, max_value=10, value=3, step=1)
    llm_name = st.selectbox("[Step 5] 모델을 선택해주세요", ["openchat", "llama2:70b", "phi", "mixtral"])
    
    if st.button("설정 완료"):
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['title'] = title
        st.session_state['episode'] = episode
        st.session_state['num_likes'] = num_likes
        st.session_state['llm_name'] = llm_name
        st.session_state['setup'] = True

if st.session_state.get('setup'):
    # model loading
    llm = Ollama(model=st.session_state['llm_name'])
    model = Summarizer()
    st.write("[1/3] llm 모델이 로딩되었습니다.")  

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(st.session_state['uploaded_file'].getvalue())
        tmp_file_path = tmp_file.name
    df_pd = pd.read_csv(tmp_file_path)
    print(df_pd)
    df_pd = df_pd.sort_values(by='Like', ascending=False)
    all_comments = list(df_pd['Comment'])
    all_comments = "\n ".join(all_comments)
    st.write(f"[2/3] csv 파일에 총 {len(df_pd)} 댓글, {len(all_comments)}자가 존재합니다.")  

    title_comments = df[df["title"] == st.session_state['title']]
    df_pd = title_comments[title_comments["episode"] == st.session_state['episode']]
    df_pd = df_pd.sort_values(by='Like', ascending=False)
    df_pd = df_pd.iloc[:st.session_state['num_likes']]
    all_comments = list(df_pd["Comment"])
    all_comments = "\n ".join(all_comments)
    st.session_state['results'] = all_comments
    st.write(f"[3/3] 상위 {st.session_state['num_likes']} 베댓 선정 후, 총 {len(df_pd)} 댓글, {len(all_comments)}자가 존재합니다. 아래는 결과입니다.")  
    temp_view = df_pd.iloc[:st.session_state['num_likes'], df_pd.columns.isin(["Username", "Top", "Comment", "Like"])]
    st.dataframe(temp_view)

# User input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

# Applying the user input box
question = get_text()

# Response output
def generate_response(question):
    prompt_template = """
        {question}            

        {comments} 
        """    
    prompt_text = PromptTemplate(template=prompt_template, input_variables=["question", "comments"])
    reduced_result = llm(prompt=prompt_text.format(comments=st.session_state['results'], question=question))            
    return reduced_result

if question:
    response = generate_response(question)
    message(question, is_user=True)
    message(response)
