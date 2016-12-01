import matplotlib.pyplot as plt

def presentData(pandas_frame, columns=[]):
    indices = range(len(pandas_frame.index))
    plt.title('Chart')
    for column in columns:
        data = map(float, list(pandas_frame[column]))
        plt.plot(indices, data)

    plt.legend(columns, loc='upper left')
    plt.show()

def saveChart(pandas_frame, columns=[], file_name='figure.png'):
    indices = range(len(pandas_frame.index))
    plt.title('Chart')
    for column in columns:
        data = map(float, list(pandas_frame[column]))
        plt.plot(indices, data)

    plt.legend(columns, loc='upper left')
    plt.savefig(file_name)
    plt.close()


