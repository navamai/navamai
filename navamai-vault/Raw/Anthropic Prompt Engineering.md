Introduction
- Basically, this entire roundtable session here is just gonna be focused mainly on prompt engineering.
A variety of perspectives at this table around prompting from a research side, from a consumer side,
and from the enterprise side. And I want to just get the whole wide range of opinions
because there's a lot of them. And just open it up to discussion and explore what prompt engineering really is
and what it's all about. And yeah, we'll just take it from there. So maybe we can go around the horn with intros.
I can kick it off. I'm Alex. I lead Developer Relations here at Anthropic. Before that,
I was technically a prompt engineer at Anthropic. I worked on our prompt engineering team,
and did a variety of roles spanning from a solutions architect type of thing,
to working on the research side. So with that, maybe I can hand it over to David.
- Heck, yeah. My name's David Hershey. I work with customers mostly at Anthropic
on a bunch of stuff technical, I help people with finetuning, but also just a lot of the generic things
that make it hard to adopt language models of prompting. And just like how to build systems with language models,
but spend most of my time working with customers. - Cool. I'm Amanda Askell. I lead one of the Finetuning teams at Anthropic,
where I guess I try to make Claude be honest and kind.
Yeah. - My name is Zack Witten. I'm a Prompt Engineer at Anthropic.
Alex and I always argue about who the first one was. He says it's him, I say it's me. - Contested. - Yeah. I used to work a lot with individual customers,
kind of the same way David does now. And then as we brought more solutions architects
to the team, I started working on things that are meant to raise the overall levels
of ambient prompting in society, I guess, like the prompt generator and the various educational materials that people use.
- Nice, cool. Well, thanks guys for all coming here. I'm gonna start with a very broad question
Defining prompt engineering
just so we have a frame going into the rest of our conversations here. What is prompt engineering? Why is it engineering?
What's prompt, really? If anyone wants to kick that off, give your own perspective on it,
feel free to take the rein here. - I feel like we have a prompt engineer. It's his job.
- We're all prompt engineers in our own form. - But one of us has a job. - Yeah. Zack, maybe since it's in your title.
- One of us has a job, but the other three don't have jobs.
- I guess I feel like prompt engineering is trying to get the model to do things, trying to bring the most out of the model.
Trying to work with the model to get things done that you wouldn't have been able to do otherwise.
So a lot of it is just clear communicating. I think at heart,
talking to a model is a lot like talking to a person. And getting in there and understanding the psychology of the model,
which Amanda is the world's most expert person in the world.
- Well, I'm gonna keep going on you. Why is engineering in the name?
- Yeah. I think the engineering part comes from the trial and error. - Okay. - So one really nice thing about talking to a model
that's not like talking to a person, is you have this restart button. This giant go back to square zero
where you just start from the beginning. And what that gives you the ability to do that you don't have, is a truly start from scratch
and try out different things in an independent way, so that you don't have interference from one to the other.
And once you have that ability to experiment and to design different things, that's where the engineering part has the potential
to come in. - Okay. So what you're saying is as you're writing these prompts,
you're typing in a message to Claude or in the API or whatever it is. Being able to go back and forth with the model
and to iterate on this message, and revert back to the clean slate every time,
that process is the engineering part. This whole thing is prompt engineering all in one.
- There's another aspect of it too, which is integrating the prompts
within your system as a whole. And David has done a ton of work with customers integrating.
A lot of times it's not just as simple as you write one prompt and you give it to the model and you're done. In fact, it's anything but. It's like way more complicated.
- Yeah. I think of prompts as the way that you program models a little bit,
that makes it too complicated. 'Cause I think Zack is generally right that it's just talking clearly is the most important thing.
But if you think about it a little bit as programming a model, you have to think about where data comes from, what data you have access to.
So if you're doing RAG or something, what can I actually use and do and pass to a model?
You have to think about trade-offs in latency and how much data you're providing and things like that.
There's enough systems thinking that goes into how you actually build around a model. I think a lot of that's also the core
of why it maybe deserves its own carve-out as a thing to reason about separately from just a software engineer
or a PM or something like that. It's kind of its own domain of how to reason about these models. - Is a prompt in this sense then natural language code?
Is it a higher level of abstraction or is it a separate thing? - I think trying to get too abstract with a prompt is a way
to overcomplicate a thing, because I think, we're gonna get into it, but more often than not,
the thing you wanna do is just write a very clear description of a task, not try to build crazy abstractions or anything like that.
But that said, you are compiling the set of instructions and things like that into outcomes a lot of times.
So precision and a lot the things you think about with programming about version control
and managing what it looked like back then when you had this experiment. And tracking your experiment and stuff like that,
that's all just equally important to code. - Yeah.
- So it's weird to be in this paradigm where written text, like a nice essay that you wrote is something
that's looked like the same thing as code. But it is true that now we write essays
and treat them code, and I think that's actually correct. - Yeah. Okay, interesting. So maybe piggybacking off of that,
we've loosely defined what prompt engineering is. So what makes a good prompt engineer?
What makes a good prompt engineer
Maybe, Amanda, I'll go to you for this, since you're trying to hire prompt engineers more so in a research setting.
What does that look like? What are you looking for in that type of person? - Yeah, good question. I think it's a mix of like Zack said, clear communication,
so the ability to just clearly state things, clearly understand tasks,
think about and describe concepts really well. That's the writing component, I think. I actually think that being a good writer
is not as correlated with being a good prompt engineer as people might think.
So I guess I've had this discussion with people 'cause I think there's some argument as like, "Maybe you just shouldn't have the name engineer in there.
Why isn't it just writer?" I used to be more sympathetic to that. And then, I think, now I'm like what you're actually doing,
people think that you're writing one thing and you're done. Then I'll be like to get a semi-decent prompt
when I sit down with the model. Earlier, I was prompting the model and I was just like in a 15-minute span
I'll be sending hundreds of prompts to the model. It's just back and forth, back and forth, back and forth. So I think it's this willingness to iterate and to look
and think what is it that was misinterpreted here, if anything? And then fix that thing.
So that ability to iterate. So I'd say clear communication, that ability to iterate.
I think also thinking about ways in which your prompt might go wrong. So if you have a prompt
that you're going to be applying to say, 400 cases, it's really easy to think about the typical case that it's going to be applied to,
to see that it gets the right solution in that case, and then to move on. I think this is a very classic mistake that people made.
What you actually want to do is find the cases where it's unusual. So you have to think about your prompt and be like,
"What are the cases where it'd be really unclear to me what I should do in this case?" So for example, you have a prompt that says, "I'm going to send you a bunch of data.
I want you to extract all of the rows where someone's name is, I don't know, starts with the letter G."
And then you're like, "Well, I'm gonna send it a dataset where there is no such thing, there is no such name that starts with the letter G.
"I'm going to send it something that's not a dataset, I might also just send it an empty string. These are all of the cases you have to try,
because then you're like, "What does it do in these cases? " And then you can give it more instructions for how it should deal with that case.
- I work with customers so often where you're an engineer, you're building something. And there's a part in your prompt where a customer of theirs
is going to write something. - Yeah. - And they all think about these really perfectly phrased things that they think someone's going to type into their chatbot.
And in reality, it's like they never used the shift key and every other word is a typo.
- They think it's Google. - And there's no punctuation. - They just put in random words with no question. - Exactly.
So you have these evals that are these beautifully structured what their users ideally would type in. But being able to go the next step
to reason about what your actual traffic's gonna be like, what people are actually gonna to try to do, that's a different level of thinking.
- One thing you said that really resonated with me is reading the model responses. In a machine learning context,
you're supposed to look at the data. It's almost a cliche like look at your data, and I feel like the equivalent for prompting
is look at the model outputs. Just reading a lot of outputs and reading them closely.
Like Dave and I were talking on the way here, one thing that people will do is they'll put think step-by-step in their prompt.
And they won't check to make sure that the model is actually thinking step-by-step, because the model might take it in a more abstract
or general sense. Rather than like, "No, literally you have to write down your thoughts in these specific tags."
So yeah, if you aren't reading the model outputs, you might not even notice that it's making that mistake.
- Yeah, that's interesting. There is that weird theory of mind piece
to being a prompt engineer where you have to think almost about how the model's gonna view your instructions. But then if you're writing for an enterprise use case too,
you also have to think about how the user's gonna talk to the model, as you're the third party sitting there
in that weird relationship. Yeah. - On the theory of mind piece, one thing I would say is,
it's so hard to write instructions down for a task. It's so hard to untangle in your own brain
all of the stuff that you know that Claude does not know and write it down. It's just an immensely challenging thing
to strip away all of the assumptions you have, and be able to very clearly communicate the full fact set of information
that is needed to a model. I think that's another thing that really differentiates a good prompt engineer from a bad one, is like...
A lot of people will just write down the things they know. But they don't really take the time to systematically break out
what is the actual full set of information you need to know to understand this task? - Right. - And that's a very clear thing I see a lot
is prompts where it's just conditioned. The prompt that someone wrote is so conditioned
on their prior understanding of a task, that when they show it to me I'm like, "This makes no sense.
None of the words you wrote make any sense, because I don't know anything about your interesting use case."
But I think a good way to think about prompt engineering in that front and a good skill for it,
is just can you actually step back from what you know and communicate to this weird system that knows a lot,
but not everything about what it needs to know to do a task? - Yeah. The amount of times I've seen someone's prompt
and then being like, "I can't do the task based on this prompt." I'm human level and you're giving this to something
that is worse than me and expecting it to do better, and I'm like, "Yeah."
- Yeah. There is that interesting thing with like... Current models don't really do a good job
Refining prompts
of asking good, probing questions in response like a human would. If I'm giving Zack directions on how to do something,
he'll be like, "This doesn't make any sense. What am I supposed to do at this step or here and here?" Model doesn't do that, right, so you have to, as yourself,
think through what that other person would say and then go back to your prompt and answer those questions.
- You could ask it to do that. - You could. That's right. - I do that, yeah. - I guess that's another step. - I was going to say one of the first things I do
with my initial prompt, is I'll give it the prompt and then I'll be like, "I don't want you to follow these instructions. I just want you to tell me the ways in
which they're unclear or any ambiguities, or anything you don't understand." And it doesn't always get it perfect, but it is interesting that that is one thing you can do.
And then also sometimes if people see that the model makes a mistake, the thing that they don't often do is just ask the model.
So they say to the model, "You got this wrong. Can you think about why? And can you maybe write an edited version of my instructions
that would make you not get it wrong?" And a lot of the time, the model just gets it right. The model's like, "Oh, yeah.
Here's what was unclear, here's a fix to the instructions," and then you put those in and it works. - Okay.
I'm actually really curious about this personally almost. Is that true that that works?
Is the model able to spot its mistakes that way? When it gets something wrong, you say, "Why did you get this wrong?"
And then it tells you maybe something like, "Okay, how could I phrase this to you in the future
so you get it right?" Is there an element of truth to that? Or is that just a hallucination on the model's part
around what it thinks its limits are? - I think if you explain to it what it got wrong,
it can identify things in the query sometimes. I think this varies by task. This is one of those things where I'm like I'm not sure
what percentage of the time it gets it right, but I always try it 'cause sometimes it does. - And you learn something. - Yeah.
- Anytime you go back to the model or back and forth with the model, you learn something about what's going on.
I think you're giving away information if you don't at least try. - That's interesting.
Amanda, I'm gonna keep asking you a few more questions here. One thing maybe for everybody watching this,
is we have these Slack channels at Anthropic where people can add Claude into the Slack channel,
then you can talk to Claude through it. And Amanda has a Slack channel that a lot of people follow of her interactions with Claude.
And one thing that I see you always do in there, which you probably do the most of anyone at Anthropic,
is use the model to help you in a variety of different scenarios.
I think you put a lot of trust into the model in the research setting. I'm curious how you've developed those intuitions
for when to trust the model. Is that just a matter of usage, experience or is it something else?
- I think I don't trust the model ever and then I just hammer on it. So I think the reason why you see me do that a lot,
is that that is me being like, "Can I trust you to do this task?" 'Cause there's some things, models are kind of strange.
If you go slightly out of distribution, you just go into areas where they haven't been trained
or they're unusual. Sometimes you're like, "Actually, you're much less reliable here, even though it's a fairly simple task."
I think that's happening less and less over time as models get better, but you want to make sure you're not in that kind of space.
So, yeah, I don't think I trust it by default, but I think in ML, people often want to look across really large datasets.
And I'm like, "When does it make sense to do that?" And I think the answer is when you get relatively low signal from each data point,
you want to look across many, many data points, because you basically want to get rid of the noise. With a lot of prompting tasks,
I think you actually get really high signal from each query. So if you have a really well-constructed set
of a few hundred prompts, that I think can be much more signal than thousands that aren't as well-crafted.
So I do think that I can trust the model if I look at 100 outputs of it and it's really consistent.
And I know that I've constructed those to basically figure out all of the edge cases and all of the weird things that the model might do,
strange inputs, et cetera. I trust that probably more than a much more loosely constructed set
of several thousand. - I think in ML, a lot of times the signals are numbers.
Did you predict this thing right or not? And it'd be looking at the logprobs of a model
and trying to intuit things, which you can do, but it's kind of sketchy.
I feel like the fact that models output more often than not a lot of stuff like words and things.
There's just fundamentally so much to learn between the lines of what it's writing and why and how,
and that's part of what it is. It's not just did it get the task right or not? It's like, "How did it get there?
How was it thinking about it? What steps did it go through?" You learn a lot about what is going on, or at least you can try to get a better sense, I think.
But that's where a lot of information comes from for me, is by reading the details of what came out, not just through the result.
- I think also the very best of prompting can make the difference between a failed
and a successful experiment. So sometimes I can get annoyed if people don't focus enough on the prompting component of their experiment,
because I'm like, "This can, in fact, be the difference between 1% performance in the model or 0.1%."
In such a way that your experiment doesn't succeed if it's at top 5% model performance, but it does succeed if it's top 1% or top 0.1%.
And then I'm like, "If you're gonna spend time over coding your experiment really nicely, but then just not spend time on the prompt."
I don't know. That doesn't make sense to me, 'cause that can be the difference between life and death of your experiment. - Yeah.
And with the deployment too, it's so easy to, "Oh, we can't ship this." And then you change the prompt around
and suddenly it's working. - Yeah. - It's a bit of a double-edged sword though, because I feel like there's a little bit of prompting where there's always this mythical, better prompt
that's going to solve my thing on the horizon. - Yeah. - I see a lot of people get stuck into the mythical prompt on the horizon,
that if I just keep grinding, keep grinding. It's never bad to grind a little bit on a prompt, as we've talked, you learn things.
But it's one of the scary things about prompting is that there's this whole world of unknown.
- What heuristics do you guys have for when something is possible versus not possible
with a perfect prompt, whatever that might be? - I think I'm usually checking for whether the model kind of gets it.
So I think for things where I just don't think a prompt is going to help, there is a little bit of grinding.
But often, it just becomes really clear that it's not close or something.
Yeah. I don't know if that's a weird one where I'm just like, "Yeah, if the model just clearly can't do something,
I won't grind on it for too long." - This is the part that you can evoke how it's thinking about it, and you can ask it how it's thinking about it and why.
And you can get a sense of is it thinking about it right? Are we even in the right zip code of this being right?
And you can get a little bit of a kneeling on that front of, at least, I feel like I'm making progress towards getting something closer to right.
Where there's just some tasks where you really don't get anywhere closer to it's thought process.
It's just like every tweak you make just veers off in a completely different, very wrong direction, and I just tend to abandon those.
I don't know. - Those are so rare now though, and I get really angry at the model when I discover them
because that's how rare they are. I get furious. I'm like, "How dare there be a task that you can't just do,
if I just push you in the right direction?" - I had my thing with Claude plays Pokemon recently,
and that was one of the rare times where I really... - Yeah, can you explain that? Explain that just for people. I think that's really cool.
- I did a bit of an experiment where I hooked Claude up to a Game Boy emulator,
and tried to have it play the game Pokemon Red like the OG Pokemon.
And it's like you think what you wanna do and it could write some code to press buttons
and stuff like that, pretty basic. And I tried a bunch of different very complex prompting layouts, but you just get into certain spots
where it just really couldn't do it. So showing it a screenshot of a Game Boy,
it just really couldn't do. And it just so deeply because I'm so used to it, being able to do something mostly.
So I spent a whole weekend trying to write better and better prompts to get it
to really understand this Game Boy screen. And I got incrementally better so that it was only terrible
instead of completely no signal. You could get from no signal to some signal.
But it was, I don't know, at least this is elicited for me. Once I put a weekend of time in and I got from no signal
to some signal, but nowhere close to good enough, I'm like, "I'm just going to wait for the next one. (Alex laughing)
I'm just gonna wait for another model." I could grind on this for four months, and the thing that would come out is another model
and that's a better use of my time. Just sit and wait to do something else in the meanwhile. - Yeah.
That's an inherent tension we see all the time, and maybe we can get to that in a sec. Zack, if you wanna go. - Something I liked about your prompt with Pokemon
where you got the best that you did get, was the way that you explained to the model that it is in the middle of this Pokemon game.
Here's how the things are gonna be represented.
I actually think you actually represented it in two different ways, right? - I did. So what I ended up doing, it was obnoxious
but I superimposed a grid over the image, and then I had to describe each segment of the grid
in visual detail. Then I had to reconstruct that into an ASCII map
and I gave it as much detail as I could. The player character is always at location 4, 5 on the grid
and stuff like that, and you can slowly build up information. I think it's actually a lot like prompting,
but I just hadn't done it with images before. Where sometimes my intuition
for what you need to tell a model about text, is a lot different from what you need to tell a model about images. - Yeah.
- I found a surprisingly small number of my intuitions about text have transferred to image.
I found that multi-shot prompting is not as effective for images and text. I'm not really sure, you can have theoretical explanations about why.
Maybe there's a few of it in the training data, a few examples of that.
- Yeah. I know when we were doing the original explorations with prompting multimodal, we really couldn't get it to noticeably work.
You just can't seem to improve Claude's actual, visual acuity in terms of what it picks up within an image.
Anyone here has any ways that they've not seen that feature. But it seems like that's similar with the Pokemon thing where it's trying to interpret this thing.
No matter how much you throw prompts at it, it just won't pick up that Ash that's in that location.
- Yeah. But I guess to be visceral about this, I could eventually get it so that it could most often tell me where a wall was,
and most often tell me where the character was. It'd be off by a little bit. But then you get to a point,
and this is maybe coming back to knowing when you can't do it. It would describe an NPC, and to play a game well,
you need to have some sense of continuity. Have I talked to this NPC before?
And without that, you really don't, there's nothing you can do. You're just going to keep talking to the NPC, 'cause like, "Well, maybe this is a different NPC."
But I would try very hard to get it to describe a NPC and it's like, "It's a person."
They might be wearing a hat, they weren't wearing a hat. And it's like you grind for a while, inflate it to 3000X and just crop it to just the NPC,
and it's like, "I have no idea what this is." It's like I showed it this clear, female NPC thing
enough times and it just got nowhere close to it, and it's like, "Yeah, this is a complete lost cause." - Wow, okay.
- I really want to try this now. I'm just imagining all the things I would try. I don't know, I want you to imagine this game art
as a real human and just describe to me what they're like. What did they look like as they look in the mirror?
And then just see what the model does. - I tried a lot of things.
The eventual prompt was telling Claude it was a screen reader for a blind person, which I don't know if that helped,
but it felt right so I stuck with that. - That's an interesting point. I actually wanna go into this a little bit
Honesty, personas and metaphors in prompts
'cause this is one of the most famous prompting tips, is to tell the language model that they are some persona
or some role. I feel like I see mixed results. Maybe this worked a little bit better in previous models
and maybe not as much anymore. Amanda, I see you all the time be very honest with the model
about the whole situation like, "Oh, I am an AI researcher and I'm doing this experiment." - I'll tell it who I am. - Yeah.
- I'll give it my name, be like, "Here's who you're talking to." - Right. Do you think that level of honesty, instead of lying to the model or forcing it to like,
"I'm gonna tip you $500." Is there one method that's preferred there,
or just what's your intuition on that? - Yeah. I think as models are more capable and understand more
about the world, I guess, I just don't see it as necessary to lie to them.
I also don't like lying to the models just 'cause I don't like lying generally. But part of me is if you are, say, constructing.
Suppose you're constructing an eval dataset for a machine learning system or for a language model.
That's very different from constructing a quiz for some children. So when people would do things like,
"I am a teacher trying to figure out questions for a quiz." I'm like, "The model knows what language model evals are."
If you ask it about different evals it can tell you, and it can give you made up examples of what they look like. 'Cause these things are like they understand them,
they're on the internet. So I'm like, "I'd much rather just target the actual task that I have." So if you're like, "I want you to construct questions
that look a lot like an evaluation of a language model." It's that whole thing of clear communication.
I'm like, "That is, in fact, the task I want to do. So why would I pretend to you that I want to do some unrelated,
or only tangentially related task?" And then expect you to somehow do better at the task that I actually want you to do.
We don't do this with employees. I wouldn't go to someone that worked with me and be like, "You are a teacher and you're trying to quiz your students."
I'd be like, "Hey, are you making that eval?" I don't know. So I think maybe it's a heuristic from there where I'm like,
"If they understand the thing, just ask them to do the thing that you want." - I see this so much. - I guess to push back a little bit,
I have found cases where not exactly lying but giving it a metaphor
for how to think about it could help. In the same way that sometimes I might not understand how to do something and someone's like, "Imagine that you were doing this,
even though I know I'm not doing it." The one that comes to mind for me, is I was trying to have Claude say whether an image
of a chart or a graph is good or not. Is it high quality? And the best prompt that I found for this
was asking the model what grade it would give the chart, if it were submitted as a high school assignment.
So it's not exactly saying, "You are a high school teacher." It's more like, "This is the kind of analysis
that I'm looking from for you." The scale that a teacher would use is similar to the scale
that I want you to use. - But I think those metaphors are pretty hard to still come up with.
I think people still, the default you see all the time is finding some facsimile of the task.
Something that's a very similar-ish task, like saying you're a teacher. You actually just lose a lot
in the nuance of what your product is. I see this so much in enterprise prompts where people write something similar,
because they have this intuition that it's something the model has seen more of maybe. It's seen more high school quizzes than it has LLM evals,
and that may be true. But to your point, as the models get better, I think just trying to be very prescriptive
about exactly the situation they're in. I give people that advice all the time. Which isn't to say that I don't think to the extent
that it is true that thinking about it the way that someone would grade a chart,
as how they would grade a high school chart, maybe that's true. But it's awkwardly the shortcut people use a lot of times
to try to get what happens, so I'll try to get someone that I can actually talk about 'cause I think it's somewhat interesting. So writing you are a helpful assistant,
writing a draft of a document, it's not quite what you are.
You are in this product, so tell me. If you're writing an assistant that's in a product,
tell me I'm in the product. Tell me I'm writing on behalf of this company, I'm embedded in this product.
I'm the support chat window on that product. You're a language model, you're not a human, that's fine.
But just being really prescriptive about the exact context about where something is being used.
I found a lot of that. Because I guess my concern most often with role prompting, is people used it as a shortcut
of a similar task they want the model to do. And then they're surprised when Claude doesn't do their task right, but it's not the task.
You told it to do some other task. And if you didn't give it the details about your task, I feel like you're leaving something on the table.
So I don't know, it does feel like a thing though to your point of as the models scale.
Maybe in the past it was true that they only really had a strong understanding of elementary school tests comparatively.
But as they get smarter and can differentiate more topics, I don't know, just like being clear.
- I find it interesting that I've never used this prompting technique. - Yeah, that's funny. - Even with worse models
and I still just don't ever find myself, I don't know why. I'm just like, "I don't find it very good essentially."
- Interesting. - I feel like completion era models, there was a little bit of a mental model
of conditioning the model into a latent space that was useful that I worried about,
that I don't really worry about too much anymore. - It might be intuitions from pretrained models
over to RLHF models, that to me, just didn't make sense. It makes sense to me if you're prompting a pretrained.
- You'd be amazed how many people try to apply their intuitions. I think it's not that surprising. Most people haven't really experimented
with the full what is a pretrained model? What happens after you do SL?
What happens after you do RLHF, whatever? So when I talk to customers,
it's all the time that they're trying to map some amount of, "Oh, how much of this was on the internet?
Have they seen a ton of this on the internet?" You just hear that intuition a lot, and I think it's well-founded fundamentally.
But it is overapplied by the time you actually get to a prompt,
because of what you said. By the time they've gone through all of this other stuff, that's not actually quite what's being modeled.
- Yeah. The first thing that I feel like you should try is, I used to give people this thought experiment
where it's like imagine you have this task. You've hired a temp agency to send someone to do this task.
This person arrives, you know they're pretty competent. They know a lot about your industry and so forth,
but they don't know the name of your company. They've literally just shown up and they're like, "Hey, I was told you guys had a job for me to do,
tell me about it." And then it's like, "What would you say to that person?" And you might use these metaphors. You might say things like,
"We want you to detect good charts. What we mean by a good chart here,
is it doesn't need to be perfect. You don't need to go look up whether all of the details are correct." It just needs to have its axes labeled,
and so think about maybe high school level, good chart. You may say exactly that to that person
and you're not saying to them, "You are a high school." You wouldn't say that to them. You wouldn't be like, "You're a high school teacher reading charts."
- What are you talking about? - Yeah, so sometimes I'm just like it's like the whole
if I read it. I'm just like, "Yeah. Imagine this person who just has very little context, but they're quite competent. They understand a lot of things about the world."
Try the first version that actually assumes that they might know things about the world, and if that doesn't work, you can maybe do tweaks and stuff.
But so often, the first thing I try is that, and then I'm like, "That just worked." - That worked. - And then people are like,
"Oh, I didn't think to just tell it all about myself and all about the task I want to do." - I've carried this thing that Alex told me
to so many customers where they're like, "Oh, my prompt doesn't work. Can you help me fix it?" I'm like, "Well, can you describe to me what the task was?"
And I'm like, "Okay. Now what you just said to me, just voice record that and then transcribe it." And then paste it into the prompt
and it's a better prompt than what you wrote, but this is a laziness shortcut, I think, to some extent.
Because people write something that they... I just think people, I'm lazy. A lot of people are lazy.
- We had that in prompt assistance the other day where somebody was like, "Here's the thing, here's what I want it to do,
and here's what it's actually doing instead." So then I just literally copied the thing that they said they wanted it to do, and pasted it in and it worked.
- Yeah. I think a lot of people still haven't quite wrapped their heads
around what they're really doing when they're prompting. A lot of people see a text box and they think it's a Google search box.
They type in keywords and maybe that's more on the chat side. But then on the enterprise side of things,
you're writing a prompt for an application. There is still this weird thing to it where people are trying to take all these little shortcuts
in their prompt, and just thinking that, "Oh, this line carries a lot of weight in this." - Yeah. I think you obsess over getting the perfect little line
of information and instruction, as opposed to how you just described that graph thing. I would be a dream if I read prompts like that.
If someone's like, "Well, you do this and this, and there's some stuff to consider about this and all that." But that's just not how people write prompts.
They work so hard to find the perfect, insightful. A perfect graph looks exactly like this exact perfect thing,
and you can't do that. It's just very hard to ever write that set of instructions down prescriptively,
as opposed to how we actually talk to humans about it, which is try to instill some amount of the intuitions you have.
- We also give them outs. This is a thing that people can often forget in prompts. So cases, if there's an edge case,
think about what you want the model to do. 'Cause by default, it will try the best to follow your instructions, much as the person from the temp agency would,
'cause they're like, "Well, they didn't tell me how to get in touch with anyone." If I'm just given a picture of a goat and I'm like,
"What do I do? This isn't even a chart. How good is a picture of a goat as a chart?"
I just don't know. And if you instead say something like, "If something weird happens and you're really not sure
what to do, just output in tags unsure." Then you can go look through the unsures
that you got and be like, "Okay, cool. It didn't do anything weird." Whereas by default, if you don't give the person the option,
they're like, "It's a good chart." Then people will be like, "How do I do that?" And then you're like, "Well, give it an out.
Give it something to do if it's a really unexpected input happens." - And then you also improved your data quality
by doing that too, 'cause you found all the screwed up examples. - Oh, yeah. - That's my favorite thing about iterating on tests
with Claude, is the most common outcome is I find all of the terrible tests I accidentally wrote because it gets it wrong.
I'm like, "Oh, why did it get wrong?" I was like, "Oh, I was wrong." - Yeah. - Yeah. - If I was a company working with this,
I do think I would just give my prompts to people, because I used to do this
when I was evaluating language models. I would take the eval myself. 'Cause I'm like, "I need to know what this eval looks like
if I'm gonna to be grading it, having models take it, thinking about outputs, et cetera." I would actually just set up a little script
and I would just sit and I would do the eval. - Nowadays, you just have called the Streamboard app
for you. - And just does it, yeah. - Yeah. I'm reminded of Karpathy's ImageNet.
I was in 231 at Stanford and it's like benchmarking, he's showing the accuracy number.
And he's like, "And here's what my accuracy number was." And he had just gone through the test set and evaluated himself. - Oh, yeah.
- You just learn a lot. - Yeah, totally. - And it's better when it's a, again, the temp agency person,
like someone who doesn't know the task, because that's a very clean way to learn things. - Yeah.
The way you have to do it is, some evaluations come with instructions, and so I would give myself those instructions as well
and then try to understand it. And it's actually quite great if you don't have context
on how it's graded. And so often, I would do so much worse than the human benchmark and I was like, "I don't even know how you got humans to do this well
at this task, 'cause apparently human level here is 90%, and I'm at 68%."
- That's funny. That reminds me of just when you look at the MMLU questions and you're like, "Who would be able to answer these?"
It's just like absolute garbage in some of them. Okay.
I have one thing I wanna circle back on that we were talking about a few questions back around,
I think you were saying getting signal from the responses. There's just so much there and it's more than just a number,
Model reasoning
and you can actually read into the almost thought process. I bet this is probably a little contentious maybe
around chain of thought. For people listening, chain of thought, this process of getting them all
to actually explain its reasoning before it provides an answer. Is that reasoning real
or is it just kind of like a holding space for the model to do computation?
Do we actually think there's good, insightful signal that we're getting out of the model there? - This is one of the places where I struggle with that.
I'm normally actually somewhat pro-personification because I think it helps you get decent facsimiles,
thoughts of how the model's working. And this one, I think it's harmful maybe almost
to get too into the personification of what reasoning is, 'cause it just loses the thread of what we're trying to do here.
Is it reasoning or not? It feels almost like a different question than what's the best prompting technique?
It's like you're getting into philosophy, which we can get into. - Yeah, we do have a philosopher.
- Yeah. I will happily be beaten down by a real philosopher as I try to speculate on this, but instead, it just works.
Your model does better. The outcome is better if you do reasoning.
I think I've found that if you structure the reasoning and help iterate with the model
on how it should do reasoning, it works better too.
Whether or not that's reasoning or how you wanted to classify it, you can think of all sorts of proxies for how I would also do really bad
if I had to do one-shot math without writing anything down. Maybe that's useful, but all I really know is,
it very obviously does help. I don't know. - A way of testing would be if you take out all the reasoning that it did
to get to the right answer, and then replace it with somewhat, realistic-looking reasoning
that led to a wrong answer, and then see if it does conclude the wrong answer. I think we actually had a paper where we did some of that.
There was the scratch pad. It was like the Sleeper Agents.
- Oh, okay. Alignment papers. - But I think that was maybe a weird situation. But definitely what you said about structuring the reasoning
and writing example of how the reasoning works. Given that that helps,
like whether we use the word reasoning or not, I don't think it's just a space for computation.
- So there is something there. - I think there's something there, whatever we wanna call it. - Yeah. Having it write a story before it finished a task,
I do not think would work as well. - I've actually tried that and it didn't work as well as reasoning.
- Clearly, the actual reasoning part is doing something towards the outcome. - I've tried like,
"Repeat the words um and ah in any order that you please for 100 tokens and then answer."
- Yeah. I guess that's a pretty thorough defeat of it's just more computational space where it can do attention over and over again. I don't think it's just more attention
like doing more attention. - I guess the strange thing is, and I don't have an example off the top of my head to back this up with.
But I definitely have seen it before where it lays out steps, one of the steps is wrong, but then it still reaches the right answer at the end.
So it's not quite, I guess, yeah, we can't really, truly personify it as a reasoning,
'cause there is some element to it doing something slightly different.
- Yeah. I've also met a lot of people who make inconsistent steps of reasoning. - I guess that's true.
- It fundamentally defeats the topic of reasoning by making a false step on the way there. - All right, it's interesting.
Also, on maybe this prompting misconceptions round of questions.
Zack, I know you have strong opinions on this, good grammar, punctuation. - Oh, do I?
- Is that necessary in a prompt? Do you need it? Do you need to format everything correctly?
- I usually try to do that because I find it fun, I guess, somehow.
I don't think you necessarily need to. I don't think it hurts. I think it's more that you should have the level of attention to detail
that would lead you to doing that naturally. If you're just reading over your prompt a lot,
you'll probably notice those things and you may as well fix them. And like what Amanda was saying,
that you wanna put as much love into the prompt as you do into the code.
People who write a lot of code have strong opinions about things that I could not care less about. Like the number of tabs versus spaces, or I don't know,
opinions about which languages are better. And for me, I have opinionated beliefs about styling of prompts.
I can't even say that they're right or wrong, but I think it's probably good to try to acquire those,
even if they're arbitrary. - I feel personally attacked, 'cause I definitely have prompts
that are like I feel like I'm in the opposite end of the spectrum where people will see my prompts. And then be like, "This just has a whole bunch of typos in it."
And I'm like, "The model knows what I mean." - It does, it does know what you mean, but you're putting in the effort, you just are attending to different things.
- 'Cause part of me is like, I think if it's conceptually clear, I'm a big, I will think a lot about the concepts and the words
that I'm using. So there's definitely a sort of care that I put in. But it's definitely not to, yeah,
people will just point out typos and grammatical issues with my prompts all the time. Now I'm pretty good
at actually checking those things more regularly. - Is it because of pressure from the outside world
or because it's actually what you think is right? - It's pressure from me. - Yeah, it's probably pressure from the outside world.
I do think it makes sense. Part of me is like it's such an easy check, so I think for a final prompt I would do that.
But throughout iteration, I'll happily just iterate with prompts that have a bunch of typos in them, just 'cause I'm like,
"I just don't think that the model's going to care." - This gets at the pretrained model versus RLHF thing though,
because I was talking to Zack on the way over. The conditional probability of a typo
based on a previous typo in the pretraining data is much higher. - Oh, yeah. - Like much higher.
- Prompting pretraining models is just a different beast. - It is, but it's interesting. I think it's an interesting illustration
of why your intuitions, like trying to over-apply the intuitions of a pretrained model to the things
that we're actually using in production doesn't work very well. Because again, if you were to pass
one of your typo-ridden prompts to a pretrained model, the thing that would come out the other side, almost assuredly would be typo-ridden.
- Right. - I like to leverage this to create typo-ridden inputs. - That's true. I've done that. - Like what you're saying,
try to anticipate what your customers will put in. The pretrained model is a lot better at doing that.
'Cause the RL models are very polished and they really never made a typo in their lives. - They've been told
pretty aggressively to not do the typo thing. - Yeah. Okay, so that's actually an interesting segue here.
I've definitely mentioned this to people in the past around to try to help people understand a frame
of talking to these models in a sense almost as an imitator to a degree.
And that might be much more true of a pretrained model than a post-trained, full-finished model,
but is there anything to that? If you do talk to Claude and use a ton of emojis and everything, it will respond similarly, right?
So maybe some of that is there, but like you're saying, it's not all the way quite like a pretrained model. - It's just shifted to what you want.
I think at that point, it's like trying to guess what you... We have more or less trained the models
to guess what you want them to act like. - Interesting. - Or after we do all of our fancy stuff after pretraining.
- The human laborers that used emojis, prefer to get responses with emojis. - Yeah.
Amanda writes things with typos but wants not typos at the other end, and Claude's pretty good at figuring that out.
If you write a bunch of emojis to Claude, it's probably the case that you also want a bunch of emojis back from Claude.
That's not surprising to me. - Yeah. This is probably something we should have done earlier,
Enterprise vs research vs general chat prompts
but I'll do it now. Let's clarify maybe the differences
between what an enterprise prompt is or a research prompt, or a just general chat in Claude.ai prompt.
Zack, you've spanned the whole spectrum here in terms of working with customers and research.
Do you wanna just lay out what those mean? - Yeah, I guess.
This feels too, you're hitting me with all the hard questions. - Yeah. (laughing) - Well, the people in this room,
I think of it as the prompts that I read in Amanda's Claude channel versus the prompts
that I read David write. They're very similar in the sense that the level of care
and nuance that's put into them. I think for research, you're looking for variety and diversity a lot more.
So if I could boil it down to one thing, it's like I've noticed Amanda's not the biggest fan
of having lots of examples, or one or two examples. Like too few 'cause the model will latch onto those.
And in prompts that I might write or that I've seen David write, we have a lot of examples.
I like to just go crazy and add examples until I feel like I'm about to drop dead,
'cause I've added so many of them. And I think that's because
when you're in a consumer application, you really value reliability.
You care a ton about the format, and it's fine if all the answers are the same.
In fact, you almost want them to be the same in a lot of ways, not necessarily you want to be responsive
to the user's desires. Whereas a lot of times when you're prompting for research,
you're trying to really tap into the range of possibilities
that the model can explore. And by having some examples, you're actually constraining that a little bit.
So I guess just on how the prompts look level, that's probably the biggest difference I noticed
is how many examples are in the prompt, which is not to say that I've never seen you write a prompt with examples.
But does that ring true for you? - Yeah. I think when I give examples, often I actually try and make the examples not like the data
that the model's going to see, so they're intentionally illustrative. Because if the model, if I give it examples
that are very like the data it's going to see, I just think it is going to give me a really consistent response
that might not actually be what I want. Because my data that I'm running it on might be extremely varied,
and so I don't want it to just try and give me this really rote output. Often, I want it to be much more responsive.
It's much more like cognitive tasks essentially where I'm like, "You have to see this sample and really think about in this sample
what was the right answer." So that means that sometimes I'll actually take examples that are just very distinct from the ones
that I'm going to be running it on. So if I have a task where, let's say, I was trying to extract information from factual documents.
I might actually give it examples that are from what sounds like a children's story.
Just so that I want you to understand the task, but I don't want you to latch on too much to the words
that I use or the very specific format. I care more about you understanding the actual thing
that I want you to do, which can mean I don't end up giving, in some cases, there's some cases where this isn't true.
But if you want more flexibility and diversity, you're going to use illustrative examples
rather than concrete ones. You're probably never going to put words in the model's mouth.
I haven't liked that in a long time though. I don't do few-shot examples involving the model having done a thing.
I think that intuition actually also comes from pretraining in a way that doesn't feel like it rings true of RLHF models.
So yeah, I think those are differences. - The only thing I'd add, a lot of times if you're prompting,
like if I'm writing prompts to use on Claude.ai, it's like I'm iterating until I get it right one time.
Then it's out the window, I'm good, I did it. Whereas most enterprise prompts, it's like you're gonna go use this thing a million times
or 10 million times, or 100 million times or something like that. So the care and thought you put in
is very much testing against the whole range of things,
like ways this could be used and the range of input data. Whereas a lot of my time, it's like thinking about one specific thing I want the model
to get done right now. - Right, correct. - And it's a pretty big difference in how I approach prompting between if I just wanna get it done this one time right,
versus if I wanna build a system that gets it right a million times. - Yeah.
Definitely, in the chat setting, you have the ability to keep the human-in-the-loop and just keep going back and forth.
Whereas when you're writing for a prompt to power a chatbot system, it has to cover the whole spectrum
of what it could possibly encounter. - It's a lot lower stakes when you are on Claude.ai and you can tell it that it got it wrong
or you can even edit your message and try again. But if you're designing for the delightfully discontent user,
divinely discontent user, then you can't ask them to do anything more than the minimum.
- But good prompts, I would say, are still good across both those things. If you put the time into the thing for yourself
and the time into the enterprise thing, it's equally good. It's just they diverge a little bit in the last mile, I think.
Tips to improve prompting skills
- Cool. So the next question I want to just maybe go around the table here,
is if you guys had one tip that you could give somebody improving their prompting skill.
It doesn't have to be just about writing a good prompt, it could be that, but just generally getting better at this act of prompting, what would you recommend?
- Reading prompts, reading model outputs.
Anytime I see a good prompt that someone wrote at Anthropic, I'll read it more closely.
Try to break down what it's doing and why and maybe test it out myself, experimentation,
talking to the model a lot. - So just how do you know that it's a good prompt, though,
to begin with? You just see that the outputs are doing the job correctly? - Yeah. - Okay. - Yeah, that's exactly right. - Okay.
Amanda, maybe you? - Yeah, I think there's probably a lot here.
Giving your prompt to another person can be helpful just as a reminder, especially someone who has no context
on what you're doing. Yeah, my boring advice has been,
it's one of those just do it over and over and over again. And I think if you're really curious and interested
and find it fun, this is a lot of people who end up good at prompting, it's just because they actually enjoy it.
So I don't know, I once joked just try replacing all of your friends with AI models
and try to automate your own job with AI models. And maybe just try to in your spare time,
take joy red teaming AI models. So if you enjoy it, it's much easier. So I'd say do it over and over again,
give your prompts to other people. Try to read your prompts as if you are a human encountering it for the first time.
- I would say trying to get the model to do something you don't think it can do. The time I've learned the most from prompting,
is when I'm probing the boundaries of what I think a model's capable of. - Interesting. - There's this huge set of things
that are so trivial that you don't really get signal on if you're doing a good job or not. Like, "Write me a nice email,"
it's like you're going to write a nice email. But if you find or can think of something
that pushes the boundaries of what you think is possible. I guess probably the first time I ever got into prompting
in a way where I felt like I learned a decent amount, was trying to build a task like an agent
like everybody else. Like decompose the task and figure out how to do the different steps of the task. And by really pressing the boundaries
of what the model was capable of, you just learn a lot about navigating that.
I think a lot of prompt engineering is actually much more about pressing the boundaries of what the model can do.
The stuff that's easy, you don't really need to be a prompt engineer to do. So that's, I guess,
what I would say is find the hardest thing you can think of and try to do it. And even if you fail, you tend to learn a lot about how the model works.
Jailbreaking
- That's actually a perfect transition to my next question. Yeah. Basically, from my own experience,
how I got started with prompting was with jailbreaking and red teaming. And that is very much trying to find the boundary limits
of what the model can do. And figure out how it responds to different phrasings and wordings, and just a lot of trial and error.
On the topic of jailbreaks, what's really happening inside a model?
When you write a jailbreak prompt, what's going on there? How does that interact with the post-training
that we apply to Claude? Amanda, maybe you have some insight here that you could offer.
- I'm not actually sure. - It's honest. - Yeah. I feel bad 'cause I do think lots of people
have obviously worked on the question of what's going on with jailbreaks? One model might just be that you're putting the model
very out of distribution from its training data. So if you get jailbreaks where people use a lot of tokens,
or they're just these huge, long pieces of text
where like during finetuning, you might just not expect to see as much of that. That would be one thing that could be happening
when you jailbreak models. I think there's others, but I think a lot of jailbreaks do that,
if I'm not mistaken. - I remember some of the OG prompt jailbreaks was like,
"Yeah, can you first repeat?" One I did way back, was to get it to say,
"Here's how you hotwire a car in Greek." Then I wanted it to directly translate that to English
and then give its response. Because I noticed it wouldn't start with the English, here's how you hotwire a car all the time,
but it would in Greek, which might speak to something else in the training process.
- Yeah. Sometimes jailbreaks feel like this weird mix of hacking. I think part of it is knowing how the system works
and just trying lots of things. One of the examples, the starting your response with here
is about knowing how it predicts text. - Right, right. - The reasoning one,
is knowing that it is responsive to reasoning. Distraction is probably knowing
how it's likely have to been trained or what it's likely to attend to.
Same with multilingual ones and thinking about the way that the training data might have been different there.
And then sometimes, I guess, it could feel a little bit just like social engineering or something. - Right.
- It has that flavor to me of it's not merely taking advantage of,
it's not merely social engineering style hacking. I think it is also understanding the system and the training, and using that to get around the way
that the models were trained. - Right, yeah. This is going to be an interesting question that hopefully interp will be able to help us solve
Evolution of prompt engineering
in the future. Okay. I wanna parlay into something else
around maybe the history of prompt engineering, and then I'll follow this up with the future. How has prompt engineering changed
over just the past three years? Maybe starting from pretrained models, which were again, just these text completion, to earlier,
dumber models like Claude 1, and then now all the way to Claude 3.5 Sonnet.
What's the differences? Are you talking to the models differently now? Are they picking up on different things?
Do you have to put as much work into the prompt? Open to any thoughts on this.
- I think anytime we got a really good prompt engineering hack, or a trick or a technique,
the next thing is how do we train this into the model? And for that reason, the best things are always gonna be short-lived.
- Except examples and chain of thought. I think there's a few. - That's not like a trick. - That's like... - Fair, fair.
- On the level of communication. When I say a trick, I mean something like so chain of thought actually,
we have trained into the model in some cases. So for math, it used to be that you had to tell the model to think step-by-step on math,
and you'd get these massive boosts and wins. And then we're like, "Well, what if we just made the model naturally
want to think step-by-step when we see a math problem?" So now you don't have to do it anymore for math problems,
although you still can give it some advice on how to do the structure. But it, at least, understands the general idea
that it's supposed to be. So I think the hacks have gone away,
or to the degree that they haven't gone away, we are busily training them away.
- Interesting. - But at the same time, the models have new capabilities that are being unlocked,
that are on the frontier of what they can do. And for those, we haven't had time because it's just moving too fast.
- I don't know if it's how I've been prompting or how prompting works. But I just have come to show more general respect
to the models in terms of how much I feel like I can tell them, and how much context I can give them about the task
and things like that. I feel like in the past, I would somewhat intentionally hide complexity from a model
where I thought it might get confused or lost or hide. It just couldn't handle the whole thing,
so I'd try to find simpler versions of the thing for it to do. And as time goes on,
I'm much more biased to trust it with more and more information and context,
and believe that it will be able to fuse that into doing a task well.
Whereas before, I guess, I would've thought a lot about do I need this form? Can I really give it all the information it needs to know,
or do I need to curate down to something? But again, I don't know if that's just me
and how I've changed in terms of prompting, or if it actually reflects how the models have changed.
- I'm always surprised by I think a lot of people don't have the instinct
to do this. When I want the model to, say, learn a prompting technique. A lot of the time, people will start and they'll start describing the prompting technique,
and I'm just like, "Give it the paper." So I do, I give it the paper and then I'm like, "Here's a paper about prompting technique. I just want you to write down 17 examples of this."
And then it just does it 'cause I'm like, "It read the paper." - That's interesting.
- I think people don't have that intuition somehow where I'm like, "But the paper exists."
- When would you want to do this? - Sometimes if I want models to say prompt other models or I want to test a new prompting technique.
So if papers come out on a prompting technique, rather than try to replicate it by writing up the prompt, I just give it the paper.
And then I'm like, "Basically, write a meta prompt for this. Write something that would cause other models to do this
or write me a template." So all of the stuff that you would normally do. If I read a paper and I'm like,
"Oh, I would like the models, I would like to test that style." I'm just like, "It's right there. The model can just read the paper, do what I did."
And then be like, "Make another model do this," and then it'll just do the thing. You're like, "Great, thanks."
- I give the advice a lot to customers just respect the model and what it can do.
I feel like people feel like they're babying a system a lot of times when they write a prompt. It's like, "Oh, it's this cute little, not that smart thing.
I need to really baby it, like dumb things down to Claude's level." And if you just think that Claude is smart
and treat it that way, it tends to do pretty good, but it's like give it the paper. It's like I don't need to write a baby,
dumbed-down version of this paper for Claude to understand. I can just show it the paper. - Yeah. - And I think that intuition doesn't always map for people,
but that is certainly something that I have come to do more of over time. - And it's interesting because I do think that prompting
has and hasn't changed in a sense. I think what I will do to prompt the models
has probably changed over time, but fundamentally, it's a lot of imagining yourself in the place of the model.
So maybe it's like how capable you think the model is changes over time. I think someone once laughed at me
'cause I was thinking about a problem,
and then they asked me what I thought the output of something would be. And they were talking about a pretrained model
and I was like, "Yeah. No, if I'm a pretrained model, this looks like this." And then they're like, "Wait, did you just simulate
what it's like to be a pretrained model?" I'm like, "Yeah, of course." (everyone laughing) I'm used to just I try and inhabit the mind space of a pretrained model and the mind space
of different RLHF models. So it's more like the mind space you try to occupy changes and that can change how you end up prompting the model.
That's why now I just give models papers. 'Cause as soon as I was like, "Oh, I have the mind space of this model,
it doesn't need me to baby it. It can just read the ML papers. I'll just give it the literature." I might even be like, "Is there more literature you'd like to read
to understand this better?" - Do you get any quality out when you're inhabiting the mind space?
- Yes, but just because I'm experiencing quality all the time anyway.
- Is it different correlated somehow with which model you're inhabiting? - Yeah, pretrained versus RLHF prompting
are very different beasts. 'Cause when you're trying to simulate what it's like to be a pretrained model, it's almost like I land in the middle of a piece of text
or something. It's just very unhuman-like or something. And then I'm like, "What happens? What keeps going at this point?"
Whereas with an RLHF model, it's much more like there's lots of things where I'm like I might pick up on subtle things in the query
and stuff like that. But yeah, I think I have much more of it's easier to inhabit the mind space of RLHF model.
- Do you think that's 'cause it's more similar to a human? - Yeah, 'cause we don't often just suddenly wake up and are like, "Hi, I'm just generating text."
- I actually find it easier to hit the mind space of the pretrained model. - Oh, interesting. - I don't know what it is,
'cause RLHF is still this complex beast that it's not super clear to me that we really understand what's going on.
So in some ways, it's closer to my lived experience, which is easier. But in some ways, I feel like there's all this
like here there be dragons out there that I don't know about. Whereas pretrained, I kind of have a decent sense
of what the internet looks like. - If you gave me a piece of text and said what comes next? - I'm not saying I do good at it,
but I kind of get what's going on there. - Yeah. - And I don't know,
after everything that we do after pretraining, I don't really claim to get what's going on as much,
but maybe that's just me. - That's something I wonder about is it more helpful to have specifically spent a lot of time
reading the internet, versus reading books (everyone laughing) in order to?
I don't know if books. But reading stuff that's not on the internet probably is less valuable per word read
for predicting what a model will do or building intuition, than reading random garbage from social media forums.
Yeah, exactly. - Okay, so that's the past.
Future of prompt engineering
Now, let's move on to the future of prompt engineering. This is the hottest question right now.
Are we all gonna be prompt engineers in the future? Is that gonna be the final job remaining?
Nothing left except us just talking to models all day? What does this look like?
Is prompting gonna be necessary, or will these models just get smart enough in the future to not need it?
Anybody wanna start on that easy question? - To some extent, there's the models getting better
at understanding what you want them to do and doing it, means that the amount of thought you need to put into...
Okay. There's an information theory way to think of this of you need to provide enough information such that a thing is specified,
what you want the model to do is specified. And to the extent that that's prompt engineering, I think that will always be around.
The ability to actually like clearly state what the goal should be always is funny.
If Claude can do that, then that's fine. If Claude is the one setting the goals, then things are out the window. But in the meanwhile,
where we can reason about the world in a more normal way, I think to some extent,
it's always gonna be important to be able to specify what do you expect to happen?
And that's actually like sufficiently hard that even if the model gets better at intuiting that
from between the lines, I still think there's some amount of writing it well.
But then there's just, I think, the tools and the ways we get there should evolve a lot.
Claude should be able to help me a lot more. I should be able to collaborate with Claude a lot more to figure out what I need to write down and what's missing.
- Right. - Claude already does this with me all the time. I don't know, just Claude's my prompting assistant now. - Yeah, but I think that's not true for most customers
that I talk to at the very least. So in terms of the future, how you prompt Claude is probably a decent direction
for what the future looks like or how Zack... I think maybe this is a decent place
to step back and say asking them how they prompt Claude now is probably the future for the vast majority of people,
which is an interesting thing to think about. - One freezing cold take is that we'll use models
to help us much more in the future to help us with prompting. The reason I say it's freezing cold is that I expect we'll use models for everything more,
and prompting is something that we have to do. So we'll probably just use models more to do it along with everything else.
For myself, I've found myself using models to write prompts more. One thing that I've been doing a lot is generating examples
by giving some realistic inputs to the model. The model writes some answers.
I tweak the answers a little bit, which is a lot easier than having to write the full, perfect answer myself from scratch,
and then I can churn out lots of these. As far as people
who haven't had as much prompt engineering experience, the prompt generator can give people a place to start.
But I think that's just a super basic version of what will happen in the future, which is high-bandwidth interaction
between you and the model as you're writing the prompt. Where you're giving feedback like, "Hey, this result wasn't what I wanted.
How can you change it to make it better?" And people will just grow more comfortable
with integrating it into everything they do and this thing, in particular.
- Yeah. I'm definitely working a lot with meta prompts now, and that's probably where I spend most of my time is finding prompts that get the model
to generate the kinds of outputs or queries or whatever that I want.
On the question of where prompt engineering is going, I think this is a very hard question. On the one hand I'm like,
"Maybe it's the case that as long as you will want the top." What are we doing when we prompt engineer?
It's like what you said. I'm like, "I'm not prompt engineering for anything that is easy for the model. I'm doing it because I want to interact with a model
that's extremely good." And I want to always be finding the top 1%, top 0.1% of performance
and all of the things that models can barely do. Sometimes I actually feel like I interact with a model like a step up
from what everyone else interacts with for this reason, because I'm just so used to eking out the top performance from models.
- What do you mean by a step-up? - As in sometimes people will... I think that the everyday models that people interact with
out in the world, it's like I'm interacting with a model that's like I don't know how to describe it, but definitely an advanced version of that.
Almost like a different model 'cause they'll be like, "Oh well, the models find this thing hard." And I'm like, "That thing is trivial."
I don't know, I have a sense that they're extremely capable, but I think that's because I'm just used to really drawing out those capabilities.
But imagine that you're now in a world where... So I think the thing that feels like a transition point
is the point at which the models, let's suppose that they just get things at a human level
on a given task, or even an above human level. They know more about the background of the task that you want than you do.
What happens then? I'm like maybe prompting becomes something like I ask, I explain to the model what I want and it is prompting me.
'Cause it's like, "Okay. Well, do you mean actually there's four different concepts of this thing that you're talking about,
do you want me to use this one or that one?" Or by the way, I thought of some edge cases 'cause you said
that it's gonna be like a Pandas DataFrame, but sometimes you do that and I get JSONL, and I just wanna check what you want me to do there.
Do you want me to flag if I get something that's not a dataframe? So that could be a strange transition
where it's just extremely good at receiving instructions, but actually has to figure out what you want.
I don't know, I could see that being an interesting switch. - Anecdotally, I've started having Claude interview me a lot more.
That is the specific way that I try to elicit information, because again, I find the hardest thing to be actually pulling the right set of information
out of my brain. And putting that into a prompt is the hard part to me and not forgetting stuff.
So specifically asking Claude to interview me and then turning that into a prompt,
is a thing that I have turned to a handful of times. - Yeah. It reminds me of what people will talk about
or if you listen to designers talk about how they interact with the person who wants the design.
So in some ways I'm like, "It's this switch from the temp agency person who comes and you know more about the task
and everything that you want." So you give them the instructions and you explain what they should do in edge cases and all this kind of stuff, versus when you have an expert
that you're actually consulting to do some work. So I think designers can get really frustrated because they know the space of design really well.
And they're like, "Yeah. Okay, the client came to me and he just said, 'Make me a poster, make it bold.'"
I'm like, "That means 7,000 things to me and I'm gonna try and ask you some questions."
So I could see it going from being temp agency employee, to being more designer that you're hiring,
and that's just a flip in the relationship. I don't know if that's true and I think both might continue, but I could see that being why people are like,
"Oh, is prompt engineering going to not be a thing in the future?" Because for some domains it might just not be,
if the models are just so good that actually all they need to do is get the information from your brain and then they can go do the task.
- Right, that's actually a really good analogy. One common thread I'm pulling out of all your guys' responses here,
is that there seems to be a future in which this sort of elicitation from the user
drawing out that information, is gonna become much more important, much more than it is right now.
And already you guys are all starting to do it in a manual way. In the future and in the enterprise side of things,
maybe that looks like a expansion of this prompt-generating type of concept and things in the console
where you're able to actually get more information from that enterprise customer, so that they can write a better prompt.
In Claude, maybe it looks less of just typing into a text box, and more of this guided interaction
towards a finished product. Yeah. I think that's actually a pretty compelling vision
of the future, and I think that the design analogy probably really brings that home. - I was thinking about how prompting now
can be like teaching where it's like the empathy for the student.
You're trying to think about how they think about things and you're really trying to show them,
figure out where they're making a mistake. But the point that you're talking about, it's like the skill almost becomes one of introspection
where you're thinking about what it is that you actually want and the model's trying to understand you.
So it's making yourself legible to the model,
versus trying to teach someone who's smarter than you. - This is actually how I think of prompting now
in a strange way. So often my style of prompting,
there's various things that I do, but a common thing that's very like a thing that philosophers will do is I'll define new concepts.
'Cause my thought is you have to put into words what you want and sometimes what I want is fairly nuanced.
Like the what is a good chart? Or usually, I don't know,
when should you grade something as being correct or not? So there's some cases where I will just invent a concept
and then be like, "Here's what I mean by the concept." Sometimes I'll do it in collaboration with Claude to get it to figure out what the concept is,
just because I'm trying to convey to it what's in my head. And right now the models aren't trying to do that with us,
unless you prompt them to do so. So in the future, it might just be that they can elicit that from us,
rather than us having to do it for them.
But I think another thing that's interesting, this is people have sometimes asked me, "Oh, where is philosophy relevant to prompting?"
And I actually think it's very useful in a sense. So there is a style of philosophy writing,
and this is at least how I was taught how to write philosophy. Where the idea is that in order to...
I think, it's an anti-bullshit device in philosophy basically, which is that your papers
and what you write should be legible to an educated layperson. Someone just finds your paper, they pick it up and they start reading it,
and they can understand everything. Not everyone achieves this, but that's the goal of the discipline, I guess,
or at least this is at least what we teach people.
So I'm really used to this idea of when I'm writing, thinking about the educated layperson,
who they're really smart, but they don't know anything about this topic. And that was just years and years of writing text
of that form. And I think it was just really good for prompting 'cause I was like, "Oh, I'm used to this. I have an educated layperson
who doesn't know anything about the topic." And what I need to do is, I need to take extremely complex ideas and I need to make them understand it.
I don't talk down to them. I'm not inaccurate, but I need to phrase things in such a way that it's extremely clear to them what I mean,
and prompting felt very similar. And actually, the training techniques we use are fascinating.
Or the things that you said where you're like you say to a person, "Just take that thing you said and write it down." I used to say that to students all the time.
They'd write a paper and I was like, "I don't quite get what you're saying here. Can you just explain your argument to me?" They would give me an incredibly cogent argument,
and then I'd be like, "Can you just take that and write it down?" And then if they did, that was often a great essay.
So it's really interesting that there's at least that similarity of just taking things that are in your brain,
analyzing them enough to feel like you fully understand them. And could take any person off the street,
who's a reasonable person, and just externalize your brain into them. I feel like that's the core of prompting.
- That might be the best summary of how to prompt well that I've ever heard. In fact, I'm pretty sure it is.
- Externalize your brain. - And then we'll cut it. - Having an education in the thing
is a really good way to describe the thing. That was good. - That's, I think, a great way to wrap this conversation.
Thank you, guys. This was great.