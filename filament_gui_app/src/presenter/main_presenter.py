from view.components.form import FilamentForm

class MainPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_presenter(self)
        self.refresh_filament_list()

    def add_filament(self, data):
        """Add a new filament to the database."""
        self.model.add_filament(
            data['brand'],
            data['color'],
            data['material'],
            float(data['weight']),
            data['purchase_link'],
            float(data['cost']),
            data['RGB_color'],
            float(data['k_factor']),
            float(data['flow_rate'])  # New field
        )
        self.refresh_filament_list()

    def update_filament(self, filament_id, brand, color, material, weight, purchase_link, cost):
        self.model.update_filament(filament_id, brand, color, material, weight, purchase_link, cost)
        self.refresh_filament_list()

    def delete_filament(self, filament_id):
        """Delete a filament by its ID."""
        self.model.delete_filament(filament_id)
        self.refresh_filament_list()

    def refresh_filament_list(self):
        """Fetch the list of filaments from the model and update the view."""
        filaments = self.model.get_filaments()
        self.view.update_filament_list(filaments)

    def load_filament_details(self, filament_id):
        filament = self.model.get_filament_by_id(filament_id)
        self.view.display_filament_details(filament)

    def show_add_filament_screen(self):
        """Navigate to the Add Filament screen."""
        self.view.show_form(submit_callback=self.add_filament)

    def show_edit_filament_screen(self, filament_id):
        """Navigate to the Edit Filament screen."""
        filament = self.model.get_filament_by_id(filament_id)
        if not filament:
            self.view.show_error("Filament not found.")
            return

        def submit_callback(updated_data):
            self.model.update_filament(
                filament_id,
                updated_data['brand'],
                updated_data['color'],
                updated_data['material'],
                float(updated_data['weight']),
                updated_data['purchase_link'],
                float(updated_data['cost']),
                updated_data['RGB_color'],
                float(updated_data['k_factor']),
                float(updated_data['flow_rate'])  # New field
            )
            self.refresh_filament_list()

        self.view.show_form(filament, submit_callback)

    def show_filament_properties(self, filament_id):
        filament = self.model.get_filament_by_id(filament_id)
        if not filament:
            self.view.show_error("Filament not found.")
            return

        # Dynamically display properties
        properties = {key: value for key, value in filament.items() if value is not None}
        self.view.show_properties_popup(properties)

    def confirm_and_delete_filament(self, filament_id):
        """Prompt the user for confirmation and delete the filament if confirmed."""
        filament = self.model.get_filament_by_id(filament_id)
        if not filament:
            self.view.show_error("Filament not found.")
            return

        # Ask for confirmation
        confirmed = self.view.show_confirmation_popup(
            f"Are you sure you want to delete the filament '{filament.brand}' ({filament.color})? This action cannot be undone."
        )
        if confirmed:
            self.model.delete_filament(filament_id)
            self.refresh_filament_list()
    
    def show_flushing_matrix(self):
        """Show the NxN flushing volume matrix."""
        filaments = self.model.get_filaments()
        column_names = self.model.get_column_names()
        filaments = [dict(zip(column_names, filament)) for filament in filaments]  # Convert tuples to dictionaries

        flushing_volumes = {
            (row[0], row[1]): row[2] for row in self.model.get_all_flushing_volumes()
        }

        def save_callback(changes):
            for (from_index, to_index), volume in changes.items():
                from_filament_id = filaments[from_index]['id']
                to_filament_id = filaments[to_index]['id']
                self.model.set_flushing_volume(from_filament_id, to_filament_id, volume)

        self.view.show_flushing_matrix(filaments, flushing_volumes, save_callback)