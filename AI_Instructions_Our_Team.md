# AI Instructions
## AI is not allowed to edit this file
## Only the repository owner, the human, is allowed to edit this file
## 11:43 AM
/*(Matiyas Dawit: using codex as an AI tool)*/

Explain this project structure to me in simple terms

## 11:56 AM

ok before we do implementation, let ne first ask you exploratory questions. Let us plan how to develop code before we start implementation. So lets do it and develop a general approach. 

## 11:58 AM

Ok so this is the goal 

Goal: Create a web based authoring tool for "Create Your Own Adventure" stories.

The Challenge: Branching storylines are difficult to manage. Authors have to keep track of different stories. Sometimes branching story lines can come back to the same place.

Approach: Start with "The Cave of Time" a classical CYOA story downloade from https://pdfcoffee.com/1-the-cave-of-time-choose-your-own-adventure-pdf-free.html. Segment it into pieces, write out all the possible stories as well as the story-graph. We'll assume the authors will write similar pieces of text, parts of the story, they will want to create a similar story-graph to visualize the story so far.

How can we provide a web based interface for authors? They should be able to upload the start of story. Choose multiple ways the story can be extended. Upload those parts. Easily move between different paths in the story graph. Easily see and visualize the unfirnished part, parts that have similar endings, etc.

In addition to the authoring tool. The web site should also offer a way to "read" the story. That part is easy. It can even be static HTML once all the story parts are in place.


## 12:04 PM

Sure do that

## 12:11 PM

nice explanation, yeah ok do that lets continue

## 1:07 PM

yeah ok lets go with your recommednation

## 1:24 PM

ok yeah implement the code fully for this

## 2:04

yeah polish the UI and let us test it I want to see it

## 2:24

the story map looks blurry, could you fix that. Also could you make it so that under the heading of "Story pieces" It would have its own scroller so that I when I scroll that piece tab would be the only one that is scrolling and also do the same thing for the "Checks". And make sure the grammar is correct. I found trailing "2" and "4" and "|" and incorrect wording that doesnot make senes why they are there, especially since it is not there in the book (i think it is formatting issues)  

## 2:41

on page 6 I only have the option to go to page 114 although it says If you accept the ride back to
the castle, tun to page 22.

If you decline the invitation and
try to find your way back into the
Cave of Time, turn to page 114.

and also there are grammar issues like words connected together like "youas" on page 6. Look for others as well, but otherwise it is looking good

## 2:53 

There are still grammer issues check all of the pages and fix any grammar issues that you can find

## 3:16

ok write the  Codebase.md explaining the project architecture and approach taken and if you can extend and deploy your project on a public website, if not tell me how to 
