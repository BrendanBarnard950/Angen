### Thursday, February 13th, 2025
## 22:42
Ok, so we've done a lot, and I'll be real, I don't know how a lot of it works. It's like building a puzzle of my favourite car, but only seeing the backs of the pieces. I'm making things fit together in a way that sorta looks right, but it might not be a good way. For now thisis okay.

The goal is a Minimum Viable Product by Sunday. It's ambitious, but I think it is manageable. for now we haev some issues, most of which relating to my own ignorance. That being said, the GUI works. The next step is either to try to hook in Mistral so the chatinterface works to talk to the model, or get the FAISS db up and running. data ingress is still fairly beyond me, but thisis a learning excersize, after all.

I think I want to spend some time making sure I actually *get* what's going on. I've never worked with PyQt (or any python-based gui code) before, so a lot of this is trial and error and some script-kiddie behaviour. Truly despicable. So, plan of action, see if I can fix the scrolling issue, and maybe watch a tutorial video on PyQt.


### Friday, February 14th, 2025
## 19:40
Happy Valentine's day. I ended up doing very little extra last night, and today my 9-5 managed to be more of a 6-6. Still, I'm here, trying to figure out smooth scrolling. After that, my goal for tonight is to get the LLM hooked in. If I can have a 'conversation' with  Mistral before I go to bed I'll consider today a success. Who knows, maybe it will be a lot easier than I think. Probably not, but a man can dream.

## 21:43
I have been fighting to install llama. It isn't working and it's driving me nuts. I had to trash the venv from the repo because I have to install so many dependancies. It's going to be a nightmaer cleaning everything up after. As we speak this thing is still running after trying another fix. If I suddenly start cursing, you'll know it just spat out the errors. Again. I know I'm working with very advanced shit I can hardly comprehend but just _once_ I'd like something to work out of the box, you know? Half the job is debugging, and I dont mind debugging my own stupidity, but I'm not smart enough to fix my computer's stupidity.

## 21:46
Motherfucker.

## 23:32
I think I did it. Gonna need to add this to the readme for sure. I had to manually download a whl, downgrade my Python version, and do about a dozen other ultimately pointless things, but now, finally, I have llama installed. I havent even tested it. I dont even know how to test it yet. Time to go do some learning.

### Saturday, February 15th, 2025
## 02:46
Boys, I did it. The computer is talking to me. It is really slow, and limited to only 100 tokens on the response for now, but dammit, it's working. I am wired, and I cant decide between getting some sleep or plowing on and trying to optimise a little. I'm not using my GPU enough, I think. Usage _barely_ reaches 60%. If I can crowd more onto the GPU I might be able to get speedier responses. If I can split to the CPU too, maybe more. I dont mind revvnig both up into the 90's if need be.