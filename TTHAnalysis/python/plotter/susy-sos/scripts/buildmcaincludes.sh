#!/bin/bash

function do_help() {
    printf "Use this to generate a directory named <year> with mca files
Fetches info from the path ./metadata
Usage:
$(basename $0) --md <metadata-dir> [--make-draft] [--one-file]
"
    exit 0
}

while [ ! -z "$1" ]; do
    [ "$1" == "--help" ] && do_help
    [ "$1" == "--md" ] && { metadata=$PWD/$2; shift 2; continue; }
    [ "$1" == "--make-draft" ] && { mkdraft=true; shift; continue; }
    [ "$1" == "--one-file" ] && { onefile=true; shift; continue; }
    echo "Unrecognized cli argument $1"
    exit 1
done


## check args and build env
{ [ -z "$CMSSW_BASE" ] || ! [[ $PWD =~ .*$(echo $CMSSW_BASE | sed s/.*$USER//).* ]]; } && { echo "Run cmsenv"; exit 1; }
cd $CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/susy-sos/mca-includes
[ -z "$mkdraft" ] && { mkdraft=false; dirout=.; } || { dirout=draft; rm -rf $dirout; }
[ -z "$onefile" ] && onefile=false
[ -z "$metadata" ] && { echo "Please provide the metadata dir using --md <metadata>"; exit 1; }
[ -z "$buildfiles" ] && { echo "Getting the filelist to create from the matadata/ dir."; buildfiles=$metadata/filesToChange_fakes.txt; }
$mkdraft && { # if is making draft mk the draft dir, otherwise already exists
    mkdir $dirout || { echo "Output dir $dirout failed to be created. Check if it exists already."; exit 1; }
}

## look up info for labels and colors
function getLabel() {
    smpl=$1
    if echo $smpl | grep "DYJets" > /dev/null; then ret='Label="DY(fakes)"'
    elif echo $smpl | grep "WJets" > /dev/null; then ret='Label="Wj(fakes)"'
    elif echo $smpl | grep "^TT" > /dev/null; then ret='Label="tt(fakes)"'
    elif echo $smpl | grep -i "^t[^t]" > /dev/null; then ret='Label="t(fakes)"'
    elif echo $smpl | grep "WW\|ZZ\|VV\|WZ" > /dev/null; then ret='Label="VV(fakes)"'
    fi
    echo $ret
    return 0
}
# function getColor() {
#     smpl=$1
#     echo $smpl | grep DYJets > /dev/null && ret="FillColor=ROOT.kGray"
#     echo $smpl | grep WJets > /dev/null && ret="FillColor=ROOT.kGray"
#     echo $smpl | grep ^TT > /dev/null && ret="FillColor=ROOT.kGray"
#     echo $smpl | grep -i ^t[^t] > /dev/null && ret="FillColor=ROOT.kGray"
#     echo $smpl | grep "WW\|ZZ\|VV\|WZ" > /dev/null && ret="FillColor=ROOT.kGray"
#     echo $ret
#     return 0
# }


## loop over the files asked to create
cat $buildfiles | while read line; do
    ## check validity of line
    [[ $line =~ ^$ ]] && continue
    file=$(echo $line | sed -r "s/^([^,]*),.*/\1/")
    buildfile=$dirout/$(echo $file | sed s@.*mca\-includes/@@)

    ## create file
    ! [ -z "$buildfile" ] && echo "-----> file: $buildfile" || { echo "buildfile var is empty"; exit 2; }
    where=$(dirname $buildfile)
    ! [ -e $where ] && mkdir -p $where
    ! $mkdraft && buildfile=$buildfile.tmp
    touch $buildfile # be sure that you can access the file in hand

    ## find source file
    srcfile=$(echo $buildfile | sed "s@$dirout/@@; s@\.tmp@@")
    echo "-----> srcfile: $srcfile"

    ## get analysis
    if echo $file | grep 2los > /dev/null; then samples=$metadata/2los_mcfakes.txt
    elif echo $file | grep 3l > /dev/null; then samples=$metadata/3l_mcfakes.txt
    else
	echo "couldn't identify analysis for $file, skipping.."
	continue
    fi

    ## get matching cuts & samples
    cuts=$(echo $line | sed "s/^[^,]*,//; s/,/@/g")
    samples=$(cat $samples | tr '\n' '@')
    oldifs=$IFS && IFS='@'

    ## write file
    #echo "## file: $(echo $file)" >> $buildfile
    #echo >> $buildfile
    for cut in $cuts; do
	echo "-----> cut: $cut";
    weight=$(echo $cut | sed -r "s/^(.[^ ]*) .*/\1/" | sed "s/_SHYEAR//")
	echo "## weight: $weight" >> $buildfile

	## get extra info from the src file
	# echo $weight
	weight=$(echo $weight | sed s/\*.*//)
	name=$(grep $weight $srcfile | sed -r "s/^([^:]*):.*/\1/; s/ *$//" | grep -v ^# | sort -u)
	label=$(grep $weight $srcfile | grep -o "Label=[^,]*" | sed "s/ *$//" | sort -u)
	color=$(grep $weight $srcfile | grep -o "FillColor=[^,]*" | sed "s/ *$//" | sort -u)
	echo $name
	echo $label
	echo $color
	$(echo $label | wc | awk '{if ($1>1) print "true"; else print "false"}') && uselookup=true || uselookup=false

	for sample in $samples; do
        ## get the year
        [[ $sample =~ 201[678] ]] && { year=$sample; shyear=${year: -2}; printf "\n## $year\n"  >> $buildfile; continue; }
	    ## skip these lines
	    { [ "$sample" == "----" ] || [[ $sample =~ ^$ ]]; } && continue

	    ## check if the sample is commented out and modify cut
	    [[ $sample =~ ^\#[^\#]* ]] && { # if the sample is commented out, move '#' before line
		sample=$(echo $sample | sed s/^#//)
		name="#$name"
	    }

	    #echo $cut
        cutmodded=$(echo $cut| sed "s@SHYEAR@$shyear@"| sed "s@/YEAR/@/$year/@")
        #echo $cutmodded
        # if label is not unique, get info for label from the look up function
	    $uselookup && label=$(getLabel $sample)

	    ## print the line
	    if echo $cutmodded | grep "; *$" > /dev/null; then
            printf "%-25s:%-30s:%s %s,%s,years=\"%s\"\n" $name $sample $cutmodded $label $color $year >> $buildfile
	    else
            printf "%-25s:%-30s:%s,%s,%s,years=\"%s\"\n" $name $sample $cutmodded $label $color $year >> $buildfile
	    fi

	    ## clean '#' for the next use
	    name=$(echo $name | sed s/^#//)
	done
	echo >> $buildfile
    done
    IFS=$oldifs # revert delimeter splitting

    ## move the tmp file to its correct name (only of not draft)
    ! $mkdraft && mv $buildfile $(echo $buildfile | sed s/\.tmp$//)
    $onefile && break # testing
done

exit 0
