from sqlalchemy.ext.asyncio import AsyncSession
from geopy.geocoders import Nominatim
from datetime import datetime, timezone, timedelta
import random
from ..models import (
    Station, StationVehicle, Vehicle, VehicleInsurance,
    VehicleTracking, VehicleMaintenance, VehicleBatteryLog
)
from sqlalchemy.future import select

# Khởi tạo geolocator
geolocator = Nominatim(user_agent="station_locator")

# Dữ liệu địa chỉ
stations_data = [
    ("Hàm Nghi", "10 Hàm Nghi - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    ("Trường Cao đẳng Kỹ thuật Cao Thắng", "126 Hàm Nghi - Phường Nguyễn Thái Bình - Quận 1 - TP Hồ Chí Minh"),
    ("Công ty Cổ phần Vận tải Đường sắt Sài Gòn", "136 Hàm Nghi - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    ("Thương xá Tax", "102 Nguyễn Huệ - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    ("Nguyễn Huệ", "1 Nguyễn Huệ - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Sở Giao dịch Chứng khoán", "130-166 Nguyễn Công Trứ - Phường Nguyễn Thái Bình - Quận 1 - TP Hồ Chí Minh"),
    ("Phạm Hồng Thái", "46 Phạm Hồng Thái - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    ("Công viên 23/9 (đường Phạm Ngũ Lão)", "111-103 Phạm Ngũ Lão - Phường Phạm Ngũ Lão - Quận 1 - TP Hồ Chí Minh"),
    # ("Công viên 23/9 (đường Phạm Ngũ Lão)", "Đối diện 201 Phạm Ngũ Lão - Quận 1 - TP Hồ Chí Minh"),
    ("Tòa nhà Kumho", "39 Lê Duẩn - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Công viên 30/4", "Công viên 30/4 - Lê Duẩn - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    ("Thảo Cầm Viên", "2 Nguyễn Bỉnh Khiêm - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Công viên Tao Đàn", "Công viên Tao Đàn - Trương Định - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    ("Cung Văn hóa Lao Động", "57 Nguyễn Thị Minh Khai - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    ("Tổng công ty xây dựng Số 1", "111a Pasteur, Phường Bến Nghé, Quận 1, TP Hồ Chí Minh"),
    ("Nhà văn hóa Thanh Niên", "4 Phạm Ngọc Thạch - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    ("Mạc Đĩnh Chi", "22 Nguyễn Thị Minh Khai - Phường Đa Kao - Quận 1 - TP Hồ Chí Minh"),
    ("Trung tâm TDTT Hoa Lư", "2 Đinh Tiên Hoàng - Phường Đa Kao - Quận 1 - TP Hồ Chí Minh"),
    ("Công xã Paris", "1 Công xã Paris - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    ("Khách sạn Le Méridien Saigon", "3c Tôn Đức Thắng - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Trung tâm thương mại Sài Gòn", "37 Đường Tôn Đức Thắng - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Bảo tàng Tôn Đức Thắng", "5 Tôn Đức Thắng - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Lê Thánh Tôn", "2 Lê Thánh Tôn - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Sở Kế hoạch Đầu tư", "32 Lê Thánh Tôn - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Công viên Chi Lăng", "Lê Thánh Tôn - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Bảo tàng Hồ Chí Minh", "65 Lý Tự Trọng - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Công Trường Lam Sơn", "15 Công Trường Lam Sơn - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Trường Mầm Non Bé Ngoan", "108 Nguyễn Đình Chiểu - Phường Đa Kao - Quận 1 - TP Hồ Chí Minh"),
    # ("Khách Sạn Park Hyatt Sài Gòn", "15 Hai Bà Trưng - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Lê Thị Hồng Gấm", "159 Lê Thị Hồng Gấm - Phường Cầu Ông Lãnh - Quận 1 - TP Hồ Chí Minh"),
    # ("Trung tâm thương mại Saigon Centre", "65 Lê Lợi - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Bệnh viện đa khoa Sài Gòn", "123 Lê Lợi - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    # ("Trường Tiểu Học Trần Hưng Đạo", "250 Đường Trần Hưng Đạo - Phường Nguyễn Cư Trinh - Quận 1 - TP Hồ Chí Minh"),
    # ("Trống Đồng", "12b Cách Mạng Tháng 8 - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    # ("Huyền Trân Công Chúa", "1 Huyền Trân Công Chúa - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    # ("Bệnh viện Nhi Đồng 2", "33 Nguyễn Du - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Chu Mạnh Trinh", "31 Nguyễn Du - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Công viên Lê Văn Tám", "Đối diện 227 Điện Biên Phủ - Phường Đa Kao - Quận 1 - TP Hồ Chí Minh"),
    # ("Lê Lai", "60 Lê Lai - Phường Phạm Ngũ Lão - Quận 1 - TP Hồ Chí Minh"),
    # ("Công viên 23/9 (đường Lê Lai)", "Đối diện 144-146 Lê Lai - Phường Bến Thành - Quận 1 - TP Hồ Chí Minh"),
    # ("Công viên 23/9 (đường Phạm Ngũ Lão)", "Đối diện 311 Phạm Ngũ Lão - Phường Phạm Ngũ Lão - Quận 1 - TP Hồ Chí Minh"),
    # ("UBND Quận 1", "34 Công xã Paris - Phường Bến Nghé - Quận 1 - TP Hồ Chí Minh"),
    # ("Văn phòng TNGo Hồ Chí Minh", "13M đường số 14 khu dân cư Miếu Nổi - Phường 3 - Quận Bình Thạnh - TP Hồ Chí Minh"),
    # ("Khách sạn Wink", "75 Nguyễn Bỉnh Khiêm - Phường Đa Kao - Quận 1 - TP Hồ Chí Minh"),
    # ("TINI Coworking", "152 Đ. Võ Văn Kiệt Phường Nguyễn Thái Bình Quận 1"),
    # ("Nguyễn Siêu", "18 Nguyễn Siêu, phường Bến Nghé, Quận 1, TP Hồ Chí Minh"),
    # ("Trạm Ga Metro Bến Thành (Đường Lê Lai)", "20 Lê Lai, Phường Bến Thành, Quận 1, TP Hồ Chí Minh"),
    # ("Trạm Ga Metro Bến Thành (Đường Trần Hưng Đạo)", "Đối diện 201 Phạm Ngũ Lão - Quận 1 - TP Hồ Chí Minh")
]

qr_code={1: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338933/zkljwxd7vqblk0yad2bm.png'}, 2: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338935/onadkxl3mphqa1nvwsvz.png'}, 3: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338935/crslrgqobosiqoafzorv.png'}, 4: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338936/zunjasddqgam8yvr10nc.png'}, 5: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338937/fhmdpr6fyl0gjso4wtem.png'}, 6: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338937/hccs2w01zzuw5mknw0vw.png'}, 7: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338938/pxe2oweyfkfa2otksqv2.png'}, 8: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338939/cy37wj8jlpitxsn7l5jt.png'}, 9: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338940/hnmfwdvjfsswtxu5e4er.png'}, 10: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338941/utllwmvxyypw5pdurmir.png'}, 11: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338941/x9zjdsbkqyzykpvselpq.png'}, 12: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338943/trpy4odiim82srzly2yf.png'}, 13: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338943/lgd09613r55bpqmqepvb.png'}, 14: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338944/nvezu0k6uthfgld4uprc.png'}, 15: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338945/bla9qbxphjo0blf3sn27.png'}, 16: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338945/eed9znxgnn3koq2m5ttk.png'}, 17: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338946/tz2alq6gujz9relhocjn.png'}, 18: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338947/psyz9wcgndwxo7moo40j.png'}, 19: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338947/juzuig8paeuprkytlljl.png'}, 20: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338948/ujhulb74a7xpa47jer2p.png'}, 21: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338949/qh5va1dvan57alo9wltw.png'}, 22: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338950/qgafjqosuase8kwacvqc.png'}, 23: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338950/mn9uzeqjaz9kqc5sttmf.png'}, 24: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338951/tk1whp6u6ngcmc4rbgui.png'}, 25: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338952/eqtuqdmhtxzpcckrppjo.png'}, 26: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338953/rp2kiysdhhfyhujsn7g6.png'}, 27: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338954/a5kkbuwkdmdmfxwptzxa.png'}, 28: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338954/qn9jzmfcghy2wc7oipvy.png'}, 29: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338955/ho81jrkrlkyxovejo8ka.png'}, 30: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338955/f7jlcidefm28n8lcumdq.png'}, 31: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338956/dm52l7vuf3bca9hwfylq.png'}, 32: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338957/dedwjvvrpsftypf7r6i8.png'}, 33: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338958/rf6ji2372r0hxetllino.png'}, 34: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338958/kocwtmmifqsgw1nlyycg.png'}, 35: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338959/n1poht0wlqovutt4wqaw.png'}, 36: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338960/gb9nfdccpxjj0niym2ii.png'}, 37: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338960/luznictgyxbxyjm0xost.png'}, 38: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338961/bkhthhnlfn2ki6kkaia1.png'}, 39: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338961/ftokvr1s62zhcnl2ta1p.png'}, 40: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338962/bg825pcigjbmb6prikfq.png'}, 41: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338963/ga9bvrvczwn6hyhlbbvh.png'}, 42: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338963/tyochtfsdk8d77zy7214.png'}, 43: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338964/urpne5p6m4s5b3epkpyl.png'}, 44: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338965/d5srtgkpadx8nemmuj1j.png'}, 45: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338965/ekxl5amsksdngwkqzzxv.png'}, 46: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338966/fzxfc8izr554lxmcdtyy.png'}, 47: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338966/lxtq6lu1mrnhtskxlbmn.png'}, 48: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338967/kim4nvd5ejdavycc2sun.png'}, 49: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338968/rixep2oh9x6cvazo5o3e.png'}, 50: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338968/d501ypplnhnywnufkpsi.png'}, 51: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338969/br2njc1vstaqxknyefco.png'}, 52: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338970/frega6ddcxcsxbi4msmi.png'}, 53: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338971/z2hquujljvbcm8vuz0iq.png'}, 54: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338972/wv3ic9kenponaukastlu.png'}, 55: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338972/ww7orwbjufc7r0fuxxfq.png'}, 56: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338973/g6ncbxoma2nmm77gzn7l.png'}, 57: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338974/eoot42tiupc9r0zfqtoe.png'}, 58: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338974/cahproxavwxtpasalxxl.png'}, 59: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338975/jrozy9dayobswyjzx0zj.png'}, 60: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338976/tnlsfi4saatkl8u5cxs7.png'}, 61: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338976/bcqkspbxeeqmstu5ke4k.png'}, 62: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338977/pos0uypsic0edhob6dwn.png'}, 63: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338978/zufy1kksbbsirb28vaux.png'}, 64: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338978/d1pdaffzgc3c6ouqopqj.png'}, 65: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338979/uonpxnhukw3bz41bl44c.png'}, 66: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338980/pw8nk9zxowi8jk2orrne.png'}, 67: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338981/w7vzycvtvl6yolqkxxoz.png'}, 68: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338981/l2nkfac3aiccp8yope24.png'}, 69: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338982/expdjife6yez4jkyvdw5.png'}, 70: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338982/bzl5s6iktr7kc7jtdysp.png'}, 71: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338984/obnw7xgqropw8tpmigd1.png'}, 72: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338985/k5mp1iylwrzptrbiplkl.png'}, 73: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338985/w11dqsnqzrlvnsvzevzv.png'}, 74: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338986/ke4d6badydztj62i7ke2.png'}, 75: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338987/x011k3tze6fsca0njrwb.png'}, 76: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338987/zntuuxzfnt22umq0qsri.png'}, 77: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338988/h5uovqitsqixzncprext.png'}, 78: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338989/oynuvordsrjugtoytj1v.png'}, 79: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338989/fxm2ppyvj5pbjvhlaosc.png'}, 80: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338990/nn8h7schhqhazwkkxfsd.png'}, 81: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338991/glabyjlp7vryiblaolhk.png'}, 82: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338991/bgi0ujstyusu6t5ibk4j.png'}, 83: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338992/wxezhxiuoemm7ybjcfuc.png'}, 84: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338992/ye6brinm8y6gosc3mc0n.png'}, 85: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338993/iswocmk7yzus8cvklhes.png'}, 86: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338994/lbzkbmj1reaucwmz5xyg.png'}, 87: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338994/vvlr98zhorfq7iihyd6p.png'}, 88: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338995/jpreqwxyugafxj3fqq4l.png'}, 89: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338996/l9lte5mqcopgd6lq2mqc.png'}, 90: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338996/bgsuc2mcndtpgcbuyjk2.png'}, 91: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338997/mcyj6sysutzs2arbafdu.png'}, 92: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338998/bxdlz4d7jbzsv4e1ju5g.png'}, 93: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338998/n2qye3evymt9xtn64nou.png'}, 94: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740338999/jhsknb4cwydbqiwnzlbe.png'}, 95: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740339000/ale4yodqm9jegg45zt9k.png'}, 96: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740339000/wcbe1bky3qqglofxvsdh.png'}, 97: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740339001/dn08tseomm75upuj0avl.png'}, 98: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740339002/yt0jrrdjpjjvkedmweit.png'}, 99: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740339002/r2yuepcndpgcj9phdf5z.png'}, 100: {'url': 'https://res.cloudinary.com/dvysar483/image/upload/v1740339003/wg6w2gnhbrje7zms6xq5.png'}}

def get_lat_lon(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None


qr_code_mapping = {item_id: data["url"] for item_id, data in qr_code.items()}


async def seed_data(db: AsyncSession):
    result = await db.execute(select(Station))
    existing_stations = result.scalars().all()
    vehicle_count: int = 1

    if not existing_stations:
        for name, address in stations_data:
            latitude, longitude = get_lat_lon(address)
            if latitude and longitude:
                station = Station(
                    name=name,
                    location=address,
                    latitude=latitude,
                    longitude=longitude,
                    total_slots=10,
                    available_vehicles=5,
                    charging_capacity=3,
                    status="active"
                )
                db.add(station)
                await db.flush()

                vehicles = []
                for i in range(5):  # Seed 5 xe cho mỗi trạm
                    qr_code_url = qr_code_mapping.get(vehicle_count, f"QR-{vehicle_count}")  # Nếu không có, gán mã mặc định
                    vehicle = Vehicle(
                        licence_plate=f"XX-{(9999 - vehicle_count)}",
                        model="Electric Scooter",
                        battery_capacity=100,
                        current_station_id=station.id,
                        total_km_driven=random.randint(1000, 5000),
                        last_maintenance_date=datetime.now(timezone.utc) - timedelta(days=30),
                        next_maintenance_due=datetime.now(timezone.utc) + timedelta(days=60),
                        insurance_expiry_date=datetime.now(timezone.utc) + timedelta(days=180),
                        qr_code=qr_code_url  # Ánh xạ QR Code từ danh sách
                    )
                    db.add(vehicle)
                    vehicles.append(vehicle)

                    await db.flush()  # Flush để lấy ID

                    # Seed các bảng liên quan
                    insurance = VehicleInsurance(
                        vehicle_id=vehicle.id,
                        provider_name="ABC Insurance",
                        policy_number=f"INS-{random.randint(1000, 9999)}",
                        start_date=datetime.now(timezone.utc) - timedelta(days=180),
                        expiry_date=datetime.now(timezone.utc) + timedelta(days=180),
                        coverage_details="Full coverage"
                    )
                    db.add(insurance)

                    tracking = VehicleTracking(
                        vehicle_id=vehicle.id,
                        current_latitude=latitude + random.uniform(-0.01, 0.01),
                        current_longitude=longitude + random.uniform(-0.01, 0.01),
                        speed=random.randint(0, 50),
                        battery_level=random.randint(20, 100)
                    )
                    db.add(tracking)

                    maintenance = VehicleMaintenance(
                        vehicle_id=vehicle.id,
                        maintenance_type="Battery Check",
                        start_date=datetime.now(timezone.utc) - timedelta(days=30),
                        end_date=datetime.now(timezone.utc) - timedelta(days=29),
                        cost=random.randint(50, 200),
                        maintenance_details="Routine battery check and replacement if needed"
                    )
                    db.add(maintenance)

                    battery_log = VehicleBatteryLog(
                        vehicle_id=vehicle.id,
                        station_id=station.id,
                        start_time=datetime.now(timezone.utc) - timedelta(hours=5),
                        end_time=datetime.now(timezone.utc) - timedelta(hours=4),
                        battery_before=random.randint(20, 50),
                        battery_after=random.randint(80, 100),
                        energy_used=random.randint(10, 30)
                    )
                    db.add(battery_log)

                    station_vehicle = StationVehicle(
                        station_id=station.id,
                        vehicle_id=vehicle.id,
                        arrival_time=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 10)),
                        departure_time=None,
                        charging_status="charging"
                    )
                    db.add(station_vehicle)

                    vehicle_count += 1

        await db.commit()
