import pandas as pd
from sqlalchemy import create_engine
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
# Create the SQL engine
engine = create_engine('sqlite:///slynd.db')

# Load the table from the database into a pandas DataFrame
df = pd.read_sql_table('slynd_table', engine)

# Initialize an LLM
llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")

# Create a pandas dataframe agent
agent = create_pandas_dataframe_agent(llm, df, verbose=True)

# Function to ask questions against the dataframe
def ask_question(question):
    return agent.invoke({"input": question})

# Example usage
response = ask_question("What is the total ad spend for the body positivity topic?")
print(response)
