import pyodbc
from mainAppFolder import app
from mainAppFolder.crmapi.functions import handle_datetimeoffset

server = '11.11.11.16,9433'
database = 'CRM'
username = 'rk7'
password = 'rk7'


def get_cardcode_password(CardCode):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
        ';DATABASE=' + database +
        ';UID=' + username +
        ';PWD=' + password +
        ';MARS_Connection=Yes'
    )
    myfile = cnxn.cursor()
    myfile.execute("""select 
                                CARD_CARDS.CARD_CODE,
                                CARD_CARDS.TEXT_PASSWORD,
                                CARD_CARDS.PEOPLE_ID
                                from CARD_CARDS 
                                WHERE LEN(CARD_CODE) = 6 AND CARD_CODE = '{}'
                          """.format(CardCode))
    records = myfile.fetchall()
    myfile.close()
    del myfile
    cnxn.close()
    return records


def change_password(CardCode, CardCode_password):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
        ';DATABASE=' + database +
        ';UID=' + username +
        ';PWD=' + password +
        ';MARS_Connection=Yes'
    )
    myfile = cnxn.cursor()
    myfile.execute("""UPDATE
                                CARD_CARDS
                                SET
                                TEXT_PASSWORD = '{1}'
                                WHERE
                                CARD_CODE = '{0}'
                                '*Rb180219'
                          """.format(CardCode, CardCode_password))
    #    print('GoGo')
    cnxn.commit()
    myfile.close()
    del myfile
    cnxn.close()


def get_transactions(CardCode, date_from, date_to):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
        ';DATABASE=' + database +
        ';UID=' + username +
        ';PWD=' + password +
        ';MARS_Connection=Yes'
    )
    myfile = cnxn.cursor()
    cnxn.add_output_converter(-155, handle_datetimeoffset)
    myfile.execute("""SELECT CARD_TRANSACTIONS.TRANSACTION_ID, CARD_TRANSACTIONS.SUMM,CARD_TRANSACTIONS.TRANSACTION_TIME,CARD_CLIENTS.NAME,CARD_TRANSACTION_NOTES.XML_CHECK
                                FROM CARD_CARDS
                                LEFT JOIN CARD_PEOPLE_ACCOUNTS ON CARD_CARDS.PEOPLE_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ID
                                JOIN CARD_TRANSACTIONS ON CARD_TRANSACTIONS.ACCOUNT_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ACCOUNT_ID
                                LEFT JOIN CARD_CLIENTS ON CARD_TRANSACTIONS.CLIENT_ID = CARD_CLIENTS.CLIENT_ID
                                LEFT JOIN CARD_TRANSACTION_NOTES ON CARD_TRANSACTIONS.TRANSACTION_ID = CARD_TRANSACTION_NOTES.TRANSACTION_ID
                                WHERE CARD_TRANSACTIONS.TRANSACTION_TYPE = 42 AND CARD_CARDS.CARD_CODE = '{}' AND CARD_TRANSACTIONS.TRANSACTION_TIME >= '{}' AND CARD_TRANSACTIONS.TRANSACTION_TIME < '{}' 
                              """.format(CardCode, date_from, date_to))
    records = myfile.fetchall()
    myfile.close()
    del myfile
    cnxn.close()
    return records


def get_card_info(CardCode, card_code_type):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
        ';DATABASE=' + database +
        ';UID=' + username +
        ';PWD=' + password +
        ';MARS_Connection=Yes'
    )
    myfile = cnxn.cursor()
    myfile.execute("""SELECT
                                CARD_CARDS.CARD_CODE,
                                CARD_CARDS.PEOPLE_ID,
                                CARD_PEOPLES.F_NAME,
                                CARD_PEOPLES.L_NAME,
                                CARD_PEOPLES.FULL_NAME,
                                CARD_CARDS.TEXT_PASSWORD,
                                CARD_PEOPLES.BIRTHDAY,
                                CARD_PEOPLES.SOURCE,
                                CARD_PEOPLE_ACCOUNTS.BALANCE,
                                CARD_GROUPS.NAME as 'Hang The'
                                FROM
                                CARD_CARDS
                                LEFT JOIN
                                CARD_PEOPLES
                                ON
                                CARD_CARDS.PEOPLE_ID = CARD_PEOPLES.PEOPLE_ID
                                LEFT JOIN
                                CARD_PEOPLE_ACCOUNTS
                                ON
                                CARD_PEOPLES.PEOPLE_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ID
                                LEFT JOIN
                                CARD_ACCOUNT_TYPES
                                ON
                                CARD_ACCOUNT_TYPES.ACCOUNT_TYPE_ID = CARD_PEOPLE_ACCOUNTS.ACCOUNT_TYPE_ID
                                LEFT JOIN
                                CARD_GROUPS
                                ON
                                CARD_GROUPS.GROUP_ID = CARD_CARDS.GROUP_ID
                                WHERE
                                LEN(CARD_CODE) = 6 AND (CARD_ACCOUNT_TYPES.NAME LIKE '{}') AND CARD_CODE = '{}'
                            """.format(card_code_type, CardCode))
    records = myfile.fetchall()
    del myfile
    return records


def get_coupons(CardCode):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
        ';DATABASE=' + database +
        ';UID=' + username +
        ';PWD=' + password +
        ';MARS_Connection=Yes'
    )
    myfile = cnxn.cursor()
    myfile.execute("""SELECT CARD_CARDS.CARD_CODE,CARD_COUPONS.PEOPLE_ID,COUPON_ID,COUPON_CODE,CARD_COUPON_TYPES.NAME,DATE_FROM,DATE_TO,CARD_COUPONS.FLAGS
                        FROM CARD_COUPONS
                        LEFT JOIN CARD_COUPON_TYPES
                        ON CARD_COUPONS.COUPON_TYPE_ID = CARD_COUPON_TYPES.COUPON_TYPE_ID
                        LEFT JOIN CARD_CARDS
                        ON CARD_CARDS.PEOPLE_ID = CARD_COUPONS.PEOPLE_ID
                        WHERE CARD_CODE = '{}'
                              """.format(CardCode))
    records = myfile.fetchall()
    myfile.close()
    del myfile
    cnxn.close()
    return records
