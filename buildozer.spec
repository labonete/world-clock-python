[app]

# (Your application's name)
title = World Clock

# (Your application's package name)
package.name = worldclock

# (Your application's domain, usually reversed)
package.domain = org.kevinacer.worldclock

# (The directory where your main.py is located)
source.dir = .

# (The version of your app)
version = 1.0

# (The Python libraries your app requires)
requirements = python3,kivy,pytz

# (App orientation)
orientation = portrait

# (Icon filename)
icon.filename = %(source.dir)s/icon.png

# (Libraries to exclude from the build)
# blacklist.filename =

[buildozer]

# (Loglevel for the build process)
# 0: error, 1: info, 2: debug
log_level = 2

# (Number of threads to use for the build)
# 0 = auto
build_dir = ./build
bin_dir = ./bin