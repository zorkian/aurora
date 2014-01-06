title: The Root of All Evil
time: 18:14
categories: Operations
publish: no

It's a little pretentious to make a post in this blog and name it
"The Root of All Evil". But that's what I'm doing, that's what you're
reading. May I not regret this.

Today's subject is something that is, in fact, the root of everything
that breaks, fails, or otherwise crumbles at three in the goddamn
morning when you were just about to get to the good part of that
dream, but no, your phone lights up like a demonic Christmas tree with
an unholy tune (because you keep forgetting to change it back from
that Bieber song your coworker changed it to when you left your phone
unlocked and unattended and it started paging you and she had to deal
with it).

Ring ring. PagerDuty is happy to let you know that Nagios alert "site:
is this shit working" is DOWN. Would you like to Acknowledge, Resolve,
or Spread The Pain To The Secondary?

You ack the alert and grab your laptop. Step 1: Check if shit is
working. Well, it's not. Getting paged in the middle of the dream right
before that really hot person takes off their shirt is really damned
annoying, but at least it's not a false page. Something is actually
broken and you, as the SRE On-Call, are now responsible for figuring out
why.

Let's take a step back.

In the years I've been doing this job, there's one rule that seems to
hold true no matter what: if I get paged and something is actually
wrong, then **something has changed**.

This is an overly simplistic statement of the probably very obvious,
but the day I really realized this it felt like a light burst from a
cloud and I was thoroughly englightened (and roasted in ultraviolet
radiation). Once I had this realization, I could start tuning my
monitoring and alerting to highlight things that change: in essence, to
find likely problem areas quicker and more accurately than I was before.

The primary source of change is humans going about their daily lives,
and this is particularly true in the world of startups. Until you get
into a world where you have fancy Change Management Processes and People
Who Make Sure That Change Management Processes Are Being Followed, you
instead live in this lovely world I like to call "hello I seem to have
found myself on top of a raging bull that is trying to throw me off and
I'm not sure how, is this the right number to call in the 4.3 seconds
before I'm thrown unceremoniously to my face in front of millions of
users?"

Being an SRE at a startup is like riding the bull. Sometimes you win,
sometimes you lose, but it's at least guaranteed to be one hell of a
time.

# Changes

There are many things that change in the course of a day, and one of the
most useful skills you can have is understanding how to quickly rank the
likely sources of change and figure out which one is responsible for
your current hair-pulling event.

A concrete example: my company pushes code out to the site pretty
regularly, but it's generally always in the afternoon, Monday through
Friday. This is a *major change event* and, statistically speaking,
deployments are the most likely causes of outages (this is based on
experience, I don't actually record the data, so it's as accurate
as most statistic). Anyway, things are fine, your site is working,
everybody is happy; then someone dares to do their job and write some
code and then has the temerity to deploy that shit! To users!

Things break. Nearly inevitably, as the size of a codebase grows, the
chances of something breaking during a deployment approach 100%. So,
back to changes: if I get paged at 2PM on a Thursday, the very first
thing I will do, before anything else, is ask "did someone just push the
site?"

The answer is almost always "yeah, did something break?"

Engineers. Can't live without 'em.

(PS, I love you all even if sometimes I want to kick your puppies.)

# More Changes

A relatively unsorted list of things that comes to mind when I'm
reaching for the list of things that might have changed:

* Someone restarted things. Or did something. In production. Because
we're SREs, we do that and we break things. (It turns out we're
engineers, too.)

* The Internet is shitty. (Packet loss or other network troubles.)

* Traffic is at a new high in some metric.

* A database lost a disk and the RAID is now degraded.

* Load balancer auto-negotiated to 100Mbps and half-duplex.

* Puppet/Chef ran. Or that one instance of cfengine that still lives on
decided to do something.

* Someone decided that we haven't had a backup in a while, so they
kicked off a full database dump during peak hours.

* Disk filled up somewhere.

* Network filled up somewhere (gigabit is really quite slow). Or you've
hit a *packet per second limit* even though your bits per second are
totally fine. (Turns out most systems can only do about 100k pps.)

* Someone is attacking your service: (D)DoS, slowloris, etc.

* Your CEO is doing a press conference right now and (again) forgot to
tell the on-call to expect a spike.

There's a million more. Really, it's quite hard to make a list like
this. I think that most of us just do it for years until we've bashed
our heads against the wall enough times that our brains have taken on
the consistency of porridge and our forehead resembles cardboard after a
night out in the rain.

Okay, that's gross, but it makes the point: learning through suffering
is alive and well in the world of SRE. Nobody can write you a list, and,
even worse: every service is different. Yeah, there are some common
failure patterns, but every time you move to a new service you'll have
to learn the new and interesting ways that it fails, too.

# TL;DR

Stuff breaks when things change. Most changes come from humans or
something in particular failing. Find what changed or broke and you'll
probably find what's wrong and can get back to the business of sleeping.
