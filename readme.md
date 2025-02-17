# Introduction

Angen is a simple RAG bot that can dynamically accept context from text files and answer questions based on that context. The primary use-case is for it to be a writing assistant for me. That way I don't have to slog through hundreds of pages of my own docs to find an answer, I can just ask the bot.

# Usage

This is still very much in development. If you want to use it, you do so at your own risk. I tried writing decent code, but I was focused on getting a Minimum Viable Product done, not writing something fast. Future plans are to optimize, keep an eye on the release notes for official notes and the devlog for more incoherant notes. Anyway, lets get on with it.

## System Requirements

Here are my specs. These are the only specs that are confirmed working. If I test on any other rigs, I'll append them here.

- **CPU**: Intel i7-7700K
- **GPU**: GTX 1070Ti
- **RAM**: 24 GB DDR4
- **OS**: Windows 10

## Installations

For now no excecutable exists. To run Angen clone the repo. I HIGHLY recommend you create a virtual environment to run this in. Learn how [here](https://docs.python.org/3/library/venv.html). Now we have a problem. Dependancies.

### Dependancies

Angen has a lot of them. First, we need the C++ Build Tools (if you have them, do not update to 17.13.0, it has causes the Cuda toolkit to be unable to install), installed through the [Visual Studio installer](https://visualstudio.microsoft.com/downloads/). Instructions [here](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation?view=msvc-170). Then install the CUDA toolkit, which can be downloaded [here](https://developer.nvidia.com/cuda-toolkit). I used Version 12.8.0. Then, we need to install all the pip dependancies from the requirements document. Do this by running `pip install -r requirements.txt` from inside the Angen folder. Most of our dependencies behave, but there are three that did not. The cuplrits?

- `pyqt6-plugins`
- `pyqt6-tools`

These two are harmless to leave out. They exist for the UI building side of things, but aren't needed to run Angen. They aren't in the requirements doc and you shouldn't worry about them. Unfortunately the same can't be said for the last culprit.

- `llama_cpp_python`

This is the bane of my existance. So, here's what you do. Download the dependancy [here, from the official GitHub repo](https://github.com/abetlen/llama-cpp-python/releases), and install it from file. Installing it from remote never worked for me.



### Model

The model is pretty big, so I left it from the repo. Download it [here](https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF/blob/main/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf) and place it into the `/model/` folder of the repo. Make sure the model's filename is `capybarahermes-2.5-mistral-7b.Q5_K_M.gguf`.

## Using Angen

### Launching Angen
1. Open your terminal of choice
2. Activate your virtual environment
3. Run `python -m UI.main_window` from inside the Angen folder

### Loading your own context

1. Click on the 'Data Ingress' tab.
2. Click the 'Select Folder' button and select a location for your context database. This is where the information you feed Angen will be stored. Might experience a few moments of lag after selection.
3. Click on the 'Select File' button and select the context file you want to use. For now, Markdown works best. Try to limit filesize to 5000 words or less, as more can cause some instability.
4. Use the catagory dropdown to select a catagory for the context you have added.
5. Add tags, seperated by comments, eg: chapter 1, Character1, Character2, Big fight.
6. Click on 'Submit Context'. Once tag field clears, you'll know the loading is done.

### Querying Angen

1. Click on the 'Chat' tab.
2. Enter your question in the bottom text box. For now, try to keep questions under 100 words.
3. Wait. I haven't added loading indicators yet. The program might say "not responding", but it is still working. Responses usually take between 5 and 20 seconds on my hardware.
