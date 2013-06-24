title: Handling an Outage
time: 15:00
categories: Operations
publish: yes

Last night the colocation provider I use for Dreamwidth,
[ServerBeach](http://www.serverbeach.com/), was down for nearly four
hours from 0000 CST to about 0330 CST. This blog post is a customer-side
postmortem about the company's handling of this outage.

# Outage Notification

I generally classify outages as trivial (seconds to, say, 2-3 minutes),
minor (3-10 minutes), or major (10+ minutes). I will refer to these in
the rest of this post as the handling does change -- to help balance
resolution time with customer comfort, mostly. Of course, it's worth
mentioning that one size does not fit all, and what I find as best
practices might be somewhat different if you have an SLA or if you are
in another industry.

Outage handling starts when you are notified of a problem. This usually
happens at the bottom somewhere -- a customer service rep, a customer,
or your monitoring solution will alert someone to the problem. There are
pretty good odds that this is someone who is external to the company or
someone who has nothing to do with your technical operations.

For Dreamwidth, I never notice an outage first. It's always a user or
one of our volunteers or other staff who will find out that we're down
before I ever do. Even Nagios isn't as fast as a human who is actively
using the site.

In some situations, too, your monitoring system won't work. In last
night's outage, the problem was that the entire data center went off
the air. Our monitoring system, being purely internal, had no way of
alerting us. (We have in the past had external monitoring, but I found
Pingdom unreliable and other options proved too expensive. Maybe there
are better options now?) Even if your monitoring system is working fine,
some outages just aren't noticed by it. We've all had situations where
something isn't correctly monitored or is giving false positives!

For these reasons, it is important to provide a method for users
(internal and external) to advise of an outage. Dreamwidth has
a Twitter account that end users can talk to, and our mid- to
senior-level volunteers and staff all have phone numbers for our systems
administrators and know that they can call us 24/7 to advise of an
outage.

That's how I found out we were down last night: one of our employees
called me and advised me within minutes of the site being down. By that
point of course, the outage was considered a minor outage since it had
been more than a few minutes.

We have trained our users that, during downtimes, our Twitter account
is the place to go for updates. We put up a message advising them that
we were down and we were investigating and had no ETA. This took less
than a minute of our time and the effects were immediate -- users knew
we were aware, that we were on the problem, and they could relax. They
responded by being pleasant and thankful and went off to do other things
on the Internet instead of continually refreshing the site and getting
more and more angry.

The effect this small bit of information can have on your customers
is worth overstating: it is the difference between a bad experience
where your customer debates finding another provider and one where the
customer feels confidence in you and that you are on top of the problem.
Internally, it doesn't matter what's going on, **let your customers know
you're aware**. Be calm and confident, but communicate!

Now the caveat I mentioned about outage sizes: I first check to see if
the problem is something I can resolve in a minute or less. I.e., if
it's a trivial outage, it's better to get the site up immediately and
then post a notification that it was down. However, if I realize the
outage is at least a minor outage, then it's vital to notify people that
there is a problem.

This gives us the first two pieces of a solid outage handling process:

1. Have a way for users/staff to notify you of downtimes
2. Acknowledge the downtime immediately if it's minor (3+ minutes)

ServerBeach failed on both fronts. I had no way of notifying them of
a downtime except calling their tech support line, which I tried to
do, but their phone lines were failing (not picking up at all) and I
couldn't get through. I ultimately was able to reach PEER1 (the parent
company) but they couldn't really help me.

I could have assumed they knew about the outage, but it would have only
been an assumption -- and it's not a good business practice for me to
just assume that an outage is being fixed! -- so I had to keep trying
for 20 minutes to reach somebody. That was a huge waste of my time, and
all because they didn't provide notification that they were aware of a
problem.

The first notification I can find was nearly an **hour** after the
downtime started. Completely unacceptable. The entire data center was
offline -- thousands of customers -- and they took an hour to let us
know.

# Ongoing Outages

In this case, the outage was a long one. Nearly four hours of
downtime. Outages of that caliber start to get very unnerving for the
users, because now you've graduated from "annoyance" to "potentially
catastrophic". Why is it taking four hours to come back up? Was there a
fire or flood? Meteor strike? Did the government come in and seize the
building because of Mega?

At this point someone needs to be on point for communication. It should
be someone who can, every so often (I find 30-60 minutes is frequent
enough) post and let users know that you're still aware of the problem
and, yes, you're still working on it. Even if, like in Dreamwidth's
case, we had no information and were just crossing our fingers that
ServerBeach would fix things sometime soon. Your very presence is
comforting to your users, though, and lets them know that they're
important. That feeling is extremely valuable to have -- if you don't
encourage goodwill, the lack thereof will be bad for your business.

In this outage, I got most of my information from other customers
on Twitter. I followed the #peer1 and #serverbeach hashtag and was
collecting information from other people who were customers. **This
is stupid and bad!** I shouldn't have to rely on other *customers* to
give me information about what's going on. It makes the company look
incompetent. Seriously.

It was **two hours** after the outage started before there was official
information about the problem. Unfortunately, this information was in
a place I never looked -- because the person I did get on the phone
earlier told me to look at the PEER1 network status forums, which
are separate from the ServerBeach status forums. (Even though my
management portal and branding is all PEER1, but because this data
center was acquired via ServerBeach, they have a different area for
status updates.) This is also ridiculous.

The important parts of the process here:

1. Have a predictable place to find status updates
2. Keep users informed of status and ETA (if available)

The first point cannot be stressed enough. Users need to know where to
go to find things out. Staff needs to know, too, so they can give the
right information to users. Giving a customer wrong information is worse
than no information. I spent the whole night thinking that ServerBeach
never posted anything -- which was wrong, they had; even if it was way
too slow.

In retrospect, now that I'm reading the outage thread on ServerBeach's
side, once they got the ball rolling they were following a good flow
for updating. They posted every 30-45 minutes and updated with as much
information as they had, which was great. Kudos to them for having a
good flow once things got going.

# Outage Closing

The end of an outage should be handled with the same ideas repeated. Let
people know that you're back up, then let them know what happened in as
much detail as you have and advise if you will be giving a postmortem.
Commit to followthrough so that people know what to expect.

1. Post an end-of-outage notification, advise if there will be a
postmortem
2. If providing a postmortem later, make it predictably
located and linked

ServerBeach did well here (excepting of course that I didn't know where
to find this information): they posted an update at the end, said what
happened, why it caused an outage, and what they would be doing to fix
it. This is a good response -- although since they mentioned a number of
things that were unexplained or unclear, it will need to be followed up
with a response when those things are clarified.

# Communication

It is my opinion that service providers should overcommunicate. You will
almost never fail by telling the users exactly what is going on, and you
will probably find that people are remarkably forgiving if they feel
included in the process. Because of this outage, Dreamwidth was down
for nearly four hours, but our users were polite and **thankful**. Just
because we let them know what was going on.

ServerBeach's outage was bad, but everything breaks sometime. The
real fault here is their handling of the notification process and how
disconnected they were from the users. This is inexcusable in a service
provider, particularly these days when hosting providers are a dime
a dozen and competition is not so much about price. For that matter,
I'd pay a premium to ensure that I am hosted with a service that can
actually communicate when something is going on.

Now, can someone tell ServerBeach to post a postmortem about their
handling of the communication during this outage? :-)

End of rant.

# Update

I just received a call from Dax Moreno, Director of Customer Experience.
He reached out to talk about the outage. I was able to convey most of
this content to him in a less ranty, more constructive way. (Or I hope
it came across that way!)

Major points to ServerBeach/PEER1 for reaching out like that. It is
never good to have an outage, and the handling at the beginning leaves
much to be desired (which Dax agreed with), but having a personal
contact from someone nets a huge gain in goodwill from the customer
and makes them feel more in control of what is, by its nature, an
uncontrollable experience.

Good on 'em for that, then.
