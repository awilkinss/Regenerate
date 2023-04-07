# Regenerate
For the Machine Learning Piano project led by Alim Wilkins and invaluably contributed to by Hannah Fowler, Miles Berry, and Becky McQuilken.

## The General Idea:

We train a random forest model to predict notes and chords to accompany a piano player trained from MIDI files of piano performances. This is done using a random forest model, an autoencoder (an encoder and decoder), and the ports that connect the Yamaha Diskclavier to our computers. Instead of generating pieces of music we'll focus solely on accompaniment; encoding the tree to generate predictions from and decoding the tree to get suggestions for how to accompany.

## Setup:

Download *regenerate.yml* from the repo and run the command **conda env create -f regenerate.yml**
This will create our very own ~~non-magenta~~ enviornment!

The environment is important because it replaces sklearn's unfinished autoencoder commands with working versions. Thanks @kingfengji 

## Discord:
Join for project updates, suggestions, and assignments. Way better than an email chain or repo edit history I promise
https://discord.gg/DKwc2nHMEF

### Further Details:

If you wanna read up on the stuff we're using (you probably should) here's the sauce
- https://github.com/kingfengji/eForest (Eforest Original Repo; no need to install it's already in our conda environment)
- Music21 guides [https://web.mit.edu/music21/doc/index.html] and modules [https://web.mit.edu/music21/doc/py-modindex.html]
- The tds post that explains what the hell eforest/autoencoders even are [https://towardsdatascience.com/building-a-simple-auto-encoder-via-decision-trees-28ba9342a349]
