OUTDIR=/data1/peruzzi/skim

for year in $*
do
    FIXMET=""
    if [[ "${year}" -eq "2017" ]]
    then
	FIXMET="--mcc susy-sos/mcc_METFixEE2017.txt"
    fi
    python skimTreesNew.py --skim-friends --Fs {P}/recleaner -P /eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6/${year} -f -j 8 --split-factor=-1 --year ${year} --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos.txt --mcc susy-sos/mcc_triggerdefs.txt ${FIXMET} -p data susy-sos/mca-includes/${year}/mca-skim-${year}.txt susy-sos/skim_2lep_met125.txt ${OUTDIR}/${year}
    python skimTreesNew.py --skim-friends --Fs {P}/recleaner --FMCs {P}/bTagWeights --FMCs {P}/jetmetUncertainties -P /eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6/${year} -f -j 8 --split-factor=-1 --year ${year} --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos.txt --mcc susy-sos/mcc_triggerdefs.txt ${FIXMET} --xp data susy-sos/mca-includes/${year}/mca-skim-${year}.txt susy-sos/skim_2lep_met125.txt ${OUTDIR}/${year}
done
