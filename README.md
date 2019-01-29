# Install
Prerequisities: Docker & Docker Compose.  
Tested under docker-compose 1.21.0, lower versions might be incompatible.

## Setup steps
 1. Download this repository
 2. Go to the root of this repository
 3. Run `./setup.sh`. This process might take 5-10 minutes depending on your internet connection. Wait until everything is done.
 4. Run `docker-compose up`

The recommender is now available under `http://localhost:5000`.

Use `CTRL+C` to stop the application.

## API-Keys
Keys must be inserted in the following source files:
 * app/app.py
 * app/reddit_subscriptions.py
 * app/twitter_api.py
 * app/twitter_api_friends.py
 * app/loaduser.py

## How to Connect to the VM?

## Tools 
Download and install [Putty] (https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

## Setup Key-Pair
*This is only required if you want to omit the step of typing in the very complicated and long vm password each time you connect to the VM.*
1. Open the Putty Key Generator (e.g. by typing puttygen into the windows search bar or executing the command in your local bash)
2. Click on Generate
3. Move the mouse continuously over the tools blank field to generate the key
4. Set a keyphrase (your new password, if you make this too complicate now you missed the purpose of this)
5. Save both private and public key locally.

## Connect to the VM
1. Open Putty
2. Fill in the details according to the following pictures:  
![PuTTY 1](/examples/images/Putty1.PNG)  
![PuTTY 2](/examples/images/Putty2.PNG)  
3. Click on open and use the standard VM password in the following prompt.

Thats it, you're connected with the VM.

*If you created a key pair in the previous step, you can now do*
1. nano /home/di-g3_adm/.ssh/authorized_keys
2. add a new line to the file and copy the content of your public key into the file
3. Save the file. Next time you will connect to the VM, you can use your private password.
