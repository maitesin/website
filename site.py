from flask import Flask, render_template

app = Flask("forner")

@app.route("/")
def index():
    return render_template('blog.html')

@app.route("/projects")
def projects():
    return render_template('projects.html')

@app.route("/resume")
def blog():
    return render_template('resume.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run("0.0.0.0")
