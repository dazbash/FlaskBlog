from flask import render_template, request
from flask_sqlalchemy import get_debug_queries

from . import blog
from .models import Post, Category
from .forms import SearchForm
from sqlalchemy import or_

@blog.route('/')
def index():
    search_form = SearchForm()
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts, search_form=search_form)


@blog.route('/<string:slug>')
def single_post(slug):
    search_form = SearchForm()
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('blog/single_post.html', post=post, search_form=search_form)


@blog.route('/search')
def search_blog():
    search_form = SearchForm()
    search_query = request.args.get('q', '')
    title_cond = Post.title.ilike('{}%'.format(search_query))
    summary_cond = Post.summary.ilike('{}'.format(search_query))
    content_cond = Post.content.ilike('{}'.format(search_query))
    found_posts = Post.query.filter(or_(title_cond, summary_cond, content_cond )).all()
    print(found_posts)
    print(search_query)
    print(get_debug_queries())
    return render_template('blog/index.html', posts=found_posts, search_form=search_form)


@blog.route('/category/<string:slug>')
def single_category(slug):
    search_form = SearchForm()
    category = Category.query.fiter(Category.slug==slug).first_or_404()
    return render_template('blog/index.html', posts=category.posts, search_form=search_form)





