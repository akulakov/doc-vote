# DocVote
DocVote is a documentation system with voting and comments.

DocVote is a documentation system that allows voting and comments to be applied to each node
(usually a paragraph or a snippet of code). The system stores each node as a database entry
with votes and comments attached.

The nodes are entered in markdown format.

## Rationale

Voting is intended to alert maintainers to the "weaker" spots of documentation, in terms of
both style or accuracy. Maintainers of documentation, expecially of Open Source projects,
often have very limited time to spend on documentation and it is often low on their list of
priorities. As a result, useful projects sometimes don't find their audience because the docs
are not complete, up to date, or user friendly enough.

DocVote is intended to crowd source review of documentation and help pinpoint the parts of
documentation that need urgent attention and are the main "pain points" for potential or
existing users.

It will be much easier for maintainers to justify spending time on documentation improvement
as the scope of needed changes can be easily defined and improvement for the given effort can
be quantified (for example, updating 10 paragraphs in various parts of the documentation that
have the lowest scores).

## Installation and Setup

DocVote is a Django app that works with Django 2.0.3+ and can be installed as any other
Django app. You will need to self-host it. Refer to your hosting service docs on how to set
up Django, database and add an app.

## Workflow for users of documentation

Users will see a side pane that will show score, vote buttons, and a form for leaving
comments for each node (paragraph). Low scores will indicate that respective feature of the
project will need extra effort from the user to understand and use; the user may plan ahead
to use alternative sources of support if the feature in question is important to him or her;
user may also review comments attached to the node to see if other users provided hints on
the use of the feature.

User will vote for the nodes he or she reads. The down-votes are especially important because
they are the call to action to improve respective node. Up-votes may be used to balance out
unwarranted down-votes or to highlight especially useful nodes.

## Workflow for the maintainers

A maintainer will review node scores and will pay attention to low-scored nodes, looking at
the comments for such nodes for explanation of what the users find lacking in the node. Once
a maintainer updates a node to fix all of the related issues, he or she may reset the score.
Users may continue adding new scores that will reflect on the new content of the node. The
comments are kept for historical purpose.

## Actions available to maintainers

 - insert new node (after current)
 - delete node
 - move node down or up
 - reset node scores

## What size of projects can DocVote be used for?

Currently DocVote is meant for small to medium sized projects because there's no automated
support for things like menus and tags.

## Screenshots

!(https://github.com/akulakov/doc-vote/raw/master/screenshots/Screen%20Shot%202018-02-28%20at%2011.31.56%20AM.png)

!(https://github.com/akulakov/doc-vote/raw/master/screenshots/Screen%20Shot%202018-02-28%20at%2011.32.27%20AM.png)
