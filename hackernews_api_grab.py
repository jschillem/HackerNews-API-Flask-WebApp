from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import NewsItem, app
import requests
import time

app.app_context().push()

instance_folder = app.instance_path

engine = create_engine(f'sqlite:////{instance_folder}/site.db')
Session = sessionmaker(bind=engine)

API_URL = "https://hacker-news.firebaseio.com/v0"
topPosts = requests.get(f"{API_URL}/topstories.json").json()

counter = 0
start = time.process_time()
with Session() as session:
    try:
        for postId in topPosts:
            item = session.query(NewsItem).filter_by(id=postId).first()

            # if the ID is not already in the database
            if item is None:
                post = requests.get(f"{API_URL}/item/{postId}.json").json()
                if post['type'] == 'story':
                    new_item = NewsItem(
                        id=int(post['id']),
                        by=post.get('by', None),
                        descendants=post.get('descendants', None),
                        score=int(post.get('score', None)),
                        text=post.get('text', None),
                        title=post.get('title', None),
                        time=int(post.get('time', None)),
                        type=post['type'],
                        url=post.get('url', None)
                    )
                    session.add(new_item)
                    counter += 1
    finally:
        session.commit()
        session.close()

elapsed = time.process_time() - start
print(f'It took {elapsed} seconds to add {counter} news items.')
