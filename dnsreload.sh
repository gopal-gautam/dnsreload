#!/bin/bash
OPTIND=1
verbose=0
host=""
arguments=""

function display_help() { echo -e "usage $SCRIPT [-w <viewzone>] [-s <server>] [-t <dns type>] host \n By Default when -w is not specified the view will be internal,external and when -s in not specified the server will be ns1 and ns2"; exit 0; }

while getopts "h?w:s:vdt:" opt; do
	case "$opt" in
		h|\?)
			display_help
			;;
		v)	arguments=$arguments" -v " >&2
			;;
		w)	arguments+=" -w $OPTARG" >&2
			;;
		s)	arguments+=" -s $OPTARG" >&2
			;;
		d)	arguments+=" --debug " >&2
			;;
		t)	arguments+=" -t $OPTARG" >&2	
			;;	
	esac
done

host=${@:$OPTIND:1}
if [ -z "$host" ]; then
	echo "No host defined here"
	display_help
fi

if [ -z "$arguments" ] || [ -z "$*" ]; then
	[ -z "$host" ] && display_help
fi

if [ "$arguments" != *"forward"* ]; then
	prev_user=$(dig -x $host | grep .in-addr.arpa. | grep example.com | grep -v "ns[12].example.com" | sed -E 's/[[:space:]]/ /g' | cut -d ' ' -f5 | cut -d'-' -f1;)
	if [[ -n "$prev_user" ]]; then
		echo "previously this ip was assigned to $prev_user"
	fi
fi

echo autodnsreload.pyc$arguments $host
python autodnsreload.pyc$arguments $host
