import pymysql

class Database:
    def __init__(self):
        host = #Host
        user = #Database User
        password = #Database Password
        db = #Database Name

        self.con = pymysql.connect(
            host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    ############################ STUDENTS #########################
    def list_students(self):
        self.cur.execute("SELECT * FROM ogrenci")
        result = self.cur.fetchall()
        return result

    def get_students_number(self):
        self.cur.execute(
            "SELECT COUNT(*) FROM ogrenci")
        result = self.cur.fetchone()
        return result

    def get_students_by_completing_internship(self, is_completed_internship):
        self.cur.execute(
            "SELECT * FROM ogrenci WHERE staj_bitti=%s", is_completed_internship)
        result = self.cur.fetchall()
        return result

    def get_student_by_student_number(self, student_number):
        self.cur.execute(
            "SELECT * FROM ogrenci WHERE ogrenci_no=%s", student_number)
        result = self.cur.fetchone()
        return result

    def add_student(self, data):
        self.cur.execute(
            "INSERT INTO ogrenci(ogrenci_no, isim, soyisim, ogretim) VALUES(%s, %s, %s, %s)", data)
        self.con.commit()

    def delete_student_by_student_number(self, student_number):
        self.cur.execute(
            "DELETE FROM ogrenci WHERE ogrenci_no=%s", student_number)
        self.con.commit()

    def update_student_by_student_number(self, data):
        self.cur.execute(
            "UPDATE ogrenci set staj_bitti=%s WHERE ogrenci_no=%s", data)
        self.con.commit()
    ###############################################################

    ############################ TOPIC ############################
    def list_topics(self):
        self.cur.execute("SELECT * FROM konu")
        result = self.cur.fetchall()
        return result

    def get_topics_number(self):
        self.cur.execute("SELECT COUNT(*) FROM konu")
        result = self.cur.fetchone()
        return result

    def add_topic(self, data):
        self.cur.execute("INSERT INTO konu VALUES(%s)", data)
        self.con.commit()

    def update_topic(self, data):
        self.cur.execute("UPDATE konu SET isim=%s WHERE isim=%s", data)
        self.con.commit()

    def delete_topic(self, data):
        self.cur.execute("DELETE FROM konu WHERE isim=%s", data)
        self.con.commit()
    ###############################################################

    ######################### INTERNSHIPS #########################
    def list_internships(self):
        self.cur.execute("SELECT * FROM staj")
        result = self.cur.fetchall()
        return result

    def get_total_days_by_city(self, sehir):
        self.cur.execute("SELECT SUM(toplam_gun) FROM staj WHERE sehir=%s", sehir)
        result = self.cur.fetchone()
        return result

    def get_accepted_days_by_city(self, sehir):
        self.cur.execute("SELECT SUM(kabul_edilen_gun) FROM staj WHERE sehir=%s", sehir)
        result = self.cur.fetchone()
        return result

    def get_topic_number(self, data):
        self.cur.execute("SELECT COUNT(*) FROM staj WHERE staj_konusu=%s", data)
        result = self.cur.fetchone()
        return result

    def get_topic_number_by_internship(self, data):
        self.cur.execute("SELECT COUNT(*) FROM staj WHERE staj_konusu=%s and SUBSTR(baslama_tarihi,1,4)=%s", data)
        result = self.cur.fetchone()
        return result
    
    def get_sum_of_total_days(self, data):
        self.cur.execute("SELECT SUM(toplam_gun) FROM staj WHERE staj_konusu=%s and SUBSTR(baslama_tarihi,1,4)=%s", data)
        result = self.cur.fetchone()
        return result
    
    def get_sum_of_total_days_general(self, data):
        self.cur.execute("SELECT SUM(toplam_gun) FROM staj WHERE staj_konusu=%s", data)
        result = self.cur.fetchone()
        return result

    def get_sum_of_accepted_days(self, data):
        self.cur.execute("SELECT SUM(kabul_edilen_gun) FROM staj WHERE staj_konusu=%s and SUBSTR(baslama_tarihi,1,4)=%s", data)
        result = self.cur.fetchone()
        return result

    def get_sum_of_accepted_days_general(self, data):
        self.cur.execute("SELECT SUM(kabul_edilen_gun) FROM staj WHERE staj_konusu=%s", data)
        result = self.cur.fetchone()
        return result

    def get_internships_number(self):
        self.cur.execute("SELECT COUNT(*) FROM staj")
        result = self.cur.fetchone()
        return result

    def add_internship(self, data):
        self.cur.execute(
            "INSERT INTO staj VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
        self.con.commit()

    def delete_internship(self, data):
        self.cur.execute(
            "DELETE FROM staj WHERE ogrenci_no=%s and baslama_tarihi=%s", data)
        self.con.commit()

    def get_internship(self, data):
        self.cur.execute(
            "SELECT * FROM staj WHERE ogrenci_no=%s and baslama_tarihi=%s", data)
        result = self.cur.fetchone()
        return result

    def get_internships_by_is_interviewed(self, is_interviewed):
        self.cur.execute(
            "SELECT * FROM staj WHERE staj_degerlendirildi=%s", is_interviewed)
        result = self.cur.fetchall()
        return result

    def get_internship(self, data):
        self.cur.execute(
            "SELECT * FROM staj WHERE ogrenci_no=%s and baslama_tarihi=%s", data)
        result = self.cur.fetchone()
        return result

    def get_internships_by_student_number(self, student_number):
        self.cur.execute(
            "SELECT * FROM staj WHERE ogrenci_no=%s", student_number)
        result = self.cur.fetchall()
        return result

    def get_total_days_by_student_number(self, student_number):
        self.cur.execute(
            "SELECT SUM(toplam_gun) FROM staj WHERE ogrenci_no=%s", student_number)
        result = self.cur.fetchone()
        return result

    def get_accepted_days_by_student_number(self, student_number):
        self.cur.execute(
            "SELECT SUM(kabul_edilen_gun) FROM staj WHERE ogrenci_no=%s", student_number)
        result = self.cur.fetchone()
        return result

    def update_internship(self, data):
        self.cur.execute(
            "UPDATE Staj SET staj_degerlendirildi=%s, kabul_edilen_gun=%s WHERE ogrenci_no=%s and baslama_tarihi=%s", data)
        self.con.commit()
    ###############################################################

    ########################### TEACHERS ##########################
    def get_teachers(self):
        self.cur.execute(
            "SELECT * FROM komisyon")
        result = self.cur.fetchall()
        return result

    def get_teachers_by_id(self, id):
        self.cur.execute(
            "SELECT * FROM komisyon where id=%s", id)
        result = self.cur.fetchone()
        return result

    ######################### INTERVIEWS ##########################
    def add_interview(self, data):
        self.cur.execute(
            "INSERT INTO Mulakat(ogrenci_no, baslama_tarihi, tarih, saat, komisyon_uye1, komisyon_uye2) VALUES(%s, %s, %s, %s, %s, %s)", data)
        result = self.con.commit()

    def get_interviews_number(self):
        self.cur.execute(
            "SELECT COUNT(*) FROM Mulakat")
        result = self.cur.fetchone()
        return result

    def get_interviews(self):
        self.cur.execute(
            "SELECT * FROM Mulakat")
        result = self.cur.fetchall()
        return result

    def delete_interview(self, data):
        self.cur.execute(
            "DELETE FROM Mulakat WHERE ogrenci_no=%s and baslama_tarihi=%s", data)
        self.con.commit()

    def update_interview(self, data):
        self.cur.execute(
            "UPDATE Mulakat SET devam=%s, calisma=%s, isi_vaktinde_yapma=%s, amire_davranis=%s, is_arkadaslarina_davranis=%s, prove=%s, duzen=%s, sunum=%s, icerik=%s, mulakat=%s WHERE ogrenci_no=%s and baslama_tarihi=%s", data)
        self.con.commit()

    def add_commission(self, data):
        self.cur.execute(
            "INSERT INTO komisyon(unvan, isim_soyisim) VALUES(%s, %s)", data)
        self.con.commit()

    def close(self):
        self.cur.close()
        self.con.close()
