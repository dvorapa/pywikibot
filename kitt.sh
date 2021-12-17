#!/bin/bash
set -e 
set -o pipefail

if [ "$1" == "pull" ]; then
	current=$(git rev-parse --abbrev-ref HEAD)
fi

if [ -n "$2" ]; then
	target="$2"
elif [ -n "$current" ]; then
	target="$current"
else
	read -p "Target branch: " target
fi

if [ "$1" == "clone" ]; then
	git clone "https://gerrit.wikimedia.org/r/pywikibot/core" pywikibot
	cd pywikibot/
	git remote add update git@github.com:dvorapa/pywikibot.git
	git remote set-url --push origin git@github.com:dvorapa/pywikibot.git
	git fetch update

	# libovolná
	git checkout $target

	git branch -D master
	git checkout -t update/master
	git branch -u origin
elif [ "$1" == "pull" ]; then
	git checkout master
	git pull --rebase=false update master
else
	echo "-bash: command not found"
	exit 127
fi

git pull --rebase=false --no-edit

# ta druhá
for branch in dvorapa-test dvorapabot-remote dvorapabot-local; do
	git checkout $branch
	if [ "$1" == "pull" ]; then
		git pull --rebase=false update $branch
	fi
	git merge master --no-edit
done

git push --all update

# aktuální
git checkout $target

# ta druhá
for branch in dvorapa-test dvorapabot-remote dvorapabot-local; do
	if [ "$branch" != "$target" ]; then
		git branch -D $branch
	fi
done

git submodule update --init
