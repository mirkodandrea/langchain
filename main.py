import json
from datetime import datetime

import requests
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from openai import OpenAI

from google_news_search import get_news_articles
import dotenv
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


query = "wildfire AND forest fire AND Canada AND 2024"
date = datetime.strptime("2024-05-15", "%Y-%m-%d").date()
all_news = get_news_articles(query, date, "EN")

urls = []
for _news in all_news:
    url = _news[1]
    if url.startswith('https://news.google.com/rss/articles/'):
        downloaded = requests.get(url).text
        # find the url in the html
        try:
            url = downloaded.split('<link rel="canonical" href="')[
                1].split('"')[0]
            # print('google news detected', url)
        except:
            # print('google news detected but no url found')
            continue

    urls.append(url)

results = []

for idx, url in enumerate(urls):
    print(f'{idx+1}/{len(urls)}: {url}')
    loader = AsyncHtmlLoader([url])
    docs = loader.load()

    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    article = docs_transformed[0].page_content

    my_assistant = client.beta.assistants.retrieve(
        "asst_JdkhCC6FXBmdTYCLtIGSqU0k")

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": article,
            }
        ]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=my_assistant.id
    )

    while run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")

            # Step 6: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            break
        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break

        data = json.loads(all_messages.data[0].content[0].text.value)
        data['url'] = url
        results.append(data)

        json.dump(results, open('results.json', 'w'))
