import tkinter as tk
from tkinter import ttk, messagebox
import database as db


class ParcInformatiqueLocal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de Parc Informatique")
        self.geometry("960x650")

        # --- CHARTE COULEURS INSPIRÉE DE LA PHOTO ---
        self.BG_MAIN = '#fdfbf7'
        self.BG_HEADER = '#6f4e37'
        self.TEXT_DARK = '#3e2723'
        self.BG_CARD = '#eae2d6'
        self.COLOR_ACCENT = '#8d6e63'
        self.COLOR_SUCCESS = '#4e342e'
        self.COLOR_DANGER = '#b71c1c'

        self.configure(bg=self.BG_MAIN)
        self.current_filter = "Tous"

        self.dict_categories = {}

        self.setup_styles()
        self.setup_ui()
        self.charger_categories_db()
        self.load_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview", background="white", fieldbackground="white",
                        foreground=self.TEXT_DARK, font=('Segoe UI', 10), rowheight=35, borderwidth=0)
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), background="#f5f0e6",
                        foreground=self.TEXT_DARK, relief="flat", borderwidth=0)
        style.map("Treeview", background=[('selected', '#d7ccc8')], foreground=[('selected', self.TEXT_DARK)])

    def setup_ui(self):
        # --- 1. BANDEAU HAUT ---
        header = tk.Frame(self, bg=self.BG_HEADER, height=65)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="💻 PARC INFORMATIQUE", font=('Segoe UI', 14, 'bold'), fg="#ffffff",
                 bg=self.BG_HEADER).pack(side="left", padx=25, pady=15)
        tk.Label(header, text="OPERATIONS DES EQUIPEMENTS", font=('Segoe UI', 10, 'bold'), fg="#ffecb3",
                 bg=self.BG_HEADER).pack(side="right", padx=25, pady=18)

        # --- 2. VUE GLOBALE ---
        frame_kpi = tk.Frame(self, bg=self.BG_MAIN)
        frame_kpi.pack(fill="x", padx=25, pady=15)

        self.total_var = tk.StringVar(value="📦 Total Matériel\n0")
        self.panne_var = tk.StringVar(value="⚠️ en Panne\n0")
        self.repar_var = tk.StringVar(value="🔧 en Reparation\n0")

        tk.Label(frame_kpi, textvariable=self.total_var, font=('Segoe UI', 10, 'bold'), bg=self.BG_CARD,
                 fg=self.TEXT_DARK, width=22, height=3, bd=1, relief="solid").pack(side="left", padx=(0, 15))
        tk.Label(frame_kpi, textvariable=self.panne_var, font=('Segoe UI', 10, 'bold'), bg=self.BG_CARD,
                 fg=self.TEXT_DARK, width=22, height=3, bd=1, relief="solid").pack(side="left", padx=15)
        tk.Label(frame_kpi, textvariable=self.repar_var, font=('Segoe UI', 10, 'bold'), bg=self.BG_CARD,
                 fg=self.TEXT_DARK, width=22, height=3, bd=1, relief="solid").pack(side="left", padx=15)

        # --- 3. ZONE FORMULAIRE ---
        frame_form = tk.Frame(self, bg=self.BG_MAIN, highlightbackground="#bcaaa4", highlightthickness=1, padx=15,
                              pady=15)
        frame_form.pack(fill="x", padx=25, pady=(0, 15))

        tk.Label(frame_form, text="Enregistrer un nouvel équipement", font=('Segoe UI', 11, 'bold'), fg=self.TEXT_DARK,
                 bg=self.BG_MAIN).grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))

        tk.Label(frame_form, text="DESIGNATION:", font=('Segoe UI', 9, 'bold'), fg=self.TEXT_DARK,
                 bg=self.BG_MAIN).grid(row=1, column=0, padx=5, sticky="w")
        self.entry_nom = tk.Entry(frame_form, width=20, font=('Segoe UI', 10), bd=1, relief="solid")
        self.entry_nom.grid(row=2, column=0, padx=5, pady=(2, 10))

        tk.Label(frame_form, text="CATEGORIE:", font=('Segoe UI', 9, 'bold'), fg=self.TEXT_DARK, bg=self.BG_MAIN).grid(
            row=1, column=1, padx=5, sticky="w")
        self.combo_cat = ttk.Combobox(frame_form, width=18, font=('Segoe UI', 10), state="readonly")
        self.combo_cat.grid(row=2, column=1, padx=5, pady=(2, 10))

        tk.Label(frame_form, text="STATUT:", font=('Segoe UI', 9, 'bold'), fg=self.TEXT_DARK, bg=self.BG_MAIN).grid(
            row=1, column=2, padx=5, sticky="w")
        self.combo_statut = ttk.Combobox(frame_form, values=["Fonctionnel", "en Panne", "en Reparation"], width=18,
                                         font=('Segoe UI', 10), state="readonly")
        self.combo_statut.grid(row=2, column=2, padx=5, pady=(2, 10))
        self.combo_statut.current(0)

        tk.Button(frame_form, text="Enregistrer", bg=self.COLOR_SUCCESS, fg="white", font=('Segoe UI', 10, 'bold'),
                  bd=0, command=self.add_item, cursor="hand2", padx=20, pady=3).grid(row=2, column=3, padx=25,
                                                                                     pady=(0, 8), sticky="ns")

        # --- 4. BARRE D'ONGLETS FILTRES ---
        self.tab_bar = tk.Frame(self, bg=self.BG_MAIN)
        self.tab_bar.pack(fill="x", padx=25, pady=(5, 0))

        self.btn_tab_tous = tk.Button(self.tab_bar, text="Tous les matériels", font=('Segoe UI', 9, 'bold'), bd=1,
                                      relief="solid", bg="white", fg=self.TEXT_DARK, padx=15, pady=4,
                                      command=lambda: self.switch_tab("Tous"))
        self.btn_tab_tous.pack(side="left", padx=(0, 2))

        self.btn_tab_panne = tk.Button(self.tab_bar, text="⚠️ en Panne", font=('Segoe UI', 9), bd=1, relief="solid",
                                       bg=self.BG_CARD, fg=self.TEXT_DARK, padx=15, pady=4,
                                       command=lambda: self.switch_tab("en Panne"))
        self.btn_tab_panne.pack(side="left", padx=2)

        self.btn_tab_repar = tk.Button(self.tab_bar, text="🔧 en Reparation", font=('Segoe UI', 9), bd=1, relief="solid",
                                       bg=self.BG_CARD, fg=self.TEXT_DARK, padx=15, pady=4,
                                       command=lambda: self.switch_tab("en Reparation"))
        self.btn_tab_repar.pack(side="left", padx=2)

        # --- 5. ZONE DE LISTE PRINCIPALE ---
        self.container_tree = tk.Frame(self, bg="white", highlightbackground="#bcaaa4", highlightthickness=1)
        self.container_tree.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        self.tree = ttk.Treeview(self.container_tree, columns=("id", "nom", "categorie", "statut"), show="headings")
        self.tree.heading("id", text="ID Matériel")
        self.tree.heading("nom", text="Nom de la machine")
        self.tree.heading("categorie", text="Catégorie")
        self.tree.heading("statut", text="Statut")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("nom", width=300, anchor="w")
        self.tree.column("categorie", width=200, anchor="w")
        self.tree.column("statut", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        # --- 6. PIED DE PAGE ---
        frame_actions = tk.Frame(self, bg=self.BG_MAIN)
        frame_actions.pack(fill="x", padx=25, pady=(0, 20))

        tk.Button(frame_actions, text="Actualiser", font=('Segoe UI', 9, 'bold'), command=self.load_data,
                  bg=self.COLOR_ACCENT, fg="white", bd=1, relief="solid", padx=15, pady=4, cursor="hand2").pack(
            side="left", padx=(0, 5))
        tk.Button(frame_actions, text="Supprimer la sélection", font=('Segoe UI', 9, 'bold'), command=self.delete_item,
                  bg=self.COLOR_DANGER, fg="white", bd=1, relief="solid", padx=15, pady=4, cursor="hand2").pack(
            side="left", padx=5)

    def charger_categories_db(self):
        categories = db.lister_categories()
        if not categories:
            messagebox.showwarning("Attention",
                                   "Aucune catégorie trouvée dans la base de données. Veuillez en créer via MySQL.")
            return

        self.dict_categories = {cat[1]: cat[0] for cat in categories}
        self.combo_cat['values'] = list(self.dict_categories.keys())
        self.combo_cat.current(0)

    def switch_tab(self, filter_type):
        self.current_filter = filter_type
        tabs = [(self.btn_tab_tous, "Tous"), (self.btn_tab_panne, "en Panne"), (self.btn_tab_repar, "en Reparation")]
        for btn, name in tabs:
            if name == filter_type:
                btn.configure(bg="white", font=('Segoe UI', 9, 'bold'))
            else:
                btn.configure(bg=self.BG_CARD, font=('Segoe UI', 9))
        self.load_data()

    def update_kpis(self, all_rows):
        total = len(all_rows)
        # Dans ton fichier database.py, l'état est à l'index 2 du tuple renvoyé
        pannes = sum(1 for row in all_rows if row[2] == "en Panne")
        reparations = sum(1 for row in all_rows if row[2] == "en Reparation")

        self.total_var.set(f"📦 Total Matériel\n{total}")
        self.panne_var.set(f"⚠️ en Panne\n{pannes}")
        self.repar_var.set(f"🔧 en Reparation\n{reparations}")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        all_rows = db.lister_materiels()

        # Cas où la base de données n'arrive pas à se connecter
        if all_rows is None:
            return

        self.update_kpis(all_rows)

        for row in all_rows:
            # Format renvoyé par database.py : (id_materiel, nom, etat, nom_categorie)
            # Index : 0=id, 1=nom, 2=etat, 3=categorie
            valeurs_affichage = (row[0], row[1], row[3], row[2])
            statut_db = row[2]

            if self.current_filter == "Tous":
                self.tree.insert("", "end", values=valeurs_affichage)
            elif self.current_filter == "en Panne" and statut_db == "en Panne":
                self.tree.insert("", "end", values=valeurs_affichage)
            elif self.current_filter == "en Reparation" and statut_db == "en Reparation":
                self.tree.insert("", "end", values=valeurs_affichage)

    def add_item(self):
        nom = self.entry_nom.get().strip()
        categorie_nom = self.combo_cat.get()
        statut = self.combo_statut.get()

        if not nom:
            messagebox.showwarning("Champs manquants", "Veuillez entrer une désignation.")
            return

        id_categorie = self.dict_categories.get(categorie_nom)

        # Appel de la fonction (qui s'occupe du print en cas d'erreur ou de succès)
        db.ajouter_materiel(nom, id_categorie, statut)

        # Rafraîchissement des données et nettoyage du champ
        self.load_data()
        self.entry_nom.delete(0, tk.END)

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection manquante", "Veuillez sélectionner un élément.")
            return

        item_values = self.tree.item(selected[0])['values']
        item_id = item_values[0]
        item_nom = item_values[1]

        if messagebox.askyesno("Confirmation", f"Voulez-vous supprimer l'équipement : {item_nom} (ID: {item_id}) ?"):
            db.supprimer_materiel(item_id)
            self.load_data()


if __name__ == '__main__':
    app = ParcInformatiqueLocal()
    app.mainloop()