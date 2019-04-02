from mle import mle_cal
import operator

def secondStage():
	CentralityOfCC, nodeOfCC = mle_cal('code/BetaStage/secondStageInput.txt')
	source = max(CentralityOfCC.items(), key=operator.itemgetter(1))[0]
	return source
