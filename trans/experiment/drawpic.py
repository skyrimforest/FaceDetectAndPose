
import matplotlib.pyplot as plt



if __name__ == '__main__':

    fig,ax1 = plt.subplots(figsize=(8,6))
    x=[128,160,320,480,640]
    time=[1.5777130126953125,
            1.6365549564361572,
            1.909911870956421,
            1.9849967956542969,
            2.112592935562134,]
    pre=[0.9062736249632306,
            0.9215976809843992,
            0.9544568109412154,
            0.9573866875290521,
            0.956705862917186,]
    plt.xlabel('Resolution')
    plt.grid(True)

    plt.title('Time Cost and Precision tendency with resolution')

    ax1.set_ylabel('Time (seconds)')
    ax1.plot(x,time,label='Time Cost',color='red',linewidth=2,linestyle='--')
    ax1.set_ylim([1,2.5])
    for x_it, y in zip(x, time):
        ax1.text(x_it, y, f'{y:.2f}', ha='center', va='bottom')


    ax2=ax1.twinx()
    ax2.plot(x,pre,label='Precision',color='blue',linewidth=2,linestyle='solid')
    ax2.set_ylabel('Precision')
    ax2.set_ylim([0.9,0.98])
    for x_it, y in zip(x, pre):
        ax2.text(x_it, y, f'{y:.2f}', ha='center', va='bottom')

    fig.legend()
    fig.show()
