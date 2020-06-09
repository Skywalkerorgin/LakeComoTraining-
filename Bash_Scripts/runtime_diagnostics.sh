# set number of seeds
SEEDS=$(seq 0 5)
ISLANDS=$(seq 0 1)
JAVA_ARGS="-cp MOEAFramework-2.9-Demo.jar"

# .set files need to add three lines to the top of the file to describe the problem (for MOEAFramework to recognize)
sed -i '1i # Objectives = 2' sets/*.set
sed -i '1i # Variables = 46' sets/*.set
sed -i '1i # Problem = Como' sets/*.set

# .set files also need a # at the end for MOEA framework to recognize
for SEED in ${SEEDS}
do
	echo "#" >> sets/LakeComo_S${SEED}.set
done

# Find the reference set with DVs using the MOEAFramework
java -cp MOEAFramework-2.9-Demo.jar org.moeaframework.analysis.sensitivity.ResultFileMerger -r sets/* -o sets/ComoTestDVs.reference -e 0.01,0.01 -d 2 -v 46

# create a reference set file without DVs (for runtime diagnostics)
java -cp MOEAFramework-2.9-Demo.jar org.moeaframework.analysis.sensitivity.ResultFileSeedMerger sets/*.set -o sets/ComoTest.reference -e 0.01,0.01 -d 2

# calc runtime metrics with the calc_runtime_metrics.sh script
# (THIS WILL SUBMIT 6 JOBS INTO THE QUEUE!)
for ISLAND in ${ISLANDS}
do
for SEED in ${SEEDS}
do
SLURM="#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=1\n\
#SBATCH --export=ALL\n\
#SBATCH -t 2:00:00\n\
#SBATCH --job-name=calc_metrics_como_S${SEED}_M${ISLAND}\n\
#SBATCH --output=metrics_info_como_S${SEED}_M${ISLAND}.out\n\
#SBATCH --error=metrics_info_como_S${SEED}_M${ISLAND}.error\n\

./calc_runtime_metrics.sh ${SEED} ${ISLAND}"

echo -e $SLURM | sbatch
sleep 0.5
done
done