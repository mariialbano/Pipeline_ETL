# API
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app/swagger-ui/index.html#/Users%20Controller/findById'

# Reading the .csv file with IDs number
import pandas as pd

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

# Returning users with IDs
import requests
import json

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))



# importing openai and integrating with our system
import openai

# Creating a openAI key
openai_api_key = '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'

openai.api_key = openai_api_key

def generate_ai_news(user):
    params = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um especialista em investimentos."},
            {"role": "user", "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo 100 caracteres)"}
        ]
    }

    try:
        # sending the request to the openAI API
        response = openai.ChatCompletion.create(**params)

        # getting the generated answer
        completions = response['choices'][0]['message']['content']
        return completions
    except Exception as e:
        print(f"Erro ao gerar notícia AI: {e}")
        return None
    

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
    "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
    "description": news
})


# updating message to user
def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False
  
for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}!")
