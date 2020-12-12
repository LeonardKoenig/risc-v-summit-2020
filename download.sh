#! /bin/sh

dirlist='day01 day02 day03 day04'

#Meet_the_Speakers
kinds='Conference Keynote Tech_Talk Tutorial'

for d in $dirlist; do
    echo "> Working on $d"
    mkdir -p $d
    pushd $d >/dev/null
    for g in $kinds; do
        echo ">> Downloading all kinds of $g"
        mkdir -p $g
        pushd $g >/dev/null

        g=${g/_/ }
        events=$(jq '.[] | select(.kind|match("'"$g"'")) | .title' ../${d}.json)
        IFS=$'\n'
        i=0
        for ev in $events; do
            url=$(jq '.[] | select(.kind|match("'"$g"'")) | .url' ../${d}.json | jq -s ".[$i]")
            url=${url//\"/}      # remove all ""
            title=${ev// /_}     # replace space with _
            title=${title/%\"/}  # remove ""
            title=${title/#\"/}  # around title
            title=${title//\//-} # replace slashes with -
            file=$title.mp4
            if [ -f "$title.mp4" ]; then
                echo "."
            else
#                echo $url
                echo "$title"
                youtube-dl --output "$title.%(ext)s" $url
            fi

            i=$i+1
        done
        unset IFS
        popd >/dev/null
    done
    popd >/dev/null
done
