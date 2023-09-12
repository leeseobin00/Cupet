# Cupet (Cupid + pet)
Raising a virtual pet for people suffering from social depression, such as distance-keeping in Corona mix

## Main goal
- Raising a virtual pet for people
- Chatting to communicate with the pet

## Brief description 
- Selecting a pet
  - first-time users choose which pet to grow using the button
  - enter a string from the user to name the pet
  
- Raising a pet
  - image representation of pet growth process
  - add variable background music depending on the situation
  - feeding/shower/play function implemented as a button
  - user: Implemented by the GUI button to receive command
  - server: output to the pet’s response string for that command

- Communicating with a pet
  - user: enter what user want to say to the pet in the text box
  - server: output as a response string to a user’s word


## Key Features
### Selecting a pet
<img width="680" alt="img1" src="https://github.com/leeseobin00/Cupet/assets/70849467/2fafe2e9-f450-4011-a943-af432284409e">

- Puppies/Cats/Meerkats are selected using buttons implemented using the GUI
- Name the pet after selection

### Raising a pet
<img width="680" alt="img2" src="https://github.com/leeseobin00/Cupet/assets/70849467/912594b1-6854-40f9-8642-3b5763e6cfa6">

- Click the Feed/Snack button to feed the pet
- Click the shower button implemented using the GUI
- Click the Play button
- Recognize strings except for interrogations, emoticons, etc.
- Keywords are specified so that users can enter content for keywords.
- Image of pet size change over time/with food intake

### Image / Button/Dialog Window Implementation using GUI
<img width="680" alt="img3" src="https://github.com/leeseobin00/Cupet/assets/70849467/915959c5-5b54-4a25-8db3-a55eb616517b">

- Image: Show pet size changes and express movement as animation or image changes
- Pet's reaction: The pet responds according to the button pressed by the user
- Button: Dog/cat/meerkat, feeding/showering/playing, feeding/snacking, and throwing/taking a walk.
- Chatting service through text boxes that users can type in and output boxes that can hear answers from the pet.
