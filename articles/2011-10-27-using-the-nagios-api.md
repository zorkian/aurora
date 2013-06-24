time: 12:45
categories: Operations, Nagios
publish: yes
title: Using the Nagios API

This entry talks about how to set up and test the [Nagios
API](https://github.com/xb95/nagios-api) in your environment. We cover
the CLI and also using it from the web.

# Getting the Code

For now, this project doesn't support packaging or have a setup.py file,
so you will have to do it by hand. This isn't very hard, but since the
project is in such a state of growth, it's easier this way.

First, you need to check out the code on your local Nagios server. The
API daemon needs to run on a machine where it has access to the files
that Nagios creates -- the status file, log file, and external commands
pipe. This should be on your central Nagios server.

If you are using Nagios in distributed mode, you want to run the daemon
on the central machine that receives all of the distributed check
results. I.e., the machine that sends the alerts.

    $ git clone git://github.com/xb95/nagios-api.git

That command creates a directory appropriately named `nagios-api`.
Inside this directory are several executables, some documentation, and a
library directory.

# Test Run

Before we can run it, we have to figure out where your Nagios
installation is stashing the files we need. Most of these are probably
in `/etc/nagios3/nagios.cfg`, so open that file up and look for:

 * `status_file` is the main file we need, that's where Nagios writes
   out the giant dump of status.

 * `log_file` is a running tally of everything Nagios is thinking. This
   is optional, but the API daemon can follow this and allow other people
   to access log information through the API.

 * `command_file` is only relevant if you have `check_external_commands`
   on, but since most of us do, you should probably have this configured.
   The API will use this pipe to write out commands. If you don't give this
   to the API, it will operate still -- but in read-only mode.

With these three configuration options, you can now run the API daemon:

    $ ./nagios-api -s STATUS_FILE -c COMMAND_FILE -l LOG_FILE

What you should see next is something like:

    [Thu Oct 27 14:03:20 2011] {nagios-api:info} Listening on port 6315, starting to rock and roll!

If you do -- congrats! The API daemon is now up and running. If you
don't, the most likely culprit will be that it can't find one of the
files you indicate. Also, if it can't bind on port 6315, then it would
fail. (You can change the port with `-p PORT_NUMBER`.)

# Testing the API

Great. The daemon is up and running ... now what? Well, let's make sure
that it worked. Let's break out the CLI program, `nagios-cli`, and use
it. This should work:

    $ ./nagios-cli hosts

If everything is working, you should see a list of all of the hosts
defined in your Nagios configuration. This isn't particularly exciting
information, so let's use the raw mode and see exactly what the global
state object says:

    $ ./nagios-cli --raw state | python -mjson.tool
    {
        "absinthe": {
            "active_checks_enabled": "1", 
            "comments": {}, 
            "current_state": "0", 
            "downtimes": {}, 
            "last_check": "1319742372", 
            "last_hard_state": "0", 
            "last_notification": "0", 
            "notifications_enabled": "1", 
            "plugin_output": "PING OK - Packet loss = 0%, RTA = 0.19 ms", 
            "problem_has_been_acknowledged": "0", 
            "scheduled_downtime_depth": "0", 
            "services": {
                "Adaptec RAID": {
                    "active_checks_enabled": "1", 
                    "comments": {}, 
                    "current_state": "0", 
                    "downtimes": {}, 
                    "last_check": "1319742359", 
                    "last_hard_state": "0", 
                    "last_notification": "0", 
                    "notifications_enabled": "1", 
                    "plugin_output": "Logical Device 0 Optimal,Controller Optimal,Battery Status ZMM Optimal", 
                    "problem_has_been_acknowledged": "0", 
                    "scheduled_downtime_depth": "0"
                }, 
                "PING": {
                    "active_checks_enabled": "1", 
    ...

Now! Data! You will see a rather large JSON format dump showing a lot
of information about every host, service, comment, and downtime defined
in Nagios right now. It is updated automatically from the status object
Nagios writes out every ~10 seconds.

The `nagios-cli` tool in raw mode is simply doing an HTTP request for
us. The above output could also be retrieved with a simple GET:

    $ curl http://localhost:6315/state | python -mjson.tool

The next thing you might want to do is actually do something with the
CLI -- say, schedule a downtime for a host that you're about to do an
upgrade on. First, let's see what options the CLI has:

    $ ./nagios-cli -h

As of this writing there are downtime related options and then two
status commands for viewing hosts and services. More will be added
later, but let's play with the downtimes.

First, let's pick one of our hosts to operate on. Let's pretend that
`web01` needs an upgrade. From the CLI, we can easily put it into
downtime:

    $ ./nagios-cli schedule-downtime web01 4h

Simply, that command puts in a four hour fixed downtime starting
immediately for the host `web01`. If you wanted to put in downtimes
for the host and all of the services on it, you can do that with the
`--recursive` option:

    $ ./nagios-cli schedule-downtime web01 4h -r

To see all of the options this command supports:

    $ ./nagios-cli schedule-downtime -h

Later, when we're done with the upgrade, we can cancel that downtime:

    $ ./nagios-cli cancel-downtime web01

Or cancel the downtime for the host and any services that are in downtime:

    $ ./nagios-cli cancel-downtime web01 -r

That's a short and easy introduction to the CLI.

# Using the API from the Web

If you're like me, the CLI is your one-stop shop for everything. I
generally work from terminal because I can express whatever I need
easily and manipulate the text with a million and one tools for every
occasion. That's great.

Sometimes, though, I just want a web GUI. I don't really want to spend
a lot of time debating the finer points of CLIs and GUIs, but here you
don't have to -- the API is a RESTful JSON system because it works great
from the command line *and* the web browser.

For now, let's kill the running `nagios-api` and give it a new command
line option:

    $ ./nagios-api -s STATUS_FILE -c COMMAND_FILE -l LOG_FILE -o \*

(You have to escape the asterisk, at leats from Bash.)
The `-o` parameter instructs the daemon to send out a
`Access-Control-Allow-Origin` header with every response. This
header is part of the relatively new [Cross-Origin Resource
Sharing](http://www.w3.org/TR/cors/) spec.

> *A Short History Lesson*
>
> For many years, your web browser has been locked in a box that only
> allows JavaScript and other dynamic tools to talk to the same origin
> that served them. I.e., if you load a JavaScript from foo.com on port
> 80, any HTTP requests that code makes *must* target foo.com on port 80.
> 
> This is called the [same origin
> policy](http://en.wikipedia.org/wiki/Same_origin_policy) and has
> been a cornerstone of Internet security for many years. It was a
> very smart idea that makes a lot of sense, but in the modern day of
> "dynamic everything!", it has posed some interesting challenges to web
> developers.
> 
> Anyway, this has changed recently with the introduction of the CORS spec
> linked above. This spec is supported in recent versions of all major
> browsers (Opera does not support it) and allows us to write JavaScript
> that targets the Nagios API, even if that API is running on a different
> host or port. (Which it undoubtedly is.)

Now your API is configured to export the appropriate header (in this
case, "allow everybody") and you can write JavaScript that targets the
API. Let's test this out.

First, you need to be able to reach your Nagios server from your
browser. Try navigating to it on the port you configured (default is
6315), and you should see something like this:

    {"content": "Invalid request URI", "success": false}

If you don't see that, then you should stop here and figure out what's
wrong. Are you on the right network? VPN up? You know your configuration
better than I do.

Once that works, now navigate your browser to
[jquery.com](http://jquery.com). We use this site because the next step
requires the jQuery library, and the easiest way to make sure it's
loaded is just to go to their site in the browser.

Now, fire up your browser's development console. I'm only familiar with
this in Chrome, if you use Firefox or Safari, you will have to modify
these instructions.

In the development console, you can paste the following code to define a
little processing function that we're going to call shortly.

    function get_status(data, t, j) {
        if (!data.success) return;
        for (var host in data.content) {
            console.log(host + ' ' + data.content[host].plugin_output);
        }
    }

Make sure to hit enter. Okay, now we can actually hit the API and do
something. Adjust the following snippet with the appropriate URL, then
paste it in and hit enter:

    $.getJSON('http://my-nagios-server:6315/state', get_status);

You should see, very shortly, a dump of all of the hosts in your Nagios
system with the most recent output from whatever host check you use. In
my case I see a bunch of PING results.
    
And that's it! You can access the API from your browser.

# Productionizing

To make sure that your API stays up and running, I would suggest you
consider the following:

 * Monitor the API with Nagios so you are alerted if it crashes. Since
   it's a JSON server, you can do an HTTP check to make sure that it
   responds to a simple command. Alternately you can just do a TCP port
   check.

 * Use something like [Angel](https://github.com/jamwt/angel) or
   supervisor (I can never find a good link to it). Basically, something
   that runs the daemon and restarts it if it crashes.

 * If you are going to use the API from the web, you will want to consider
   setting an appropriate Access-Control-Allow-Origin header. See above.

 * Documentation. Because every operations team should document the
   daemons and other systems they have running.

That's it. Now the API should be resilient to failure and allow you to
depend on it in the rest of your infrastructure.

# Further Development

The future of the Nagios API is somewhat dependent on what the community
needs. For my own purposes, it already does everything I need. Certainly
over time I will need a few more functions to be implemented, but that's
easy.

Most of my future plans involve the Next Generation of Monitoring
Software, whatever it ends up being called, which is a Nagios
replacement that I've had cooking in my head for years now. I'll be
writing more about that soon, though.
