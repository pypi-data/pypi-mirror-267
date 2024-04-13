#!/bin/bash
# change the package name to the existing PyPi package you would like to build
pkg='movinglines'
# adjust the Python versions you would like to build
array=( 3.7 3.8 3.9 )
#echo "Building conda package ..."
#cd ~
#conda skeleton pypi $pkg
#cd $pkg
#wget https://conda.io/docs/_downloads/build1.sh
#wget https://conda.io/docs/_downloads/bld.bat
#cd ~
# building conda packages
#for i in "${array[@]}"
#do
#	conda-build --python $i $pkg
#done
#conda build --output-folder ./conda-out/ ./conda/
# convert package to other platforms
#cd ~
platforms=( osx-64 osx-arm64 linux-32 linux-64 win-32 win-64 win-arm64 )
find $HOME/fp/conda-out/linux-64/ -name *1.48*.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $HOME/conda-bld/
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $HOME/fp/conda-out/
    done    
done
# upload packages to conda
find $HOME/fp/conda-out/ -name *1.48*.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done
echo "Building conda package done!"
