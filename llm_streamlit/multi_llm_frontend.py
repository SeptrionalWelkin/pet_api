import streamlit as st
import anthropic
import time
from openai import OpenAI


# Function to initialize the Claude client
def init_claude(anthropic_api_key):
    return anthropic.Anthropic(api_key=anthropic_api_key)


def init_open_ai(open_ai_api_key):
    return OpenAI(api_key=open_ai_api_key)


messages = []


# Function to generate response from Claude
def generate_claude_response(client, prompt, temperature, top_p, top_k, stream_output, stream_box):
    model = "claude-3-5-sonnet-20240620"  # if mode == "Instruct" else "claude-3-5-sonnet-20240620-chat"

    # Configuration for Claude API
    params = {
        "model": model,
        "messages": [{"role": "user",
                      "content": prompt}],
        # "prompt": prompt,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_tokens": 300,
    }

    messages.append(params)

    if stream_output:
        # response = client.messages.stream(**params)
        # for message in response:
        #     yield message['completion']
        #     time.sleep(0.1)

        running_stream = ""

        with client.messages.stream(**params) as stream:
            for event in stream.text_stream:
                running_stream += event
                time.sleep(.002)
                stream_box.write(running_stream)

    else:
        response = client.messages.create(**params)
        stream_box.write(response.content[0].text)


def generate_gpt_response(client, user_input, temperature, top_p, stream_output, stream_box):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are helpful assistant"},
            {"role": "user", "content": user_input}
        ],
        temperature=temperature,
        top_p=top_p,
        stream=stream_output
    )

    if stream_output:
        running_stream = ''
        for chunk in completion:
            if chunk.choices[0].finish_reason == "stop":
                break
            for c in chunk.choices[0].delta.content:
                running_stream += c
                time.sleep(.002)
                stream_box.write(running_stream)

    else:
        result = completion.choices[0].message.content
        stream_box.write(result)


# Streamlit UI
def main():
    st.title("Multi Model Chat App")

    claude_api_key = CLAUDE_KEY
    open_ai_api_key = OPENAI_KEY

    #Configuration buttons
    st.sidebar.header("Configuration")
    model = st.sidebar.radio("Model", ["OpenAI", "Claude"])
    # mode = st.sidebar.radio("Mode", ["Instruct", "Chat"])
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
    top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9)
    top_k = st.sidebar.slider("Top K (Not Supported in OpenAI)", 0, 100, 50)
    stream_output = st.sidebar.checkbox("Stream Output", value=True)

    claude_client = init_claude(claude_api_key)
    open_ai_client = init_open_ai(open_ai_api_key)
    st.header(f"Chat with {model}")

    prompt = st.text_area("Enter your prompt here", height=100)

    chat_history = st.empty()
    stream_box = st.empty()

    if st.button("Generate Response"):
        if prompt:
            # st.write("### Output")
            # output_container = st.empty()

            if model == "Claude":
                # responses = generate_claude_response(claude_client, prompt, temperature, top_p, top_k,
                #                                      stream_output, stream_box)
                generate_claude_response(claude_client, prompt, temperature, top_p, top_k,
                                         stream_output, stream_box)
                # for response in responses:
                #     # output_container.markdown(response)
                #     chat_history.markdown(f"**You:** {prompt}\n\n**Assistant:** {response}")
            elif model == "OpenAI":
                # responses = generate_gpt_response(open_ai_client, prompt, temperature, top_p, stream_output, stream_box)
                generate_gpt_response(open_ai_client, prompt, temperature, top_p, stream_output, stream_box)
                # chat_history.markdown(f"**You:** {prompt}\n\n**Assistant:** {responses}")

                # for response in responses:
                #    output_container.markdown(response)
        else:
            st.error("Prompt is empty. Please enter a valid prompt.")


if __name__ == "__main__":
    main()
