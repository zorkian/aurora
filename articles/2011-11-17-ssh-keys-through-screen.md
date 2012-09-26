title: SSH key forwarding and screen/tmux
time: 15:48
categories: Tips, Operations
publish: yes

*If you just want the answer, skip to the end. This is written as an
educational post and has a lot more detail than just how to solve this
problem. Thanks!*

If you're like me, you spend a lot of time connected to various servers.
In any given day I'm using a dozen or more servers to accomplish
whatever it is I'm setting out to do. I'm also bouncing between networks
-- wired and wireless, typically, but also sometimes the wireless
drops, or I want to walk across the building, or even dare to go home
sometimes.

For years now, I've been taking advantage of
[screen](http://www.gnu.org/s/screen/) (and more recently, a newer
system called [tmux](http://tmux.sourceforge.net/)) to allow me to keep
state when I'm reconnecting from various locations. If you haven't used
it, it's well worth the time to learn one of these tools.

Next time you launch that six hour job and realize, three hours later,
that it's time to go home -- no problem. You can just leave it running
in the screen session and reconnect tomorrow or from home or wherever
you go next. No status lost.

The biggest problem with using screen is that, unless you have properly
configured everything, you often run into a problem with SSH key
forwarding.

> *Before We Begin*
>
> To really follow along here, you're going to need with you the machine
> you're working on, a remote machine that you will connect to, and an
> SSH key. Setting up SSH key access to your server is beyond the scope
> of this particularl tutorial.
>
> Really, you will need to have two or more machines in your production
> environment, because this is really an advanced technique designed for
> places wehere you have to connect to many servers.
>
> I assume that you have SSH key forwarding working already. You should
> be able to `ssh user@host` and not have to type a password (except
> maybe your SSH key passphrase).

## How SSH works, in brief

SSH is a layered system. If you are familiar with the [OSI
model](http://en.wikipedia.org/wiki/OSI_model), you know that there are
different layers that build up the networking stack that we're familiar
with. When you connect to a web site, the stack usually looks something
like this:

* *Layers 5-7*: HTTP in your browser (Chrome, Firefox, Safari, IE, etc...)
* *Layer 4*: TCP (provides reliable, ordered delivery of bytes)
* *Layer 3*: IP (allows two machines to talk to each other across the Internet)
* *Layer 2*: Ethernet (your NIC on your computer)
* *Layer 1*: CAT-5/6 cable (or other physical connection)

Each layer has its own set of responsibilities and allows the layers on
top of it to operate without knowing the intricacies of how everything
else works. When you want to connect to 8.8.8.8 on port 53, you don't
care that this involves an extremely complex system involving everything
from routing to physically sending electrical impulses. It just works.

SSH has its own layers. When you fire up an SSH connection to a machine,
you are really establishing several things:

* The SSH transport layer
* User authentication to the remote machine
* A plethora of distinct SSH channels for moving data

The transport and authentication layers are responsible for establishing
your initial connection to the remote server. Once that's done, SSH
gives you channels for moving data back and forth. This is very similar
to how IP gives you the ability to send data to a specific port -- the
underlying data link layer (layer 2 in the OSI model) doesn't have that
concept or care.

SSH uses a single TCP connection to a host to allow you to do many
things over that single connection. If you are using port forwarding,
SSH still uses a single TCP connection and multiplexes your forwarded
connections, your shell, and whatever else you're doing all through the
same pipe.

## The problem statement

Now let's move to forwarding. In our example today, we're going to be
using three machines. Your laptop will be named `laptop` (original, I
know) and you will be first connecting to the machine named `gateway`.
You have a screen session on that machine and you want to then connect
to `web01` and all of your other servers.

    mark@laptop:~$ ssh gateway
    mark@gateway:~$

When you type that command, SSH gets busy establishing a transport layer
and performing user authentication. Since we're not debugging auth right
now, let's just assume it works.

You are now presented with a shell on your remote machine. From this
bare shell, you can connect off to your webserver and it should just
work:

    mark@gateway:~$ ssh web01
    mark@web01:~$

Done. That was easy. If you just want to do this, there's really not
much you have to do. Assuming your original SSH client is forwarding,
you should be able to hop that to the next server.

But let's go back to our gateway machine and fire up screen...

    mark@web01:~$ exit
    mark@gateway:~$ screen

Now you will be back in a shell, but you will be inside of screen. I am
also not going to give you a screen tutorial in this blog post. I will
assume that you know how to basically use screen -- attach, detach, and
reattach are all you really need to know for this.

From inside of screen, now SSH to your webserver. *It works!* But wait,
you haven't done anything to configure anything yet! That's right, it'll
work ... for now. Go ahead and detach from screen (detach -- don't
terminate!) and then log out of your gateway machine.

    mark@gateway:~$ ^ad
    [detached from 23038.main]

    mark@gateway:~$ exit
    mark@laptop:~$

You are now back on your laptop, but your screen is still running.
Reconnect to gateway and reattach your screen and then try to connect to
your web server:

    mark@laptop:~$ ssh gateway
    mark@gateway:~$ screen -r
    mark@gateway:~$ ssh web01
    mark@web01's password:

You get a password prompt -- you aren't allowed in! How did this happen?

## SSH forwarding, how it works

On `gateway`, after establishing the SSH connection, take a look at the
environment of your shell:

    mark@gateway:~$ env | grep SSH
    SSH_CLIENT=68.38.123.35 45926 22
    SSH_TTY=/dev/pts/0
    SSH_CONNECTION=68.38.123.35 48926 10.1.35.23 22
    SSH_AUTH_SOCK=/tmp/ssh-hRNwjA1342/agent.1342

The important one here is `SSH_AUTH_SOCK` which is currently set to some
file in `/tmp`. If you examine this file, you'll see that it's a Unix
domain socket -- and is connected to the particular instance of `ssh`
that you connected in on. Importantly, *this changes every time you
connect*.

As soon as you log out, that particular socket file is gone. Now, if
you go and reattach your screen, you'll see the problem. It has the
environment from when screen was _originally_ launched -- which could
have been weeks ago. That particular socket is long since dead.

From inside of screen, your shell has no idea that there is real SSH
authentication socket somewhere else. It just knows that the one you
have told it to use doesn't exist.

## Solving the crisis

There are several ways of solving this problem. I believe the following
to be the easiest and most reliable of the ones I've tried. This works
in `bash` and `zsh` and probably will work in other shells as well.

Solution: since we know the problem has to do with knowing where the
currently live SSH authentication socket is, let's just put it in a
predictable place!

In your `.bashrc` or `.zshrc` file, add the following:

    # Predictable SSH authentication socket location.
    SOCK="/tmp/ssh-agent-$USER-screen"
    if test $SSH_AUTH_SOCK && [ $SSH_AUTH_SOCK != $SOCK ]
    then
        rm -f /tmp/ssh-agent-$USER-screen
        ln -sf $SSH_AUTH_SOCK $SOCK
        export SSH_AUTH_SOCK=$SOCK
    fi

That's it. Make sure to put this on every machine that you intend to
connect through, then you're done. SSH to `gateway`, reconnect to your
screen, and you can immediately SSH over to `web01` or wherever you want
to go. It just works.

All this code does is, when you first SSH in to the machine, is set your
`SSH_AUTH_SOCK` variable to a predictable value. It's a symlink that
points to whatever your current SSH authentication socket happens to be.
Every time you SSH in to this machine, that symlink gets rebuilt.

Inside of screen, the environment never has to change. It dereferences
the symlink to find the correct socket and just works. No matter how
many times you reconnect.

## Conclusion and room for improvement

It took me a while to settle on this method. Originally I tried
something fancy with getting screen/tmux to automatically import
the environment of the shell I was attaching from, but that proved
hard/impossible.

I also tried building a wrapper around the SSH command to automatically
set the right environment variables. That turned out to work OK but
was clumsy and hard to maintain between different machines. It also
required building more and more wrappers to get other commands to work
and ultimately proved unsustainable.

This particular solution came from, I'm pretty sure, somewhere else on
the Internet. I would attribute if I remembered where I got the idea
from. It's simple and just works.

The only trouble I've had is when I leave a terminal up at home, then go
to work and connect from there (overwriting the symlink), and then when
I get back home I have to close that terminal. I can't just use it. This
happens so rarely that I haven't tried to engineer a fix to it. Let me
know if you come up with one, though.

Thanks for reading. I hope this improves your systems administration
experience.
