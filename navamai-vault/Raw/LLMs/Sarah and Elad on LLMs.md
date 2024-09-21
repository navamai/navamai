to think that most companies will end up
being competitive outside of a
fundamental breakthrough in the model
architecture cost of actually training
and then running inference on the model
or doing the post training site so I
think it's a really interesting open
question but it does feel like we're
moving into a stage of more and more
consolidation I don't know what do you
think about it most that makes sense to
Competition and decreasing API costs
me I would argue that the market has
become more competitive not less over
the last like year and a half maybe it's
competitive between a set of players
that have like as you described it you
know a capital mod that there's some
Breakaway scale but the dynamic now at
least from the consumption side is
there's continual and aggressive
performance increases and like
competition on The Benchmark and price
decreases uh uh and also you know real
open source players and so you can have
consolidation and people not necessarily
making money yet I think you actually
raised a really interesting point which
um shouldn't be underd discussed which
is the API costs have dropped something
like 200x
in the last 18 to 24 months or something
along along that order of magnitude
David on my team actually pulled
together a chart of all the pricing for
all the various models and uh what that
looks like over time and it's dramatic
in terms of how cheap um you know the
dollars per million tokens has
gotten and so I I think related to that
if you have a 200x decrease in the cost
of running these things or influencing
these things and part of that
distillation part of that is like what
do you actually using in terms of the
generation of GPU etc
etc um the actual margin available in
the in the the the revenue available is
increasing from the perspective of usage
but it it's becoming harder and harder
to just go out and compete with the with
the model at least as an API business
right and so that kind of pushes you
into specialization into other areas of
doing either B book specialized models
or specific types of post training or
vertical applications or things like
that I think the other way that you
Innovation in LLM productization
could look at the consolidation is just
like what is the argument for Capital at
that scale from a business perspective
and like the mostly unsaid thing is like
really like it's still AGI is the
business right there will be emergent
models emergent behaviors and
capabilities in the model where it will
figure out how to make money for us or
it will be obvious like how valuable it
is but I think in the more you know
immediate and I'm not even saying that's
wrong but I'd say in the more immediate
and um like two to three years
Horizon you know you have consumer as a
business either apps um uh like uh
advertising or subscriptions and
nobody's gone the advertising route in
Anger yet or Enterprise as a business
both of these are real today um but I I
think also it's become like much more of
a uh product fight right you have the
big hires of Mikey Kay and Kevin wheel
at anthropic and open AI I think you see
players trying to build Moes around the
um Capital mode and research that
they've done to make more than just chat
as an interface um and so I don't I I
think on both sides like you're you're
going to see providers try and push
customers down a more locked in path and
terms of like apis right we saw this
with you know AWS you're going have
sophistication around like don't just do
it's a it's a storage bucket you're
you'll have prompt caching and Json
output interfaces fine-tuning
and that actually makes it much less of
a commodity Market if people adopt it um
because it's easier yeah there's a lot
more features being built in and I think
you're referring to sort of what
anthropic has done on the caching side
which is a really interesting move in
terms of you know how that impacts cost
and timing and everything else or
latency yeah and I I do think I'm pretty
excited as a consumer um like what we
should expect from interfaces right not
that chat goes away but um you can
imagine much smarter chat with automatic
contacts and different surfaces so I I
do think that like you know there's a
there's a question about whether or not
you can compete with the consolidation
there's a question of how the big
players compete but the challenges I
think that are possible in the market
that people are trying today or the
reasons you could still go after would
be um like if people are taking
different very different reasoning
approaches where you know you can you
can collect the amount of capital
required to get to comp itive scale
which decreases you know uh when you're
repeating work that has already been
done um a and because you have the
benefit of like you know the hardware
progress that continues to be made but
here you have people working on you know
math and code for self-play and so I
think that's interesting it's not
necessarily like purely different
architecture but what the next level of
scaling is and then just um you know
distillation and relev of small model um
uh fine-tuning I I I think is like
another open question of like how people
are going to really use these things
yeah and I think um it's important to
clarify that we're talking specifically
about language models right and so
there's lots of other model types that
will be coming over time in physics and
biology and Material Science and uh
image gen of different forms Etc and you
know in some cases these things are
going multimodal but in many cases
you're going to have unique models for
each and really what we're referring to
right now is sort of this core large
language Model Market and you know how
that evolves over time and then to your
point there's other pieces on top of
that that could be used either for
language models or other types of models
in terms of uh reasoning models agentic
flows like it's it's almost like a
orthogonal axis and then the third piece
of it is the differentiation within the
um infrastructure around the model so
you mentioned caching as an example and
then there's long context window there's
rag there's all sorts of other things as
well and so I do think as we think about
how all this stuff evolves we're going
to see Evolution across all three axes
and the real question that we're trying
to address right now is just simply for
the core llm Market You're Building
better and better larger language models
you know how does that evolve and there
it does feel like things have
Consolidated a bit but you know uh it's
funny you look at the history of social
networks and everybody thought this
company called frenster was going to win
Comparing the LLM and social network market
and everybody thought Myspace was going
to win and then Facebook emerged and by
the time Facebook emerged everybody said
well it's just a commodity market and
there'll never be a long-term
differentiate and then Facebook one sort
of the core social piece and then even
after that you had Instagram and you had
Twitter and you had um Snapchat and
eventually by dance and Tik Tok right so
there there are these ongoing waves of
stuff even after people called the end
of Social and so I think the same thing
is likely to be true here where there'll
be certain people who start to grab
parts of the market you know LinkedIn
became the sort of um uh Enterprise
identity social network or whatever you
want to call it right your resume social
network but then Facebook Facebook
became one core piece insta became one
core piece Twitter became one core piece
Etc you know Twitter was kind of news
and realtime information the same thing
should happen here over time do you
think the um direction of other domains
let's say like video or audio or um
other model domains goes in the
direction of this commoditization I
think the reality is that it's going to
be um general purpose models for certain
things and then specialized ones for
other application areas and that could
be wrong right it comes down to what's
the degree of generalizability that you
have not only in the model capabilities
but then also in the tooling around it
and then does the tooling need to be
vertically integrated with the model and
so say for example you have a really
good image gen product and it may have
artistic applications it may have
graphic design applications it may have
UI design applications is that all one
model is it fine tunes or post training
on one model or is it you know one big
model for for one aspect and then a
bunch of fine tune model model or I
should say specialized models for other
things and I think that's a really big
open question and you know I think
there's similar discussions to be had
just around um AGI or more general
purpose intelligence right like is that
going to be if you look at the way the
brain works it's a set of reasonably
specialized modules for vision and
vision processing for different aspects
of emotion you know there there's these
really interesting things in the
psychological literature where somebody
will literally have like a steel beam
accidentally driven through their head
in a construction site and sudden
they'll lose a very specific type of
emotional functioning or reasoning but
everything else is fine right and so the
question is like how specialized will
these models be in how generalized and I
think that's also true things for things
like image gen you know will you have a
different model for graphic design than
what you're using for artistic
expression I don't know you know it's a
it's an interesting question um and I
think time will sort of tell on that as
well I do think one thing that's been
interesting is in the last couple months
it does feel like the image and Market
has started to kind of heat up right
before just felt like mid Journey was
going to be the default independent
player that wins and then maybe end up
with some multimodal stuff around Dolly
and open a or some of the stuff Gemini
was doing but there's like an increasing
number of companies now that are really
emerging that seem really interesting in
terms of the Fidelity of their models
one of the things that makes me feel a
little bit silly is if I like have a
belief like you know video video and
image models Audio models like they will
tend toward like rapidly increasing
capability and some commoditization and
then still being surprised by the pace
right and and so I I do think that
there's like when when Sora came out for
Increasing competition in image generation
example um uh it's it's an amazing
research advance but there's also a
sense of like who's really going to be
able to catch them and you know you
could argue now that you have a handful
of companies that are showing really
amazing video generation
capabilities where it's not actually
like a bunch of smaller players are step
function behind there between um Runway
and Pika and even um you know if you go
from as you said like image and video
you have like very small players or um
uh mid-stage players like the ideograms
hot shots of the world like it's it's
impressive to me how many times I see
researchers come out have a five person
team and not that much capital and
versus The Narrative of the AI like
Market five six months ago say like oh
like you know we can produce something
really competitive um even the stuff
that Luma Labs has been coming out with
right and so I think that's been an
update for me mentally I think one thing
that's striking is the size of the
models is shrinking relative to
performance over time too right and so
that may be through distillation that
may be through other things but across
the board we're seeing more and more
performance off off of smaller and
smaller models which I think is the
other thing that um I think a priority
wasn't as expected say a year or two ago
when all this stuff was kicking off like
you knew there was there was room to
sort of effectively compress certain
things but you know it's it's it's been
striking how far you can go in some
cases um and again the brain may be a
Trend in smaller models with higher performance
good a good example of what is possible
because you have a 20 or 30 watt device
running in your head that's pretty good
in terms of being general purpose and
doing image identification and other
things you know we have very cheap
Hardware
running um so you know for that
perspective there's still quite a bit of
room to go and it's in a compact space I
think we're going to see really really
cool experiences on the image video
audio side because as you say if the
models get smaller and they get better
um they also get you know and there's
different architectures like what CIA is
working on you're going to get much more
real time and we don't uh I I don't
think we have a lot of realtime
applications in production at scale
today and the the difference and
experience like Mark talked about this
of you know you can generate images as
you speak is a very different one than
um the uh like you know I'm an artist
making an output experience and so I
think that will happen over the next
couple couple months there's sort of two
areas of innovation um relative to the
stuff we're talking about and we we
should probably touch on both of them
one is sort of the chip layer
and how that may further accelerate
certain things um and then secondly I
think it's a little bit of like what how
do you think about what you actually do
in terms of the output the data you
train on Etc and how much do you push
the envelope on that so for example say
Areas of innovation
you go back to the early days of Google
and there was huge controversial
controversies at Google around Google
because what Google was doing it was
indexing the web so it's taking all this
content that was distributed around the
world and it was it was um from the
perspective itive of some of the folks
back then they were effectively scraping
the web right they were taking all the
news content they were taking everything
that everybody had written and posted
and they were indexing it and then they
were making money off of it and one of
the things they would do is they'd have
this small what was called a snippet
right and if you look at the Google
result there's like a little Blaha text
and then the link and that Blaha text
some people claimed um wasn't under fair
use for copyright law there this concept
of fair use like you know can you use a
small thing without having to pay the
copyright owner and so there was all
these lawsuits and people coming after
Google both on the news side as well as
um the fact that they were portraying
these Snippets that that some people
viewed as copyrighted information and
where that all netted out years later
was sort of three things number one is
they invented somebody known something
known as robots. text which is a file
that you put on your website that tells
a WebCrawler like Google or Bing or
whoever whether or not they're allowed
to index your information or call it um
number two is um people decided these
Snippets fell under fair use from a
copyright law
perspective number three is there were
some content deals that were stru for
Content um particularly around very
specialized content where Google was
getting feeds and then incorporating
them into their one boxes and things
like that and then um the fourth thing I
think that happened was that some of the
people realized it was better to be in
Google than not because they'd get
attribution and so a lot of the news
parties that pulled themselves out of
the Google index as that just removed me
from the index realized they lost a ton
of traffic by doing that and so they
went back and said actually you can can
start indexing us again because we
realize it's a bigger Financial penalty
to not do it than to do it right and
this took maybe a decade or 15 years to
play out right it was kind of this
ongoing
Arc and Google by pushing the envelope
um and being very thoughtful actually
about the legalities of these things
they had a really sharp team focused
specifically on copyright in other areas
um kind of threaded the needle right and
kind of made it out um reasonably
unscathed by all this um how do you
think that evolves for other companies
in terms of you know the places that
perhaps are seeing some some questioning
of approaches or image gen some of the
audio companies Etc you know how how
much risk do you think a startup should
take and how should they think about the
various approaches and again we we have
this really interesting set of P past
case examples that that may be
informative relative to this so we have
we have these businesses like as
historical examples that absolutely push
the envelope like Airbnb and U that
challenge the concepts of you know
restrictions on Leasing and medallions
Legacy of AirBnB and Uber pushing boundaries
as regulatory capture right and the
companies these Services wouldn't exist
that many consumers love if they hadn't
said like well you know we think
consumers want this business we're going
to try to get to scale and try to
understand the risk profile as we go um
and then at some point when we have more
Market power of people actually using
the business you know we will address
some of these issues and like come up
with a policy point of view and I I I do
think a lot of companies that are
operating in the AI space will have to
Wrangle with these questions along the
way um I think a really common question
for um many companies is like is Google
likely to come after you for scraping
YouTube data for example um because
there's you know and I I'd be shocked to
find out if there are ways to get to
scale of video data that don't involve
some YouTube data um and you know I I I
think the the overall um orientation
toward this should be like a business
risk one right um if you think about the
story you just told about fair use and
Google and like their General attitude
towards scraping I'd ask like well why
do they you know why do they allow Ser
businesses to exist is um taking a
certain stance on YouTube hypocritical
legally relative to their Core Business
there's also some examples of companies
in the past that were completely
obliterated by going too far so Napster
would be an example of that where the
music industry sued it basically into
the grave right um and and the music
industry in particular there's lots of
examples of uh companies that have um
died due to
lawsuits um and you know I guess there's
there's two types of risk there's almost
the legal go/ lawsuit risk which aren't
always the same thing right there's a
third type the second type of risk which
is regulatory are you doing something
that's pushing the regulatory envelope
or where the regulations are very
unclear you know crypto would be an
example of that but there's some
examples in AI right now and then the
third is almost like reputation
risk what outputs are you willing to
allow and I think grock has been really
interesting from that perspective in
terms of their explosively saying we're
not going to
police the output that much right
relative to what all the parties are
doing and that includes what images will
allow to be generated and that includes
um what sort of text we allow to be
generated or the kind of responses that
we allow and to some extent that's
probably a closer mimic to human
behavior than what many of these
companies have been doing right a lot of
the companies have really been
actively um you know focused on
preventing lots of different types of
output from these models and in some
cases it feels like it's trying to do
the right thing by users and in some
cases it feels very politically driven
in terms of the orientation and so you
know I think that's a really fascinating
experiment that's ongoing right now in
terms of um how much does society care
about the output of the model in terms
of what you allow and don't allow
relative to what are other norms for
speech or other norms for Creative
expression that already exist in society
and I think the a lot of the companies
have actually curtailed it more than the
norms for much of society right there
may be a slim part of society that feels
a certain way but for most of society
you know there tends to be or it looks
like there's broader tolerance for
certain types of things and obviously
there's things that you never want to
have that are you know um truly
disturbing or are illegal in terms of
content output but I I think it'll be
interesting to watch how that all goes I
think it's a philosophical question as
well of um you know are are you are the
restrictions to be on generation or on
distribution right because I think it's
um a much stronger argument that if you
own a platform like controlling for
certain types of distribution is a
responsibility generation feels a little
bit more like Free Speech but um but but
I think it is like a complicated
question uh should we should we talk
about semis no I guess the other piece
that we talked about touching on here
one was sort of content and risk and you
know how you think about the degree to
which you should or should not push the
envelope as a company the other piece
was semiconductors and since
semiconductor performance underlies a
lot of everything that's happening in AI
right now be it training be it inference
Etc how do you think about the coming
wave of semiconductor startups or system
startups that it really started to
emerge again I think there was a prior
wave maybe six seven years ago which was
Gro and cerebrus and a few other folks
and now it seems like we have a new wave
between um natx and um etched and a few
other companies some of whom are are
going to participate uh in this podcast
reasonably soon what do you think is
interesting in this market what's going
on so as you said the the wave like uh
you know more than five years back now
um was and I really admire the foresight
of some of these companies saying uh
we're going to have a different workload
that AI workload requires a different
type of computation but making a bet so
far in the future on um chip and systems
design is a very hard thing right and so
I I think the um you know seven years
ago it was not abundantly clear that
scale Transformers were going to be such
a big piece of the workload and so I'd
say um uh you know the the market has
evolved in very unpredictable ways and
now you have I think a cluster of
companies that is very focused on
optimizing for Transformer architectures
and like area allocated to Matrix math
um and and so I I think it'll be
interesting question of whether or not
you can um uh surpass the economics of
AMD
and the economics you know performance
for economics of AMD and Nvidia um which
uh have been really strong like
high-speed innovators to date um with
you know some argument that AMD is
making progress especially with the um
the the investmen in um that ZT
acquisition as well but i' I'd say like
the the whole thing with chip investing
is like what architectural bet are you
willing to make because you have to run
on a multi-year cycle and then then pace
of delivery and then price performance
right U but it it feels like that bet is
worth making you know you I think you
know a lot also about um the um like
shape of demand that is that has also
emerged right you have like a lot of
sovereign Cloud demand as well which is
an interesting opportunity for companies
yeah what do you make of the AMD ZT
AMD Acquires ZT
Acquisitions how do you think about why
they didn't what's the purpose like what
what is this move by AMD right now I'd
say the market is pretty divided about
whether or not AMD can become
competitive if you look at the pieces
that they need um you know they need a
they need better software uh like if you
think about the competitiv with Cuda and
so they bought this company
Silo um uh a little while back which is
essentially like a $600 million Aqua
hire of hundreds of AI engineers and
researchers who' done a lot of work on
AMD so there's that layer then you have
the networking piece so they're part of
like UA link open source competitor to
NV link and then like the the
theoretical like missing component that
ZT fills is um if you think of it as
like a 1 to2 billion doll Aqua hire of a
th000 systems designs folks to support
the like rack and data center scale AI
business instead of like individual
chips or component scales because the
you know the the thing that Nvidia is
really selling now is full systems
through like multi-year strategy of you
know delivering these essentially like
data centers for um for research labs
and and the question is like can AMD go
assemble the pieces go do that but you
know one could argue these are all the
components cool I think we're at time
all right well I'm excited to like talk
to um you know ET and madx and cerebrus
and some of the companies that are are
working on this uh in the next wave yeah
it should be very exciting uh and I'm
going to do a quick PSA so uh I'm very
Elad’s looking for a Robot
interested in buying either a a human
form SL humanoid robot or a like a spa
or something else from like Boston
Dynamics or you know one of one of those
really interesting robots so if you if
you have any suggestions or advice ping
me or if you have one for sale let me
know find us on Twitter at no prior pod
subscribe to our YouTube channel if you
want to see our faces follow the show on
Apple podcast Spotify or wherever you
listen that way you get a new episode
every week and sign up for emails or
find transcripts for every episode at
no- pri.com