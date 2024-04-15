from feedgen.feed import FeedGenerator
from flask import render_template
from datetime import datetime
import markdown
import argparse
import shutil
import json
import pytz
import os
import re

class LibrePPC:

    current_dir = os.path.dirname(__file__)

    def __init__(self, app) -> None:
        self.app = app
        self.data = json.load(open("config.json"))
        self.load_blog_previews()

        if not 'theme' in self.data.keys():
            self.data['theme'] = 'mastodon'

    def render_main(self, is_building: bool=False) -> str:
        data = self.data.copy()
        if is_building:
            data['basepath'] = './'
        else:
            data['basepath'] = '../'

        render = render_template("index.html", **data)
        render = render.replace("&lt;", "<")
        render = render.replace("&gt;", ">")
        return render

    def render_post(self, index: int, postId: str) -> str:
        previous_post = self.get_post_file(index+1)
        next_post = self.get_post_file(index-1)

        text = ""
        blog_dir = self.data['blog_dir']
        postId = postId.replace('.html', '')
        with open(f'{blog_dir}/{postId}.md') as file:
            text = file.read()

        html = markdown.markdown(text, extensions=['fenced_code', 'nl2br', 'tables'])
        data = self.data.copy()
        data['post'] = self.make_post_dict(postId, html)
        data['previous_post'] = previous_post
        data['next_post'] = next_post

        render = render_template("post.html", **data)
        render = render.replace("&lt;", "<")
        render = render.replace("&gt;", ">")
        return render

    def generate_rss(self) -> FeedGenerator:
        fg = FeedGenerator()
        fg.id(self.data['base_url'])
        fg.title(f"{self.data['username']}'s blog")
        fg.author(name=self.data['username'], email='')
        fg.link(href=self.data['base_url'], rel='alternate')
        fg.logo(self.data['avatar'])
        fg.subtitle(self.data['description'])
        fg.link(href=f"{self.data['base_url']}/feed.atom", rel='self')
        fg.language('en')

        blog_dir = self.data['blog_dir']
        files = self.get_post_files()
        files.sort()

        for filename in files:
            postId = filename.replace('.md', '')
            with self.app.app_context():
                path = f'{blog_dir}/{postId}.md'
                with open(path) as file:
                    text = file.read()
                html = markdown.markdown(text, extensions=['fenced_code', 'nl2br', 'tables'])
                post = self.make_post_dict(postId, html)
                fe = fg.add_entry()
                fe.id(f"{self.data['base_url']}/post/{postId}")
                fe.title(post['plain_title'])
                fe.link(href=f"{self.data['base_url']}/post/{postId}.html")
                fe.description(post['plain_description'])
                fe.content(post['text'])

                utc = pytz.timezone('UTC')
                published = datetime.fromtimestamp(os.path.getctime(path))
                published = utc.localize(published)
                fe.published(published)

                updated = datetime.fromtimestamp(os.path.getmtime(path))
                updated = utc.localize(updated)
                fe.updated(updated)

        return fg

    def make_post_dict(self, postId: str, html: str) -> dict:
        cleaner = re.compile('<.*?>')
        lines = html.split('\n')
        title = lines[0]
        description = '\n'.join(lines[:3])
        return {
            'id' : postId.replace('.md', ''),
            'title' : title,
            'description' : description,
            'plain_title' : re.sub(cleaner, '', title),
            'plain_description' : re.sub(cleaner, '', description),
            'text' : html
        }

    def load_blog_previews(self) -> None:
        blog_dir = self.data['blog_dir']
        self.data['blog'] = list()
        for filename in self.get_post_files():
            with open(f"{blog_dir}/{filename}", 'r', encoding="utf-8") as file:
                text = file.read()
                html = markdown.markdown(
                    text, 
                    extensions=['fenced_code', 'nl2br', 'tables']
                )
                self.data['blog'].append(
                    self.make_post_dict(filename, html)
                )

    def get_post_files(self) -> list:
        files = os.listdir(self.data['blog_dir'])
        files.sort()
        files.reverse()
        return files

    def get_post_file(self, index: int) -> str | None:
        if index < 0: return None
        files = self.get_post_files()
        if index >= len(files): return None
        return self.get_post_files()[index].removesuffix('.md')

    def find_post_file(self, postId: str) -> int:
        for index, file in enumerate(self.get_post_files()):
            if file.removesuffix('.md') == postId:
                return index
        return -1

    def parse_args(self):
        parser = argparse.ArgumentParser(
            prog='LibrePPC',
            description='A simple profile page creator',
        )
        parser.add_argument('-b', '--build', action='store_true')
        parser.add_argument('-s', '--serve', action='store_true')
        args = parser.parse_args()
        return args

    def build(self) -> None:
        print("Building the site...")
        print("Make build dir...")
        os.makedirs("build/static", exist_ok=True)
        os.makedirs("build/post", exist_ok=True)

        with open("build/index.html", "w") as file:
            print("Render index.html...")
            with self.app.app_context():
                file.write(self.render_main(True))

        for index, postname in enumerate(self.get_post_files()):
            print(f"Render {postname}...")
            postId = postname.replace('.md', '')
            with open(f"build/post/{postId}.html", "w") as file:
                with self.app.app_context():
                    file.write(self.render_post(index, postId))

        print("Generate rss...")
        fg = self.generate_rss()
        fg.atom_file("build/static/feed.atom")

        print("Copy styles...")
        theme = self.data['theme']
        shutil.copy(f"{self.current_dir}/static/{theme}.css", f"build/static/{theme}.css")
        print("Complete building!")
