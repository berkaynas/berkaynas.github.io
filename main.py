from openai import OpenAI
import os
import shutil
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

    random_text = "sdg345345sdsdg"

    with open(PATH_TO_BLOG/"index.html","w") as f:
     f.write(random_text)


def create_new_blog(title,content,cover_image):
    cover_image = Path(cover_image)

    files = len(list(PATH_TO_CONTENT.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_content = PATH_TO_CONTENT/new_title

    shutil.copy(cover_image,PATH_TO_CONTENT)

    if not os.path.exists(path_to_new_content):
        #Write a new HTML File
        with open(path_to_new_content,"w") as f:
            f.write('<!DOCTYPE HTML>/n')

    else:
        raise FileExistsError("File already exists, please check again your name! Aborting!")


update_blog()
#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
