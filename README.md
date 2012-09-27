# Roflcommits

Roflcommits is a git hook that allows you to take snapshots using your webcam
each time you make a commit, and then upload them to Flickr. You can then
integrate the roflpictures in another application, for example to display the
picture of the commit that made the tests fail.

This project is largely inspired by
[lolcommits](https://github.com/mroth/lolcommits).

## Dependencies

Roflcommits makes use of the following libraries/programs:

* mplayer (only on Linux, for taking snapshots)
* python-flickrapi (only if you use Flickr publication)
* PIL (aka python imaging library)

## Installation

Install the dependencies listed above and then use pip to install roflcommits:

    pip install git+git://github.com/sephii/roflcommits@master

You can also use pip to install the dependencies like so:

    pip install pil flickrapi

## Usage

Start by adding the commit hook on one of your git repositories:

    roflcommits enable-commit-hook

This will create a commit hook file in your `.git/hooks/` directory. This hook
will just take a picture on each commit and store it in your ~/.roflcommits
directory. If you want to upload the pictures to Flickr, use the following:

    roflcommits enable-commit-hook --api-key=xxx --api-secret=yyy

Where `api_key` and `api_secret` are your API key and secret from your Flickr
account.

If you have some images in your `~/.roflcommits` directory you want to upload,
you can simply execute the following from anywhere:

    roflcommits upload --api_key=xxx --api_secret=yyy
