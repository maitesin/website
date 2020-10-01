![Screenshot of the website](https://github.com/maitesin/website/raw/master/post/static/img/website.png)
# Structure of this Powerfull website

The structure of the website is quite simple and relies a lot on the backend to do the hard work.

## Backend

The backend is build using **Django** and **SQLite**. Since the current usage of the blog can be handled by **SQLite** without a problem I have not bothered in changing it. Thanks to **Django**'s integration with the different database backends, I can change it to **PostgreSQL** changing a couple of lines if required.

The database contains four tables: **posts**, **categories**, **tags** and **post-tags**.

 * **posts** contains the information about each post and its content (written in **Markdown**).
 * **categories** contains the name of each category.
 * **tags** contains the name of each tag.
 * **post-tags** contains the relation between all posts and their associated tags.

The template engine for this website is **Jinja2** and it allows to create incredible and extendable themes and sites with a minimal boilerplate.

## Frontend

The frontend is build using **HTML5** and **CSS**. I avoided the use of **JavaScript** as much as I could for several reasons.

 * **Slow website on mobile devices**. Since more than 70% of the people coming to my previous website where coming from a mobile device, I wanted them to have a great experience (without sacrificing the experience of the ones coming from a computer).
 * Since I do not know **Javascript**, I wanted to avoid it as much as possible to not have to maintain code that I do not understand how it works.

The theme used for the website is inspired on a **Jekyll** theme called [Hyde](http://hyde.getpoole.com/).
