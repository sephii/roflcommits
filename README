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

## Installation

Install the dependencies listed above and then use pip to install roflcommits:

    pip install http://github.com/sephii/roflcommits

## Usage

Start by adding the commit hook on one of your git repositories:

    roflcommits enable-commit-hook

This will create a commit hook file in your `.git/hooks/` directory. This hook
will just take a picture on each commit and store it in your ~/.roflcommits
directory. If you want to directly upload the picture to Flickr, just edit the
hook file `.git/hooks/post-commit` and replace `snapshot` by
`snapshot-and-upload`. Doing this will make your commits take more time because
you'll have to wait for your picture to be uploaded each time you make a commit.
Also the upload won't work if you're not connected to the internets.

A better way is to keep using the `snapshot` command on commit and use the
`upload` command on push. To do that, use the following:

    roflcommits enable-push-hook

This will add a push hook that will upload all the pictures that have been taken
along with your commits.

