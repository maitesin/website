+++
title = "New website using Python, HTML5 and CSS"
date = "2015-06-24T13:50:46+02:00"
author = "Oscar Forner"
tags = [""]
categories = ["Development"]
+++

### Table of Contents
[TOC]

### Introduction
My new website has reached the point where it has all the minimum features required to work. In this post, I talk about the reasons for creating it and what the used design and technology are. The code of my website can be found in my [GitHub](https://github.com/maitesin/website).

### Why create a website from scratch?

My first blog was hosted in [blogspot](http://maitesin.blogspot.co.uk), but it was too limiting in what can be done in the blog and the theming.

The next iteration was in [GitHub](http://maitesin.github.io/). In this case, I had more freedom regarding the hosting and theming, but it was done using [Jekyll](https://jekyllrb.com/) and **I have no idea about Ruby**. This was a problem when I wanted to improve how the site was behaving. Regarding the themes, if I wanted to do some changes, I would have to learn its framework.

Finally, the current iteration has been done **from scratch and self hosted**. But why? **The answer is simple, freedom**. I am able to change any part of it, such as the backend or the CSS theme or even host videos.

### Why use Django?

The first idea was to use something similar to [Jekyll](https://jekyllrb.com/) to generate static websites, but written in a language I already knew. With that criteria I found [Pelican](https://blog.getpelican.com/), a static site generator written in **Python**. The only drawback of **Pelican** is that the community is smaller than the one in **Jekyll** and that means that it is harder to find help, tutorials and documentation online.

After playing with **Pelican**, and other static site generators, and not finding anything that  met my requirements, **I decided to go one step further**. So, I decided to find a python based **web framework**. The two main contenders are [Django](https://www.djangoproject.com/) and [Flask](http://flask.pocoo.org/).

**Flask** is an awesome and lightweight **web framework** with a really small learning curve, great documentation and community. Also, **Django** is an incredible **web framework** with batteries included. **Django** has one of the best documentation I have seen in any project and the community is really engaging. **Flask** is also more *pythonistic* than **Django**.

The reasons why I picked **Django** over **Flask** were basically three:

 * **Django** has a bigger community, more people developing it. That means that it has more probablilities to last longer than **Flask**. I do not think that **Flask** is going to go away anytime soon. To build a *big* project such as my personal website, however, I prefer to base it on a project that will last for a long time.
 * **Django**'s documentation is incredible. **Flask** has a really complete and helpful documentation, but I find **Django**'s documentation easier to work with.
 * **Django**'s support for **SQLite** out of the box and its integration with **Django**'s models.

### Structure of the website

The structure of the website is quite simple and relies a lot on the backend to do the hard work.

#### Backend

The backend is build using **Django** and **SQLite**. Since the current usage of the blog can be handled by **SQLite** without a problem I have not bothered in changing it. Thanks to **Django**'s integration with the different database backends, I can change it to **PostgreSQL** changing a couple of lines if required.

The database contains four tables: **posts**, **categories**, **tags** and **post-tags**.

 * **posts** contains the information about each post and its content (written in **Markdown**).
 * **categories** contains the name of each category.
 * **tags** contains the name of each tag.
 * **post-tags** contains the relation between all posts and their associated tags.

The template engine for the website is **Jinja2** and it allows to create incredible and extendable themes and sites with a minimal boilerplate.

#### Frontend

The frontend is build using **HTML5** and **CSS**. I avoided the use of **JavaScript** as much as I could for several reasons.

 * **Slow website on mobile devices**. Since more than 70% of the people coming to my previous website where coming from a mobile device, I wanted them to have a great experience (without sacrificing the experience of the ones coming from a computer).
 * Since I do not know **Javascript**, I wanted to avoid it as much as possible to not have to maintain code that I do not understand how it works.

The theme used for the website is inspired on a **Jekyll** theme called [Hyde](http://hyde.getpoole.com/).

### Final thoughts

I am happy with the current state of the website, although I will keep improving it and adding new features as I need them - since that was the whole purpose of building my own website.

If you are thinking about creating a blog or a personal website please do not jump to create your own from scratch as I did. I do recommend to use first something such as **blogspot** to start with.

Afterwards, if you find the platform too limiting, then I would suggest to go to a **static generated website** or some other similar option.

Finally, if you already tried all of these and still feels like you are missing something, then I would say it is time to think about creating your own website.
