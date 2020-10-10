#!/user/bin/env sh

# abort on errors
set -e

# build
yarn build

# navigate int the build dir
cd dist

git init
git add -A
git commit -m "deploy"

# deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:YanickJair/nlpdemo.git master:gh-pages

cd -