time: 21:08
categories: Tools
publish: no
title: Using Git Flow on GitHub

A while ago while at StumbleUpon we looked at using git flow, an
implementation of the workflow outlined in the post A Successful Git
Branching Model. It looked really interesting and I wanted to try it but
never got around to it.

Lately, I have. Thanks to this very helpful post on the subject, I
have now worked this tool in to my daily open source work. It actually
integrates quite well with GitHub, now that I've gotten down a very
functional workflow.

The first thing that I've done is forced myself to have very good
hygiene in my repository. I don't develop on master and smash everything
together now, I use feature branches for all of my development. Branches
are extremely cheap in git, so there is no real excuse not to separate
things out. It makes for a little more merging down the road, but that
trade-off seems worth it. Particularly when you are talking about
GitHub, which allows you to easily share code and contribute back to
other projects.

Today I decided to contribute back some of the recent Perlbal changes
I had made. For this blog post, we'll look at one of those -- a small
change to add a DEFAULT command. (What the change does exactly doesn't
matter for the purpose of this post.)

## Set Up (Forking, Config, Git Flow)

The code I wanted to change is on GitHub already in the repository
`perlbal/Perlbal`. I clicked the "Fork" button and a few moments later,
GitHub gave me my own copy of the code to do with as I will.

Most of you have probably used git before, so you won't be surprised by
the next step:

    $ git checkout git@github.com:xb95/Perlbal.git
    $ cd Perlbal/
    $ git remote add upstream git@github.com:perlbal/Perlbal.git
    $ git flow init

Executed on my local Linux installation, this command checked out and
set up the code for me to interact with. It landed in a `Perlbal/` folder
under the current working directory and then configured the upstream
remote to point back at the source for Perlbal so I can pull down
changes they make later.

Finally, the Git Flow system is initialized. I recommend you accept all
of the defaults, they are reasonable and work well.

## Write Some Code

Now we're ready to kick some code. From inside of the `Perlbal/` folder,
you can instruct Git Flow that you are about to start developing on
something. The only thing you have to decide right now is what to call
it. For today's example:

    $ git flow feature start default-command

A few moments later, you will have a new branch named
feature/default-command. It does a little other magic in the background
and some sanity checks to make sure you don't have uncommitted changes,
but otherwise, it's mostly just creating a branch for you.

Now do your development and commit, just like normal. (This part
I assume you know how to do and am not going to spend any time
discussing.)

## Submit to GitHub

At this point, you normally would use Git Flow to finish the feature, it
would merge your changes back into the development branch, and you could
share that with other people. In our case, however, since we're using
GitHub and we want to upstream this change, we actually want to leave
the feature branch open.

This is important: do not use git flow feature finish yet! If you do,
I'm not sure how to recover from that situation. (I'd love to know, if
anybody out there has some good advice on the matter.)

What you should actually do is this:

    $ git flow feature publish default-command

This command causes the branch you've created and worked on to be
created on the origin which is, in our case, `xb95/Perlbal.git` on
GitHub. That's exactly what we want. A few moments later, you can see
the branch has been created if you visit the GitHub UI. Great!

Now select your branch on GitHub and click the "Pull Request" button.
You will be taken to a page that allows you to start building your pull
request. Importantly, you should see that it only shows the commits that
you have made to this feature -- nothing else!

Once you click the "Send pull request" button, you will have finished
what is, to me, the cleanest and easiest way to work on code and send it
upstream I have yet found. Bravo!

## Write More Code

...

## Cleanup

...


