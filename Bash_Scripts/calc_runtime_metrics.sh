#/bin/bash

SEED=$1
ISLAND=$2


JAVA_ARGS="-cp MOEAFramework-2.9-Demo.jar"
java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 2 -i runtime/LakeComo_S${SEED}_M${ISLAND}.runtime -r sets/ComoTest.reference -o S${SEED}_M${ISLAND}.metrics

