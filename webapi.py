# -*- coding: utf-8 -*-
from flask import Flask
import decimal
import psycopg2
from datetime import datetime

import time

app = Flask(__name__)


@app.route("/a=<cardid>,b=<bx>,c=<aaa>,d=<rane>")
def Sum(cardid, bx , aaa, rane):

    time.sleep(0.1)

    class MyCardReader(object):

        # RANE = '1'
        RANE = rane
        modoriti = 0
        bx = 0


        def _notice1(self):  # 登録済みカードの1回目のタッチ
            cr.modoriti = 1

        def _notice2(self):  # 登録済みカードの2回目のタッチ
            cr.modoriti = 2

        def _error(self):  # 未登録カードのタッチ
            cr.modoriti = 3

        def card_search(self):

            # ifカードがタッチされたら
            connection = psycopg2.connect(
                host="ec2-52-205-61-60.compute-1.amazonaws.com",
                port="5432",
                dbname="dcg3sava0u5ic6",
                user="tlvwasltznluaj",
                password="828dff754cd6db621b4756042f5c3b47623ca41fcf8cf4e817fa7efffef3a21c"
            )
            cursor = connection.cursor()
            # 作業員管理テーブル「sample_member」の内容を全て取得する
            cursor.execute("SELECT * FROM sample_member;")
            results = cursor.fetchall()  # fetchallで、取得したテーブルの内容を全て変数resultsに代入(resultsはタプル型になる)
            print(results)

            hanbetu = -1
            for a in range(len(results)):  # sample_memberを、一致するカードIDがあるまで参照する

                # (カードIDが一致)and(stateが"0")＝1回目のタッチ
                if ((results[a][0] == cardid) and (results[a][4] == "0")):
                    hanbetu = 0
                    cr._notice1()
                    print('start')
                    now = datetime.now()
                    # date型からstr型に変換。このnowが作業開始時刻
                    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
                    print(now_str)
                    cursor.execute("update sample_member set state='%s', rane='%s' where card_id='%s';" % (
                        now_str, MyCardReader.RANE, cardid))
                    break

                # (カードIDが一致)and(stateが"0"でない)＝2回目のタッチ
                elif ((results[a][0] == cardid) and (results[a][4] != "0") and (results[a][5] == MyCardReader.RANE)):
                    hanbetu = 0
                    if (results[a][1] == "収穫"):  # 収穫の時ケースの数と効率を出すプログラム付き
                        # 開始時刻                                                    stateに開始時刻がある状態で、レーン番号が一致しない場合は他のレーンでの2回目のタッチを忘れている。

                        cr.modoriti = 4

                        break
                    else:
                        # 開始時刻                                                    stateに開始時刻がある状態で、レーン番号が一致しない場合は他のレーンでの2回目のタッチを忘れている。
                        cr._notice2()
                        print('finish')
                        start = results[a][4]
                        finish = datetime.now()
                        # strptimeでstartの型をstrに変換
                        WORK_TIMEx = abs(
                            finish - datetime.strptime(start, '%Y-%m-%d %H:%M:%S'))
                        WORK_TIMEs = WORK_TIMEx.total_seconds()  # 作業時間(秒)
                        decimal.getcontext().prec = 2  # 有効桁設定
                        MIN = decimal.Decimal(WORK_TIMEx.total_seconds())
                        M60 = decimal.Decimal(60)
                        WORK_TIMEm = MIN / M60  # ◆作業時間(分)
                        member = results[a][2]  # ◆作業者(名字)
                        work = results[a][1]  # ◆作業内容

                        tabname = 'b_%s_%s' % (finish.year, finish.month)
                        d_ymd = '%s年%s月%s日' % (
                            finish.year, finish.month, finish.day)  # ◆
                        dd = '%s' % (finish.day)  # ◆
                        dt = '%s時%s分%s秒' % (
                            finish.hour, finish.minute, finish.second)  # ◆
                        cursor.execute("INSERT INTO %s(card_id,member,work_time,work,rane,d_ymd,dt,dd)\
                        VALUES('%s','%s','%s','%s','%s','%s','%s','%s');" % (
                        tabname, cardid, member, WORK_TIMEm, work, MyCardReader.RANE, d_ymd, dt, dd))

                        cursor.execute("update sample_member set state='0', rane='0' where card_id='%s';" % (
                            cardid))  # 開始時刻と作業中レーンを0にリセット
                        break

                elif ((results[a][0] == cardid) and (results[a][4] != "0") and (results[a][5] != MyCardReader.RANE)):
                    # stateに開始時刻がある状態で、レーン番号が一致しない場合は他のレーンでの2回目のタッチを忘れている。
                    hanbetu = 0
                    print("%sレーンでカードをタッチしてください！" % (results[a][5]))
                    break
            if hanbetu == -1:
                cr._error()
                print('登録されていないカードです')


            connection.commit()
            cursor.close()  # cursorを閉じる
            connection.close()  # connectionを閉じる

        def card_4(self):

            # ifカードがタッチされたら
            connection = psycopg2.connect(
                host="ec2-52-205-61-60.compute-1.amazonaws.com",
                port="5432",
                dbname="dcg3sava0u5ic6",
                user="tlvwasltznluaj",
                password="828dff754cd6db621b4756042f5c3b47623ca41fcf8cf4e817fa7efffef3a21c"
            )
            cursor = connection.cursor()
            # 作業員管理テーブル「sample_member」の内容を全て取得する
            cursor.execute("SELECT * FROM sample_member;")
            results = cursor.fetchall()  # fetchallで、取得したテーブルの内容を全て変数resultsに代入(resultsはタプル型になる)
            print(results)

            # id_ = -1
            # for a in range(len(results)):
            #     if ((results[a][0] == cardid) and (results[a][4] != "0") and (results[a][5] == MyCardReader.RANE)):
            #         if (results[a][1] == "収穫"):
            #             id_ = a
            #
            # if id_ != -1:
            #     a = id_
            #     print('finish2')
            #     start = results[a][4]
            #     finish = datetime.now()
            #     # strptimeでstartの型をstrに変換
            #     WORK_TIMEx = abs(
            #         finish - datetime.strptime(start, '%Y-%m-%d %H:%M:%S'))
            #     WORK_TIMEs = WORK_TIMEx.total_seconds()  # 作業時間(秒)
            #     decimal.getcontext().prec = 2  # 有効桁設定
            #     MIN = decimal.Decimal(WORK_TIMEx.total_seconds())
            #     M60 = decimal.Decimal(60)
            #     WORK_TIMEm = MIN / M60  # ◆作業時間(分)
            #     WORK_TIMEm = float(WORK_TIMEm)
            #
            #     # lcd_string("Enter a number.>", LCD_LINE_1)
            #     # cr.key_lcd()
            #
            #     WORK_TIME = float(WORK_TIMEm)
            #     self.bx = float(self.bx)
            #     print(self.bx)
            #     print(WORK_TIME)
            #     eff = self.bx / WORK_TIME  # 効率の計算式
            #     eff = (eff / 0.04) * 100
            #     eff = "{:.1F}".format(eff)
            #
            #     WORK_TIMEm = round(WORK_TIMEm)
            #     WORK_TIME = str(WORK_TIMEm)
            #     eff = str(eff)  # 効率
            #     bx = self.bx
            #     bx = str(bx)  # 個数
            #     member = results[a][2]  # ◆作業者(名字)
            #     work = results[a][1]  # ◆作業内容
            #
            #     tabname = 'b_%s_%s' % (finish.year, finish.month)
            #     d_ymd = '%s年%s月%s日' % (
            #         finish.year, finish.month, finish.day)  # ◆
            #     dd = '%s' % (finish.day)  # ◆
            #     dt = '%s時%s分%s秒' % (
            #         finish.hour, finish.minute, finish.second)  # ◆
            #     cursor.execute("INSERT INTO %s(card_id,member,work_time,work,rane,d_ymd,dt,dd,bx,eff)\
            #                             VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
            #         tabname, cardid, member, WORK_TIMEm, work, MyCardReader.RANE, d_ymd, dt, dd, bx, eff))
            #     # print("update")
            #     cursor.execute("update sample_member set state='0', rane='0' where card_id='%s';" % (
            #         cardid))
            #     # cursor.execute("update sample_member set state='%s', rane='%s' where card_id='%s';" % (
            #     #     str(0), str(0), cardid))
            #     # cursor.execute("update sample_member set state='0', rane='0' where card_id='012e4cd4865951ba';")
            #
            # else:
            #     cr._error()
            #     print('登録されていないカードです')
            #
            # connection.commit()
            # cursor.close()  # cursorを閉じる
            # connection.close()  # connectionを閉じる

            hanbetu = -1
            for a in range(len(results)):  # sample_memberを、一致するカードIDがあるまで参照する

                if ((results[a][0] == cardid) and (results[a][4] != "0") and (results[a][5] == MyCardReader.RANE)):

                    hanbetu = 0

                    if (results[a][1] == "収穫"):  # 収穫の時ケースの数と効率を出すプログラム付き
                        # 開始時刻                                                    stateに開始時刻がある状態で、レーン番号が一致しない場合は他のレーンでの2回目のタッチを忘れている。

                        cr.modoriti = 5

                        print('finish2')
                        start = results[a][4]
                        finish = datetime.now()
                        # strptimeでstartの型をstrに変換
                        WORK_TIMEx = abs(
                            finish - datetime.strptime(start, '%Y-%m-%d %H:%M:%S'))
                        WORK_TIMEs = WORK_TIMEx.total_seconds()  # 作業時間(秒)
                        decimal.getcontext().prec = 2  # 有効桁設定
                        MIN = decimal.Decimal(WORK_TIMEx.total_seconds())
                        M60 = decimal.Decimal(60)
                        WORK_TIMEm = MIN / M60  # ◆作業時間(分)
                        WORK_TIMEm = float(WORK_TIMEm)

                        # lcd_string("Enter a number.>", LCD_LINE_1)
                        # cr.key_lcd()

                        WORK_TIME = float(WORK_TIMEm)
                        self.bx = float(self.bx)
                        print(self.bx)
                        print(WORK_TIME)
                        eff = self.bx / WORK_TIME  # 効率の計算式
                        eff = (eff / 0.04) * 100
                        eff = "{:.1F}".format(eff)

                        WORK_TIMEm = round(WORK_TIMEm)
                        WORK_TIME = str(WORK_TIMEm)
                        eff = str(eff)  # 効率
                        bx = self.bx
                        bx = str(bx)  # 個数
                        member = results[a][2]  # ◆作業者(名字)
                        work = results[a][1]  # ◆作業内容

                        tabname = 'b_%s_%s' % (finish.year, finish.month)
                        d_ymd = '%s年%s月%s日' % (
                            finish.year, finish.month, finish.day)  # ◆
                        dd = '%s' % (finish.day)  # ◆
                        dt = '%s時%s分%s秒' % (
                            finish.hour, finish.minute, finish.second)  # ◆
                        cursor.execute("INSERT INTO %s(card_id,member,work_time,work,rane,d_ymd,dt,dd,bx,eff)\
                        VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
                        tabname, cardid, member, WORK_TIMEm, work, MyCardReader.RANE, d_ymd, dt, dd, bx, eff))

                        cursor.execute("update sample_member set state='0', rane='0' where card_id='%s'" % (
                            cardid))  # 開始時刻と作業中レーンを0にリセット
                        break
                    elif ((results[a][0] == cardid) and (results[a][4] != "0") and (results[a][5] != MyCardReader.RANE)):
                        # stateに開始時刻がある状態で、レーン番号が一致しない場合は他のレーンでの2回目のタッチを忘れている。
                        print("%sレーンでカードをタッチしてください！" % (results[a][5]))
                        break



            if hanbetu == -1:
                cr._error()
                print('登録されていないカードです')

            connection.commit()
            cursor.close()  # cursorを閉じる
            connection.close()  # connectionを閉じる


    # if __name__ == '__main__':
    #     cr = MyCardReader()
    #     while True:
    #         print(cardid)
    #         cr.bx = bx
    #         if (aaa == "1"):
    #             cr.card_search()
    #         else:
    #             cr.card_4()
    #
    #         return str(cr.modoriti)
    #return str(int(x) + int(y))

    cr = MyCardReader()
    print(cardid)
    cr.bx = bx
    if (aaa == "1"):
        cr.card_search()
    else:
        cr.card_4()

    return str(cr.modoriti)



# if __name__ == "__main__":
#     app.run(debug=True, port=80)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
