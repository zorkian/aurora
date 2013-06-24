title: Singularity, an Introduction
time: 17:21
categories: Operations, Singularity
publish: yes

Today I want to talk about Singularity, a system I've been developing to
help with certain administration/operation related tasks. Some time ago
I wrote about my ideas on a new monitoring system -- this is not that.
This may be able to do that, but right now this is something else.

Singularity is, in essence, a software agent that you run one all of
your servers. It gives you certain functionality that I find really nice
to have. Nothing that is earth-shattering -- yes, you can get this same
functionality through other systems, but there is nothing I've found
that works as easily and completely as Singularity. Let me show you what
I mean.

# Singularity as Remote Execution

Originally I wanted something faster than [Fabric](http://fabfile.org/).
It's a fantastic system and very flexible, but it uses SSH and it's
serial. I don't need SSH here (it's an entirely internal network) and I
want it to be parallel. Above a certain point, serial is just way too
slow!

Singularity lets you execute something on a remote host:

    $ sng-client -H app1 exec /usr/bin/blah

Or multiple:

    $ sng-client -H app1,app2,app3 exec /usr/bin/blah

Or perhaps you want to do something globally:

    $ sng-client -A exec "service puppetd start"

Finally, you can specify roles. If you assign a machine to a role (and
a machine can have many roles), then you can execute things on those
roles. I use this for, say, our Riak nodes, App nodes, etc.

    $ sng-client -H app1 add_role app
    $ sng-client -H app2 add_role app
    $ sng-client -R app exec /usr/sbin/blah

That final command executes on app1 and app2.

# Singularity as Locking Service

A design pattern that I use is sometimes I want cron to start something
if it's offline, but otherwise, do nothing. This is easily done with
any init script that supports a status command -- or you can check for
a pid file -- or you can use a tool purpose built to do locking on the
filesystem.

All of these will work, but you will have to figure out how you want to
do it. Singularity lets you do it easily:

    $ sng-client -L mylock exec /usr/bin/somecommand

This will attempt to get the local (i.e., on this machine only) lock
called mylock and, if successful, will then run that command. That's
great, nothing special...

Well, now realize that you can do it remotely, fetching a lock on the
machine and only running if the lock can be gotten.

    $ sng-client -H app1 -L mylock exec /usr/bin/compact-files

You can also use *global locks*, which can only be held once across the
entire infrastructure. (We use [doozer](https://github.com/ha/doozerd)
for the central locking/PAXOS service.)

    $ sng-client -G globalmylock exec /do/something/big

Global locks can be useful for cron jobs. Imagine if you have the same
cron job on your four app nodes, and you need there to be only one copy
of it running anywhere globally. It's an important payment job. You tell
Singularity this, and only one of those nodes will ever run your job.

If the machine running your job goes away, then one of the other cron
jobs will succeed and start up since that global lock will no longer be
claimed.

# Borrowing from Puppet

Another interesting thing that Singularity does, but isn't fully exposed
yet, is that we depend on [Puppet](http://puppetlabs.com/)'s program
called Facter. This gathers a lot of information about the machine it
runs on and exports RAM, disks, OS, and other useful information.

This information will allow Singularity to make intelligent choices
about where to put processes. (More on that later when we talk about my
plans for the future of this project.)

This information also allows us to export inventory style information.
Ever wanted to build a UI that shows what kind of hardware you have, but
didn't want to go through the work of keeping it up to date? Singularity
is already gathering all of the information you need automatically and
collating it.

# Under the Hood

This project is written in [Go](http://golang.org/) and uses
[ZeroMQ](http://www.zeromq.org/) and [Protocol
Buffers](https://developers.google.com/protocol-buffers/) internally for
all communication. This helps ensure reliability and will eventually
ensure speed and flexibility.

The Go language is a really good fit for this kind of systems project.
Low footprint, compiled distribution, fast execution, and the built-in
concurrency is fantastic. If you haven't used Go, I recommend you give
it a shot.

The organization of components is the doozer PAXOS service in the
middle. You can configure doozer as a HA system with failover. The
Singularity agents then connect to your doozer cloud and use that to
coordinate what they're doing -- i.e., to make sure only one of the
agents is running the global scheduler.

Everything is designed with distribution in mind. There are global lock
clearers that make sure that if a machine crashes, locks are released.
Or if a machine is taken offline, it gets removed from the cloud of
machines in Singularity.

# Singularity -- Soon

Once I started hacking on this project, I realized that there are
so many things we do in operations that we could just replace with
something like Singularity and make our lives so much easier. For
example, cron -- it's an archaic system that we all love to hate, but
it could be so much better. Instead of just building a better cron that
understands "I want this job to run, but it could run on any app node",
that seems a better fit for something like an integrated inventory/cron
system.

Soon, you will be able to give Singularity configurations to run, and it
will manage them for you. I.e., you could do something like this:

    log_rotate:
        role: app
        command: /usr/sbin/logrotate
        daily: 2am

That example is easily understood, but you can already do that with
cron. More interesting is if you add in some of the other features and
things that Singularity can do:

    profiler:
        local_lock: profiler
        command: /usr/sbin/profiler
        every: 1m
        constraint:
            - load_avg.1m < 3
            - cpu.idle > 20%

This example configuration specifies a profiler that runs every minute.
However, only ever run one at a time -- if it takes more than a minute,
the lock constraint fails and you don't end up stacking up profilers.
Additionally, it specifies to only run on machines with a load average
under 3 and more than 20% idle.

That would be a little more difficult to do in standard cron.

I have some more ideas for this system. Events, chaining inputs
and outputs, integration with [OpenTSDB](http://opentsdb.net/) for
monitoring, [PagerDuty](http://pagerduty.com) for alerting, etc. The
future is exciting.

# Source and Development

The code is available on GitHub:

[https://github.com/xb95/singularity](https://github.com/xb95/singularity)

There is no documentation and a lot of gotchas. I am writing this post
to help sort out my thoughts, and to get something online. You are
welcome to play with it if you want, and feedback is always welcome.
