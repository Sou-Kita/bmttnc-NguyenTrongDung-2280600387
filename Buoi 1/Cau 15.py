def dem_so_lan_xuat_hien(lst):
    count_dict = {}
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict
input_String = input("Nhập danh sách các từ, cách nhau bằng dấu phẩy: ")
word_list = input_String.split(',')
so_lan_xuat_hien = dem_so_lan_xuat_hien(word_list)
print("Số lần xuất hiện của các phần tử là", so_lan_xuat_hien)