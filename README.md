# Blog of the Scientific Python community

An open source, _community_ driven blog for the Scientific Python community.

## Call for Contributions

We appreciate and welcome contributions. Head over to our website for more
information on how you can help make a difference!

- For authors:
  https://blog.scientific-python.org/about/submit/

- To help review content:
  https://blog.scientific-python.org/about/review/

## For blog developers

### Terms

- **summary**: [First paragraph or so](https://gohugo.io/content-management/summaries/) of a blog post.
- **description**: A shorter description of a blog post, used when, e.g., a link to a blog post is shared (many social media sites then render that description in a "card").

### Layouts

- `index.html`: front page
- `posts/list.html`: list of all posts
- `_default/term.html`: posts of a certain #tag

### Partials

Located in `layouts/partials`.

- `posts.html`: list of posts with author and tags
- `posts_with_summary.html`: list of posts, with summary added
- `posts_with_description.html`: lists of posts, with the description added

Lower level partials:

- `post_meta.html`: renders post author, date, and tags
- `post_summary.html`: render post summary
- `post_description.html`: render post description
- `head.html`: header included in each page
