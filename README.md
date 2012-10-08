# Roflcommits

Roflcommits is a git hook that allows you to take snapshots using your webcam
each time you make a commit, and then upload them to Flickr. You can then
integrate the roflpictures in another application, for example to display the
picture of the commit that made the tests fail.

This project is largely inspired by
[lolcommits](https://github.com/mroth/lolcommits).

## Dependencies

Roflcommits makes use of the following libraries/programs:

* mplayer (only if you're running GNU/Linux, for taking snapshots)
* python-flickrapi (only if you're going to use Flickr publication)
* PIL (aka python imaging library)

## Installation

### Install dependencies

If you're running GNU/Linux, start by installing mplayer and some libraries that
are required to install PIL correctly (with JPEG and TrueType support):

    sudo apt-get install mplayer libfreetype6 libfreetype6-dev libjpeg62 libjpeg62-dev

Then, whatever OS you're running, install the dependencies using pip:

    sudo pip install flickrapi pil

If you don't have pip installed, you can get it that way:

    sudo easy_install pip

### Install Roflcommits

Once the dependencies are installed, install roflcommits:

    sudo pip install git+git://github.com/sephii/roflcommits@master

That's it! You can now skip to the section "Usage".

### Installation without pip

If you really don't want to have pip installed, you can still try to install the
dependencies with easy_install:

    sudo easy_install pip flickrapi

Then install roflcommits:

    sudo easy_install https://github.com/sephii/roflcommits/zipball/master

## Usage

Start by adding the commit hook on one of your git repositories:

    roflcommits enable-commit-hook

This will create a commit hook file in your `.git/hooks/` directory. This hook
will just take a picture on each commit and store it in your ~/.roflcommits
directory. If you want to upload the pictures to Flickr, use the following
instead:

    roflcommits enable-commit-hook --api-key=xxx --api-secret=yyy

Where `api-key` and `api-secret` are your API key and secret from your Flickr
account.

You can change the commit hook at any time by editing the
`.git/hooks/post-commit` file.

If you have some images in your `~/.roflcommits` directory you want to upload,
you can simply execute the following from anywhere:

    roflcommits upload --api-key=xxx --api-secret=yyy

Here's the whole program documentation for reference:

    Usage: roflcommits [options] command
    
    Available commands:
      enable-commit-hook   		Enables the `snapshot-and-upload` command on each commit
      disable-commit-hook  		Disables the commit hook
      snapshot             		Makes a snapshot and stores it in your ~/.roflcommits/ directory
      upload               		Uploads all snapshots in your ~/.roflcommits/ directory on Flickr
      snapshot-and-upload  		Takes a snapshot and upload it to Flickr
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      --api-key=API_KEY     your Flickr API key
      --api-secret=API_SECRET
                            your Flickr API secret
      -s DELAY, --delay=DELAY
                            delay in seconds before taking the snapshot
      -d DESTINATION, --destination=DESTINATION
                            path to directory that will hold the snapshots
                            (default is ~/.roflcommits)
      -v DEVICE, --device=DEVICE
                            Linux only. The device to tell mplayer to use to take
                            the snapshot
      --font=FONT_PATH      path to font to use
      --font-size=FONT_SIZE
                            font size to use, in pt
      --image-size=IMAGE_SIZE
                            size of the final image
