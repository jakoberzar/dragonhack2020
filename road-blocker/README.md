# Road Blocker

This is the component of the project that is responsible for blocking the roads, covered with fire inside the OpenStreetMap files.

There are some dependencies; libosmium, pthreads, zlib, bzip2 and expat.
The compiler must have support for C++17 filesystem.

## Building

```
mkdir build
cd build
cmake ..
make
cd src
ln -sf ./../../../server/cache/v2 ./imgs
```

## Use

```
cd build/src
./roadblocker <path to the .osm.bz2 or (preferably) .osm.pbf file
```
