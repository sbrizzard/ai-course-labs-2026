from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import llm

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是编程助教，每次用一句中文回答。"),
    ("human", "解释：{topic}")])
chain = prompt | llm | StrOutputParser()
print("INVOKE:", chain.invoke({"topic": "Git commit"}))
print("BATCH:", chain.batch([{"topic": "Docker镜像"}, {"topic": "Docker容器"}]))
print("STREAM:", end=" ")
for chunk in chain.stream({"topic": "WSL"}):
    print(chunk, end="", flush=True)
print()
