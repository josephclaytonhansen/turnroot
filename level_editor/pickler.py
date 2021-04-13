import pickle
with open('tmp/kybs.trkp', 'rb') as fh:
    pickle_cuts = pickle.load(fh)
print(pickle_cuts)