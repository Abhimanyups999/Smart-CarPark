from flask import Flask,render_template,request,redirect,session,jsonify
from DBConnection import Db

app = Flask(__name__)
app.secret_key="abc"


@app.route('/login',methods=['get','post'])
def login():
    if request.method=="POST":
        name=request.form['textfield']
        paswd=request.form['textfield2']
        db=Db()
        res= db.selectOne("select * from login where user_name='"+name+"'and password='"+paswd+"' ")
        if res is not None:
            session['lid'] = res['login_id']
            if res['user_type']=='admin':
                session['log'] = "lo"
                return redirect('/adminhome')
            elif res['user_type']=='building':
                session['lid']=res['login_id']
                session['log'] = "lo"
                return redirect('/buildinghome')
            else:
                return '''<script>alert("INVALID USER");window.location="/"</script>'''
        else:
            return '''<script>alert("INVALID USER");window.location="/"</script>'''
    else:

        return render_template("login_index.html")


@app.route('/logout')
def logout():
    session.clear()
    session['log']=""
    return redirect('/')




@app.route('/adminhome')
def adminhome():
    if session['log']=="lo":
        return render_template("admin/admin_index.html")
    else:
        return redirect('/')

@app.route('/')
def HOME():
    return render_template("index.html")

@app.route('/about')
def ABOUT():
    return render_template("about.html")



@app.route('/CHANGEPASSWD',methods=['get','post'])
def CHANGEPASSWD():
    if session['log'] == "lo":
        if request.method=="POST":
            current=request.form['textfield']
            new=request.form['textfield2']
            confirm=request.form['textfield3']
            db=Db()
            qry=db.selectOne("select * from login where user_type='admin'")
            if qry['password']==current:
                if new==confirm:
                    db.update("update login set password='"+confirm+"' where user_type='admin'")
                    return '''<script>alert("success");window.location="/"</script>'''
                else:
                    return '''<script>alert("password mismatch!!");window.location="/CHANGEPASSWD"</script>'''
            else:
                return '''<script>alert("password incorrect!!");window.location="/CHANGEPASSWD"</script>'''
        else:
            return render_template("admin/CHANGE_PASSWORD.html")
    else:
        return redirect('/')

@app.route('/verifybuilding')
def verifybuilding():
    if session['log'] == "lo":
        db = Db()
        ss = db.selectOne("select * from building,login where building.building_id=login.login_id ")
        if ss is None:
            return '''<script>alert("NOT AVAILABLE NOW!!");window.location="/adminhome"</script>'''
        else:
            qry = db.select("select * from building,login where building.building_id=login.login_id ")
            return render_template('admin/VERIFY_BUILDING.html',data=qry)
    else:
        return redirect('/')




@app.route('/APPROVE/<AID>')
def APPROVE(AID):
    if session['log'] == "lo":
        db = Db()
        db.update("update login set user_type='building' where login_id='"+AID+"'")
        return redirect('/verifybuilding')
    else:
        return redirect('/')

@app.route('/REJECT/<AID>')
def REJECT(AID):
    if session['log'] == "lo":
        db = Db()
        db.update("update login set user_type='reject' where login_id='"+AID+"'")
        db.delete("delete from login where login_id='"+AID+"'")
        db.delete("delete from building where building_id='" + AID + "'")
        return redirect('/verifybuilding')
    else:
        return redirect('/')


@app.route('/VIEWBOOKING')
def VIEWBOOKING():
    if session['log'] == "lo":
        db = Db()
        ss = db.selectOne("select * from booking,user where booking.user_id=user.user_id and booking.status='completed'")
        if ss is None:
            return '''<script>alert("NOT AVAILABLE NOW!!");window.location="/adminhome"</script>'''
        else:
            qry=db.select("select * from booking,user where booking.user_id=user.user_id and booking.status='completed'")
            return render_template("admin/VIEW_BOOKING_HISTORY.html",data=qry)
    else:
        return redirect('/')



@app.route('/view_complaint')
def view_complaint():
    if session['log'] == "lo":
        db = Db()
        ss = db.selectOne("select * from complaint,user where complaint.user_id=user.user_id")
        if ss is None:
            return '''<script>alert("NOT AVAILABLE NOW!!");window.location="/adminhome"</script>'''
        else:
            qry = db.select("select * from complaint,user where complaint.user_id=user.user_id")
            return render_template("admin/VIEW_COMPLAINT.html", data=qry)
    else:
        return redirect('/')


@app.route('/SENDREPLY/<cid>', methods=['get', 'post'])
def SENDREPLY(cid):
    if session['log'] == "lo":
        if request.method == "POST":
            reply = request.form['textarea']

            db = Db()
            db.update("update complaint set reply='" + reply + "',reply_date=curdate() where complaint_id='" + str(cid) + "'")
            return '''<script>alert("reply send");window.location="/view_complaint"</script>'''

        else:
            return render_template("admin/SEND_REPLY.html")
    else:
        return redirect('/')


@app.route('/VIEWRATING')
def VIEWRATING():
    if session['log'] == "lo":
        db = Db()
        ss = db.selectOne("select * from rating,user where rating.user_id=user.user_id")
        if ss is None:
            return '''<script>alert("NOT AVAILABLE NOW!!");window.location="/adminhome"</script>'''
        else:
            qry = db.select("select * from rating,user where rating.user_id=user.user_id")
            return render_template("admin/VIEW_RATING.html",data=qry)
    else:
        return redirect('/')

@app.route('/VIEWUSER')
def VIEWUSER():
    if session['log'] == "lo":
        db = Db()
        ss = db.selectOne("select * from user")
        if ss is None:
            return '''<script>alert("NOT AVAILABLE NOW!!");window.location="/adminhome"</script>'''
        else:
            qry = db.select("select * from user")
            return render_template("admin/VIEW_USER.html", data=qry)
    else:
        return redirect('/')

@app.route('/VIEWVERIFIEDBUILDING')
def VIEWVERIFIEDBUILDING():
    if session['log'] == "lo":
        db = Db()
        ss = db.selectOne("select * from building,login where building.building_id=login.login_id and login.user_type='building'")
        if ss is None:
            return '''<script>alert("NOT AVAILABLE NOW!!");window.location="/adminhome"</script>'''
        else:
            qry = db.select("select * from building,login where building.building_id=login.login_id and login.user_type='building'")
            return render_template("admin/VIEW_VERIFIED_BUILDING.html", data=qry)
    else:
        return redirect('/')

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/buildinghome')
def buildinghome():
    if session['log'] == "lo":
        return render_template("building/building_index.html")
    else:
        return redirect('/')



@app.route('/CHANGEPASSWORD',methods=['get','post'])
def CHANGEPASSWORD():
    if session['log'] == "lo":
        if request.method == "POST":
            current = request.form['textfield']
            new = request.form['textfield2']
            confirm = request.form['textfield3']
            db = Db()
            res = db.selectOne("select * from login where login_id='"+str(session['lid'])+"'")
            if res['password'] == current:
                if new == confirm:
                    db.update("update login set password='" + confirm + "' where login_id='"+str(session['lid'])+"'")
                    return '''<script>alert("success");window.location="/"</script>'''
                else:
                    return '''<script>alert("password mismatch!!");window.location="/CHANGEPASSWORD"</script>'''
            else:
                return '''<script>alert("password incorrect!!");window.location="/CHANGEPASSWORD"</script>'''
        else:
             return render_template("building/CHANGE_PASSWORD.html")
    else:
        return redirect('/')
@app.route('/REG',methods=['get','post'])
def REG():
    if request.method=='POST':
        name=request.form['textfield']
        floor=request.form['textfield2']
        place=request.form['textfield3']
        post=request.form['textfield4']
        pin=request.form['textfield5']
        email=request.form['textfield6']
        password=request.form['textfield7']
        db=Db()
        q=db.selectOne("select * from login where user_name='"+email+"'")
        if q is None:
            res=db.insert("insert into login VALUES ('','"+email+"','"+password+"','pending')")
            db.insert("insert into building VALUES ('"+str(res)+"','"+name+"','"+floor+"','"+place+"','"+post+"','"+pin+"','"+email+"')")
            return '''<script>alert("REGISTER SUCCESSFULLY");window.location="/REG"</script>'''
        else:
            return '''<script>alert("email already exist");window.location="/"</script>'''

    else:
        return render_template("register_index.html")

@app.route('/SECURITYADD',methods=['get','post'])
def SECURITYADD():
    if session['log'] == "lo":
        if request.method=='POST':
            name = request.form['textfield']
            email = request.form['textfield2']
            phno = request.form['textfield3']
            db=Db()
            res = db.insert("insert into login VALUES ('','"+email+"','"+phno+"','security')")
            db.insert("insert into security VALUES ('"+str(res)+"','"+name+"','"+str(session['lid'])+"','"+email+"','"+phno+"')")
            return '''<script>alert("SECURITY ADDED SUCCESSFULLY");window.location="/SECURITYVIEW"</script>'''

        qry = "select * from security WHERE building_id='"+str(session['lid'])+"'"
        return render_template("building/SECURITY_ADD.html",data=qry)
    else:
        return redirect('/')

@app.route('/SECURITYEDIT/<up>',methods=['get','post'])
def SECURITYEDIT(up):
    if session['log'] == "lo":
        if request.method == 'POST':
            name = request.form['textfield']
            email = request.form['textfield3']
            phno = request.form['textfield2']
            db = Db()
            db.update("update security set security_name='"+name+"',email='"+email+"',phone_no='"+phno+"' where security_id = '"+up+"'")
            return '''<script>alert("SECURITY UPDATED SUCCESSFULLY");window.location="/SECURITYVIEW"</script>'''
        else:
            db=Db()
            a=db.selectOne("select * from security where security_id = '"+up+"'")

            return render_template("building/SECURITY_EDIT.html",data=a)
    else:
        return redirect('/')
@app.route('/SECURITYDEL/<de>')
def SECURITYDEL(de):
    if session['log'] == "lo":
        db=Db()
        db.delete("delete from security where security_id = '"+de+"'")
        return '''<script>alert("SECURITY DELETED SUCCESSFULLY");window.location="/SECURITYVIEW"</script>'''
    else:
        return redirect('/')

@app.route('/SECURITYVIEW')
def SECURITYVIEW():
    if session['log'] == "lo":
        db = Db()
        qry = db.select("select * from security WHERE building_id='"+str(session['lid'])+"'")
        print(qry)
        return render_template("building/SECURITY_VIEW.html",data=qry)
    else:
        return redirect('/')

@app.route('/SERVICEADD',methods=['get','post'])
def SERVICEADD():
    if session['log'] == "lo":
        if request.method == 'POST':
            s=request.form['textarea']
            db=Db()

            db.insert("insert into services VALUES ('','" + str(session['lid']) + "','" +s+ "')")
            return '''<script>alert("REGISTER SUCCESSFULLY");window.location="/B_VIEWSERVICE"</script>'''

        return render_template("building/SERVICE_ADD.html")
    else:
        return redirect('/')

@app.route('/SERVICEDEL/<dd>')
def SERVICEDEL(dd):
    if session['log'] == "lo":
        db = Db()
        db.delete("delete from services where service_id = '" + dd + "'")
        return '''<script>alert("SERVICE DELETED SUCCESSFULLY");window.location="/B_VIEWSERVICE"</script>'''
    else:
        return redirect('/')

@app.route('/SLOTADD',methods=['get','post'])
def SLOTADD():
    if session['log'] == "lo":
        if request.method == 'POST':
            num=request.form['textfield']
            db=Db()
            db.insert("insert into slot VALUES ('','"+str(session['lid'])+"','"+num+"','pending')")
            return '''<script>alert("SLOT ADDED SUCCESSFULLY");window.location="/SLOTVIEW"</script>'''
        qry = "select * from building,slot WHERE building.building_id=slot.building_id"
        return render_template("building/SLOT_ADD.html" ,data=qry)
    else:
        return redirect('/')
@app.route('/SLOTEDIT/<i>/<j>',methods=['get','post'])
def SLOTEDIT(i,j):
    if session['log'] == "lo":
        if request.method == 'POST':
            num = request.form['textfield2']
            db = Db()
            db.update("update slot set num_of_slot ='"+num+"' where slot_id ='"+j+"'")
            return '''<script>alert("SLOT EDITED SUCCESSFULLY");window.location="/SLOTVIEW"</script>'''

        return render_template("building/SLOT_EDIT.html",data=i)
    else:
        return redirect('/')
@app.route('/SLOTDEL/<ee>')
def SLOTDEL(ee):
    if session['log'] == "lo":
        db = Db()
        db.delete("delete from slot where slot_id = '" + ee + "'")
        return '''<script>alert("SLOT DELETED SUCCESSFULLY");window.location="/SLOTVIEW"</script>'''
    else:
        return redirect('/')

@app.route('/SLOTVIEW')
def SLOTVIEW():
    if session['log'] == "lo":
        db=Db()
        qry = db.select("select * from slot WHERE building_id='"+str(session['lid'])+"'")
        return render_template("building/SLOT_VIEW.html",data=qry)
    else:
        return redirect('/')
@app.route('/B_VIEWBOOKING')
def B_VIEWBOOKING():
    if session['log'] == "lo":
        db=Db()
        qry=db.select("SELECT * FROM slot,booking,user where slot.slot_id = booking.slot_selection and booking.user_id = user.user_id")
        return render_template("building/VIEW_BOOKING.html",data=qry)
    else:
        return redirect('/')
# @app.route('/B_VIEWRATING')
# def B_VIEWRATING():
#     if session['log'] == "lo":
#         db=Db()
#         qry=db.select("select * from rating,user where rating.user_id = user.user_id")
#         return render_template("building/VIEW_RATING.html",data=qry)
#     else:
#         return redirect('/')


@app.route('/B_VIEWRATING')
def ar():
    # qry="select rating.*,customer.* from rating,customer where customer.lid=rating.user_id"
    db=Db()
    qry="select rating.rating,rating.date_time,`user`.user_name,user.photo,rating.rating_id from `user`,rating where `user`.user_id=rating.user_id"
    res=db.select(qry)
    ar_rt = []

    for im in range(0, len(res)):
        val = str(res[im]['rating'])
        ar_rt.append(val)
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    arr = []

    for rt in ar_rt:
        print(rt)
        a = float(rt)

        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]
            arr.append(ar)

        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]
            arr.append(ar)

        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]
            arr.append(ar)

        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]
            arr.append(ar)

        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]
            arr.append(ar)

        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]
            arr.append(ar)

        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]
            arr.append(ar)

        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]
            arr.append(ar)

        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]
            arr.append(ar)

        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]
            arr.append(ar)

        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]
            arr.append(ar)
        print(arr)
    # return render_template('admin/adm_view_apprating.html',data=re33,r1=ar,ln=len(ar55))
    return render_template("building/VIEW_RATING.html", resu=res, r1=arr, ln=len(arr))

@app.route('/B_VIEWSERVICE')
def B_VIEWSERVICE():
    if session['log'] == "lo":
        db = Db()
        qry = db.select("select * from services WHERE building_id='" + str(session['lid']) + "'")
        print(qry)
        return render_template("building/VIEW_SERVICE.html",data=qry)
    else:
        return redirect('/')



# =======================================================================================================
#                                         USER HOME
# =======================================================================================================

@app.route('/and_login',methods=['post'])
def and_login():
    name = request.form['u']
    paswd = request.form['p']
    db = Db()
    res = db.selectOne("select * from login where user_name='" + name + "' and password='" + paswd + "' ")
    print(res)
    if res is not None:
        return jsonify(status="ok",type=res['user_type'],lid=res['login_id'])
    else:
        print("hhhhhhhhhhhhhhhhhhhhhh")
        return jsonify(status="no")


@app.route('/and_send_complaint',methods=['post'])
def and_send_complaints():
    c=request.form['comp']
    id=request.form['id']
    db = Db()
    db.insert("insert into complaint VALUES ('','"+id+"',curdate(),'"+c+"','pending','pending')")
    return jsonify(status="ok")


@app.route('/and_view_reply',methods=['post'])
def and_view_reply():
    id = request.form['id']
    db = Db()
    qry=db.select("select * from complaint where user_id='"+id+"'")
    if len(qry)>0:
        return jsonify(status="ok",data=qry)
    else:
        return jsonify(status="no")

@app.route('/and_send_rating', methods=['post'])
def and_send_rating():
    id = request.form['id']
    rating = request.form['r']
    db = Db()

    qry = db.insert("insert into rating(user_id,date_time,rating) VALUES('"+id+"',now(),'"+rating+"')")
    if (qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
        return jsonify(status="no")




@app.route('/and_Registration', methods=['post'])
def and_Registration():
        name = request.form['e1']
        place = request.form['e2']
        phone = request.form['e3']
        email = request.form['e4']
        passwd = request.form['e5']
        p=request.files['pic']
        import datetime
        d=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        p.save(r"C:\Users\hp-pc\PycharmProjects\SmartCar\static\pic\\"+d+'.jpg')
        path='/static/pic/'+d+'.jpg'
        db = Db()
        uid = db.insert("insert into login(user_name,password,user_type)values('"+name+"','"+passwd+"','user')")
        db.insert("insert into user(user_id,user_name,email,ph_no,place,photo)values('"+str(uid)+"','"+name+"','"+email+"','"+phone+"','"+place+"','"+path+"')")
        if (uid) > 0:
            return jsonify(status="ok", data=uid)
        else:
            return jsonify(status="no")



@app.route('/and_Change_Password', methods=['post'])
def and_Change_Password():
    currentpaswd = request.form['e1']
    newpaswd = request.form['e2']
    id = request.form['e3']
    db = Db()
    qry = db.update("update login set password='"+newpaswd+"' where login_id='"+id+"' and password='"+currentpaswd+"'")
    if (qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
                return jsonify(status="no")







@app.route('/and_view_building', methods=['post'])
def and_view_building():
    db = Db()
    qry = db.select("select * from building ")

    if len(qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
        return jsonify(status="no")


@app.route('/and_view_booking', methods=['post'])
def and_view_booking():
    db = Db()
    id = request.form['id']
    qry = db.select("select * from booking,building,slot where booking.slot_selection=slot.slot_id and slot.building_id=building.building_id and user_id='"+id+"' and booking.status='pending' and book_date=curdate() ")

    if len(qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
        return jsonify(status="no")

@app.route('/and_history', methods=['post'])
def and_history():
    db = Db()
    id = request.form['id']
    print(id,"eeeeeeeeeeeeeee")
    qry = db.select("select * from booking,building,slot where booking.slot_selection=slot.slot_id and slot.building_id=building.building_id and user_id='"+id+"' and booking.status='completed'")

    if len(qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
        return jsonify(status="no")

@app.route('/and_view_rating', methods=['post'])
def and_view_rating():
    id = request.form['id']
    db = Db()
    qry = db.select("select * from user,rating WHERE user.user_id=rating.user_id")
    if len(qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
        return jsonify(status="no")

@app.route('/and_booking_cancel', methods=['post'])
def and_booking_cancel():
    db = Db()
    id = request.form['s']
    qry = db.delete("delete from booking WHERE booking_id='"+id+"'")

    if (qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
        return jsonify(status="no")


@app.route('/and_view_slot', methods=['post'])
def and_view_slot():
    id=request.form['id']
    db = Db()
    qry = db.select("select * from slot WHERE building_id='"+id+"'")
    if len(qry) > 0:
        return jsonify(status="ok", data=qry)
    else:
        return jsonify(status="no")

@app.route('/and_slot_booking', methods=['post'])
def and_slot_booking():
    id = request.form['id']
    s = request.form['s']
    db = Db()
    qry = db.insert("insert into booking values('','','"+id+"',curdate(),'"+s+"','pending')")
    import qrcode

    # Create qr code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=4,
    )

    # The data that you want to store
    data = str(qry)

    # Add data
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image()

    # Save it somewhere, change the extension as needed:
    # img.save("image.png")
    # img.save("image.bmp")
    # img.save("image.jpeg")
    import datetime
    img.save(r"C:\Users\hp-pc\PycharmProjects\SmartCar\static\qrcode\\"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(qry)+".jpg")
    path="/static/qrcode/"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(qry)+".jpg"
    db.update("update booking set qrcode='"+path+"' where booking_id='"+str(qry)+"'")
    if (qry) > 0:
        return jsonify(status="ok")
    else:
        return jsonify(status="no")

@app.route('/custom_service', methods=['post'])
def custom_service():
    bid=request.form['bid']
    db=Db()
    qry=db.select("select * from services where building_id='"+bid+"'")
    if len(qry) > 0:
        return jsonify(status="ok",data=qry)
    else:
        return jsonify(status="no")















        # =======================================================================================================
                                        # SECURITY MODULE
# =======================================================================================================

@app.route('/and_profile_security',methods=['post'])
def and_profile_security():
    id = request.form['id']
    db = Db()
    qry=db.selectOne("select * from security where security_id='"+id+"'")
    print(qry)
    if qry is not None:
        return jsonify(status="ok",data=qry)
    else:
        return jsonify(status="no")


@app.route('/and_building_security',methods=['post'])
def and_building_security():
    id = request.form['id']
    db = Db()
    qry=db.selectOne("select security.email as em,security.*,building.* from building,security where building.building_id=security.building_id AND security_id='"+id+"'")
    if len(qry)>0:
        return jsonify(status="ok",data=qry)
    else:
        return jsonify(status="no")



@app.route('/and_security_booking',methods=['post'])
def and_security_booking():
    id = request.form['id']
    db = Db()
    qry=db.select("select booking.status as st,booking.*,slot.*,security.*,user.* from booking,slot,security,user where booking.slot_selection=slot.slot_id and slot.building_id=security.building_id and booking.user_id=user.user_id and security.security_id='"+id+"' and booking.status!='complete' and book_date=curdate()")
    print("select * from booking,slot,security,user where booking.slot_selection=slot.slot_id and slot.building_id=security.building_id and booking.user_id=user.user_id and security.security_id='"+id+"' and booking.status!='complete' and book_date=curdate()")
    if len(qry)>0:
        return jsonify(status="ok",data=qry)
    else:
        return jsonify(status="no")

@app.route('/update_application', methods=['post'])
def update_application():
    booking_id = request.form['booking_id']
    db = Db()
    qry=db.update("update booking set status='check in' WHERE booking_id='"+booking_id+"'")
    return jsonify(status="ok")


@app.route('/update_application2', methods=['post'])
def update_application2():
    booking_id = request.form['booking_id']
    db = Db()
    qry = db.update("update booking set status='complete' WHERE booking_id='" + booking_id + "'")
    return jsonify(status="ok")


if __name__ == '__main__':
    app.run(debug=True,port=3000,host="0.0.0.0")
