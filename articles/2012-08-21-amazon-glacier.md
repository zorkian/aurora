title: Amazon Glacier
time: 10:50
categories: Operations
publish: yes

Today, Amazon announced a new service being provided under the AWS
umbrella:  [Amazon Glacier](http://aws.amazon.com/glacier/). In summary,
this is a service designed to replace off-site archival storage,
commonly used for backups and long-term storage of infrequently accessed
data.

## The Use Case

Glacier is not for your standard backups. This is designed for storing
the long-term versions of backups that you only ever fall back to in
case of major catastrophe. As an example, I'm considering storing my
MySQL archives in Glacier. This wouldn't be my only backup, I maintain
last week's backup locally in my data center.

In case of machine failure or operator error, I can restore from that
backup plus binlogs to get back up to right before the failure. Glacier
is not involved. Where this service comes in is if, somehow, my database
dies, my backup is deleted, and the mirrored database (slave or
standby-master) is also wiped.

If three full copies of my data goes away, that's a catastrophe and I
will have to restore from Glacier.

To date, most of us have bitten the bullet and used Amazon's S3 for
this, even though the cost for this service is quite exorbitant. At my
day job, we also use [Tarsnap](http://www.tarsnap.com/) -- an encrypted
data storage service that is backed by S3. While a fantastic service,
the cost of storing many terabytes of data really starts to add up.

S3 also provides a lot of functionality that isn't needed for doing
off-site archival backups. While the CDN-like nature of S3 is great, I
really don't care if my backups are easily downloadable by HTTP. I'd
actually rather they weren't -- which, thankfully, S3 lets you do. You
still end up feeling slightly like you're misusing this service and, in
effect, paying for functionality you just don't need.

## Cost Effectiveness

Whenever Amazon announces a product, my first step is to understand
the product and see if it's useful to me. This one is. Next, the big
question: is it cost effective for my purposes? Let's try to figure that
out.

For this back-of-the-envelope comparison, let's imagine we have 10TB
of data we want to archive and store. This includes some number of
copies of the database, a bunch of files we want to keep "just in case",
etc. We expect that this data will only ever need to be used as a last
line of defense.

In Amazon Glacier, storing 10TB costs **$102.40 per month** (10,240 GB
at $0.01/GB).

(Compare this to Amazon S3 which would cost about USD $1126 per
month. Glacier is 10% of the cost of S3.)

But what about comparing this to hosting it yourself? Let's assume that
you are going to build out your own hardware and store it in a data
center. There are a number of ways you can go to accomplish this, and
I'm going to be generous with the discounts and pricing.

The best price I can find on a tape storage system puts the box
at slightly over USD $3000 for a machine capable of storing 18TB
uncompressed. (I'm assuming the 10TB above is compressed already and you
won't get much out of storage-level compression.)

Assuming even a 50% discount (which you almost certainly wouldn't get),
that's still USD $1500 for raw storage for 18TB of data. This is just
the machine, though, now you need to put it somewhere. If you store it
in your office, the cost might be negligible -- but now you don't really
have secure backups. All of your company's data is now beholden to the
security of your physical location -- which may or may not be good.

If you want to collocate your backup server, you've got an akward
situation -- unless you already have multiple data centers, storing it
in your existing location means it isn't off-site. If you have to rent a
spot somewhere else, it will be at least $100/month to get this machine
online and powered. By the time you've bought the hardware and put it
somewhere, you've *well exceeded the cost of Amazon Glacier for this
dataset*.

Let's not even talk about the cost for tapes, the labor required when
you have hardware failures, and other such issues. For once, I can say
that Amazon's pricing on a service is well below what you could achieve
yourself for this use.

The other option is rotational media -- but the cost for that is more
than tape. Disks also tend to have a higher failure rate than tape in my
experience, driving up your costs in labor and spares-on-hand.

Even if you somehow managed to get the cost of one system down low
enough to be competitive, now you've built a system that is perhaps
slightly cheaper, but not redundant. Glacier is replicated across
multiple data centers and to multiple locations in each facility. I
can't imagine any way in which an end-user can beat that. Amazon has a
huge economy of scale.

Amazon Glacier is easily cheaper than hosting your own backups, not to
mention more convenient.

## Who It's Not For

So, then, why wouldn't everybody use this service?

For one, if you already have facilities in several locations and spare
power. Adding a server won't change your opex appreciably, and sinking
a little into capex is often a better plan for most businesses than
increased opex. This also assumes that you have people going to those
facilities already, so the added cost of having someone swap in a tape
is pretty minimal.

Also, at scale -- Glacier is a linear service. 100TB costs ten times as
much as 10TB, but that's not the case if you're doing it yourself. At
some point when you can start buying petabyte-level storage, you almost
certainly already have the infrastructure such that you won't save much
money by using Amazon.

Finally, security. Whatever data you submit to Amazon is encrypted
in-transit, but they don't encrypt your data on their end. You lose
a little control of the security of your data. You could encrypt it
locally before sending, but that requires some effort on your end. It's
not terribly hard, but it does require some consideration.

In my experience, this rules out large companies that wouldn't consider
using Amazon's services anyway. For the rest of us who work in startups
or small to medium businesses, though, Glacier looks great.

## Some Caveats on Pricing and Usage

One thing that is important to mention: this is the equivalent of Iron
Mountain or similar long-term archival storages. It's like a glacier --
large, small-moving, and very, very frozen.

Technically, this means that you need to be storing things you
don't intend to retrieve very frequently. In fact, if you over-use
retrieval, it will cost you to get your data back out: [Amazon Glacier
Pricing](http://aws.amazon.com/glacier/#pricing).

Importantly:

* You can retrieve **up to 5%** of your stored-data monthly, for
free. More than 5% requires you to pay, and this *starts at* USD $0.01/GB.
(This 5% is slightly misleading, too, as you are actually limited to
retrieving 5% per-month, but no more than 1/30th of that per day. In
other words, if you have 10TB stored as in our example, you can only
retrieve about 17GB/day before you start paying.)

* If you delete something that has been stored for less than 90 days,
you pay a USD $0.03/GB fee.

This last point is important, as it means that you are promising Amazon
that you will be storing data for at least three months. If you don't,
you will be paying for three months of storage *anyway*.

That said, I will be moving my archive backups to Glacier. It looks good
and the caveats are well within reason. Kudos to Amazon for providing a
useful service that really fills a need.
