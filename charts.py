import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import pandas as pd
from pandas.plotting import table

# TODO: 
# clean up code (as if lmao)

def text_length_factor(text_number): 
    if text_number < 10:
        return 2
    else:
        return 1

def make_chart(data_input, name, rows):
    w = 19.2
    h = 10.8
    sizefactor = 0.1
    x = 0
    for i in range(0,rows):
        x += 1
        if x == 10:
            sizefactor = sizefactor/1.2
            x = 0
    if rows > 4:
        h = h*rows*0.2
    elif rows > 10:
        h = h*rows*sizefactor
    


    plt.rcParams['figure.figsize'] = [w, h]
    plt.rc('font', size=20)

    plt.rc('axes', titlesize=32) #fontsize of the title
    plt.rc('axes', labelsize=16) #fontsize of the x and y labels
    plt.rc('xtick', labelsize=16) #fontsize of the x tick labels
    plt.rc('ytick', labelsize=16) #fontsize of the y tick labels
    plt.rc('legend', fontsize=16) #fontsize of the legend

    plt.rcParams["figure.autolayout"] = True
    plt.tight_layout()

    max_arr = []
    for row in data_input:
        max_arr.append(row[1])
        max_arr.append(row[2])
        max_arr.append(row[3])
    max_arr = np.array(max_arr)
    max_value = np.max(max_arr)

    df = pd.DataFrame(data_input, columns=['GPU', '0.1% Low', '1% Low', 'Average']
        )
    df = df.sort_values(by=['Average'])

    data_input = df.to_numpy()


    manipulated_data = []
    for line in data_input:
        manipulated_data.append([line[0], line[1], line[2] - line[1], line[3] - line[2]])

    # create data
    df = pd.DataFrame(manipulated_data, columns=['GPU', '0.1% Low', '1% Low', 'Average']
        )
        
    # plot data in stack manner of bar type
    ax = df.plot(x='GPU', kind='barh', stacked=True,
            title=name, xlabel="")

    for t in ax.get_yticklabels():
        t.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    
    for t in ax.get_xticklabels():
        #print(t)
        t.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])

    ax.title.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    ax.spines["top"].set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    ax.spines["left"].set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    ax.spines["right"].set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    ax.spines["bottom"].set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    

    # I have no idea what I'm doing.
    # That's a lie, but I sure don't know a lot of what I'm doing
    # The big if statements are the important part in making text not overlap
    col = 0
    remaining_space_in_one_percent_bar = {}
    space_in_one_percent_bar_used = {}
    col_1_text = {}
    for c in ax.containers:
        texts = ax.bar_label(c, label_type='edge')
        total_width = 0 
        for row in range(0, len(texts)):
            texts[row].set_text(data_input[row][col+1])
            width = c.patches[row].get_width()
            min_size = max_value/20
            graph_text_start = max_value/100
            space_in_average_bar = manipulated_data[row][3]
            space_in_one_percent_bar = manipulated_data[row][2]
            col_3 = data_input[row][3]
            col_2 = data_input[row][2]
            col_1 = data_input[row][1]
            txt = False
            if col == 0:
                texts[row].set_text("")
                if col_1 == col_3:
                    pass
                elif col_1 >= min_size/text_length_factor(col_1):
                    txt = ax.text(graph_text_start, row, data_input[row][col+1], ha='left', va='center')
                    col_1_text[row] = txt
                elif col_1 + space_in_one_percent_bar >= min_size/text_length_factor(col_1):
                    txt = ax.text(graph_text_start, row, data_input[row][col+1], ha='left', va='center')
                    col_1_text[row] = txt
                    space_in_one_percent_bar_used[row] = True
                    remaining_space_in_one_percent_bar[row] = col_2 - min_size/text_length_factor(col_1)
            elif col == 1:
                if space_in_one_percent_bar == 0:
                    texts[row].set_text("")
                elif col_3 < min_size/text_length_factor(col_2):
                    if col_1_text.get(row, False):
                        col_1_text.get(row, False).set_text("")
                    texts[row].set_text("")
                elif not space_in_one_percent_bar_used.get(row, False):
                    if space_in_one_percent_bar >= min_size/text_length_factor(col_2):
                        texts[row].set_text("")
                        txt = ax.text(col_2, row, data_input[row][col+1], ha='right', va='center')
                    elif space_in_average_bar < min_size/text_length_factor(col_2):
                        if space_in_average_bar + space_in_one_percent_bar >= min_size/text_length_factor(col_2):
                            texts[row].set_text("")
                            txt = ax.text(col_2, row, data_input[row][col+1], ha='center', va='center')
                        elif col_3 >= min_size/text_length_factor(col_2):
                            texts[row].set_text("")
                            if col_3 - min_size/text_length_factor(col_1) < min_size/text_length_factor(col_2):
                                if col_1_text.get(row, False):
                                    col_1_text.get(row, False).set_text("")
                                txt = ax.text(graph_text_start, row, data_input[row][col+1], ha='left', va='center')
                            else:
                                txt = ax.text(col_3, row, data_input[row][col+1], ha='right', va='center')
                elif space_in_one_percent_bar_used.get(row, False) and remaining_space_in_one_percent_bar.get(row, 0) >= min_size/text_length_factor(col_2):
                    texts[row].set_text("")
                    txt = ax.text(col_2, row, data_input[row][col+1], ha='right', va='center')
                elif space_in_one_percent_bar_used.get(row, False) and remaining_space_in_one_percent_bar.get(row, 0) < min_size/text_length_factor(col_2):
                    if space_in_average_bar < min_size/text_length_factor(col_2):
                        texts[row].set_text("")
                        if col_3 - min_size/text_length_factor(col_1) < min_size/text_length_factor(col_2):
                            if col_1_text.get(row, False):
                                    col_1_text.get(row, False).set_text("")
                            if col_1 + space_in_one_percent_bar >= min_size/text_length_factor(col_2):
                                txt = ax.text(col_2, row, data_input[row][col+1], ha='right', va='center')
                            else:   
                                txt = ax.text(graph_text_start, row, data_input[row][col+1], ha='left', va='center')
                        else:
                            txt = ax.text(col_3, row, data_input[row][col+1], ha='right', va='center')
            elif col == 2:
                if space_in_average_bar == 0:
                    texts[row].set_text("")
                    txt = ax.text(col_3, row, data_input[row][col+1], ha='left', va='center')
            texts[row].set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
            if txt:
                pass
                txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
            
        col += 1

    plt.legend(['0.1% Low', '1% Low', 'Average'],
           bbox_to_anchor = (1, 1))
    ax.grid(axis='x')
    for l in ax.get_xgridlines() + ax.get_ygridlines():
        l.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
    plt.savefig(f'images/{name}.png', transparent=True)
