import numpy as np

STOP = set(
    'l le la les au aux un une du des c ça ce cette cet ces celle celui celles ceux je j tu il elle on nous vous ils '
    'elles me m te t se s y à de pour sans par mais ou et donc car ni or ne n pas dans que qui qu de d mon ma mes ton '
    'ta tes son sa ses notre nos votre vos leur leurs lui en quel quelle quelles lequel laquelle lesquels lesquelles '
    'dont quoi quand où comment pourquoi sur dessus tout tous toutes avec comme avec'.split())


class Prediction:
    @staticmethod
    def ls(u: np.array, v: np.array) -> float:
        return np.sum((u - v) ** 2)

    @staticmethod
    def cb(u: np.array, v: np.array) -> float:
        return np.sum(np.abs(u - v))

    @staticmethod
    def predire(d: dict, m: np.array, mot: str, n: int, methode: int) -> list:
        if methode == 0:
            f = np.dot
        elif methode == 1:
            f = Prediction.ls
        elif methode == 2:
            f = Prediction.cb
        i = d[mot]
        v = m[i]
        scores = []
        for _mot, _i in d.items():
            if _i != i and _mot not in STOP:
                scores.append((_mot, f(v, m[_i])))
        return sorted(scores, key=lambda t: t[1], reverse=f == np.dot)[:n]
