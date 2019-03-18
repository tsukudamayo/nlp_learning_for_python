from sklearn.externals import joblib

if __name__ == '__main__':
    model = joblib.load('result/model.pkl')
    vocab = joblib.load('result/vocab.pkl')

    # 学習済モデルの確認
    for weight, word in sorted(zip(model.coef_[0], vocab), reverse=True):
        print('{0:f} {1:s}'.format(weight, word))
