import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

mcp_fetch_server = MCPServerStdio(
    command="python",
    args=["-m","mcp_server_fetch"]
)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

agent= Agent(
    model="groq:llama-3.3-70b-versatile",
    mcp_servers=[mcp_fetch_server]
)

async def fetch_summary(url):
    async with agent.run_mcp_servers():
        prompt=f"""
            You are a web agent.

            Step 1: Use the fetch tool to retrieve the full content from this URL:
            {url}

            Step 2: Read the fetched content carefully.

            Step 3: Summarize it in exactly 100 words.

            Do not guess. Do not skip tool usage.
        """
        result = await agent.run(prompt)
        output = result.output
        return output

def get_summary(url):
    return asyncio.run(fetch_summary(url))

###--------Streamlit UI-----
st.set_page_config(page_title="Web Page Summarizer", layout="centered")

st.title("🌐 Web Page Summarizer Agent")
st.write("Enter a URL and generate a 100-word summary using your AI agent.")
url_input = st.text_input("Enter webpage URL:")

if st.button("Generate Summary"):
    if url_input:
        with st.spinner("Processing..."):
            try:
                summary = get_summary(url_input)
                st.success("Summary Generated!")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")

st.markdown("---")
st.caption("Built with Streamlit + Groq LLM Agent")


# if __name__ == "__main__":
#     output = asyncio.run(main())
#     print(output)