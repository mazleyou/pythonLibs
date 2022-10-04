local_list = []
PAGE_MARGIN = 5


def add_y_height(i):
    for j in range(len(local_list)):
        if j != i and local_list[i][1] < local_list[j][1] + PAGE_MARGIN:
            local_list[j][1] = local_list[j][1] + local_list[i][3] - local_list[i][1] + PAGE_MARGIN
            local_list[j][3] = local_list[j][3] + local_list[i][3] - local_list[i][1] + PAGE_MARGIN
    return True


def minus_x_start(i, start_x):
    minus_value = local_list[i][2] - start_x
    local_list[i][2] = local_list[i][2] - minus_value
    local_list[i][4] = local_list[i][4] - minus_value
    return True


def add_y_axis(index_1, index_2):
    if local_list[index_1][2] < local_list[index_2][2]:
        # y값이 index_1의 값보다 큰 모든 요소에 index_1의 높이를 더한다.
        add_y_height(index_1)
        minus_x_start(index_2, local_list[index_1][2])
    else:
        add_y_height(index_2)
        minus_x_start(index_1, local_list[index_2][2])
    return True


def rerange(input_list):
    global local_list
    local_list = input_list
    # list[1]값이 비슷한 요소 찾기
    for i in range(len(local_list)):
        for j in range(i + 1, len(local_list)):
            if abs(local_list[i][1] - local_list[j][1]) < PAGE_MARGIN:
                add_y_axis(i, j)

    return local_list
