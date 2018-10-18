#!/bin/bash


cd ./setup1

# Prepares the deployment package
echo "Zipping package"
zip -r ../package.zip ./* 

# Remove the setup directory used
echo "Removing setup directory and virtual environment"
cd ..

# changing dirs back to dir from before
echo "Opening folder containg function package - 'package.zip'"
open .