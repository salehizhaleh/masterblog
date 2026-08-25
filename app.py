from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_posts():
    with open ("posts.json", "r") as file:
        return json.load(file)

def fetch_post_by_id(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            return post

    return None


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        with open("posts.json", "r") as file:
            blog_posts = json.load(file)

        new_id = max([post["id"] for post in blog_posts], default=0) + 1
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)

        with open("posts.json", "w") as file:
            json.dump(blog_posts, file, indent=4)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open("posts.json", "r") as file:
        blog_posts = json.load(file)

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    with open("posts.json", "w") as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_posts()

        for post in blog_posts:
            if post["id"] == post_id:
                post["author"] = author
                post["title"] = title
                post["content"] = content
                break

        with open("posts.json", "w") as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)