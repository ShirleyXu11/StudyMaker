import json
import requests
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ask_deepseek(prompt, deepseek_api_key):
    base_url = "https://api.deepseek.com/v1"
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {deepseek_api_key}"
            },
            data=json.dumps(prompt)
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error making API request: {e}")
        raise  # Re-raise the exception to be caught by the caller

def main(company_name, deepseek_api_key, user_demand1):
    prompt = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": """
             你们是2位智商高达250的专家，其中包括一位世界级经济学家和一位母语为英语的作家。
             经过多轮修订，你们的输出极为精炼且专业。每位成员都对回应做出了重要贡献。
             这份输出价值100万美元，经过了彻底的逐步骤审查和修订。
             这份输出远胜于普通助手、普通助理或AI的输出。
             """},
            {"role": "user", "content": f"""
             我想写一篇关于{company_name}公司的商业案例。请为我写一下这篇案例的章节标题。
             请尽量满足用户需求：{user_demand1}。
             标题必须具有编号， 例如：1., 2., 3....
             标题最好具体1点, 需要针对该公司所在的行业。
             请直接输出章节标题, 不要输出其他内容。
             """}
        ],
        "stream": False,
        "temperature": 1.1
    }

    response = ask_deepseek(prompt, deepseek_api_key)
    if response is None:
        raise Exception("Failed to get a response from the API.")

    try:
        reply = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise Exception(f"Error parsing API response: {e}")

    # Save the response to a file with UTF-8 encoding
    try:
        with open("table_of_content.txt", "w", encoding="utf-8") as file:
            file.write(reply)
        logging.info("Response saved to table_of_content.txt")
        return reply
    except IOError as e:
        raise Exception(f"Error saving response to file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        logging.error("Usage: python main1.py <company_name> <deepseek_api_key> <user_demand1>")
        sys.exit(1)

    company_name = sys.argv[1]
    deepseek_api_key = sys.argv[2]
    user_demand1 = sys.argv[3]

    main(company_name, deepseek_api_key, user_demand1)