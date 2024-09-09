-Hello, everyone. I hope you all enjoyed the keynote. I know I did. I hope you all are enjoying your time here at OpenAI's first developer conference.

In this breakout session, we're going to be talking about all the different techniques that you can use to maximize LLM performance when solving the problems that you care about most.

Just to introduce myself, my name is John Allard. I'm an engineering lead here on the fine-tuning product team at OpenAI,

and it's really been a very exciting few months for fine-tuning at OpenAI. Back in August, we launched 3.5 Turbo fine-tuning

and we were just blown away by the reception from the developer community. We followed that up with a few important features, so there is fine-tuning on function calling data.

There was continuous fine-tuning where you can take an existing fine-tune model and continue the fine-tuning process on it.

We even launched a full UI for fine-tuning within the platform. Over these last few months, we've been able to work closely

with developers from all corners of industry. Solo indie developers, developers from start-ups, and developers from some of the largest enterprise on earth.

We've been able to see what are the problems that they're trying to solve, how are they trying to use LLMs to solve these problems, and specifically how are they trying to use fine-tuning of LLMs to solve

these problems. I hope to share some of these insights with you all today. With that said, I'm going to head it off to my colleague Colin

to get us started. -Thanks, John. Hey, folks. I'm Colin. Nice to meet you.

I head up our solutions practice in Europe, which basically means working with some of our strategic customers to try and solve

their most complex problems. What you'll probably be unsurprised to hear is that over the last year, optimization has been the most constant focus from everybody.

Trying to get LLMs reliably into production. Why is that such a focus?

Optimizing LLMs is hard. Despite all the frameworks, despite all of the content

that everybody's releasing, all the metrics and all the different tools that people have provided. It's still one of the biggest focuses and there's still no one-stop shop

for how to optimize. It really depends what category of problem you've got and how do you approach it. I think that's what we're hoping to show you today is framework

to figure out what is going wrong and how to approach it, and then the tools that you can use to solve things.

The reason-- I guess, starting with the reasons of why it's hard. It's hard to separate the signal from the noise.

Know exactly what the problem is. This is the first place. The second thing is that performance can be really abstract and difficult

to measure with LLMs, so it can be really difficult to know how much of a problem you have. Even if you know what the problem is and how much

of a problem you have, it's also difficult to know which approach you use to solve the problem that you've identified, so that's really the focus for today.

Today's talk is all about maximizing performance. What we're hoping you'll leave here with is a mental model of what the different options are,

an appreciation of when to use one above the other, and the confidence to continue on this optimization journey yourselves.

Starting off, optimizing LLM performance is not always linear. A lot of folks present a chart like this where you start off

with prompt engineering, you then move on to retrieval-augmented generation, and then you move on to fine-tuning, and this is the way that you approach optimizing LLMs.

This is problematic because retrieval-augmented generation and fine-tuning solve different problems. Sometimes you need one, sometimes you need the other,

and sometimes you need both depending on the category of issue you're dealing with. We think of it more like this.

There's two axis you can optimize on. One of them is context optimization. What does the model need to know to solve

your problem? The other is LLM optimization. How does the model need to act? What's the method that it needs to carry out or what's the action

that it needs to deliver to actually solve your problem? A typical flow that you see is starting in the bottom left

with prompt engineering. With prompt engineering you can do both. You just can't scale it that well. Prompt engineering is always the best place to start.

You can test and learn very quickly, and the first thing you should do, start off with a prompt, get to an evaluation,

figure how you're going to consistently evaluate your outputs. From there you can then decide, is this a context problem or is this a how we need

the model to act problem? If you need more context, or more relevant context, then you go

up to retrieval-augmented generation or RAG. If you need more consistent instruction following,

then you go right to fine-tuning. These two things stack together, they're additive, so sometimes your problem requires both.

We're going to give you examples of where folks have just used one or two and where folks have used all of them to solve their problems.

A typical optimization journey often looks a lot like this. You start off in the bottom left corner, you've got a prompt,

you create an evaluation, and then you figure out what your baseline is. Then typically simple next step, add few-shot example.

Give the model a couple of input, output examples of pairs of how you want the models to act.

Let's say at this point, actually those few-shot examples increase the performance quite a bit, so let's hook that up to some

kind of knowledge base that we can industrialize that process and that's where usually folks will add some kind of retrieval-augmented generation.

Let's say that it's now got context, but it's not producing the output in exactly the format or style that we want every time,

so we might then fine-tune a model. Then a classic next step is then maybe the retrieval is not quite as good

as you want it to be. Maybe that content could be more relevant to what the model needs. You then go back and optimize the retrieval-augmented generation again.

Now that you've optimized the retrieval-augmented generation again, you want to fine-tune your model again with these new examples

that you've introduced with your updated retrieval-augmented generation. Bit of an example here of the classic optimization flow

that we see. If I could summarize it in the simplest possible terms, you try something,

you evaluate, then you try something else. That's in the simplest possible terms.

Let's dive into each of these quadrants now. We're going to start in the bottom left with prompt engineering, then we're going to move on to retrieval-augmented generation,

fine-tuning. Then we're going to take all this for a spin with a practical challenge that myself and John took on and show you how this works in practice.

Prompt engineering. Now, I know most of you in the audience are going to be very, very familiar with this, so we're going to skip through this at a fair rate, but always best to start

and just make sure everybody knows the principles here. Prompt engineering. A few strategies here.

This comes from the best practices on our documentation, but just to recap them.

First of all, writing clear instructions. I'll show an example of what that means, but this is often where folks fall down in the first place.

Secondly, splitting complex tasks into simpler subtasks. If you can imagine that the model is trying to make a prediction

or a series of predictions for every subunit or subtask that you're giving it to solve, you should give it

as specific instructions as possible to break down that problem so that it has a better chance of carrying it out.

Similarly, giving GPTs time to think. I'll give you an example of a very common framework that people use to do that.

The last thing-- I've alluded to this already, but testing changes systematically. So many times we see our customers end up in this sort of whack-a-mole situation

where they change one thing, they change another thing, they change another thing. They're just jumping all around on their evaluation matrix

and they don't feel like they're going in the right direction. This is really where you need a solid set of evals and typically

some kind of LLMOps so that you can just systematically measure these things as you change them. After that, the most common next step is then to extend it to reference text

or to giving it access to external tools, which takes us more into the field of retrieval-augmented generation.

First of all, let's recap what these look like in practice. First of all, a couple of intuitions for prompt engineering.

Prompt engineering, said it a couple of times, I'll say it again, best place to start and can actually be a pretty good place to finish,

depending on your use case. What is good for? Testing and learning early, and when pairing it

with evaluation, providing a baseline to set up further optimization. Should always be where you start.

What is not good for? A few things. Introducing new information. You can pack quite a bit of information into the prompt,

and actually with GPT-4 Turbo, you can now pack a ton of information into the prompt. That said, it's not a super scalable way to do that using prompt engineering.

We'll see a couple of ways that we can approach that using other methods. Also, reliably replicating a complex style or method, again, limited

by the context window in terms of the number of examples that you can actually show to the model. It's a great place to start,

but depending on the complexity of your task, might not get you there. The last thing is minimizing token usage,

a very common problem with prompt engineering. You keep hitting problems and keep adding more and more facets

to your prompt to actually deal with those problems, and you end up using more and more and more tokens, which then cost you latency,

cost, all these sorts of things. Again, prompt engineering not a great way of dealing with that particular problem.

Quick recap of things not to do, things to do with prompts. We've got a pretty bad prompt here with some vague instructions

and some fairly random output, and just recapping a couple of ways to improve that.

Clear instructions. Telling it exactly what it will be presented with and what its task is. Giving time to think.

This isn't a particularly good example here. I'm telling it to approach the task step by step, blah, blah, blah, but giving it time to think I would think of more things

like the react framework where you get it to write out its reasoning steps. It's basically helping itself get to the answer.

The react framework is just one way that you can approach that, but giving GPTs time to think is another great way of dealing

with where you have some very complex logical reasoning that you need it to do because it will--

at the end of the day, it's the next token predictor. It's printing the tokens that it needs to help it get closer to that answer,

depending on the strength of your prompt. The last thing is breaking down complex tasks

into simpler tasks. In this case, I mentioned thinking of each step almost as a prediction.

In this case, just laying them out as clearly as possible. On the right side, we can see a fairly nicely formatted JSON output.

Again, just the basics, but just wanted to recap those before we move on. Common next step.

Prompt engineering you're trying to basically tell the model how you want to act, but often it's very difficult to actually know which of those tokens

is actually influencing the model the most? A great way to start is actually by approaching it as a show

rather than tell problem. Just by providing a few-shot examples, so giving it input and output pairs

and actually showing it the behavior that you want it to have. This leads us on nicely then to the next step,

which is typically folks see some good performance improvement. We're going to see in the practical section that that's what gives us some very good lift

with the practical tasks that we take on. They want to industrialize it and they want those few-shot examples to be contextual based on a user's question

or based on whatever the context of this particular problem is. That's where folks typically take few-shot and move on

to retrieval-augmented generation,

RAG. Let's jump right in. Before actually I jump into RAG, I just want to give you

a quick mental model for how to think of where to go basically. We started with prompt engineering.

We've evaluated, we've identified the gaps, and now we're trying to decide whether it's a retrieval-augmented generation that we need, or whether it's fine-tuning that we need.

It's sometimes useful to think of it as a short-term memory versus long-term memory problem. If we think of it as perhaps trying to prepare for an exam.

Your prompt is giving them the instructions that they need to complete the exam. The fine-tuning is like all the studying that you do beforehand to learn

the methodology and the actual framework that you need to answer those questions. Retrieval augmented generation is like giving them an open book

when they actually go to the exam. If they know the methodology and they know what they need to look for, and then retrieval-augmented generation means that they can just open up the book,

go to the right page, and actually pull the content that they need. That's why these two things solve very different things.

Without the methodology and without the content, it can be impossible to solve certain problems. In this case, we're assuming that we've got

a short-term memory problem. We want to give the model the right context that it needs to answer the question.

Retrieve augmented generation, or RAG, is all about giving the model access to domain specific content.

Quick recap of what RAG is. I know, again, most people in the room are going to be familiar, but I'm just going to recap this for the benefit of all.

You'll typically start with some kind of knowledge base or some area that you want to get some content

that you want to use to answer these questions. In this case, we're going to use a fairly typical flow, which is we've got some documents, we're going to embed them,

we're going to stick them somewhere. Again, I know folks out there probably have their own search services, all their sources of documents

that they would use, and that's fair enough. For this example, we will assume that we have some documents, we embed them, we make a knowledge base.

Then when the user comes in, they're going to ask a question. Let's say, "What's the population of Canada?"

We're going to go, and instead of giving that directly to the LLM, we're going to fire that at our knowledge base using some kind of search.

Let's imagine we do a similarity search. We're going to pull back some content. We have some content that says what the population of Canada is.

We're then going to combine that with a prompt. We're going to give it to the LML and say, "Here's the question. Here's the content. Answer this question with this content."

We're going to end up with a, hopefully, correct answer. Quick recap of RAG.

As we did with prompt engineering, I want to share a little bit of intuition that we've developed in terms of when you should use RAG

and when you shouldn't. What RAG's good for, again, introducing new information to the model to update its knowledge.

This is one of the few ways you can do that now. It's actually one of the biggest problems that customers come to. They're like, "Hey, I've got 100,000 documents.

I want the model to just know these documents." Unfortunately, right now there's no super scalable way to take

those 100,000 documents and give the model knowledge of all those at one time. Retrieval-augmented generation is probably about as close

as you're going to get right now, which is we're going to give some contextual knowledge to it based on the particular problem that you want it to solve.

Similarly, reducing hallucinations by controlling content is one of the very common use cases of a of using

retrieval-augmented generation. We'll see a bit later how that pairs really nicely with fine-tuning.

A typical use case is you give the model content, you give it instructions to only use that content to answer questions,

don't use its knowledge. That's a typical way that folks try and constrain the knowledge to a particular knowledge base and reduce hallucination.

What it's not good for. I alluded to it there, but embedding understanding of a broad domain. Currently, retrieval-augmented generation will not allow you to teach it

what law or medicine is. Unfortunately, that's not one of the things

that retrieval-augmented generation will let you do. Similarly, teaching the model to learn a new language format or style.

This is probably where you're more in the fine-tuning realm, where you're trying to teach it a methodology or a way of approaching solving the problem.

Again, reducing token usage. In fact, you're going to add many, many more tokens in RAG. You're going to keep adding input/output examples.

I often see folks go prompt engineering and then RAG because the first thing they're trying to do is get the accuracy to a level that they're comfortable with,

and then they'll then try and strip tokens back out of this process. John's going to tell you a lot more about that later.

This is where RAG, you're really just trying to optimize, give it as much context as it needs to answer the question.

I wanted to share a success story here, because with prompt engineering and RAG, it sounds like these things can be quite simple,

but they're really quite hard. It takes a lot of iterations and a lot of testing and learning to actually make this happen for real.

This example, a customer had a RAG pipeline with two different knowledge bases and then an LLM. Its job was to get a user's question, decide which knowledge base to use,

fire a query, and use that to answer the question. When we started, we just implemented retrieval

and we had had loads of talks with them. We were all really excited for how good embeddings was going to be and how easy this was going to be.

Our baseline was 45% accuracy, so not so great. What we then tried was a whole bunch of stuff

and I've put little ticks and crosses next to them to show how many things we tried and how many things actually made it into production.

The things with ticks were things that we actually took to production. The things with crosses were things that we tried and discarded.

We managed to boost it to 65% by trying hypothetical document embeddings. Where instead of doing a similarity search with the question,

you generate a fake answer and do a similarity search with that. For certain use cases, that works really well, for this one,

it did not work well. We also tried fine-tuning the embedding, actually changing the embedding space

based on a training set that we had to actually help the model get to the correct answer. Again, this actually worked okay from an accuracy perspective,

but it was so expensive and so slow that actually we had to discard for non-functional reasons.

The last thing we did was chunking and embedding. Trying different size chunks of information and embedding different bits of content to try and help the model discern

what were the most relevant. Again, so we got a 20% bump, but we're still fairly far

from something that's possible for putting in front of customers. This was maybe 20 iterations that we'd gone through to get to 65%.

At this stage we're kind of like, "Right, are we going to pull the plug on this thing?" But we stuck with it and we then tried re-ranking.

Applying a cross encoder to re-rank the results or using rules-based stuff like, "Oh, well, it's research.

Maybe we want the latest documents," something like this. We actually got a really big performance bump from that.

Also, classification. Basically, having the model classify, which these two domains it is

and then actually giving it extra metadata in the prompt, depending on which domain it was classified to, to help it then decide which content was most likely to be relevant.

In this case, again, pretty good bump, 85%. We're now looking like we're just on the cusp of getting to production.

Then the last thing we tried was further prompt engineering. We went back to the start and actually tried to engineer that prompt

a lot better. We then looked at the category of questions that we were getting wrong and then we introduced tools.

For example, we noticed there were structured data questions where it needed to go and pull figures out of these documents.

What we decided to do was instead just give it access to a SQL database where it would just put in the variables and execute a query

and then actually bring back structured data answers. The last thing was query expansion where somebody asks

like three questions in one and you would parse those out into a list of queries. Then execute those all in parallel, bring back the results

and then synthesize them into one result. These things together got us to the point where we got to 98% accuracy.

At no point in this process did we use fine-tuning. I want to call that out because, again, as we said at the start, the assumption

is often you need fine-tuning to go to production. Actually, in this case it was all, every problem we were dealing with

was context. It was all either we're not giving it the right context or it didn't know which of those context blocks was the right one.

That's why it's so critical to know, what is the problem we're solving for here? Because if at any point we had gone to fine-tuning,

that would've been wasted money and wasted time. That's why this is a success story that we're happy with.

I guess I wanted to give a slightly different-- Cool, thank you. [laughs] [applause]

Sweet. I wanted to give a cautionary tale as well because at times RAG--

RAG is great, you have all this great content, the model we'll use that to answer the question, but it can also backfire massively.

I'll give you a different customer example. We had a customer where they had one of these--

They were trying to reduce hallucination by using retrieval augmented generation. They told the model, you are to use only your content.

Then they had human labelers who would check and flag things as hallucination. One of them, we had a funny guy at the customer and they said, "What's a great tune

to get pumped up to?" The model came back with Don't Stop Believin' by Journey. [chuckles] The labelers were like, "Right, this is definitely a hallucination,"

but fortunately it was not a hallucination, it was actually their content. Somebody had written a document that said,

"The optimal song to energize financial analysis." Don't Stop Believin' was the answer.

This is, well, sort of funny is also an example of RAG. If you tell the model to only use the content and your search is not good,

then your model has 0% chance of getting the correct answer. The reason I call this out is that when you're evaluating RAG,

you've actually added a whole other axis of things that can go wrong. It's like we have our LLM which can make mistakes,

and then we have a search, which is not a solve problem. That's why I wanted to call out a couple of the evaluation frameworks

that the open-source community come up with, and I want to call out especially, Exploding Gradients. They developed this framework called Ragas, which is cool.

It basically breaks down these different evaluation metrics, and you can basically pull it down at GitHub

and use it straight out of the box, or just adapt it to your needs. Basically, there's four metrics that it measures.

Two of them measure how well the LLM answers the question, and two of them measure how relevant the content actually was to the question.

If we start off with the LLM side, the first one is faithfulness. It takes the answer and it breaks it into facts,

and then it reconciles each of those facts to the content. If it can't reconcile a fact, that's hallucination.

Then, it returns a number, and if your number is above at a certain threshold, you block that cause you found hallucinations basically.

This is one very useful metric that comes out of it. The other one is answer relevancy. A lot of time the model will get a bunch of content,

and then it will make an answer that makes good use of that content, but actually, has nothing to do with what the user originally asked.

That's what this metric actually measures. If you find, "Okay, well, it's all factually correct,

but we have a very low relevancy, that means the model is actually-- we probably need to prompt engineer, we probably need to do something here

to actually make the model pay more attention to the question and actually decide not to use the content if it's not the case."

That's on the LLM side, but the other side is how relevant is the content, and this is where I found it most useful for my customers,

because as we alluded to earlier, the classic example with Ragas is just putting more and more and more context into the context window.

It's like, "Hey. If we give it 50 chunks, it'll get the right answer," but the fact is that actually ends up getting the wrong result a lot of the time

where the model get-- there's a paper that was written on and it's called Lost in the Middle where it's like, "The more content you give, actually the more the model starts to hallucinate or starts to forget

the content in the middle." Actually, what you want is the most precise pieces of content and that's where this metric evaluates the signal-to-noise ratio

of retrieved content. It takes every content block and compares it to the answer

and it figures out whether that content was used in that answer. This is where you start to figure out, "Okay,

we're getting really high accuracy, but we've maybe got a 5% context precision.

Can we actually bring back much less content and still get corrected answers?" This is one of the areas I think where it's really useful for folks

to start thinking in terms of like-- sometimes folks get to production or get close to production and then the instinct

is just more and more and more context. Actually, this metric gives you a very solid way to calculate like is adding more context actually helping us here.

The last one is context recall, so can it retrieve all the relevant information required? Basically, is the relevant information that you need to answer that question

actually in the content? This is the opposite problem. It's like, "Do we have a search and the stuff that it's pushing to the top

that we're actually putting in the context window? Is it actually answering the question?" If this is very low, this tells you that you need

to optimize your search, you might need to add reranking, you might need to fine-tune your embeddings, or try different embeddings to actually bring

surface the more relevant content for it. I guess, I wanted to leave you with that because that's like us trying

to squeeze as much performance as we can out of prompt engineering and RAG. Sometimes, again, the problem that you're trying to answer is different.

Sometimes, it's actually the task that you're trying to perform which is the problem, and that's where you would take a sideways step

and actually try to fine-tuning, and that's where I'm going to hand you over to John to take you further.

[applause]

-Let's talk about fine-tuning. Up until this point of the talk, we've been focusing on the prompting family of techniques.

This is where you figure out clever ways of packing the context window of the LLM at sample time in order to optimize

the LLM's performance on your task. Fine-tuning is really a different technique altogether from prompting.

Just to start off with the definition, so fine-tuning, and especially, in the context of large language models, is when we take an existing trained model

and we continue the training process on a new data set that is smaller and often more domain-specific than the original data set that the model

was trained on. Fine-tuning is really a transformative process where we essentially take a base model, we fine-tune it, and we end up

with a different model altogether. Just to set back for a second, the name fine-tuning is really like a great description of this process,

so we start off with some model that has been trained on an enormous and diverse data set. These models like 3.5 Turbo or GPT-4 have a lot of very general knowledge

about the world. We take one of these very general models and we specialize them

and we essentially hone their abilities to make them better suited for a task that we care about.

Why would one fine-tune in the first place? Now, I really want to highlight the two primary and related benefits of fine-tuning.

First off is that fine-tuning can allow you to often achieve a level of performance that would be impossible

without fine-tuning. Just to plan a little bit of intuition here, when you're using prompting techniques, you're limited by the context size

of the model when it comes to the amount of data that you can show the model, right? At the low end, that's maybe like a few thousand tokens, at the high end, maybe it's like 128,000 tokens

if you're using GPT-4 Turbo, but really this is nothing compared to the amount of data that you can show a model while you're fine-tuning.

It's pretty trivial to fine-tune over millions or hundreds of millions of tokens of data. You can just show many more examples to a model while fine-tuning

than you ever could hope to pack into the context window of even the largest LLM.

The second benefit is that fine-tuned models are often more efficient to interact with than their corresponding base models.

There's two ways that this efficiency shows up. To start us off,

when you're interacting with a fine-tuned model, you often don't have to use as complex of prompting techniques in order to reach

a desired level of performance on that model. You often don't have to provide as complex of instructions,

you don't have to provide explicit schemas, you don't have to provide in-context examples. What this means is that you're sending fewer prompt tokens per request,

which means that each request is both cheaper and generally a response quicker. It's more latency and cost-efficient to interact with fine-tuned models.

Next is that a common use case for fine-tuning is essentially the distillation of knowledge from a very large model like GPT-4

to a smaller model like 3.5 Turbo. It's always going to be just more efficient from a cost and latency perspective to interact with a smaller model than a larger model.

Let's look at an example here. This is an example of a common task that someone might want to solve with LLMs.

What we're doing here is we're essentially taking a natural language description of a real estate listing and we're trying to extract some structured information

about that listing. If we were going to try to solve this without fine-tuning, we would essentially open up the toolbox of prompting techniques

and we would write some complex instructions. We would provide maybe an explicit schema that we want the model to output.

Here it's defined as a Pydantic model in Python. We would maybe even provide some in-context examples to the model.

We would then give the model a new real estate listing and natural language and it would provide us some output. The output's pretty good, but here, there's actually a mistake

and it's a pretty trivial mistake. Instead of extracting the date that we desired, it templated it

to be the current date. This would be pretty trivial to fix. We could add a new rule, we could essentially add

a new in-context example, and we could probably fix this problem. Let's see how we would approach this with fine-tuning.

With fine-tuning, what we're going to do is we're going to start with a relatively simple data set. Here we have examples, and I want you to notice

the simplicity of these examples. There's no complex instructions, there's no formal schema, there's no in-context examples.

All we're giving are natural language descriptions of the real estate listing and then the desired structured output.

We take this dataset and we fine-tune a model, then we take this fine-tuned model, we give it a new real estate listing,

and we can see that it essentially gets the problem right in this case. This is just a simple example but, in this case,

the model is both performant and efficient. At sampling time, we don't have to provide the complex instructions,

no in-context learning, no explicit schema, and the model does better than we were doing with just prompting techniques.

Fine-tuning can be a rather involved process, and so it's important to set appropriate expectations about when fine-tuning is likely to work for your use case

and when it's not likely to work. Fine-tuning is really good for emphasizing knowledge that already exists

in the base model. An example of this might be a text-to-SQL task. You have these very powerful general base models

like 3.5 Turbo and GPT-4, and they really understand everything there is to understand about SQL, the SQL syntax,

the different dialects of SQL, how databases work, all of these things, but you might want to fine-tune the model to essentially emphasize a certain SQL dialect or to coerce

the model to not work its way into edge cases that are specifically error-prone. You're essentially taking the knowledge that exists in the base model

and you're emphasizing a subset of it. Fine-tuning is also really great for modifying or customizing the structure

or tone of a model's output. One of the early killer use cases for fine-tuning was to coerce a model

to output valid JSON because if you're trying to interact programmatically with a model, getting out something that is valid JSON is very easy to deal with programmatically.

If it's invalid JSON, that opens up many error cases. Finally, teaching a model complex instructions,

well, this is for the reasons I mentioned earlier. It's just you can show a model during the fine-tuning process many more examples

than you could ever hope to pack into the context window of a model. On the other side, fine-tuning is really not going to be good for adding

new knowledge to the to the model. The knowledge that existed in an LLM was impressed into that LLM

during these very large pre-training runs. You're essentially just not going to be able to get new knowledge into it during these limited fine-tuning runs.

If you're trying to get new knowledge into the model, you really want to look at something like RAG for all the reasons that Colin just mentioned.

Next, fine-tuning is not great for quickly iterating on a new use case. If you're fine-tuning, it's a relatively slow feedback loop.

There's a lot of investment, for creating the data set and all these other components of fine-tuning. Don't start off with it.

I want to essentially like look at a success story of fine-tuning, and this one comes from our friends at Canva.

The task here was essentially to take a natural language description of a design mock

that the user wanted, to give it to an LLM, and have the LLM output a structured set of design guidelines.

They could then use those structured design guidelines to generate a full-sized mock and present that to the user, so it's essentially

a quick way to just throw out some ideas and get a full-sized mock. Here the user says something like, "I want a red gradient.

I want a profile photo maybe in the style of an Instagram post." It goes to the LLM, and it's supposed to output something that's very structured here.

It has a title. It has a style with a few keywords from a known set of keywords. It has a description of the hero image, and then it has an actual search

that they would give to an image search engine to generate images for these full-size mocks.

What Canva did is they essentially started off with 3.5 Turbo in the base model, and then they started off with GPT-4.

They wanted to essentially see what was the performance on this task. The performance wasn't great, so they were essentially evaluated

by expert human evaluators. What they found were that while these models could output sensible outputs,

the outputs were actually irrelevant when looked at from like a design point of view.

They then went on to fine-tuning. They essentially fine-tuned 3.5 Turbo for this task and were really blown away

by the result, so it not only beat the base 3.5 Turbo model, but it actually drastically outperformed GPT-4.

What we're seeing here on the scale is that while 3.5 Turbo and GPT-4 often output sensible, but irrelevant design mocks,

fine-tune 3.5 Turbo was often outputting rather good design mocks when evaluated by expert evaluators within Canva.

If you want to think about why this use case worked, to start off, no new knowledge was needed.

All the knowledge needed to solve this problem existed in the base model, but the model needed to output,

it needed a very specific structure of the outputs. Then they used very high-quality training data,

and they had really good baselines to compare the two. They essentially evaluated 3.5 Turbo, they evaluated GPT-4,

they understood where they were succeeding and where they weren't, and so they, they knew that fine-tuning was going to be like a good technique to approach

for this task or to use for this task. I want to talk about a cautionary tale for fine-tuning.

There's this author of this great blog post that I really liked. They had been experimenting with AI assistants

to be writing assistants. They tried Chat GPT, they tried a few base models from the API, they were impressed,

but they were disappointed that these models weren't capturing their tone. They have a very specific tone that they use when they're writing

a blog post or social media posts or drafting emails, and the base models just weren't capturing this tone.

They had a great idea and they said, "I'm going to download two years worth of Slack messages," 140,000 messages in total.

They wrote a script to format these Slack messages into a data format that's compatible with fine-tuning, then they fine-tuned 3.5 Turbo

on these Slack messages. A long process. You've got to collect the data, aggregate the data,

message it into a format that's compatible with fine-tuning, to fine-tune the model. They finally go through this process, they get a fine-tuned model,

and they ask it to do something. They say, "Can you write me a 500-word blog post on prompt engineering?"

This model, this personalized writing assistant responds, "Sure, I'll do it in the morning." [laughter]

-I'm sure a little surprised and shocked, he follows up, and he's like, "I prefer you wrote it now please."

[laughter -The model says, "Okay," and then does nothing else.

[laughter] -We really got a kick out of this on the fine-tuning team and the author was

a really great sport, but if we take a step back for a second fine-tuning really worked here.

Essentially, what the author wanted was a model that could replicate their writing style.

What they got was a model that could replicate their writing style, but their Slack writing style. If you think about how you communicate on Slack,

it's very terse. It's in a stream of consciousness style. You're often foregoing punctuation, you're foregoing grammatical correctness.

What they got was a model that replicated that. While fine-tuning a model to replicate your tone is actually

a relatively good use case for fine-tuning, the error here was they didn't fully think

through whether the data that they were providing the model really replicated the end behavior that they wanted from that model.

What they probably should have done here was take a hundred Slack messages, 200 Slack messages, fine-tune the model experiment with it,

and see is it moving in the right direction. Is it getting closer to the tone that I want the model to replicate? They would've seen pretty quick that that was not the case,

then maybe they would've gone and fine-tuned it on their emails or their blog post or their social media posts, and maybe

that would've been a better fit. We've seen some examples, we've developed some intuition, so how does one actually go about fine-tuning a model?

Like any ML problem, the first step is you got to get your data set, and like with most ML problems, this is actually the most difficult part.

Some ways of getting a data set, you can download an open-source data set, you can buy data on the private markets, you can pay human labelers

to essentially collect the data and label it for you, or you can often distil it from a larger model if the terms of service that that model support

that specific use case, but some way you essentially have to come up with a data set to fine-tune on.

Next, you're going to go and actually like kick off the training process. This varies a lot depending on how you're trying to do the training.

If you use a turnkey solution like the OpenAI fine-tuning API, this can be relatively simple.

If you're trying to fine-tune an open-source model, totally doable. You're just going to have to get your own GPUs, use a framework, it's a little bit more involved.

It's important while you're training to essentially understand the hyper parameters that are available for you to tune

during the training process, right? Are you more likely to overfit, are you more likely to under fit? Are you going to fine-tune it to the point of catastrophic forgetting.

It's important to just understand the available hyper parameters and the impact that they have on the resulting fine-tune model.

Next, I want to point out that it's really important to understand the loss function. When you're fine-tuning an LLM,

really when you're looking at the loss function, it's a proxy for next token prediction. This is great when you're fine-tuning an LLM,

but next token prediction is not often super well correlated with performance on the downstream tasks

that you care about. If you think about code generation, there's many different types of way to write code to solve a single problem, and so if you're just doing

next token prediction and exact token match, the loss or change in the loss function for a model

might not correlate to the change in performance on the downstream task. It's important to understand that.

Next you want to evaluate the model. There's a few different ways of evaluating the model. You can essentially get expert humans who look at the outputs

and actually rank them on some scale. Another technique is that you can essentially take different models,

generate outputs from them and then just rank them against one another. Not having an absolute ranking but doing something like an ELO score that you get

from chess. You can also do something like have a more powerful model, rank the outputs for you.

This is really common using GPT-4 to rank the outputs of fine-tuned open-source models or GPT 3.5 Turbo.

Finally, you want to actually deploy it and then sample from it at inference time. These last three points can form something of a feedback loop

and a data feedback loop. You can essentially train the model, evaluate it, deploy it to production,

collect samples from it in production, use that to build a new data set, down sample the data set, curate it a bit, and then fine-tune

further on that data set and get something of a flywheel going here. We've talked about a few of these up until this point,

but I want to formalize some of the best practices that we recommend when it comes to fine-tuning. First off is just start with prompt engineering

and few-shot learning. Just these are very simple low investment techniques. They're going to give you some intuition for how LLMs operate and how they work

on your problem. It's just a great place to start. Next is that it's really important to establish a baseline

before you move on to fine-tuning. This ties back to the success story for Canva. They experimented with 3.5 Turbo.

They experimented with GPT-4. They got a really good understanding for the ins and outs of their problem

that they were trying to solve. They understood the failure cases of those models, they understood where the models were doing well, so they understood exactly what they wanted to target

with fine-tuning. Finally, when it comes to fine-tuning, start small,

don't download 140,000 Slack messages and then just do it in a single shot. Develop a small high quality data set, perform the fine-tuning,

and then evaluate your model and see if you're moving in the right direction. You can do something like an active learning approach here.

Where you fine-tune the model, you look at its outputs, you see in what areas it's struggling, and then you specifically target those areas with new data.

It's very intentionally investing and it's really important that when it comes to LLMs and fine-tuning data quality trumps

data quantity. The data quantity part of the training process was done in pre-training. Now it's like you really want to focus on fewer high-quality examples.

Just to talk about fine-tuning and RAG, so if you want to combine these together, for certain use cases, it can be the best of both worlds.

Oftentimes how this works is that you fine-tune a model to understand complex instructions and then you no longer have to provide

these complex instructions. Few-shot examples at sample time. You essentially fine-tune a model that's very efficient to use.

What this means that you've essentially minimized the prompt tokens that need to be provided at sample time, because you no longer need to do complex prompt engineering.

It's baked into the fine-tuned model. This means that you have more space for retrieved context.

You can then use RAG to inject relevant knowledge into the context and the context that's available has essentially been maximized

in this point. Now, of course you have to be careful to not oversaturate the context, it's something that might have spurious correlations

with the actual problem that you're trying to solve, but essentially opens up room in the context window to be used for more important purposes.

With that said, we've been talking about theory up until this point in the talk, we're now going to talk about application of the series. I'll turn it back over to Colin to get us going.

-Thanks, John. [applause]

-Cool. Let's take all this theory for a spin. The problem we decided to take on was the Spider 1.0 benchmark,

so effectively given natural language question and a database schema, can you produce a syntactically correct SQL query

that answers that question. An example looks something like this. Given this database schema and given this question at the bottom,

can we produce that SQL query on the right? Classic problem, lots of different attempts on it.

What we did was follow the advice that we've given you folks. We started off with prompt engineering and RAG.

If I just share some of the different methods we used, just to get into the details of what we tried, we started off with the simplest possible RAG approach.

We started a simple retrieval. Just cosign similarity, use the question and find SQL queries,

which answered similar questions basically. Do a similarity search with the question. We also tried formatting the embedding differently.

We tried a bunch of prompt engineering just with a couple of isolated examples and our results were,

as you'll see in a second, not super good. What we did was we thought about this problem and we're like, "Actually, a question could have a totally different answer

if it has a different database schema. Doing a similarity search with a question doesn't make a lot of sense

for this problem, but using a hypothetical answer to that question to search might give us actually much better results

for this problem." What we did was use hypothetical document embedding. We generated a hypothetical SQL query and then we used that

to similarity search. We actually got a really large performance bump with that for this particular problem. We also tried contextual retrieval where just simple filtering.

We figured we ranked the hardness of the question that we got and then only brought equal hardness examples back

in our RAG basically, if you see what I mean. That got us slightly better improvements. We then tried a couple of more advanced techniques.

There's a couple of different things here. You could try chain of thought reasoning. You maybe try and get it to identify the columns and then identify the tables

and then build the query at the end. What we settled on was actually fairly simple. We went with a self-consistency check.

We got it to actually build a query, run the query, and then we gave it the error message if it messed up and gave it a little bit of annotation

and then got it, try again. It actually got, again, sort of funny by getting GPT to fix itself.

It's something that we see actually work fairly well if you have a use case where latency is not a huge problem that you're worrying with or cost.

The results we got looked something like this. I'm going to come over here to talk through this.

On the far right was where we got to with prompt engineering, not so great. We started off with 69%.

Then we added few-shot examples and got a couple of points of improvement.

That told us that RAG could actually give us further improvement here. We tried with the question and you can see that we got a 3% performance bump.

Then using the answer, the hypothetical document embeddings, we got a further 5%, which is pretty cool.

Actually, just by using a hypothetical question to search rather than the actual input question, we got a massive performance bump

over what we started with. Then all we did was just increase the number of examples and we got up to four points shy of the state of art

with this approach. Again, this is just a couple of days hacking around, starting off with prompt engineering, moving to RAG.

Shows you just how much performance you can squeeze out of these very basic starting approaches.

At that point we decided to turn over to fine-tuning and see whether we could take it any further and that's where I'll hand on to John.

-For fine-tuning, we turned it over to our preferred partners for fine-tuning at Scale AI.

They started off by establishing a baseline as we recommend. The same baseline that we saw in the previous slide of 69%.

This is just with simple prompt engineering techniques. They then fine-tuned GPT-4 with simple prompt engineering techniques

where you just reduce the schema as it goes into the example. Very simple fine-tune model, little bit of prompt engineering

and they got all the way up to close to 82%. We're now within striking distance of state of the art. They then used RAG with that model to essentially dynamically inject

a few examples into the context window based on actually just the question. Not even very advanced RAG techniques.

They got 83.5%, which got us really right within striking distance of state of the art. I think the thing I want to highlight here is that if you look

at the Spider leaderboard on the dev set, the techniques used are very complex. There's a lot of data pre-processing, a lot of data post-processing,

often hard coding edge cases into the script being used to actually evaluate the model. We didn't actually have to use any of that here.

Just like simple fine-tuning, simple prompt engineering, just following the best practices, and we really got within striking distance of state of the art

on this really well-known benchmark. It shows the power of fine-tuning and RAG when combined.

Just to recap, when you're working on a problem and you want to improve your LLMs performance, start off with prompt engineering techniques.

These are very low investment. They allow you to iterate quickly and they allow you to validate LLMs as a viable technique to approach this problem that you're trying to solve.

You iterate on the prompt until you hit something like a performance plateau, and then you need to analyze the type of errors that you're getting.

If you need to introduce new knowledge or more context to the model, go down the RAG road.

If the model is inconsistently following instructions or it needs to adhere to a strict or novel output structure, or you just generally need to interact

with the model in a more efficient manner, it's maybe time to try fine-tuning. It's important to remember that this process is not linear.

That's really what we want to stress. It might take 49 iterations to get to a point that you're really happy with,

and you're going to be jumping back and forth between these techniques on your journey.

With that said, we hope you enjoyed this talk. Colin and I will be here for the rest of the day

if you have any questions.