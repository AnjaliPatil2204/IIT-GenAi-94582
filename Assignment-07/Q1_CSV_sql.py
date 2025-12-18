#Create a Streamlit application that allows users to upload a CSV file and view its schema.
#Use an LLM to convert user questions into SQL queries, execute them on the CSV data using pandasql,
#and explain the results in simple English.

import os
import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model

# Initialize LLM (Groq)
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
st.title("CSV SQL Query Assistant")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV loaded successfully!")

    # Display schema
    st.subheader("CSV Schema")
    st.write(df.dtypes)

    # User question
    user_question = st.text_input("Ask a question about the CSV data")
    if st.button("Generate SQL and Execute", type="primary"):

       if user_question:
        # Generate SQL using LLM
        sql_prompt = f"""
        You are an expert SQL developer.

        Table Name: data
        Table Schema:
        {df.dtypes}

        User Question:
        {user_question}

        Instruction:
        Write a valid SQLite SQL query.
        Output ONLY the SQL query.
        """

        sql_response = llm.invoke(sql_prompt).content.strip()

        if sql_response.lower().startswith("error"):
            st.error("Could not generate SQL query.")
        else:
            st.subheader("Generated SQL")
            st.code(sql_response, language="sql")

            try:
                # Execute SQL
                result_df = sqldf(sql_response, {"data": df})

                st.subheader("Query Result")
                st.dataframe(result_df)

                # Explain result
                explanation_prompt = f"""
                Explain the following SQL query result in simple English.

                User Question: {user_question}
                SQL Query: {sql_response}
                Result:
                {result_df.head().to_string()}
                """

                explanation = llm.invoke(explanation_prompt).content

                st.subheader("Explanation")
                st.write(explanation)

            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
