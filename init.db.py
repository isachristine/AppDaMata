import sqlite3

connection = sqlite3.connect('database.db') #aquivo que armazena nosso banco de dados

with open('schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()

#inserindo alguns insumos

cur.execute("INSERT INTO insumos (nome_insumo, beneficios) VALUES (?, ?)",
    ('Extrato glicólico de framboesa', 'Possui efeito adstringente na pele, proporcionando uma diminuição das secreções das glândulas sudoríparas. Possui ainda propriedades: hidratante, refrescante, e antioxidante da pele por conter grande quantidade de ácido ascórbico.' )
)

cur.execute("INSERT INTO insumos (nome_insumo, beneficios) VALUES (?, ?)",
    ('Óleo vegetal de abacate', 'O óleo de abacate é rico em sua composição. Encontramos nele agentes de ação antiinflamatória e antioxidante. Ele age na reconstrução da pele, recuperando a elasticidade e jovialidade. É um potente anti-séptico natural, pois dentre seus benefícios encontramos eficácia em ação bactericida. Em uso medicinal ele auxilia em tratamento a problemas de pele, como à dermatite e eczemas.')
)

connection.commit()
connection.close()