from git import Repo
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from openai import OpenAI
import os
import requests
import shutil

api_key = os.environ["OPENAI_API_KEY"]

print(os.environ)
client = OpenAI(api_key=api_key)

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

    #random_text = "sdg345345sdsdg"

    #with open(PATH_TO_BLOG/"index.html","w") as f:
     #f.write(random_text)


def create_new_blog(title,content,cover_image):
    cover_image = Path(cover_image)

    files = len(list(PATH_TO_CONTENT.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_content = PATH_TO_CONTENT/new_title

    shutil.copy(cover_image,PATH_TO_CONTENT)

    if not os.path.exists(path_to_new_content):
        #Write a new HTML File
        with open(path_to_new_content,"w") as f:
            f.write('<!DOCTYPE HTML>\n')
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title> {title} </title>\n")
            f.write("<head>\n")

            #OPENAI---> Completion GPT ---> "hello\nblog post\n"
            f.write("<body>\n")
            f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br />\n")
            f.write(f"<h1> {title} </h1>\n")
            f.write(content.replace("\n", "<br />\n"))
            f.write("</body>\n")
            f.write("</html>\n")
            print("Blog Created")
            return path_to_new_content

    else:
        raise FileExistsError("File already exists, please check again your name! Aborting!")

with open(PATH_TO_BLOG/"index.html") as index:
    soup = Soup(index.read(), features="html.parser")

   #Checking duplicate links

   #Write blog post link ---> index.html

def check_for_duplicate_links(path_to_new_content,links):
    urls = [str(link.get("href")) for link in links] # [1.html,2.html,3.html]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls


def write_to_index(path_to_blog, path_to_new_content):
    with open(path_to_blog / "index.html") as index:
        soup = Soup(index.read())

    links = soup.find_all("a")
    last_link = links[-1]

    if check_for_duplicate_links(path_to_new_content, links):
        raise ValueError("Link does already exist!")

    link_to_new_blog = soup.new_tag("a", href=Path(*path_to_new_content.parts[-2:]))
    link_to_new_blog.string = path_to_new_content.name.split(".")[0]
    last_link.insert_after(link_to_new_blog)

    with open(path_to_blog / "index.html", "w") as f:
        f.write(str(soup.prettify(formatter='html')))
 #OPENAI UTILS
def create_prompt(title):
    prompt = """
    Biography:
    My name is Berk and im a producer/DJ.
    Blog
    Title: {}
    tags : music production, DJing, AI, Machine learning, tech, music
    Summary: I talk about what the future of AI could hold for music production and DJing
    Full Text: """.format(title)

    return prompt

def get_blog_from_openai(blog_title):
    blog_title= "The future of Music and AI"
    response = client.completions.create(
                                    model='text-davinci-003',
                                    prompt=create_prompt(blog_title),
                                    max_tokens=1000,
                                    temperature=0.7)
    return response.choices[0].text



def dalle2_prompt(title):
    prompt = f"Pixel digital art showing: {title}"
    return prompt
    image_prompt = dalle2_prompt(title)

    response =client.images.generate(
    model="dall-e-3",
    prompt=image_prompt,
    size="1024x1024",
    quality="standart",
    n=1
)


def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream=True)

    if image_res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("Error downloading image!")
    return image_res.status_code, file_name


def get_cover_image(title, save_path):
    response = client.images.create(
        prompt=dalle2_prompt(title),
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    status_code, file_name = save_image(image_url, save_path)
    return status_code, file_name



update_blog()
#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
