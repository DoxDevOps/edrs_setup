#!/bin/bash --login
echo "____________________________________________"
echo "Removing Gemfile.lock"
echo "____________________________________________"
rm Gemfile.lock
echo "____________________________________________"
echo "Installing Local Gems"
echo "____________________________________________"
bundle install --local
echo "____________________________________________"
echo "running bin_update art"
echo "____________________________________________"
bundle exec rake edrs:setup
echo "--------------------------------------------"

