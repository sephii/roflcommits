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
directory. If you want to upload the pictures to Flickr, use the following:

    roflcommits enable-commit-hook --api-key=xxx --api-secret=yyy

Where `api-key` and `api-secret` are your API key and secret from your Flickr
account.

If you have some images in your `~/.roflcommits` directory you want to upload,
you can simply execute the following from anywhere:

    roflcommits upload --api-key=xxx --api-secret=yyy
