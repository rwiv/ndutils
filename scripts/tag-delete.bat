cd ..
set TAG_NAME=v0.1.3

git tag -d %TAG_NAME%
git push origin :refs/tags/%TAG_NAME%
pause