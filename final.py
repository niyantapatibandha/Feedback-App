import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from openai import AzureOpenAI

# Azure Text Analytics credentials
text_analytics_endpoint = "https://niyanta-service.cognitiveservices.azure.com/"
text_analytics_key = "9a81e14cbbd04cc89196f064fb5c7859"

# Initialize Text Analytics client
text_analytics_credential = AzureKeyCredential(text_analytics_key)
text_analytics_client = TextAnalyticsClient(endpoint=text_analytics_endpoint, credential=text_analytics_credential)

# Azure OpenAI credentials
openai_endpoint = "https://niyanta-chatbot.openai.azure.com/"
openai_key = "ba357d02bd874d88a68f5723eab82937"
openai_api_version = "2024-02-15-preview"

# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    azure_endpoint=openai_endpoint,
    api_key=openai_key,
    api_version=openai_api_version
)

def analyze_sentiment(input_text):
    # Analyze sentiment using Azure Text Analytics
    response = text_analytics_client.analyze_sentiment(documents=[input_text])[0]
    sentiment = response.sentiment
    return sentiment

def generate_response(input_text):
    # Create system message for OpenAI
    system_message = """You are an assistant who generates response on the basis of the feedback given by the customer on the basis of their experience. You have to analyze their emotions and give a relevant reply because you are working for a company as a customer care chatbot."""

    # Send request to Azure OpenAI model
    response = openai_client.chat.completions.create(
        model="gpt-35-turbo",
        temperature=0.7,
        max_tokens=400,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_text}
        ]
    )
    generated_text = response.choices[0].message.content
    return generated_text

def main():
    st.title("Feedback Page")
    input_text = st.text_area("We value your feedback...")

    if st.button('Submit'):
        if input_text:
            # Perform sentiment analysis
            sentiment = analyze_sentiment(input_text)
            st.subheader("Sentiment Analysis Result:")
            if sentiment == "positive":
                st.success(f"Sentiment: {sentiment.capitalize()}")
            elif sentiment == "negative":
                st.error(f"Sentiment: {sentiment.capitalize()}")
            else:
                st.warning(f"Sentiment: {sentiment.capitalize()}")

            # Generate response using Azure OpenAI based on sentiment
            response = generate_response(input_text)
            st.subheader("Generated Response:")
            st.write(response)

if __name__ == "__main__":
    main()
