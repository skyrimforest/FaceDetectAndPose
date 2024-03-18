import pickle

width=1024
height=695
with open("beforenms.pkl","rb") as f1:
    with open("afternms.pkl","rb") as f2:
        beforeNms = pickle.load(f1)
        afterNms = pickle.load(f2)
        print("beforeNms: ",beforeNms)
        with open("beforenms2.pkl","wb")as f:
            beforeNms[:, 0] *= width
            beforeNms[:, 1] *= height
            beforeNms[:, 2] *= width
            beforeNms[:, 3] *= height
            pickle.dump(beforeNms, f)
        print(beforeNms)
        with open("afternms2.pkl","wb")as f:
            afterNms[:, 0] *= width
            afterNms[:, 1] *= height
            afterNms[:, 2] *= width
            afterNms[:, 3] *= height
            pickle.dump(afterNms, f)
        print(afterNms)