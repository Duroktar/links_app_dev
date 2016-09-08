Links App, Alpha v0.0.1
=======================

Welcome
-------

Greetings, and welcome to the Alpha Dev release of the Official
Multi Platform Links app. 

This project is being developed in Python
using the cross-platform Kivy Library https://kivy.org/#home.
(Source https://github.com/kivy/kivy)
which can be compiled into the appropriate file type for various
machine architectures. 

For windows or linux Install
----------------------------
Kivy installation instructions can be found here
https://kivy.org/docs/gettingstarted/installation.html.

Install on windows can be tricky but it's possible. Installation on linux is much easier.

For Quick Install on Android
----------------------------
If you want to test any changes you make on an actual phone or andorid emulator 
without having to build an apk file. 

Get the Kivy Launcher app from the Play Store or from http://apk-dl.com/en/kivy-launcher. 
Once installed place all the files into /storage/Kivy/Links/ and you'll be able to start the app on your device.

Quick Info
----------
Kivy allows us to completely seperate the design from the functionality
of the app by way of the extremely easy to use .kv language files.
Therefore if you wish to help but aren't particularly comfortable
coding it's no problem. 

The .kv files that already exist contain the style information of all the elements.
It's alot like css so if your familiar with css, than you can help with themes or styles.

See https://kivy.org/docs/api-kivy.lang.html for more info on the kv language.

Dev
---
**Custom created .kv files will be autoloaded for use when placed into the ./data/screens/ directory.**
All modules are loaded this way (Including this About file, see ./screens/about.kv)

*Code can be viewed from the app by clicking on the bug icon in the upper right of the main window.*

Kivy also allows for dynamic access to java or android modules with the Pyjnius library (See https://github.com/kivy/pyjnius)

Builds
------
This is an incredibly difficult process. If you are ready for the challenge you can check out
the link below. 

The best way to compile is to get the provided Virtual Machine image with
*most* (but not all) dependancies installed. From there I suggest hitting the forums first for
more info.
- (See "Buildozer" https://github.com/kivy/buildozer **ADVANCED USERS ONLY**)

ToDo
----
- ***Voice support still needs to be added.*** (See https://github.com/cidermole/audiostream)
- Overall theme design.. Styles..
- Sound effects. Use files from actual Links wherever possible.
- Code layout should be more modular (my bad)
- Add more to this ToDo

Hosting & License
-----------------

This project will be hosted on GitHub at https://github.com/Duroktar/links_app_dev under the GNU GENERAL PUBLIC LICENSE.

We reserve the right to change the license at any given time, but will probably only exercise this right when and if
an offical public release is ever made.

Summary
-------
Please do any error reporting or requests, etc. in the issues tab of
the Github and please try to be helpful and respectful to everyone involved.

Pull requests or merges will be more frequent in the beginning until
the release of the Beta, at which time the release structure will be
reviewed.

Thanks & Contact
----------------

Thanks for showing your interest and support. I especially wanna thank Zunair and everyone at MVC
who made links what it is today and all the people who have hepled me get this done. 
And I should also thank my Wife and kids for putting up with me while I struggled
through this whole process. A lot of late nights have gone into this thing. (so far)

If you would like to contact me directly my e-mail is duroktar@gmail.com and I will try to
respond as quickly as possible

Author
------
Created by: traBpUkciP
