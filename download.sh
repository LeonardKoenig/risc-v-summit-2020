#! /bin/sh

dirlist='day01 day02 day03 day04'
#Meet_the_Speakers
kinds='Conference Keynote Tech_Talk Tutorial'

head='<!DOCTYPE html>
<html>
<head>
<title>RISC-V Summit 2020</title>
</head>
<body>'

tail='</body>
</html>'


echo "$head" > index.html
for d in $dirlist; do
    echo "> Working on $d"
    echo "  <h1>$d</h1>" >> index.html
    mkdir -p $d
    pushd $d >/dev/null
    for g in $kinds; do
        echo ">> Downloading all kinds of $g"
        echo "    <h2>$g</h2>" >> ../index.html
        mkdir -p $g
        pushd $g >/dev/null

        g=${g/_/ }
        events=$(jq '.[] | select(.kind|match("'"$g"'")) | .title' ../${d}.json)
        IFS=$'\n'
        i=0
        for ev in $events; do
            url=$(jq '.[] | select(.kind|match("'"$g"'")) | .url' ../${d}.json | jq -s ".[$i]")
            url=${url//\"/}      # remove all ""
            title=$ev
            title=${title/%\"/}  # remove ""
            title=${title/#\"/}  # around title
            filen=$title
            filen=${filen// /_}  # replace space with _
            filen=${filen//\//-} # replace slashes with -
            if [ -f "$filen.mp4" ]; then
                echo "."
            else
#                echo $url
                youtube-dl --output "$filen.%(ext)s" $url
            fi
            echo "      <iframe src="$url" title="$title" allowfullscreen></iframe>" >> ../../index.html

            i=$i+1
        done
        unset IFS
        popd >/dev/null
    done
    popd >/dev/null
done
echo $tail >> index.html
