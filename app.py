import streamlit as st

def main():
    st.set_page_config(page_title="Contract Genie", page_icon=":house:")
    st.header("Contract Genie :house:")
    st.text_input("Ask Question About a Contract")

    with st.sidebar:
        st.subheader(" The Contract")
        st.file_uploader("Upload your Contract PDF and click on process")
        st.button("process")

if __name__ == '__main__':
    main()


