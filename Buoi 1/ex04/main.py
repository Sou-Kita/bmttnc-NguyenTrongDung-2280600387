from QLSV import QLSV

qlsv = QLSV()

while (1==1):
    print("\nCHUONG TRING QUAN LY SINH VIEN")
    print("*************************MENU*************************")
    print("** 1. Them sinh vien.                               **")
    print("** 2. Cap nhat thong tin sinh vien boi ID.          **")
    print("** 3. Xoa sinh vien boi ID.                         **")
    print("** 4. Tim kiem sinh vien theo ten.                  **")
    print("** 5. Sap xep sinh vien theo diem trung binh.       **")
    print("** 6. Sap xep sinh vien theo ten chuyen nganh.      **")
    print("** 7. Hien thi danh sach sinh vien.                 **")
    print("** 0. Thoat chuong trinh.                           **")
    print("******************************************************")
    
    key = int(input("Nhap lua chon: "))
    if (key == 1):
        print("\n1. Them sinh vien.")
        qlsv.nhapSinhVien()
        print("\nThem sinhvien thanh cong!")
    elif (key == 2):
        if (qlsv.soLuongSinhVien()>0):
            print("\n2. Cap nhat thong tin sinh vien boi ID.")
            ID = int(input("Nhap ID sinh vien: "))
            qlsv.updateSinhVien(ID)
        else:
            print("\nKhong co sinh vien nao trong danh sach!")
    elif (key == 3):
        if (qlsv.soLuongSinhVien()>0):
            print("\n3. Xoa sinh vien boi ID.")
            ID = int(input("Nhap ID sinh vien: "))
            if(qlsv.deleteByID(ID)):
                print("\nSinh vien co id = ",ID, "da bi xoa!")
            else:
                print("\nSinh vien co id = ",ID, "khong ton tai!")
        else:
            print("\nKhong co sinh vien nao trong danh sach!")
    elif (key == 4):
        if (qlsv.soLuongSinhVien()>0):
            print("\n4. Tim kiem sinh vien theo ten.")
            print("Nhap ten sinh vien: ")
            name = input()
            searchResult = qlsv.findByName(name)
            qlsv.showSinhVien(searchResult)
        else:
            print("\nKhong co sinh vien nao trong danh sach!")
    elif (key == 5):
        if (qlsv.soLuongSinhVien()>0):
            print("\n5. Sap xep sinh vien theo diem trung binh.")
            qlsv.sortByDiemTB()
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\nKhong co sinh vien nao trong danh sach!")
    elif (key == 6):
        if (qlsv.soLuongSinhVien()>0):
            print("\n6. Sap xep sinh vien theo ten chuyen nganh.")
            qlsv.sortByName()
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\nKhong co sinh vien nao trong danh sach!")
    elif (key == 7):
        if (qlsv.soLuongSinhVien()>0):
            print("\n7. Hien thi danh sach sinh vien.")
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\nKhong co sinh vien nao trong danh sach!")
    elif (key == 0):
        print("\nBan da chon thoat chuong trinh!")
        break
    else:
        print("\nKhong co chuc nang nay trong chuong trinh!")
        print("\nHay chon chuc nang trong hop menu.")