import database as db

def preparer_donnees_test():
    connexion = db.get_connection()
    if connexion:
        cursor = connexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO categories(nom_categorie) VALUES('Ordinateurs de bureau')")
            connexion.commit()
            print("Categorie de test 'Ordinateurs de bureau' cree avec succes")
        cursor.close()
        connexion.close()

print("---DEBUT DES TEST---")

preparer_donnees_test()

print("\n1. TEST D'AJOUT DE MATERIEL")
db.ajouter_materiel("PC DELL OPTIPLEX 7090", 1)
db.ajouter_materiel("Ecran HP 24 pouces", 1, "en Panne")
db.ajouter_materiel("LaserJet 2500", 2)

print("\n2. TEST DE LECTURE DE L'INVENTAIRE")
materiels = db.lister_materiels()
for m in materiels:
    print(f"-> ID:{m[0]} | Nom: {m[1]} | Etat: {m[2]} | Categorie : {m[3]}")

print("\n3. TEST DE MISE A JOUR DE L'ETAT")
if materiels:
    id_test = materiels[0][0]
    db.modifier_etat_materiel(id_test, "en Reparation")

    print("\n4. VERIFICATION DE LA MISE A JOUR")
    materiels_ajour = db.lister_materiels()
    for m in materiels_ajour:
        print(f" -> ID: {m[0]} | Nom: {m[1]} | Etat: {m[2]}")

print("---FIN DES TEST---")