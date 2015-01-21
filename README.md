
To run the samples, right now you need to `cd` into the example directory containing the python files, and execute it from there.

```terminal
$ cd face_detection
$ python camera_face_detection.py
```


## Python openCV on Mac OS

Install `openCV` with  `brew`:

```terminal
$ brew tap homebrew/science
$ brew install opencv
```

After `brew` is done installing you might get this warning:

>==> Caveats
Python modules have been installed and Homebrew's site-packages is not
in your Python sys.path, so you will not be able to import the modules
this formula installed. If you plan to develop with these modules,
please run:
  mkdir -p ~/Library/Python/2.7/lib/python/site-packages
  echo 'import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")' >> ~/Library/Python/2.7/lib/python/site-packages/homebrew.pth

Just follow the instructions and type the tow commands provided.

```terminal
$  mkdir -p ~/Library/Python/2.7/lib/python/site-packages

$ echo 'import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")' >> ~/Library/Python/2.7/lib/python/site-packages/homebrew.pth
```

You should be ready to try importing `cv` on a python repl window.

```terminal
$ python
...
>>> import cv
>>> 
```

If something went wrong you should get an error telling you that the `cv` module was not found.


>==> Installing opencv from homebrew/homebrew-science
opencv: Java optional is required to install this formula.
You can install with Homebrew Cask:
  brew install Caskroom/cask/java

You can download from:
  http://www.oracle.com/technetwork/java/javase/downloads/index.html
Error: An unsatisfied requirement failed this build.

Fix by typing the following command in your terminal:

```terminal
$ brew cask install Caskroom/cask/java
```


