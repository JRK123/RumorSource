from mle import mle_cal
import operator

CentralityOfCC, nodeOfCC = mle_cal('secondStageInput.txt')
source = max(CentralityOfCC.items(), key=operator.itemgetter(1))[0]
print(source)
