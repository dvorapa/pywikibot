#!/bin/bash

if [ "$1" == "clone" ]; then
	git clone "https://gerrit.wikimedia.org/r/pywikibot/core" pywikibot
	cd pywikibot/
	git remote add update git@github.com:dvorapa/pywikibot.git
	git remote set-url --push origin git@github.com:dvorapa/pywikibot.git
	git fetch update

	# libovolná
	git checkout $2

	git branch -D master
	git checkout -t update/master
	git branch -u origin
elif [ "$1" == "pull" ]; then
	git checkout master
	git pull update master
else
	echo "-bash: command not found"
	exit 127
fi

git pull

# ta druhá
for branch in dvorapa-test dvorapabot-remote dvorapabot-local; do
	git checkout $branch
	if [ "$1" == "pull" ]; then
    	git pull update $branch
    fi
	git merge master
done

git push --all update

# aktuální
git checkout $2

# ta druhá
for branch in dvorapa-test dvorapabot-remote dvorapabot-local; do
	if [ "$branch" != "$2" ]; then
		git branch -D $branch
	fi
done

git submodule update --init
