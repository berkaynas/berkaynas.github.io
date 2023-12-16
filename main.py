from openai import OpenAI
import os
from git import Repo
from pathlib import Path

#api_key = os.environ["OPENAI_API_KEY"]
#print(os.environ)
#client = OpenAI(api_key=api_key)

PATH_TO_BLOG_REPO = Path("/Users/berkkaynas/PycharmProjects/github/berkaynas.github.io/.git")

PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent

PATH_TO_CONTENT = PATH_TO_BLOG/"content"
PATH_TO_CONTENT.mkdir(exist_ok=True,parents=True)


def update_blog(commit_message="Updates Blog"):

    #GitPython -- Repo Location
    repo = Repo(PATH_TO_BLOG_REPO)
    #git add
    repo.git.add(all=True)
    #git commit -m "updates blog"
    repo.index.commit(commit_message)
    #git push
    origin = repo.remote(name="origin")
    origin.push()

    random_text = "sdgsdsdg"

    with open(PATH_TO_BLOG/"index.html","w") as f:
     f.write(random_text)

update_blog()
#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
