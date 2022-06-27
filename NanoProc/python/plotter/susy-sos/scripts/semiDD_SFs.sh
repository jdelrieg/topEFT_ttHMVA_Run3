BASE_DIR=${1}; shift
LEP=2los
for YEAR in 2016 2017 2018
do
    for BIN in low med high
    do
        for REG in appl appl_col cr_ss
        do
            for SF in 1F_NoSF 2F_NoSF
            do
                [[ ${REG} == "cr_ss" && ${BIN} != "med" ]] && continue
                eval "$(python susy-sos/sos_plots.py ${BASE_DIR} --year ${YEAR} --lep ${LEP} --reg ${REG}_${SF} --bin ${BIN} --fakes mc --data --inPlots yields)"
                if [[ ${REG} == *"col"* ]]; then TXTNAME=col_${BIN}; else TXTNAME=appl_${BIN}; fi
                if [[ ${REG} == "cr_ss" ]]; then TXTNAME=cr_ss; fi
                echo "$(python susy-sos/scripts/semiDD_SFs.py ${BASE_DIR} ${YEAR} --lep ${LEP} --reg ${REG}_${SF} --bin ${BIN})" >> susy-sos/fakerate/${LEP}/ScaleFactors_SemiDD/mcc_SF_${TXTNAME}.txt
            done
        done
    done
done

LEP=3l
REG=appl
for YEAR in 2016 2017 2018
do
    for BIN in low med
    do
        for SF in 1F_NoSF 2F_NoSF 3F_NoSF
        do
            eval "$(python susy-sos/sos_plots.py ${BASE_DIR} --year ${YEAR} --lep ${LEP} --reg ${REG}_${SF} --bin ${BIN} --fakes mc --data --inPlots yields)"
            echo "$(python susy-sos/scripts/semiDD_SFs.py ${BASE_DIR} ${YEAR} --lep ${LEP} --reg ${REG}_${SF} --bin ${BIN})" >> susy-sos/fakerate/${LEP}/ScaleFactors_SemiDD/mcc_SF_${BIN}.txt
        done
    done
done

