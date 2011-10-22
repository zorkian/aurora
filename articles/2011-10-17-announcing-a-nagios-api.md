time: 14:00
categories: Operations, Nagios
title: Announcing: An easy to use Nagios API

Over the years I've been doing systems administration, I've spent
a lot of time (really, quite a lot) writing tools that pull data from
Nagios or try to make it do what I want. Command line apps to schedule
downtimes, IRC bots that parrot alerts, email/SMS gateways, status web
pages, etc etc.

Every time I take on a project like this, I usually go through three
phases: first: lamenting that I don't have the code from the last time
I did it, second: weeping over the atrocious mid-90s look, feel, and
implementation of Nagios, and finally: actually sitting down and doing
whatever it is I need to do.

It's time to cut out the first two steps. Enter nagios-api: a
REST-like, JSON API for Nagios. This allows you to quickly and easily
build command line tools, web interfaces, and other code that interfaces
with Nagios - without having to actually interface with Nagios. Leave
that to me.

If you want to go check it out now, the code is available here:

[https://github.com/xb95/nagios-api](https://github.com/xb95/nagios-api)

Right now it's fairly simple and only lets you do a few things: get
the state (enough to implement a status page), schedule/cancel downtimes
(90% of what I have to do from the command line anyway), and tail the
log (the final 10% of what I'm typically up to).

This is implemented on top of the [Diesel
framework](https://github.com/jamwt/diesel) by Jamie Turner et al.
Since coming to Bump and discovering Diesel, implementing this kind of
network/loop driven system in Python has gone from 'annoying' to 'so
easy I can do it in my sleep'. Seriously good stuff.

Future plans: add a lot more functionality, of course. There are many
verbs in the Nagios language and I want to be able to support most or
all of them. I'm sure much of that will come as I need to implement
them, and of course, from contributions by other people.

And finally, of course, I want to replace Nagios with an entirely
new system. I've been doing some work on that on the side, but
I'll talk about that another day. Ideally, whatever interface
the nagios-api project settles on will be translatable to the new
replacement monitoring system I'm working on. That way any tools
written against this API will just continue to work against whatever the
other system is when it's done.

Feedback is, as always, very welcome.
