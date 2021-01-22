OUTDIR=/data1/peruzzi/skim

for year in $*
do  
    # All data
    python skimTreesNew.py --skim-friends --Fs {P}/recleaner -P /eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6/${year} -f -j 8 --split-factor=-1 --year ${year} --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos_allYears.txt -p data susy-sos/mca-includes/mca-skim-${year}.txt susy-sos/skim_2lep_met125.txt ${OUTDIR}/${year}
    
    # All MC except signal
    python skimTreesNew.py --skim-friends --Fs {P}/recleaner --FMCs {P}/bTagWeights --FMCs {P}/jetmetUncertainties -P /eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6/${year} -f -j 8 --split-factor=-1 --year ${year} --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos_allYears.txt --xp "data,SMS_(\w+)" susy-sos/mca-includes/mca-skim-${year}.txt susy-sos/skim_2lep_met125.txt ${OUTDIR}/${year}
    
    # SMS_T2tt(_ext),SMS_T2bW(_ext) (using signalWeights)
    python skimTreesNew.py --skim-friends --Fs {P}/recleaner --FMCs {P}/bTagWeights --FMCs {P}/jetmetUncertainties --FMCs {P}/signalWeights -P /eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6/${year} -f -j 8 --split-factor=-1 --year ${year} --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos_allYears.txt -p SMS_T2tt,SMS_T2tt_ext,SMS_T2bW,SMS_T2bW_ext susy-sos/mca-includes/mca-skim-${year}.txt susy-sos/skim_2lep_met125.txt ${OUTDIR}/${year}

    # SMS_TChiWZ(_ext),SMS_HiggsinoN2N1,SMS_HiggsinoN2C1,SMS_HiggsinoPMSSM (using signalWeights and isrWeights)
    if [[ "${year}" -eq "2016" ]]
    then
        ISR="--FMCs {P}/isrWeights"
    fi
    python skimTreesNew.py --skim-friends --Fs {P}/recleaner --FMCs {P}/bTagWeights --FMCs {P}/jetmetUncertainties --FMCs {P}/signalWeights ${ISR} -P /eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_070220_v6/${year} -f -j 8 --split-factor=-1 --year ${year} --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos_allYears.txt -p SMS_TChiWZ,SMS_HiggsinoN2N1,SMS_HiggsinoN2C1,SMS_HiggsinoPMSSM susy-sos/mca-includes/mca-skim-${year}.txt susy-sos/skim_2lep_met125.txt ${OUTDIR}/${year}

done
