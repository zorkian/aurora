time: 23:50
categories: Tools
publish: yes
title: Next Generation Monitoring

I want to talk a bit about the thoughts in my head about building a
new monitoring system to replace [Nagios](http://nagios.org/). This is
something that I've been thinking about for years and years, but finally
I'm getting enough internal momentum to actually make it happen. First,
let's dive in and look at the existing landscape of monitoring tools (as
I know them).

# Define Your Terms

For the purpose of this blog post, I define "monitoring" loosely as
the act of gathering information about your services *for the express
purpose of alerting you when there's a problem*. The other side of
things, where you are creating pretty graphs to see how your servers
and services are behaving over time is what I will call **performance
trending/analysis**.

In short, Nagios is a monitoring system in that when your host goes
down, it pages you. [Cacti](http://cacti.net/), on the other hand, is a
performance analysis system that lets you keep track of how much RAM you
have free, etc.

Many systems are both, too. But for the sake of this blog post,
I'm mostly focusing on the monitoring side of the equation. If you
want a good recommendation for performance analysis, please see
[OpenTSDB](http://opentsdb.net/).

# Monitoring Today

There are, it seems, two main approaches to monitoring: Nagios and
everything else. Nagios is a fairly simple, relatively easy to use
system that is good at doing a few things and doesn't really have many
bells or whistles and doesn't do much else beyond monitoring your
services.

Everything else seems to be a "Nagios and then some" system, providing
some manner of bells and whistles that the traditional Nagios
installation doesn't provide. That's fine, I don't really mind
functionality, but it really gets away from the thing that I really
need: something to let me know when my shit is broken.

I've spent a while over the years using Nagios, but every so often
I go out and do a survey of the landscape. Sadly, the state of
the art really hasn't changed a lot in ... well, years. You have
[Zabbix](http://zabbix.com/), [OpenNMS](http://opennms.com/),
[Zenoss](http://zenoss.com/), [Hyperic](http://hyperic.com),
[Icinga](http://icinga.org/), [Opsview](http://opsview.com/), and I
might be missing a few...

And, honestly, they're all probably good and accomplish the basic goals,
but what they don't do for me is allow me to quickly and easily, with
a minimum of fuss and nonsense, just monitor my infrastructure. I want
something simple and easy to use. No surprises. A nearly flat learning
curve. A UI that works. A CLI. (Preferrably one that works, too!)

These tools are Enterprise. They've got sales reps, marketing videos,
VM appliances, and some of them are even built to do Windows, Unix,
Solaris, and VMS! It's great, I'm positive they fill needs that people
have and I don't think they're bad products. They're really just not
what I'm looking for. Far too big for my needs.

The only thing that comes close to meeting my needs (forget my wants) is
Nagios Core.

# So, why not Nagios Core?

Because the HTML it generates looks like this:

    <table border=0 width=100% cellspacing=0 cellpadding=0>
    <tr>
    <td align=left valign=top width=33%>
    <TABLE CLASS='infoBox' BORDER=1 CELLSPACING=0 CELLPADDING=0>
    <TR><TD CLASS='infoBox'>
    <DIV CLASS='infoBoxTitle'>Current Network Status</DIV>
    Last Updated: Wed Nov 2 02:26:21 CDT 2011<BR>

Okay, a little more seriously: because it's basically
[crippleware](http://en.wikipedia.org/wiki/Damaged_good). Nagios Core
has been held back to the state it was in nearly a decade ago so
that the company can differentiate its enterprise offering, [Nagios
XI](http://nagios.com/products/nagiosxi).

I'm all for the company making money -- that's great -- but their
decision to leave the open source version of the product back in the
stone age makes it so that I can't really use it to meet my needs. Over
the years I've put hundreds of my own hours into efforts that I really
shouldn't have had to because the system lacks so much that I need:

* A functioning CLI. Doesn't exist. I'm starting to write one, though,
but I really shouldn't have to.

* A UI that is at all modern. The code above demonstrates, but if you
actually interact with Nagios Core, you'll pretty quickly regret it.
It's hard to use and has arcane, confusing commentary. Just try to
schedule a downtime and do it right the first time!

* *Nice to have:* An API that I can integrate with. I would like to build
my own UIs or dashboards, so please give me access to your data in a
reasonable fashion.

* Reasonable behavior -- this is a very personal opinion, but Nagios
does a few things that confuse and consternate me.

To be fair -- Nagios is still, in my opinion, the only system that
allows me to get a monitoring environment up and running in an hour or
two of hacking. A basic setup is easy to accomplish and worth having.
I've used the software for many years now and I still choose it over
everything else, so it's not all bad.

In fact, I recommend it if you're not sure what to use. It is currently
the best system out there for monitoring your infrastructure.

# The Wheel, Again

Of course, I wouldn't have started this blog post if all I wanted to do
was bash Nagios. I really don't intend to be that hard on it. It's a
good system, it's just old and getting older. Today's infrastructures
demand a new, more interoperable monitoring system, and that's what I
want to talk about here.

I'm starting to put together a design for building a monitoring system.
I have a few key points that I am keeping in mind while doing this, but
they're things that I think should resonate with many of you:

* Prioritize simple. I'm not building an Enterprise(TM) solution here,
I'm building for the busy sysadmin who needs to make sure things are
working. Configuration and usage should be damn easy. So should setup.

* Keep it minimal. The core of this project can be defined as "make
software that tells me if my shit is broken". Other functionality can be
added by other software -- which I may or may not write, but won't be
part of the core.

* Integrate with everybody. Provide a functional API that allows people
to write web interfaces, shell scripts, or whatever they want. I will
provide libraries to do just that, too, to make it easier to get
started.

Those are my main three points right now: write something simple, make
it handle the few things it should, and allow other people to bolt
things on if they want. Add a widget to your dashboard that shows the
availability of a service? Great, that's a simple HTTP query that will
return JSON for you to consume. Make a shell script silence alerts?
Easy.

# Implementation Notes

I've spent a lot of time considering my options here, and as
much as I love Perl, these days I'm a Python guy. I'm going
to stick to Python for now. I will probably also use the
[Diesel](https://github.com/jamwt/diesel) library. That provides a lot
of network service and microthread functionality that certainly makes my
life a lot easier.

Another goal (this may not be in v1, I'm not sure) is also to make it
so that the system can run on N machines for redundancy. These days,
there's very little reason to run your monitoring system in one place.
Why not run it on five machines and just have them sort out how to divvy
up the work? This is the way many things are moving, and I see no reason
that monitoring systems can't as well.

In the name of allowing people to do some interesting and complicated
things with the system, I really want to support a full event system.
While this is actually not particularly complicated for a monitoring
system, it has a lot of implications for the rest of the ecosystem.

For example, let's say that we have an event that fires when the
monitoring system has determined that a host is down. Next, we give
people the ability to write plugins for the monitoring system that can
listen to events. Alternately we allow people to subscribe to events
using a pubsub type model of some sort?

Either way, someone could potentially write code that does a database
failover when the system detects that a database has gone down. Or maybe
they have code to automatically restart a process, reboot a server, etc
etc. The list of possibilities is endless and it doesn't compromise the
vision to build a simple system -- you never have to touch it. The power
is there, though.

# Closing Thoughts

Monitoring is a really interesting subject to me. It seems to me that
the state of the art is really pretty woeful when you consider how
important our infrastructure is these days. Most people use a handful
of tools they've cobbled together combined with a few dozen scripts of
their own and nobody ever seems to have a really great handle on it.

It would be good to simplify this and, to some extent, standardize it.
The LAMP stack has nearly been commoditized at this point, giving rise
to services like [Heroku](http://heroku.com/) that allow you to just
write code and not worry about your backend. Those are great and for
those who can use them -- awesome. I envy you a bit.

For the rest of us, though: I think it's high time to improve the state
of things. I welcome your feedback as I (continue to) embark on this
crusade.
