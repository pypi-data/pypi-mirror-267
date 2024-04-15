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

    def table_to_json(self, text: str) -> dict:
        lines = text.split('\n')
        ret, keys = list(), list()
        for index, line in enumerate(lines):
            if index == 0:
                keys = [_index.strip() for _index in line.split('|')]
            elif index == 1: continue
            else:
                ret.append({keys[_index]:value.strip() for _index, value in enumerate(line.split('|')) if  _index > 0 and _index < len(keys) - 1})
        return ret[0]

    def parse_post_metadata(self, postId: str) -> dict:
        file = self.get_post_file(
            self.find_post_file_id(postId.removesuffix('.md'))
        )
        blog_dir = self.data['blog_dir']
        with open(f'{blog_dir}/{file}.md', 'r') as fl:
            table = '\n'.join(fl.read().split('\n')[:3])
            return self.table_to_json(table)

    def remove_post_metadata(self, text: str) -> str:
        return '\n'.join(text.split('\n')[3:])

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

    def find_post_file_id(self, postId: str) -> int:
        for index, file in enumerate(self.get_post_files()):
            if file.removesuffix('.md') == postId:
                return index
        return -1

    def make_post_dict(self, postId: str, html: str) -> dict:
        cleaner = re.compile('<.*?>')
        data = self.parse_post_metadata(postId)
        return {
            **data,
            'id' : postId.removesuffix('.md'),
            'plain_title' : re.sub(cleaner, '', data['title']),
            'plain_description' : re.sub(cleaner, '', data['description']),
            'text' : html
        }

    def render_template(self, name: str, data: dict) -> str:
        render = render_template(name, **data)
        render = render.replace("&lt;", "<")
        render = render.replace("&gt;", ">")
        render = render.replace("&#34;", '"')
        render = render.replace("amp;", "")
        render = render.replace("amp;", "")
        return render

    def render_main(self, is_building: bool=False) -> str:
        data = self.data.copy()
        if is_building:
            data['basepath'] = './'
        else:
            data['basepath'] = '../'

        return self.render_template('index.html', data)

    def render_post(self, index: int, postId: str) -> str:
        previous_post = self.get_post_file(index+1)
        next_post = self.get_post_file(index-1)

        text = ""
        blog_dir = self.data['blog_dir']
        postId = postId.replace('.html', '')
        with open(f'{blog_dir}/{postId}.md') as file:
            text = file.read()

        text = self.remove_post_metadata(text)
        html = markdown.markdown(text, extensions=['fenced_code', 'nl2br', 'tables', 'codehilite'])
        data = self.data.copy()
        data['post'] = self.make_post_dict(postId, html)
        data['previous_post'] = previous_post
        data['next_post'] = next_post

        return self.render_template('post.html', data)

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
                html = markdown.markdown(text, extensions=['fenced_code', 'nl2br', 'tables', 'codehilite'])
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

    def load_blog_previews(self) -> None:
        blog_dir = self.data['blog_dir']
        self.data['blog'] = list()
        for filename in self.get_post_files():
            with open(f"{blog_dir}/{filename}", 'r', encoding="utf-8") as file:
                text = file.read()
                html = markdown.markdown(
                    text, 
                    extensions=['fenced_code', 'nl2br', 'tables', 'codehilite']
                )
                self.data['blog'].append(
                    self.make_post_dict(filename, html)
                )

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
