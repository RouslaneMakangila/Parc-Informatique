import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='python'
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        print(f"Erreur lors de la connexion a MySQL: {err}")
        return None

def ajouter_materiel(nom, id_categorie, etat = "Fonctionnel"):
    connexion = get_connection()
    if connexion:
        try:
            cursor = connexion.cursor()
            requete = """INSERT INTO materiels (nom, etat, id_categorie) VALUES (%s, %s, %s)"""
            valeurs = (nom, etat, id_categorie)

            cursor.execute(requete, valeurs)
            connexion.commit()
            print("Materiel ajoute avec succes")

        except Error as err:
            print(f"Erreur lors de l'ajout: {err}")
        finally:
            cursor.close()
            connexion.close()

def lister_materiels():
    connexion = get_connection()
    materiels = []
    if connexion:
        try:
            cursor = connexion.cursor()
            requete = """SELECT m.id_materiel, m.nom, m.etat, m.id_categorie FROM materiels m """
            cursor.execute(requete)
            materiels = cursor.fetchall()

        except Error as err:
            print(f"Erreur lors de la lecture: {err}")
        finally:
            cursor.close()
            connexion.close()

    return materiels

def modifier_etat_materiel(id_materiel, nouvel_etat):
    connexion = get_connection()
    if connexion:
        try:
            cursor = connexion.cursor()
            requete = "UPDATE materiels SET etat = %s WHERE id_materiel = %s"
            valeurs = (nouvel_etat, id_materiel)
            cursor.execute(requete, valeurs)
            connexion.commit()
            print("Etat mis a jour avec succes")

        except Error as err:
            print(f"Erreur lors de la modification: {err}")
        finally:
            cursor.close()
            connexion.close()

def supprimer_materiel(id_materiel):
    connexion = get_connection()
    if connexion:
        try:
            cursor = connexion.cursor()
            requete = "DELETE FROM materiels WHERE id_materiel = %s"
            cursor.execute(requete, (id_materiel,))
            connexion.commit()
            print("Materiel supprime avec succes")

        except Error as err:
            print(f"Erreur lors de la supprssion: {err}")
        finally:
            cursor.close()
            connexion.close()
