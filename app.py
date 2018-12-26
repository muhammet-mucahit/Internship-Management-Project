from flask import Flask, render_template, request, redirect, url_for
from database import Database
import xlsxwriter
import json

app = Flask(__name__)
app.secret_key = "secret key"

STAJ_BITIMI_MINIMUM_SURE = 57

cities = [
    'Adana',
    'Adıyaman',
        'Afyon',
        'Ağrı',
        'Amasya',
        'Ankara',
        'Antalya',
        'Artvin',
        'Aydın',
        'Balıkesir',
        'Bilecik',
        'Bingöl',
        'Bitlis',
        'Bolu',
        'Burdur',
        'Bursa',
        'Çanakkale',
        'Çankırı',
        'Çorum',
        'Denizli',
        'Diyarbakır',
        'Edirne',
        'Elazığ',
        'Erzincan',
        'Erzurum',
        'Eskişehir',
        'Gaziantep',
        'Giresun',
        'Gümüşhane',
        'Hakkari',
        'Hatay',
        'Isparta',
        'Mersin',
        'Istanbul',
        'Izmir',
        'Kars',
        'Kastamonu',
        'Kayseri',
        'Kırklareli',
        'Kırşehir',
        'Kocaeli',
        'Konya',
        'Kütahya',
        'Malatya',
        'Manisa',
        'Kahraman Maraş',
        'Mardin',
        'Muğla',
        'Muş',
        'Nevşehir',
        'Niğde',
        'Ordu',
        'Rize',
        'Sakarya',
        'Samsun',
        'Siirt',
        'Sinop',
        'Sivas',
        'Tekirdağ',
        'Tokat',
        'Trabzon',
        'Tunceli',
        'Şanlıurfa',
        'Uşak',
        'Van',
        'Yozgat',
        'Zonguldak',
        'Aksaray',
        'Bayburt',
        'Karaman',
        'Kırıkkale',
        'Batman',
        'Şırnak',
        'Bartın',
        'Ardahan',
        'Iğdır',
        'Yalova',
        'Karabük',
        'Kilis',
        'Osmaniye',
        'Düzce'
]

############################################################
########################## EXCEL ###########################


@app.route("/export_excel_uncompleted_students", methods=['GET'])
def export_excel_uncompleted_students():
    db = Database()
    completed_students = db.get_students_by_completing_internship(False)
    workbook = xlsxwriter.Workbook('UncompletedStudents.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Öğrenci No')
    worksheet.write('B1', 'İsim')
    worksheet.write('C1', 'Soyisim')
    worksheet.write('D1', 'Öğretim')

    i = 2
    for cs in completed_students:
        worksheet.write('A'+str(i), cs['ogrenci_no'])
        worksheet.write('B'+str(i), cs['isim'])
        worksheet.write('C'+str(i), cs['soyisim'])
        worksheet.write('D'+str(i), cs['ogretim'])
        i += 1

    workbook.close()
    return redirect("/students")


@app.route("/export_excel_completed_students", methods=['GET'])
def export_excel_completed_students():
    db = Database()
    completed_students = db.get_students_by_completing_internship(True)
    workbook = xlsxwriter.Workbook('CompletedStudents.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Öğrenci No')
    worksheet.write('B1', 'İsim')
    worksheet.write('C1', 'Soyisim')
    worksheet.write('D1', 'Öğretim')

    i = 2
    for cs in completed_students:
        worksheet.write('A'+str(i), cs['ogrenci_no'])
        worksheet.write('B'+str(i), cs['isim'])
        worksheet.write('C'+str(i), cs['soyisim'])
        worksheet.write('D'+str(i), cs['ogretim'])
        i += 1

    workbook.close()
    return redirect("/students")

############################################################
######################## SETTINGS ##########################


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        global STAJ_BITIMI_MINIMUM_SURE
        STAJ_BITIMI_MINIMUM_SURE = request.form['staj_bitti_suresi']
        return redirect("/")
    else:
        return render_template('settings.html')


############################################################
####################### STATISTICS #########################
topics_year = 2018


@app.route('/topics_chart', methods=['POST', 'GET'])
def topics_chart():
    db = Database()
    global topics_year
    if request.method == 'POST':
        topics_year = request.form['year']
        return redirect("/topics_chart")
    else:
        topics = db.list_topics()
        data_topics = [['Konu', 'Yüzde']]

        for t in topics:
            data = (t['isim'], topics_year, )
            count = db.get_topic_number_by_internship(data)['COUNT(*)']
            data_topics.append([t['isim'], count])

        db.close()

        return render_template('topics_chart.html', data_topics=data_topics, year=topics_year)


success_by_topics_year = 2018


@app.route('/success_by_topics_chart', methods=['POST', 'GET'])
def success_by_topics_chart():
    db = Database()
    global success_by_topics_year
    if request.method == 'POST':
        success_by_topics_year = request.form['year']
        return redirect("/success_by_topics_chart")
    else:
        topics = db.list_topics()
        data_topics = [['Konu', 'Başarı Oranı']]

        for t in topics:
            data = (t['isim'], success_by_topics_year, )
            if db.get_sum_of_accepted_days(data)['SUM(kabul_edilen_gun)'] and db.get_sum_of_total_days(data)['SUM(toplam_gun)']:
                accepted = db.get_sum_of_accepted_days(
                    data)['SUM(kabul_edilen_gun)']
                total = db.get_sum_of_total_days(data)['SUM(toplam_gun)']
                success_rate = accepted / total
            else:
                success_rate = 0

            data_topics.append([t['isim'], 100.0 * float(success_rate)])

        db.close()

        return render_template('success_by_topics_chart.html', data_topics=data_topics, year=success_by_topics_year)


@app.route('/success_by_cities')
def success_by_cities():
    global cities

    db = Database()

    data_topics = [['Şehir', 'Başarı Oranı']]

    for c in cities:
        data = (c,)
        if db.get_accepted_days_by_city(data)['SUM(kabul_edilen_gun)'] and db.get_total_days_by_city(data)['SUM(toplam_gun)']:
            accepted = db.get_accepted_days_by_city(
                data)['SUM(kabul_edilen_gun)']
            total = db.get_total_days_by_city(data)['SUM(toplam_gun)']
            success_rate = float(accepted) / float(total)
        else:
            success_rate = 0
        data_topics.append([c, 100.0 * float(success_rate)])

    db.close()

    return render_template('success_by_cities.html', data_topics=data_topics)

############################################################
########################## HOME ############################


@app.route('/')
def home():
    db = Database()
    students_number = db.get_students_number()
    topics_number = db.get_topics_number()
    internships_number = db.get_internships_number()
    interviews_number = db.get_interviews_number()

    #----------------------------------------------------------------
    topics = db.list_topics()
    data_topics = [['Konu', 'Yüzde']]

    for t in topics:
        data = (t['isim'], )
        count = db.get_topic_number(data)['COUNT(*)']
        data_topics.append([t['isim'], count])
    #----------------------------------------------------------------

    #----------------------------------------------------------------
    success_topics = [['Konu', 'Başarı Oranı']]

    for t in topics:
        data = (t['isim'], )
        if db.get_sum_of_accepted_days_general(data)['SUM(kabul_edilen_gun)'] and db.get_sum_of_total_days_general(data)['SUM(toplam_gun)']:
            accepted = db.get_sum_of_accepted_days_general(data)['SUM(kabul_edilen_gun)']
            total = db.get_sum_of_total_days_general(data)['SUM(toplam_gun)']
            success_rate = accepted / total
        else:
            success_rate = 0

        success_topics.append([t['isim'], 100.0 * float(success_rate)])
    #----------------------------------------------------------------

    #----------------------------------------------------------------
    success_cities = [['Şehir', 'Başarı Oranı']]

    for c in cities:
        data = (c,)
        if db.get_accepted_days_by_city(data)['SUM(kabul_edilen_gun)'] and db.get_total_days_by_city(data)['SUM(toplam_gun)']:
            accepted = db.get_accepted_days_by_city(
                data)['SUM(kabul_edilen_gun)']
            total = db.get_total_days_by_city(data)['SUM(toplam_gun)']
            success_rate = float(accepted) / float(total)
        else:
            success_rate = 0
        success_cities.append([c, 100.0 * float(success_rate)])
    #----------------------------------------------------------------


    db.close()
    return render_template('index.html', success_cities=success_cities, success_topics=success_topics, data_topics=data_topics, students_number=students_number, internships_number=internships_number, topics_number=topics_number, interviews_number=interviews_number)

############################################################
######################### SEARCH ###########################


@app.route('/search')
def search():
    db = Database()
    students = db.list_students()
    db.close()
    return render_template('search.html', students=students)

############################################################
######################### PROFILE ##########################


@app.route('/profile/<int:ogrenci_no>')
def profile(ogrenci_no):
    db = Database()
    student = db.get_student_by_student_number(ogrenci_no)
    internships = db.get_internships_by_student_number(ogrenci_no)
    db.close()
    return render_template('profile.html', student=student, internships=internships)

############################################################
######################## STUDENTS ##########################


@app.route('/students', methods=['GET', 'POST'])
def students():
    db = Database()
    completed_students = db.get_students_by_completing_internship(1)
    uncompleted_students = db.get_students_by_completing_internship(0)

    if request.method == 'POST':
        ogrenci_no = request.form['ogrenci_no']
        isim = request.form['isim']
        soyisim = request.form['soyisim']
        if request.form['ogretim'] == '0':
            ogretim = 0
        else:
            ogretim = 1

        if ogrenci_no and isim and soyisim:
            data = (ogrenci_no, isim, soyisim, ogretim, )
            db.add_student(data)
            return redirect('/students')
        else:
            return 'Error while adding student'

    db.close()
    return render_template('students.html', completed_students=completed_students, uncompleted_students=uncompleted_students)


@app.route('/students/<int:ogrenci_no>/delete')
def delete_student(ogrenci_no):
    db = Database()
    db.delete_student_by_student_number(ogrenci_no)
    db.close()

    return redirect('/students')

############################################################
######################### TOPICS ###########################


@app.route('/topics', methods=['GET', 'POST'])
def topics():
    db = Database()
    topics = db.list_topics()

    if request.method == 'POST':
        _name = request.form['name']
        if _name:
            db.add_topic(_name)
            return redirect('/topics')
        else:
            return 'Error while adding topic'

    db.close()
    return render_template('topics.html', topics=topics)


@app.route('/topics/<string:topic_name>/delete')
def delete_topic(topic_name):
    db = Database()
    db.delete_topic(topic_name)
    db.close()
    return redirect("/topics")


@app.route('/topics/<string:topic_name>/update', methods=['GET', 'POST'])
def update_topic(topic_name):
    db = Database()
    if request.method == 'POST':
        new_name = request.form['new_name']
        data = (new_name, topic_name)
        db.update_topic(data)
        return redirect('/topics')
    else:
        return render_template("update_topics.html", topic_name=topic_name)

############################################################
###################### INTERNSHIPS #########################


@app.route('/internships', methods=['GET', 'POST'])
def internships():
    db = Database()
    interviewed_internships = db.get_internships_by_is_interviewed(True)
    uninterviewed_internships = db.get_internships_by_is_interviewed(False)
    topics = db.list_topics()
    students = db.list_students()
    global cities

    if request.method == 'POST':
        ogrenci_no = request.form['ogrenci_no']
        kurum_adi = request.form['kurum_adi']
        sehir = request.form['sehir']
        baslama_tarihi = request.form['baslama_tarihi']
        bitis_tarihi = request.form['bitis_tarihi']
        toplam_gun = request.form['toplam_gun']
        staj_konusu = request.form['staj_konusu']
        ogrenci_sinif = request.form['ogrenci_sinif']
        dgs_mi = request.form['dgs_mi']
        if dgs_mi == 'Evet':
            dgs_mi = '1'
            kabul_edilen_gun = int(toplam_gun)
            kabul_edilen_gun /= 2
            staj_degerlendirildi = True
            kabul_edilen_gun = str(kabul_edilen_gun)
        else:
            dgs_mi = '0'
            kabul_edilen_gun = 0
            staj_degerlendirildi = False

        data = (ogrenci_no, kurum_adi, sehir, baslama_tarihi, bitis_tarihi, toplam_gun,
                staj_konusu, ogrenci_sinif, kabul_edilen_gun, staj_degerlendirildi, dgs_mi, )
        db.add_internship(data)
        return redirect('/internships')

    db.close()
    return render_template('internships.html', interviewed_internships=interviewed_internships, uninterviewed_internships=uninterviewed_internships, students=students, topics=topics, cities=cities)


@app.route('/internships/<int:ogrenci_no>/<string:baslama_tarihi>/delete')
def delete_internship(ogrenci_no, baslama_tarihi):
    db = Database()
    data = (ogrenci_no, baslama_tarihi)
    db.delete_internship(data)
    db.close()
    return redirect('/internships')


############################################################
####################### INTERVIEW ##########################
@app.route('/internships/<int:ogrenci_no>/<string:baslama_tarihi>/interview', methods=['GET', 'POST'])
def interview(ogrenci_no, baslama_tarihi):
    db = Database()

    if request.method == 'POST':
        tarih = request.form['tarih']
        saat = request.form['saat']
        komisyon1 = request.form['komisyon1']
        komisyon2 = request.form['komisyon2']
        data = (ogrenci_no, baslama_tarihi, tarih, saat, komisyon1, komisyon2,)
        db.add_interview(data)
        return redirect('/interviews')
    else:
        teachers = db.get_teachers()
        return render_template('interview_date.html', teachers=teachers, ogrenci_no=ogrenci_no, baslama_tarihi=baslama_tarihi)

    db.close()


@app.route('/interviews')
def interviews():
    db = Database()
    students = []
    commissions1 = []
    commissions2 = []
    interviews = db.get_interviews()
    for i in interviews:
        students.append(db.get_student_by_student_number(i['ogrenci_no']))
        commissions1.append(db.get_teachers_by_id(i['komisyon_uye1']))
        commissions2.append(db.get_teachers_by_id(i['komisyon_uye2']))

    return render_template('interviews.html', interviews=interviews, students=students, commissions1=commissions1, commissions2=commissions2)

    db.close()


@app.route('/interview/<int:ogrenci_no>/<string:baslama_tarihi>/delete')
def delete_interview(ogrenci_no, baslama_tarihi):
    db = Database()
    data = (ogrenci_no, baslama_tarihi,)
    db.delete_interview(data)
    return redirect("/interviews")

    db.close()


@app.route('/interview/<int:ogrenci_no>/<string:baslama_tarihi>/update', methods=['GET', 'POST'])
def update_interview(ogrenci_no, baslama_tarihi):
    db = Database()

    if request.method == 'POST':
        devam = request.form['devam']
        calisma = request.form['calisma']
        isi_vaktinde_yapma = request.form['isi_vaktinde_yapma']
        amire_davranis = request.form['amire_davranis']
        is_arkadaslarina_davranis = request.form['is_arkadaslarina_davranis']
        prove = request.form['prove']
        duzen = request.form['duzen']
        sunum = request.form['sunum']
        icerik = request.form['icerik']
        mulakat = request.form['mulakat']
        data = (devam, calisma, isi_vaktinde_yapma, amire_davranis,
                is_arkadaslarina_davranis, prove, duzen, sunum, icerik, mulakat, ogrenci_no, baslama_tarihi)
        db.update_interview(data)
        kabul_edilen_gun = (float(devam) * float(4) / 5) + (float(calisma) * float(4) / 5) + (float(isi_vaktinde_yapma)
                                                                                              * float(4) / 5) + (float(amire_davranis) * float(4) / 5) + (float(is_arkadaslarina_davranis) * float(4) / 5) + (float(prove) * float(15) / 100) + (float(duzen) * float(5) / 100) + (float(sunum) * float(5) / 100) + (float(icerik) * float(15) / 100) + (float(mulakat) * float(40) / 100)
        data = (ogrenci_no, baslama_tarihi,)
        internship = db.get_internship(data)
        kabul_edilen_gun = internship['toplam_gun'] * \
            (float(kabul_edilen_gun) / 100)
        data = (1, kabul_edilen_gun, ogrenci_no, baslama_tarihi)
        db.update_internship(data)
        if db.get_total_days_by_student_number(ogrenci_no)['SUM(toplam_gun)'] >= (STAJ_BITIMI_MINIMUM_SURE + 3) and db.get_accepted_days_by_student_number(ogrenci_no)['SUM(kabul_edilen_gun)'] >= STAJ_BITIMI_MINIMUM_SURE:
            data = (1, ogrenci_no,)
            db.update_student_by_student_number(data)
        db.close()
        return redirect('/internships')
    else:
        return render_template("update_interview.html", ogrenci_no=ogrenci_no, baslama_tarihi=baslama_tarihi)


@app.route('/commission', methods=['GET', 'POST'])
def commission():
    db = Database()

    if request.method == 'POST':
        unvan = request.form['unvan']
        isim = request.form['komisyon_isim']
        data = (unvan, isim,)
        db.add_commission(data)

    db.close()
    return redirect("/settings")


############################################################
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
