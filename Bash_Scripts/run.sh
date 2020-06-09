# arguments are <seed> <NFE> <islands>
for SEED in 0 1 2 3 4 5
do
SLURM="#!/bin/bash\n\
#SBATCH --job-name=lakeComotest\n\
#SBATCH --output=lakeComotest_S${SEED}.txt\n\
#SBATCH --error=lakeComotest_S${SEED}.error\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=16\n\
#SBATCH --export=ALL\n\
#SBATCH -t 4:00:00\n\

module load gnu8/8.3.0\n\

mpirun ./LakeComo ${SEED} 2000000 2"

echo -e $SLURM | sbatch
sleep 0.5
done