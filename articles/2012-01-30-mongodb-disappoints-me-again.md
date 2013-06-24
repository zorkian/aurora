title: MongoDB disappoints me again
time: 10:35
categories: MongoDB
publish: yes

At my employer we use [MongoDB](http://www.mongodb.org/) for one of our
core databases. I have never worked with it before I got here, but now
I'm responsible for maintaining it so I have spent some decent amount of
time banging on it and learning about it.

I'm impressed with the ease of use, configuration, and general
maintenance. It seems to do things in a reasonably sane fashion most
of the time. I am happy to recommend it to people with small to medium
infrastructures who want to focus more on the application development
and worry less about the administration overhead on the backend. For the
most part, MongoDB just works.

There are a few things that make me less happy with the system, though,
and lead me to recommend against using it for highly critical systems or
once you pass a certain size. That brings us to today.

Last week, there was an odd issue where we restarted one of our MongoDB
instances and when it came back up, some of the journal files were owned
by root. This caused the database to stop processing the journal and it
started falling behind. It also couldn't download further journal data
from the master, so it was effectively doing no work.

Our monitoring didn't catch it (it wasn't yet replicating so it
wasn't showing any replication lag), so it went a while without being
noticed. When I finally did realize it was broken, I fixed the ownership
of the files and restarted it. A while later, I checked back on the
status and saw that the replication state was `RECOVERING`. Great! I
went about my business content in the knowledge that it was now
recovering from the problem and would be back up to speed at some point.

That was Thursday. Today, the machine has still not recovered and seems
to be falling farther and farther behind. That's odd. We aren't doing so
many writes on this cluster that I would expect it to be that overloaded
-- and the other replica members aren't having these issues. In fact,
as I started to dig into it, I realized that it was doing *no useful
work at all* -- not progressing even a tiny bit.

I ended up in the log files and found:

    Mon Jan 30 11:59:03 [replica set sync] replSet error RS102 too stale to catch up, at least from blahblahblah:27018
    Mon Jan 30 11:59:03 [replica set sync] replSet our last optime : Jan 21 11:00:02 4f1aef12:d4
    Mon Jan 30 11:59:03 [replica set sync] replSet oldest at blahblahblah:27018 : Jan 29 06:05:59 4f253627:90
    Mon Jan 30 11:59:03 [replica set sync] replSet See http://www.mongodb.org/display/DOCS/Resyncing+a+Very+Stale+Replica+Set+Member
    Mon Jan 30 11:59:03 [replica set sync] replSet error RS102 too stale to catch up
    Mon Jan 30 11:59:03 [replica set sync] replSet RECOVERING

This is pretty obvious -- it's too far behind the master when it tried
to recover, so the master doesn't have enough journal data to send it
and it can't ever just come back up and recover. That's fine. I've been
a MySQL DBA long enough to know that this happens in any replicated
system. No foul here.

The problem, though, is that MongoDB uses the state `RECOVERING`. That
word has a very well understood meaning -- that something has happened
and that whatever it was will be over at some point in the future. It is
currently recovering from the failure. *It's really not, though!* This
instance will **never** recover from the state that it is in. A more
appropriate word would be `FAILED` or `ERROR` or something that actually
indicates that there is a problem that requires manual intervention!

I appreciate that MongoDB is a system that lends itself to ease of
use and is very nice to set up. That's great. But if you want to be
successful at companies with real traffic and usage, you have to build
something that is reasonably sane for sysadmins to maintain. Our lives
are already complicated enough with trying to manage dozens of systems
built in thousands of ways -- if your system lies to me, I'm not going
to feel comfortable with it and sure as heck won't recommend it to other
companies!

The status fields of any system **must** be accurate. When you
execute a `SHOW SLAVE STATUS` on MySQL, the `Slave_IO_Running` and
`Slave_SQL_Running` columns need to be correct! If they're wrong, you
suddenly can't trust the system and that takes it from a well-behaved
system that is sane to administrate to a black hole of fail that is
going to bite you in the ass at some point.

For this and other reasons, we're in the process of moving off
of MongoDB. It was a great system when we were smaller, but
we're beyond that now. We need systems that we don't have to
fight. (To that end, I have a lot of positive things to say about
[Riak](http://riak.com/). That's a subject for a different day, though.)

End of rant.
