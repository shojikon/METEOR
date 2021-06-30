from bisect import bisect_left


def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before

def fragmentation(ref_list, cand_list, vc, flow):
    try:
        chunks = 1
        matched_unigrams = 0

        current = -1
        for i, w in enumerate(ref_list):
            if w in vc.get_feature_names():
                index = vc.get_feature_names().index(w)
                flow_from_w = flow[index]
                highest_flow = max(flow_from_w)

                if not highest_flow == 0:
                    feature_names_matched_indices = [
                        i for i, x in enumerate(flow_from_w) if x == highest_flow]
                    matched_words = [vc.get_feature_names()[i]
                                     for i in feature_names_matched_indices]

                    # check cases where word doesn't map to anything.
                    matched_indices = []
                    for m in matched_words:
                        occurrences = []
                        for i, x in enumerate(cand_list):
                            if x == m:
                                occurrences.append(i)
                        matched_indices.append(
                            takeClosest(occurrences, current))
                    matched_index = takeClosest(matched_indices, current)

                    if not current + 1 == matched_index:
                        chunks += 1
                    current = matched_index
                    matched_unigrams += 1

        return chunks / matched_unigrams
    except IndexError:
        return 0