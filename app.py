import streamlit as st
import json

from chat_ai import generate_response_for_pre_indexed_repo, generate_response_for_custom_repo

st.set_page_config(page_title="Tune AI Git Issue Chat")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


with st.sidebar:
    option = st.selectbox(
        'What repo you are looking for?',
        ('Pre-Indexed', 'Custom'),
        index=None,
        placeholder="please choose an option"
    )
    if option == 'Pre-Indexed':
        option_of_repo = st.selectbox(
            'Choose any one of the pre-index repo',
            ('Tensorflow', 'Pytorch'),
            index=None,
            placeholder="please choose an option"
        )
        st.write("Select number of top issues you are looking for!")
        number_of_issues = st.number_input('Insert a number')
    elif option == 'Custom':
        repo_link = st.text_area("Please enter your public repo link!")
        st.write("Select number of top issues you are looking for!")
        number_of_issues = st.number_input('Insert a number')

    st.button("Ask Tune AI!", on_click=click_button)

if st.session_state.clicked:
    with st.spinner("Generating, It may take some minutes🫡..."):
        if option == 'Pre-Indexed' and number_of_issues:
            if option_of_repo == "Tensorflow":
                repo_choice = "Tensorflow"
            elif option_of_repo == "Pytorch":
                repo_choice = "Pytorch"
            gpt_response = generate_response_for_pre_indexed_repo(repo_choice, number_of_issues)
            if gpt_response["success"]:
                try:
                    json_data = json.loads(gpt_response["data"])
                    for issue in json_data['issues']:
                        st.markdown(f"**{issue['issue_title']}**", unsafe_allow_html=True)
                        st.write("Rating:", issue['rating']['type'])
                        st.write("Description:", issue['rating']['description'])
                except:
                    st.json(gpt_response["data"])
            else:
                st.write("Sorry we encountered some issues!")
        elif option == 'Custom' and number_of_issues and repo_link:
            gpt_response = generate_response_for_custom_repo(number_of_issues, repo_link)
            if gpt_response["success"]:
                try:
                    json_data = json.loads(gpt_response["data"])
                    for issue in json_data['issues']:
                        st.markdown(f"**{issue['issue_title']}**", unsafe_allow_html=True)
                        st.write("Rating:", issue['rating']['type'])
                        st.write("Description:", issue['rating']['description'])
                except:
                    st.json(gpt_response["data"])
            else:
                st.write("Sorry we encountered some issues!")
