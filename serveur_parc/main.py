import tkinter as tk
from tkinter import ttk, messagebox
import database as db


# --- FONCTIONS LOGIQUES ---

def rafraichir_tableau():
    """Efface le tableau actuel et le remplit avec les données à jour."""
    for ligne in tableau.get_children():
        tableau.delete(ligne)

    materiels = db.lister_materiels()

    for m in materiels:
        # m = (id, nom, etat, categorie)
        tableau.insert("", "end", values=(m[0], m[1], m[3], m[2]))


def action_ajouter():
    """Récupère les saisies et ajoute le matériel."""
    nom = entree_nom.get()
    id_cat = entree_categorie.get()

    if nom and id_cat:
        try:
            id_cat = int(id_cat)
            db.ajouter_materiel(nom, id_cat)
            entree_nom.delete(0, tk.END)
            entree_categorie.delete(0, tk.END)
            rafraichir_tableau()
            messagebox.showinfo("Succès", "Matériel ajouté avec succès.")
        except ValueError:
            messagebox.showerror("Erreur", "L'ID de la catégorie doit être un nombre.")
    else:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")


def action_supprimer():
    """Supprime l'élément sélectionné dans le tableau."""
    selection = tableau.focus()  # Récupère la ligne sélectionnée

    if selection:
        # Récupère les valeurs de la ligne (le premier élément est l'ID)
        valeurs = tableau.item(selection, 'values')
        id_materiel = valeurs[0]

        # Fenêtre de confirmation avant de supprimer (bonne pratique de sécurité)
        reponse = messagebox.askyesno("Confirmation",
                                      f"Voulez-vous vraiment retirer l'équipement (ID {id_materiel}) du parc ?")

        if reponse:
            db.supprimer_materiel(id_materiel)
            rafraichir_tableau()
            messagebox.showinfo("Succès", "Matériel supprimé avec succès.")
    else:
        messagebox.showwarning("Sélection requise", "Veuillez d'abord sélectionner un matériel dans le tableau.")


def action_modifier_etat():
    """Modifie l'état de l'élément sélectionné selon le menu déroulant."""
    selection = tableau.focus()
    nouvel_etat = combo_etat.get()

    if not selection:
        messagebox.showwarning("Sélection requise", "Veuillez sélectionner un matériel dans le tableau.")
        return

    if not nouvel_etat:
        messagebox.showwarning("Sélection requise", "Veuillez choisir un nouvel état dans le menu déroulant.")
        return

    valeurs = tableau.item(selection, 'values')
    id_materiel = valeurs[0]

    db.modifier_etat_materiel(id_materiel, nouvel_etat)
    rafraichir_tableau()
    messagebox.showinfo("Succès", f"L'état a été mis à jour vers : {nouvel_etat}")


# --- CONFIGURATION DE LA FENÊTRE PRINCIPALE ---
fenetre = tk.Tk()
fenetre.title("Gestion du Parc Informatique")
fenetre.geometry("750x600")  # Légèrement agrandie pour faire de la place

# --- ZONE FORMULAIRE (Haut) ---
frame_formulaire = tk.Frame(fenetre, pady=15)
frame_formulaire.pack()

tk.Label(frame_formulaire, text="Nom de l'équipement :").grid(row=0, column=0, padx=5)
entree_nom = tk.Entry(frame_formulaire, width=25)
entree_nom.grid(row=0, column=1, padx=5)

tk.Label(frame_formulaire, text="ID Catégorie :").grid(row=0, column=2, padx=5)
entree_categorie = tk.Entry(frame_formulaire, width=10)
entree_categorie.grid(row=0, column=3, padx=5)

bouton_ajouter = tk.Button(frame_formulaire, text="Ajouter", bg="#add8e6", command=action_ajouter)
bouton_ajouter.grid(row=0, column=4, padx=10)

# --- ZONE TABLEAU (Centre) ---
colonnes = ("ID", "Nom", "Catégorie", "État")
tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings", selectmode="browse")

for col in colonnes:
    tableau.heading(col, text=col)
    tableau.column(col, width=150, anchor="center")

tableau.pack(expand=True, fill="both", padx=20, pady=5)

# --- ZONE ACTIONS (Bas) ---
frame_actions = tk.Frame(fenetre, pady=15)
frame_actions.pack()

# Menu déroulant pour choisir le nouvel état
tk.Label(frame_actions, text="Nouvel état :").grid(row=0, column=0, padx=5)
etats_possibles = ["Fonctionnel", "en Panne", "en Reparation"]
combo_etat = ttk.Combobox(frame_actions, values=etats_possibles, state="readonly", width=15)
combo_etat.grid(row=0, column=1, padx=5)

# Bouton Modifier
bouton_modifier = tk.Button(frame_actions, text="Mettre à jour l'état", bg="#90ee90", command=action_modifier_etat)
bouton_modifier.grid(row=0, column=2, padx=20)

# Séparateur visuel simple
tk.Label(frame_actions, text=" | ").grid(row=0, column=3)

# Bouton Supprimer
bouton_supprimer = tk.Button(frame_actions, text="Supprimer le matériel", bg="#ffcccb", command=action_supprimer)
bouton_supprimer.grid(row=0, column=4, padx=20)

# --- LANCEMENT ---
rafraichir_tableau()
fenetre.mainloop()