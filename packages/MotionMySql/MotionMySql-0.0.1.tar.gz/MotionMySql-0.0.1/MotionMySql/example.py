
join = module.join()
GetColumn = module.GetColumn()  # ��
delt = module.delt()  # ɾ
Renewal = module.Renewal()  # ��
Inquire = module.Inquire()  # ��
host = input("���������ݿ��ַ")
user = input("�������û���")
password = input("����������")
while True:
    try:
        print("1����\n2��ɾ\n3����\n4����")
        i = int(input("ѡ����"))
        if 1 <= i <= 4:
            library_name = input("���������ݿ���")
            table_name = input("���������")
            join.join(host,user,password,library_name)
            if i == 1:
                GetColumn.GetColumn(join.cursor, join.conn, table_name)
                module.close(join.cursor, join.conn)
            elif i == 2:
                delt.deltf(join.cursor, join.conn, table_name)
                module.close(join.cursor, join.conn)
            elif i == 3:
                Renewal.Renewalf(join.cursor, join.conn, table_name)
                module.close(join.cursor, join.conn)
            elif i == 4:
                Inquire.run(join.cursor, join.conn, table_name)
                module.close(join.cursor, join.conn)
        else:
            print("��������ֲ���1��4֮��")
    except ValueError:
        print("������Ĳ������֣����ٴγ������룡��")