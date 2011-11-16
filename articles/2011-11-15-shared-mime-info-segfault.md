title: Segmentation fault in shared-mime-info
time: 14:21
categories: Administration
publish: no

Today one of our servers encountered a problem that caused one of our
guys to be unable to install any packages. The package system was stuck
trying to upgrade `shared-mime-info`, but it was getting a segmentation
fault every time he tried. This blog post is up because I had a hard
time finding enough information online about this problem, but also to
walk you through some steps you can take when debugging a problem like
this.

## The Problem

The original problem showed up when we were doing an `apt-get install`
of an unrelated package. Through the magic of dependencies, it required
an update to `shared-mime-info`:

    Setting up shared-mime-info (0.71-1ubuntu2) ...
    Segmentation fault
    dpkg: error processing shared-mime-info (--configure):
         subprocess installed post-installation script returned error exit status 139

Well damn. That's no good. In fact, it's downright annoying. Packages
should just install and be happy. That's half of the logic behind
using a package management system and not building your own: reliable,
repeatable installation. I want to know when I install something on one
machine that it's going to work everywhere.

## Initial Fix Attempt

From time to time, I find that a package fails in this manner because it
is secretly depending on a newer version of something (like `libc`) but
it wasn't spelled out explicitly in the package dependencies. Therefore,
when installing the newer version of the package, it fails because it's
expecting a newer version of some system package -- but can't find it.

My first response is almost always to try doing a full system upgrade to
see if that brings in all of the right packages and fixes it:

    $ apt-get update
    $ apt-get dist-upgrade

Alas, that did not fix this problem. It continued to segfault.

## To the Internet!

Next I did some searching on the Internet. If it's a big problem, odds
are that someone has already written about it and found a fix. You can
replicate their fix and move forward feeling warm and fuzzy in the
knowledge that the Internet has done a good deed this day.

Unfortunately, most of the articles I found were people talking about
the error and not actually proposing a solution. The closest I came was
someone talking about malformed XML in the directory, so I checked that
-- but it all looked fine to me. (And, more importantly, it was all
system files... we didn't have anything custom.)

We thought briefly that maybe the best solution would be to remove these
XML packages, but since one of them is the Sun Java JRE's, and we use
that, it didn't seem like a very good option.

## More Debugging

When a package is breaking like this, it's probably in the `postinst`
script. Debian packages go through several different phases and many of
those phases can have triggers -- scripts that are run by the package
installer. This lets you do some tasks in the cleanup or setup phases.

First, I wanted to look at the installation script for this package, so
I extracted it to somewhere I could look at it.

    $ dpkg-deb -e /var/cache/apt/archives/shared-mime-info* temp

Now if you look in that folder, you'll see a few files. The one we're
interested in is named `postinst`. Take a look at that file. You'll see
it does a few things, but mostly, it's just executing this one command,
and sure enough it crashes:

    $ update-mime-database /usr/share/mime
    Segmentation fault

Armed with this information, Google gave up a little more knowledge:
apparently it's not the fault of the MIME package, it's actually the
underlying XML system. Using `xmllint` fails on the given XML files.
This is a key step in debugging something: reducing the search domain.

## Enter GDB

In cases where you're segfaulting, it's pretty easy to figure out
exactly what is going on. `gdb` to the rescue:

    $ gdb xmllint
    GNU gdb (GDB) 7.1-ubuntu
    Copyright (C) 2010 Free Software Foundation, Inc.
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
    and "show warranty" for details.
    This GDB was configured as "x86_64-linux-gnu".
    For bug reporting instructions, please see:
    <http://www.gnu.org/software/gdb/bugs/>...
    Reading symbols from /usr/bin/xmllint...(no debugging symbols found)...done.

Great. Now I can tell it to run and give it the argument to the XML
file.

    (gdb) run /usr/share/mime/packages/freedesktop.org.xml
    Starting program: /usr/bin/xmllint /usr/share/mime/packages/freedesktop.org.xml

    Program received signal SIGSEGV, Segmentation fault.
    __strncmp_ssse3 () at ../sysdeps/x86_64/multiarch/../strcmp.S:100
    100     ../sysdeps/x86_64/multiarch/../strcmp.S: No such file or directory.
            in ../sysdeps/x86_64/multiarch/../strcmp.S

Okay, so we technically died in a system call. That's not super
interesting to me at this point though, since it doesn't really say
what's gone wrong or where. We can look at the stack trace, though:

    (gdb) bt
    #0  __strncmp_ssse3 () at ../sysdeps/x86_64/multiarch/../strcmp.S:100
    #1  0x00007ffff78accca in __xmlParserInputBufferCreateFilename () from /usr/lib/libxml2.so.2
    #2  0x00007ffff7881d8d in xmlNewInputFromFile () from /usr/lib/libxml2.so.2
    #3  0x000000000040aa6d in ?? ()
    #4  0x00007ffff78861b6 in xmlCreateURLParserCtxt () from /usr/lib/libxml2.so.2
    #5  0x00007ffff789cb9a in xmlReadFile () from /usr/lib/libxml2.so.2
    ...

The problem certainly does seem the fault of the XML library. That's
useful information, but what is even more useful is doing a Google
search for the method that is causing the crash. Doing that eventually
lead me to this page:

http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=439982#10

Now we're cooking.

## 
