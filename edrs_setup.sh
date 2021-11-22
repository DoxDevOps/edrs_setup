#!/bin/bash --login

echo "____________________________________________"
echo "Checking out to Current Folder"
echo "____________________________________________"
git checkout .
echo "____________________________________________"
echo "Cleaning Git Cache"
echo "____________________________________________"
git clean -f
echo "____________________________________________"
echo "Checking out to no Couch-db Application"
echo "____________________________________________"
git checkout couchdb-removed
echo "____________________________________________"
echo "Removing Gemfile.lock"
echo "____________________________________________"
rm Gemfile.lock
echo "____________________________________________"
echo "Installing Local Gems"
echo "____________________________________________"
bundle install --local
echo "____________________________________________"
echo "Setting up edrs application"
echo "____________________________________________"
bundle exec rake edrs:setup
echo "--------------------------------------------"

