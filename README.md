# xkcd.com random comics to VK posting utility

A Python utility that uses the API of [xkcd.com](http://xkcd.com) to download a random image and caption from the same comics website, and the API of [vk.com](http://vk.com) to upload and publish the downloaded image to the same social network. The utility deletes the downloaded image locally.

## Installation

1. Python 3 should already be installed. If not, then please do so.
2. You also need to have a [VK](www.vk.com) account. You also need to [create](https://vk.com/groups?tab=admin) a VK group in which you will be posting the comics with this utility.
3. Please refer to [here](https://vk.com/dev) to create an app in VK, which you will use for interacting with the VK API to post the comics (go to the "My apps" subsection there). Your app will have its own unique `client_id`, which you can see in your browser's address bar after click the "Edit" button beside your newly created VK app. Write this `client_id` down in a safe place.
4. Get your API user access key with the following access rights: `photos`, `groups`, `wall` and `offline`. It looks something like `533bacf01e1165b57531ad114461ae8736d6506a3`, and it also appears in your browser's address bar after the `access_token=` part of the address. Your access key request URL should look like this:

    https://oauth.vk.com/authorize?client_id=1234567&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos,groups,wall,offline&response_type=token&v=5.131

    (make sure to substitute your `client_id` there).

5. You can get your VK User ID and Group ID [here](https://regvk.com/id/).

6. Now create a Python virtual environment:

        python3 -m venv .venv

    Activate the environment, e.g.:

        source .venv/bin/activate

    Install the required libraries:

        pip install -r requirements.txt

7. Now you need to set up the utility by creating a file named `.env` in the utility's directory.

> Example of `.env`:

    VK_CLIENT_ID=1234567
    VK_ACCESS_TOKEN="533bacf01e1165b57531ad114461ae8736d6506a3"
    VK_UID="123456789"
    VK_GID="123456789"
    VK_API_VER="5.131"

> **Note:** If you deploy this script on a service which does not use a `.env` (or similar) file, but which would store these environment variables in its own environment (such as [Heroku](http://heroku.com)), you don't need to change anything in the code. The above environment variables will be picked up automatically from the current environment if no `.env` file is present.

## Launching the program

The standard way is to run in your command line interface

    python3 main.py

If you are in Linux and make the file executable by

    chmod +x main.py

then you can also launch directly, e.g.:

    ./main.py
